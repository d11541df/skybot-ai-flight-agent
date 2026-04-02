"""대시보드 UI 컴포넌트"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random


def render_architecture():
    """파이프라인 아키텍처 다이어그램"""
    st.markdown("### System Architecture")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 30px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    ">
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div style="text-align: center; background: rgba(255,255,255,0.15); border-radius: 12px; padding: 20px; min-width: 140px;">
                <div style="font-size: 28px;">💬</div>
                <div style="font-weight: bold; margin-top: 8px;">User Query</div>
                <div style="font-size: 12px; opacity: 0.8;">자연어 입력</div>
            </div>
            <div style="font-size: 24px;">→</div>
            <div style="text-align: center; background: rgba(255,255,255,0.15); border-radius: 12px; padding: 20px; min-width: 140px;">
                <div style="font-size: 28px;">🧠</div>
                <div style="font-weight: bold; margin-top: 8px;">LangGraph Agent</div>
                <div style="font-size: 12px; opacity: 0.8;">ReAct Pattern</div>
            </div>
            <div style="font-size: 24px;">→</div>
            <div style="text-align: center; background: rgba(255,255,255,0.15); border-radius: 12px; padding: 20px; min-width: 140px;">
                <div style="font-size: 28px;">🔧</div>
                <div style="font-weight: bold; margin-top: 8px;">Tools</div>
                <div style="font-size: 12px; opacity: 0.8;">Amadeus · ChromaDB</div>
            </div>
            <div style="font-size: 24px;">→</div>
            <div style="text-align: center; background: rgba(255,255,255,0.15); border-radius: 12px; padding: 20px; min-width: 140px;">
                <div style="font-size: 28px;">✈️</div>
                <div style="font-weight: bold; margin-top: 8px;">Response</div>
                <div style="font-size: 12px; opacity: 0.8;">항공편 정보</div>
            </div>
        </div>

        <div style="margin-top: 25px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 20px; font-size: 13px;">
                <strong>LLM:</strong> GPT-4o-mini
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 20px; font-size: 13px;">
                <strong>Framework:</strong> LangChain + LangGraph
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 20px; font-size: 13px;">
                <strong>API:</strong> Amadeus Flight API
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 20px; font-size: 13px;">
                <strong>VectorDB:</strong> ChromaDB (RAG)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_tech_stack():
    """기술 스택 카드"""
    st.markdown("### Tech Stack")

    cols = st.columns(4)
    stacks = [
        ("🐍 Backend", ["Python 3.11", "LangChain 0.3", "LangGraph 0.2", "ChromaDB"]),
        ("✈️ API", ["Amadeus Flight API", "OpenAI GPT-4o", "Real-time Data", "REST API"]),
        ("📊 Frontend", ["Streamlit", "Plotly", "Custom CSS", "Responsive UI"]),
        ("☁️ Infra", ["Streamlit Cloud", "Git/GitHub", "CI/CD Ready", ".env Config"]),
    ]

    for col, (title, items) in zip(cols, stacks):
        with col:
            st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 20px;
                height: 220px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            ">
                <h4 style="margin: 0 0 15px 0; color: #0064D2;">{title}</h4>
                {''.join(f'<div style="padding: 4px 0; color: #4A5568; font-size: 14px;">• {item}</div>' for item in items)}
            </div>
            """, unsafe_allow_html=True)


def render_metrics():
    """핵심 지표 카드"""
    st.markdown("### Agent Performance Metrics")

    cols = st.columns(4)
    metrics = [
        ("지원 도시", "120+", "40개국"),
        ("API 응답 속도", "~1.2s", "평균"),
        ("정책 DB", "10건", "RAG 검색"),
        ("도구 수", "5개", "Tool Calling"),
    ]

    for col, (label, value, sub) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value, delta=sub)


