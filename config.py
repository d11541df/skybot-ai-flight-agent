import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key):
    """환경변수 또는 Streamlit/HF secrets에서 값 가져오기"""
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        return None


OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SERPAPI_KEY = get_secret("SERPAPI_KEY")

AIRPORT_CODES = {
    "서울": "ICN", "인천": "ICN", "김포": "GMP",
    "도쿄": "NRT", "나리타": "NRT", "하네다": "HND",
    "오사카": "KIX", "후쿠오카": "FUK", "삿포로": "CTS",
    "베이징": "PEK", "상하이": "PVG", "홍콩": "HKG",
    "타이베이": "TPE", "방콕": "BKK", "싱가포르": "SIN",
    "하노이": "HAN", "호치민": "SGN", "마닐라": "MNL",
    "자카르타": "CGK", "발리": "DPS", "쿠알라룸푸르": "KUL",
    "뉴욕": "JFK", "로스앤젤레스": "LAX", "LA": "LAX",
    "샌프란시스코": "SFO", "시카고": "ORD", "워싱턴": "IAD",
    "런던": "LHR", "파리": "CDG", "프랑크푸르트": "FRA",
    "로마": "FCO", "마드리드": "MAD", "암스테르담": "AMS",
    "시드니": "SYD", "멜버른": "MEL", "괌": "GUM",
    "하와이": "HNL", "호놀룰루": "HNL", "세부": "CEB",
    "블라디보스토크": "VVO", "다낭": "DAD", "푸켓": "HKT",
    "뮌헨": "MUC", "취리히": "ZRH", "이스탄불": "IST",
    "두바이": "DXB", "제주": "CJU", "부산": "PUS",
    "대구": "TAE", "광주": "KWJ", "청주": "CJJ",
}

CITY_NAMES_EN = {
    "서울": "Seoul", "인천": "Seoul", "김포": "Seoul",
    "도쿄": "Tokyo", "나리타": "Tokyo", "하네다": "Tokyo",
    "오사카": "Osaka", "후쿠오카": "Fukuoka", "삿포로": "Sapporo",
    "베이징": "Beijing", "상하이": "Shanghai", "홍콩": "Hong Kong",
    "타이베이": "Taipei", "방콕": "Bangkok", "싱가포르": "Singapore",
    "하노이": "Hanoi", "호치민": "Ho Chi Minh City", "마닐라": "Manila",
    "자카르타": "Jakarta", "발리": "Bali", "쿠알라룸푸르": "Kuala Lumpur",
    "뉴욕": "New York", "로스앤젤레스": "Los Angeles", "LA": "Los Angeles",
    "샌프란시스코": "San Francisco", "시카고": "Chicago", "워싱턴": "Washington",
    "런던": "London", "파리": "Paris", "프랑크푸르트": "Frankfurt",
    "로마": "Rome", "마드리드": "Madrid", "암스테르담": "Amsterdam",
    "시드니": "Sydney", "멜버른": "Melbourne", "괌": "Guam",
    "하와이": "Honolulu", "호놀룰루": "Honolulu", "세부": "Cebu",
    "다낭": "Da Nang", "푸켓": "Phuket", "두바이": "Dubai",
    "제주": "Jeju", "부산": "Busan",
}

AIRLINE_NAMES = {
    "KE": "대한항공", "OZ": "아시아나항공", "7C": "제주항공",
    "TW": "티웨이항공", "LJ": "진에어", "BX": "에어부산",
    "ZE": "이스타항공", "RS": "에어서울", "4V": "플라이강원",
    "NH": "전일본공수(ANA)", "JL": "일본항공(JAL)",
    "CX": "캐세이퍼시픽", "SQ": "싱가포르항공",
    "TG": "타이항공", "VN": "베트남항공",
    "AA": "아메리칸항공", "UA": "유나이티드항공", "DL": "델타항공",
    "BA": "영국항공", "AF": "에어프랑스", "LH": "루프트한자",
    "EK": "에미레이트", "QR": "카타르항공", "SU": "아에로플로트",
    "CA": "중국국제항공", "MU": "중국동방항공", "CZ": "중국남방항공",
    "QF": "콴타스", "EY": "에티하드항공", "TK": "터키항공",
    "Korean Air": "대한항공", "Asiana Airlines": "아시아나항공",
    "Jeju Air": "제주항공", "Jin Air": "진에어",
    "Japan Airlines": "일본항공(JAL)", "All Nippon Airways": "전일본공수(ANA)",
}
