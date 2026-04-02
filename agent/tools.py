"""SerpApi Google Flights 기반 항공편 검색 도구 (Real-time)"""

import json
import urllib.request
import urllib.parse
from langchain.tools import tool
from config import SERPAPI_KEY, AIRPORT_CODES, AIRLINE_NAMES


def resolve_city(city: str) -> str:
    """한글 도시명을 IATA 공항 코드로 변환"""
    city = city.strip()
    if len(city) == 3 and city.upper() == city:
        return city
    return AIRPORT_CODES.get(city, city.upper())


def get_airline_kr(name: str) -> str:
    """항공사명을 한글로 변환"""
    return AIRLINE_NAMES.get(name, name)


def serpapi_search(params: dict) -> dict:
    """SerpApi 호출 (urllib 사용)"""
    params["api_key"] = SERPAPI_KEY
    params["output"] = "json"
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    resp = urllib.request.urlopen(url, timeout=15)
    return json.loads(resp.read().decode("utf-8"))


def format_flight_results(data: dict) -> str:
    """SerpApi Google Flights 응답을 읽기 좋은 텍스트로 변환"""
    best = data.get("best_flights", [])
    other = data.get("other_flights", [])
    all_flights = best + other

    if not all_flights:
        return "검색 결과가 없습니다. 다른 날짜나 경로를 시도해보세요."

    results = []
    for i, flight in enumerate(all_flights[:6], 1):
        price = flight.get("price", "N/A")
        total_duration = flight.get("total_duration", 0)
        hours, mins = divmod(total_duration, 60)
        duration_str = f"{hours}시간 {mins}분" if hours else f"{mins}분"

        segments = flight.get("flights", [])
        seg_details = []
        for seg in segments:
            airline = get_airline_kr(seg.get("airline", ""))
            flight_no = seg.get("flight_number", "")
            dep_airport = seg.get("departure_airport", {})
            arr_airport = seg.get("arrival_airport", {})
            dep_code = dep_airport.get("id", "")
            dep_time = dep_airport.get("time", "")
            arr_code = arr_airport.get("id", "")
            arr_time = arr_airport.get("time", "")
            airplane = seg.get("airplane", "")
            legroom = seg.get("legroom", "")

            seg_text = (
                f"  {airline} {flight_no} | "
                f"{dep_code} {dep_time} -> {arr_code} {arr_time} | "
                f"{airplane}"
            )
            if legroom:
                seg_text += f" | {legroom}"
            seg_details.append(seg_text)

        stops = len(segments) - 1
        stop_text = "직항" if stops == 0 else f"경유 {stops}회"

        if isinstance(price, (int, float)):
            price_str = f"{int(price):,}원"
        else:
            price_str = str(price)

        tag = "[추천] " if flight in best else ""
        flight_text = f"**{tag}항공편 {i}** - {price_str} ({stop_text}, {duration_str})\n"
        flight_text += "\n".join(seg_details)
        results.append(flight_text)

    # 가격 인사이트 추가
    insights = data.get("price_insights", {})
    if insights:
        lowest = insights.get("lowest_price")
        typical = insights.get("typical_price_range", [])
        level = insights.get("price_level", "")
        level_kr = {"low": "저렴", "typical": "보통", "high": "비쌈"}.get(level, level)

        insight_text = "\n---\n**가격 분석:**"
        if lowest:
            insight_text += f" 최저가 {lowest:,}원"
        if typical and len(typical) == 2:
            insight_text += f" | 일반 가격대 {typical[0]:,}~{typical[1]:,}원"
        if level_kr:
            insight_text += f" | 현재 수준: {level_kr}"
        results.append(insight_text)

    return "\n\n".join(results)