def render_tool_usage_chart():
    """도구 사용 분포 차트"""
    st.markdown("### Tool Usage Distribution")

    fig = go.Figure(data=[go.Pie(
        labels=["항공편 검색", "최저가 검색", "정책 RAG", "공항 검색", "여행지 추천"],
        values=[45, 25, 15, 10, 5],
        hole=0.4,
        marker_colors=["#0064D2", "#00A3E0", "#6B7FD7", "#95A5C6", "#C4D0E0"],
        textinfo="label+percent",
        textfont_size=13,
    )])

    fig.update_layout(
        height=350,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_popular_routes():
    """인기 노선 차트"""
    st.markdown("### Popular Routes from ICN")

    routes = pd.DataFrame({
        "노선": ["ICN→NRT", "ICN→KIX", "ICN→BKK", "ICN→LAX", "ICN→CDG",
                 "ICN→SIN", "ICN→HAN", "ICN→FUK", "ICN→SYD", "ICN→JFK"],
        "검색량": [320, 280, 250, 220, 190, 170, 160, 150, 130, 120],
        "평균가(만원)": [25, 22, 45, 120, 130, 55, 30, 18, 95, 140],
    })

    fig = px.bar(
        routes,
        x="노선",
        y="검색량",
        color="평균가(만원)",
        color_continuous_scale=["#C4D0E0", "#0064D2"],
        text="검색량",
    )
    fig.update_layout(
        height=350,
        margin=dict(t=20, b=40, l=40, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def render_agent_flow():
    """Agent 실행 플로우 시각화"""
    st.markdown("### LangGraph Agent Flow")

    st.markdown("""
    <div style="
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 25px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 2;
    ">
        <div style="color: #0064D2; font-weight: bold;">📥 Input</div>
        <div style="margin-left: 20px; color: #4A5568;">"4월 25일 도쿄 가는 비행기 있어?"</div>
        <div style="color: #718096; margin: 5px 0;">↓</div>

        <div style="color: #D69E2E; font-weight: bold;">🧠 LLM Reasoning (ReAct)</div>
        <div style="margin-left: 20px; color: #4A5568;">
            <em>Thought:</em> 서울→도쿄, 2026-04-25 항공편 검색 필요<br>
            <em>Action:</em> search_flights(origin="서울", destination="도쿄", departure_date="2026-04-25")
        </div>
        <div style="color: #718096; margin: 5px 0;">↓</div>

        <div style="color: #38A169; font-weight: bold;">🔧 Tool Execution</div>
        <div style="margin-left: 20px; color: #4A5568;">
            → resolve_city("서울") → "ICN"<br>
            → resolve_city("도쿄") → "NRT"<br>
            → Amadeus API 호출 → 5개 항공편 수신
        </div>
        <div style="color: #718096; margin: 5px 0;">↓</div>

        <div style="color: #805AD5; font-weight: bold;">🧠 LLM Synthesis</div>
        <div style="margin-left: 20px; color: #4A5568;">
            검색 결과를 자연어로 정리, 가격·시간·항공사 포함
        </div>
        <div style="color: #718096; margin: 5px 0;">↓</div>

        <div style="color: #E53E3E; font-weight: bold;">📤 Output</div>
        <div style="margin-left: 20px; color: #4A5568;">
            "4월 25일 인천→나리타 항공편 5건을 찾았습니다! ..."
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sample_conversations():
    """예시 대화"""
    st.markdown("### Try These Queries")

    examples = [
        "4월 25일에 도쿄 가는 비행기 있어?",
        "서울에서 방콕 최저가 알려줘",
        "수하물 무게 제한이 어떻게 돼?",
        "인천에서 갈 수 있는 추천 여행지 알려줘",
        "LA행 비즈니스석 마일리지 얼마야?",
    ]

    cols = st.columns(len(examples))
    for col, ex in zip(cols, examples):
        with col:
            st.markdown(f"""
            <div style="
                background: #EBF4FF;
                border: 1px solid #BEE3F8;
                border-radius: 8px;
                padding: 12px;
                text-align: center;
                font-size: 13px;
                color: #2B6CB0;
                cursor: pointer;
                min-height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">{ex}</div>
            """, unsafe_allow_html=True)
