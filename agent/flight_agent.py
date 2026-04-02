"""LangGraph 멀티 에이전트 시스템

Router → Flight Agent / Policy Agent 분기
각 Agent가 전문 도구를 사용하여 응답
"""

import time
import logging
from datetime import datetime
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, MessagesState, START, END
from agent.tools import (
    search_flights, search_nonstop_flights,
    search_round_trip, get_flight_price_insights, ALL_TOOLS,
)
from agent.vector_store import search_airline_policy
from agent.prompts import SYSTEM_PROMPT
from config import OPENAI_API_KEY

logger = logging.getLogger("skybot")

# ============ Agent Traces (모니터링) ============
_traces = []


def get_traces():
    return _traces


def clear_traces():
    global _traces
    _traces = []


def _log_trace(step: str, detail: str, duration_ms: float = 0):
    _traces.append({
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "detail": detail,
        "duration_ms": round(duration_ms, 1),
    })


# ============ Intent Router ============
ROUTER_PROMPT = """당신은 사용자 질문을 분류하는 라우터입니다.
질문을 아래 카테고리 중 하나로 분류하세요:

- "flight": 항공편 검색, 가격 비교, 직항/경유, 왕복/편도, 날짜/도시 관련
- "policy": 수하물, 마일리지, 좌석, 라운지, 체크인, 기내 서비스, 환불, 업그레이드 관련
- "general": 인사, 잡담, 기타 질문

반드시 "flight", "policy", "general" 중 하나만 답하세요."""


def classify_intent(llm, message: str) -> str:
    """사용자 메시지의 의도를 분류"""
    t0 = time.time()
    response = llm.invoke([
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=message),
    ])
    intent = response.content.strip().lower().replace('"', '')
    duration = (time.time() - t0) * 1000

    if "flight" in intent:
        result = "flight"
    elif "policy" in intent:
        result = "policy"
    else:
        result = "general"

    _log_trace("Router", f"Intent: {result} (from: '{message[:50]}...')", duration)
    return result


# ============ Multi-Agent 생성 ============
def create_flight_agent():
    """멀티 에이전트 시스템 생성"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=OPENAI_API_KEY,
    )

    today = datetime.now().strftime("%Y-%m-%d")

    # Flight 전문 Agent
    flight_prompt = SYSTEM_PROMPT + f"""

오늘 날짜: {today}

당신은 항공편 검색 전문 에이전트입니다.
항공편 검색, 가격 비교, 직항/경유 검색에 특화되어 있습니다.
반드시 도구를 사용하여 실시간 데이터를 기반으로 응답하세요."""

    flight_agent = create_react_agent(
        model=llm,
        tools=[search_flights, search_nonstop_flights,
               search_round_trip, get_flight_price_insights],
        state_modifier=flight_prompt,
    )

    # Policy 전문 Agent
    policy_prompt = SYSTEM_PROMPT + f"""

오늘 날짜: {today}

당신은 항공사 정책 전문 에이전트입니다.
수하물, 마일리지, 좌석, 라운지, 체크인 등 항공사 정책 질문에 특화되어 있습니다.
반드시 정책 검색 도구를 사용하여 정확한 정보를 기반으로 응답하세요."""

    policy_agent = create_react_agent(
        model=llm,
        tools=[search_airline_policy],
        state_modifier=policy_prompt,
    )

    # General Agent (도구 없음)
    general_agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS + [search_airline_policy],
        state_modifier=SYSTEM_PROMPT + f"\n\n오늘 날짜: {today}",
    )

    return {
        "llm": llm,
        "flight": flight_agent,
        "policy": policy_agent,
        "general": general_agent,
    }


def run_agent(agents, user_message: str, chat_history: list = None):
    """멀티 에이전트 실행 — Router가 의도 분류 후 전문 Agent에 위임"""
    t0 = time.time()

    # 1. Intent Classification
    intent = classify_intent(agents["llm"], user_message)

    # 2. Agent 선택
    agent = agents[intent]
    _log_trace("Dispatcher", f"Selected: {intent}_agent")

    # 3. 메시지 구성
    messages = []
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    # 4. Agent 실행
    t1 = time.time()
    result = agent.invoke({"messages": messages})
    agent_duration = (time.time() - t1) * 1000

    ai_messages = result["messages"]
    final_response = ai_messages[-1].content

    # 5. Tool Call 추출
    tool_calls_made = []
    for msg in ai_messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls_made.append({
                    "name": tc["name"],
                    "args": tc["args"],
                })
                _log_trace("ToolCall", f"{tc['name']}({tc['args']})")

    total_duration = (time.time() - t0) * 1000
    _log_trace("Response", f"Length: {len(final_response)} chars", agent_duration)
    _log_trace("Total", f"E2E latency", total_duration)

    return {
        "response": final_response,
        "tool_calls": tool_calls_made,
        "intent": intent,
        "all_messages": ai_messages,
        "latency_ms": total_duration,
    }