@tool
def search_flights(origin: str, destination: str, departure_date: str,
                   return_date: str = None, adults: int = 1) -> str:
    """항공편을 검색합니다. Google Flights 실시간 데이터를 사용합니다.

    Args:
        origin: 출발지 (한글 도시명 또는 공항 코드, 예: 서울, ICN)
        destination: 도착지 (한글 도시명 또는 공항 코드, 예: 도쿄, NRT)
        departure_date: 출발일 (YYYY-MM-DD)
        return_date: 귀국일 (YYYY-MM-DD, 선택사항. 없으면 편도)
        adults: 성인 승객 수
    """
    origin_code = resolve_city(origin)
    dest_code = resolve_city(destination)

    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": departure_date,
        "currency": "KRW",
        "hl": "ko",
        "adults": adults,
    }

    if return_date:
        params["return_date"] = return_date
        params["type"] = "1"
    else:
        params["type"] = "2"

    try:
        results = serpapi_search(params)
        if "error" in results:
            return f"검색 오류: {results['error']}"
        return format_flight_results(results)
    except Exception as e:
        return f"항공편 검색 중 오류: {str(e)}"


@tool
def search_nonstop_flights(origin: str, destination: str,
                           departure_date: str) -> str:
    """직항 항공편만 검색합니다.

    Args:
        origin: 출발지 (한글 도시명 또는 공항 코드)
        destination: 도착지 (한글 도시명 또는 공항 코드)
        departure_date: 출발일 (YYYY-MM-DD)
    """
    origin_code = resolve_city(origin)
    dest_code = resolve_city(destination)

    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": departure_date,
        "currency": "KRW",
        "hl": "ko",
        "adults": "1",
        "type": "2",
        "stops": "1",
    }

    try:
        results = serpapi_search(params)
        if "error" in results:
            return f"검색 오류: {results['error']}"
        return "**[직항 검색 결과]**\n\n" + format_flight_results(results)
    except Exception as e:
        return f"직항 검색 중 오류: {str(e)}"


@tool
def search_round_trip(origin: str, destination: str,
                      departure_date: str, return_date: str) -> str:
    """왕복 항공편을 검색합니다.

    Args:
        origin: 출발지 (한글 도시명 또는 공항 코드)
        destination: 도착지 (한글 도시명 또는 공항 코드)
        departure_date: 출발일 (YYYY-MM-DD)
        return_date: 귀국일 (YYYY-MM-DD)
    """
    origin_code = resolve_city(origin)
    dest_code = resolve_city(destination)

    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": departure_date,
        "return_date": return_date,
        "currency": "KRW",
        "hl": "ko",
        "adults": "1",
        "type": "1",
    }

    try:
        results = serpapi_search(params)
        if "error" in results:
            return f"검색 오류: {results['error']}"
        return "**[왕복 검색 결과]**\n\n" + format_flight_results(results)
    except Exception as e:
        return f"왕복 검색 중 오류: {str(e)}"


@tool
def get_flight_price_insights(origin: str, destination: str,
                              departure_date: str) -> str:
    """항공편 가격 분석 정보를 제공합니다 (최저가, 평균가, 가격 추이).

    Args:
        origin: 출발지 (한글 도시명 또는 공항 코드)
        destination: 도착지 (한글 도시명 또는 공항 코드)
        departure_date: 출발일 (YYYY-MM-DD)
    """
    origin_code = resolve_city(origin)
    dest_code = resolve_city(destination)

    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": departure_date,
        "currency": "KRW",
        "hl": "ko",
        "adults": "1",
        "type": "2",
    }

    try:
        results = serpapi_search(params)
        if "error" in results:
            return f"검색 오류: {results['error']}"

        insights = results.get("price_insights", {})
        if insights:
            lowest = insights.get("lowest_price", "N/A")
            typical = insights.get("typical_price_range", [])
            level = insights.get("price_level", "")
            level_kr = {"low": "저렴", "typical": "보통", "high": "비쌈"}.get(level, level)

            text = f"**{origin_code} -> {dest_code} 가격 분석:**\n\n"
            if isinstance(lowest, (int, float)):
                text += f"- 최저가: {int(lowest):,}원\n"
            if typical and len(typical) == 2:
                text += f"- 일반 가격대: {typical[0]:,}원 ~ {typical[1]:,}원\n"
            if level_kr:
                text += f"- 현재 가격 수준: **{level_kr}**\n"

            text += "\n**최저가 항공편:**\n\n"
            text += format_flight_results(results)
            return text

        return format_flight_results(results)
    except Exception as e:
        return f"가격 분석 중 오류: {str(e)}"


ALL_TOOLS = [search_flights, search_nonstop_flights, search_round_trip, get_flight_price_insights]
