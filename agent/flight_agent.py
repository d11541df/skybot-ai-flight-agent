"""LangGraph 기반 항공편 AI Agent"""

from datetime import datetime
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agent.tools import ALL_TOOLS
from agent.vector_store import search_airline_policy
from agent.prompts import SYSTEM_PROMPT
from config import OPENAI_API_KEY


def create_flight_agent():
    """LangGraph ReAct Agent 생성"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=OPENAI_API_KEY,
    )

    tools = ALL_TOOLS + [search_airline_policy]

    today = datetime.now().strftime("%Y-%m-%d")
    system_prompt = SYSTEM_PROMPT + f"\n\n오늘 날짜: {today}"

    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt,
    )

    return agent


def run_agent(agent, user_message: str, chat_history: list = None):
    """Agent 실행 및 응답 반환"""
    messages = []
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    result = agent.invoke({"messages": messages})

    ai_messages = result["messages"]
    final_response = ai_messages[-1].content

    tool_calls_made = []
    for msg in ai_messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls_made.append({
                    "name": tc["name"],
                    "args": tc["args"],
                })

    return {
        "response": final_response,
        "tool_calls": tool_calls_made,
        "all_messages": ai_messages,
    }
