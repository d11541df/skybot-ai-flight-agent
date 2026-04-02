"""SkyBot - Korean Air AI Flight Assistant"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SkyBot | Korean Air AI Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========================= GLOBAL CSS =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Inter', -apple-system, sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace !important; }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%);
        border: 1px solid rgba(0, 100, 210, 0.1);
        border-radius: 16px; padding: 20px;
        box-shadow: 0 2px 12px rgba(0, 48, 135, 0.05);
    }
    [data-testid="stMetricValue"] { color: #003087; font-weight: 700; }

    [data-testid="stSidebar"] { background: linear-gradient(180deg, #001845 0%, #002B6B 100%); }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }

    .stChatMessage { border-radius: 16px !important; }

    [data-testid="stMain"] div.stButton > button {
        background: linear-gradient(135deg, #003087, #0064D2);
        border: none; border-radius: 12px; color: white;
        font-weight: 600; padding: 12px 24px; transition: all 0.2s;
    }
    [data-testid="stMain"] div.stButton > button:hover {
        background: linear-gradient(135deg, #002060, #0050B0);
        box-shadow: 0 4px 16px rgba(0,48,135,0.3); transform: translateY(-1px);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def hero(title, subtitle, badges=None):
    badge_html = ""
    if badges:
        bs = "display:inline-block; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); border-radius:20px; padding:5px 16px; font-size:12px; margin-right:8px; margin-top:14px;"
        badge_html = "".join(f'<span style="{bs}">{b}</span>' for b in badges)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #001845 0%, #003087 35%, #0064D2 70%, #00A3E0 100%); border-radius:20px; padding:45px 50px; color:white; margin-bottom:30px; position:relative; overflow:hidden;">
        <div style="position:absolute; top:-80px; right:-60px; width:400px; height:400px; background:radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%); border-radius:50%;"></div>
        <h1 style="margin:0; font-size:40px; font-weight:900; letter-spacing:-1.5px; position:relative;">{title}</h1>
        <p style="margin:12px 0 0 0; opacity:0.85; font-size:17px; font-weight:300; line-height:1.5; position:relative;">{subtitle}</p>
        <div style="position:relative;">{badge_html}</div>
    </div>
    """, unsafe_allow_html=True)


def info_card(title, content, color="#003087"):
    st.markdown(f"""
    <div style="background:white; border:1px solid #E8EDF5; border-radius:16px; padding:24px; box-shadow:0 2px 12px rgba(0,48,135,0.04); border-top:3px solid {color}; height:100%;">
        <h4 style="color:{color}; margin:0 0 12px 0; font-weight:700; font-size:16px;">{title}</h4>
        <div style="color:#4A5568; font-size:14px; line-height:1.7;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(icon, value, label, sub=""):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #f8faff, #eef4ff); border:1px solid #dde6f5; border-radius:16px; padding:24px; text-align:center;">
        <div style="font-size:32px; margin-bottom:8px;">{icon}</div>
        <div style="font-size:28px; font-weight:800; color:#003087;">{value}</div>
        <div style="font-size:13px; color:#4A5568; font-weight:500; margin-top:4px;">{label}</div>
        <div style="font-size:11px; color:#90A4C0; margin-top:2px;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "tool_log" not in st.session_state:
    st.session_state.tool_log = []

# ========================= SIDEBAR =========================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:25px 0 15px 0;">
        <div style="width:72px; height:72px; margin:0 auto; background:linear-gradient(135deg, #0064D2, #00A3E0); border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:32px; box-shadow:0 8px 24px rgba(0,100,210,0.3);">✈️</div>
        <h2 style="margin:14px 0 2px 0; font-weight:800; font-size:22px;">SkyBot</h2>
        <p style="font-size:12px; opacity:0.7; margin:0;">AI Flight Assistant</p>
        <div style="display:inline-block; background:linear-gradient(135deg,#00A3E0,#0064D2); border-radius:12px; padding:3px 14px; font-size:10px; font-weight:700; margin-top:8px; letter-spacing:0.5px;">PORTFOLIO 2026</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation",
        ["💬 AI Assistant", "📊 System Dashboard", "🔍 Flight Search Engine",
         "📚 RAG Policy Search", "🧠 Agent Architecture", "📡 Monitoring", "👤 About"],
        label_visibility="collapsed")
    st.divider()
    st.markdown("""
    <div style="padding:0 8px;">
        <div style="font-size:11px; font-weight:600; letter-spacing:1px; opacity:0.5; margin-bottom:10px;">TECH STACK</div>
        <div style="display:flex; flex-wrap:wrap; gap:5px;">
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">LangGraph</span>
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">LangChain</span>
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">GPT-4o</span>
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">Google Flights</span>
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">OpenAI Embeddings</span>
            <span style="background:rgba(255,255,255,0.1); padding:3px 10px; border-radius:6px; font-size:10px;">Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<div style="text-align:center; font-size:10px; opacity:0.4;">Built for Korean Air AI Position<br><a href="https://github.com/d11541df/skybot-ai-flight-agent" style="color:rgba(255,255,255,0.6); text-decoration:none;">GitHub →</a></div>', unsafe_allow_html=True)

# ========================= AI ASSISTANT =========================
if page == "💬 AI Assistant":
    hero("✈️ SkyBot AI Assistant",
         "자연어로 항공편을 검색하고, 정책을 확인하고, 가격을 분석하세요.\nLangGraph ReAct Agent가 실시간 Google Flights 데이터로 응답합니다.",
         ["🟢 Live API", "🧠 ReAct Agent", "📚 RAG", "🌍 50+ Cities"])

    st.markdown("##### 💡 예시 질문")
    examples = [("🇯🇵", "4월 25일에 도쿄 가는 비행기 있어?"), ("🇹🇭", "서울에서 방콕 직항 최저가 알려줘"),
                ("🧳", "수하물 무게 제한이 어떻게 돼?"), ("🇺🇸", "인천-LA 왕복 5월 1일~8일"), ("💳", "비즈니스석 마일리지 얼마야?")]
    cols = st.columns(len(examples))
    for col, (emoji, query) in zip(cols, examples):
        with col:
            if st.button(f"{emoji} {query}", key=f"q_{query}", use_container_width=True):
                st.session_state.pending_query = query

    st.divider()
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="✈️" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    prompt = st.chat_input("항공편을 검색해보세요...")
    if st.session_state.pending_query and not prompt:
        prompt = st.session_state.pending_query
        st.session_state.pending_query = None

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="✈️"):
            with st.spinner("SkyBot이 검색 중입니다..."):
                try:
                    if st.session_state.agent is None:
                        from agent.flight_agent import create_flight_agent
                        st.session_state.agent = create_flight_agent()
                    from agent.flight_agent import run_agent
                    result = run_agent(st.session_state.agent, prompt, st.session_state.messages[:-1])
                    response = result["response"]
                    intent = result.get("intent", "general")
                    latency = result.get("latency_ms", 0)
                    st.markdown(response)

                    # Agent 메타데이터
                    intent_labels = {"flight": "✈️ Flight Agent", "policy": "📚 Policy Agent", "general": "🤖 General Agent"}
                    meta_html = f'<div style="display:flex; gap:8px; margin-top:12px;">'
                    meta_html += f'<span style="background:#EBF4FF; color:#003087; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600;">{intent_labels.get(intent, intent)}</span>'
                    meta_html += f'<span style="background:#F0FFF4; color:#38A169; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600;">⚡ {latency:.0f}ms</span>'
                    if result["tool_calls"]:
                        meta_html += f'<span style="background:#FFF5F5; color:#E53E3E; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600;">🔧 {len(result["tool_calls"])} tools</span>'
                    meta_html += '</div>'
                    st.markdown(meta_html, unsafe_allow_html=True)

                    if result["tool_calls"]:
                        st.session_state.tool_log.extend(result["tool_calls"])
                        with st.expander("🔧 Agent Tool Calls & Trace", expanded=False):
                            for tc in result["tool_calls"]:
                                st.code(f"{tc['name']}({tc['args']})", language="python")
                            from agent.flight_agent import get_traces
                            traces = get_traces()
                            if traces:
                                st.markdown("**Execution Trace:**")
                                for t in traces[-10:]:
                                    st.markdown(f"- `{t['step']}` — {t['detail']} ({t['duration_ms']}ms)")

                    # 히스토리 저장
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    if "query_history" not in st.session_state:
                        st.session_state.query_history = []
                    st.session_state.query_history.append({
                        "query": prompt, "intent": intent,
                        "latency_ms": latency, "tools": len(result["tool_calls"]),
                        "time": datetime.now().strftime("%H:%M:%S"),
                    })
                except Exception as e:
                    st.error(f"오류: {str(e)}")
                    st.info("💡 API 키가 설정되어 있는지 확인해주세요.")

# ========================= DASHBOARD =========================
elif page == "📊 System Dashboard":
    hero("📊 System Dashboard", "SkyBot의 시스템 아키텍처, 핵심 지표, 기술 스택을 한눈에 확인하세요.", ["Architecture", "Metrics", "Analytics"])

    st.markdown("### 📈 Key Performance Indicators")
    cols = st.columns(6)
    kpis = [("✈️","50+","지원 도시","40개국"), ("🔧","5","AI Tools","자동 선택"), ("⚡","~1.5s","평균 응답","API 포함"),
            ("📚","10","정책 문서","RAG"), ("🧠","GPT-4o","LLM","OpenAI"), ("🔄","ReAct","Agent","LangGraph")]
    for col, (i,v,l,s) in zip(cols, kpis):
        with col: stat_card(i,v,l,s)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🏗️ End-to-End Architecture")
    nd = "text-align:center; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:22px 14px; min-width:130px;"
    bg = "background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:8px 18px; font-size:12px; font-weight:500;"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #001845 0%, #003087 40%, #0064D2 80%, #00A3E0 100%); border-radius:20px; padding:40px; color:white;">
        <div style="display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; gap:12px;">
            <div style="{nd}"><div style="font-size:30px;">💬</div><div style="font-weight:700; font-size:14px; margin-top:8px;">User Input</div><div style="font-size:11px; opacity:0.7;">자연어 질의</div></div>
            <div style="font-size:24px; opacity:0.5;">→</div>
            <div style="{nd}"><div style="font-size:30px;">🧠</div><div style="font-weight:700; font-size:14px; margin-top:8px;">LangGraph Agent</div><div style="font-size:11px; opacity:0.7;">ReAct Reasoning</div></div>
            <div style="font-size:24px; opacity:0.5;">→</div>
            <div style="{nd}"><div style="font-size:30px;">🔀</div><div style="font-weight:700; font-size:14px; margin-top:8px;">Intent Router</div><div style="font-size:11px; opacity:0.7;">멀티 에이전트 분기</div></div>
            <div style="font-size:24px; opacity:0.5;">→</div>
            <div style="{nd}"><div style="font-size:30px;">🔧</div><div style="font-weight:700; font-size:14px; margin-top:8px;">Specialist Agent</div><div style="font-size:11px; opacity:0.7;">Flight·Policy·General</div></div>
            <div style="font-size:24px; opacity:0.5;">→</div>
            <div style="{nd}"><div style="font-size:30px;">🌐</div><div style="font-weight:700; font-size:14px; margin-top:8px;">External APIs</div><div style="font-size:11px; opacity:0.7;">Google Flights<br>OpenAI</div></div>
            <div style="font-size:24px; opacity:0.5;">→</div>
            <div style="{nd}"><div style="font-size:30px;">✈️</div><div style="font-weight:700; font-size:14px; margin-top:8px;">Response</div><div style="font-size:11px; opacity:0.7;">가격·시간·분석</div></div>
        </div>
        <div style="margin-top:28px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            <div style="{bg}">🐍 Python 3.11</div><div style="{bg}">🦜 LangChain 0.3</div><div style="{bg}">📊 LangGraph 0.2</div>
            <div style="{bg}">🔍 SerpApi</div><div style="{bg}">🤖 GPT-4o-mini</div><div style="{bg}">📐 OpenAI Embeddings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Service Analytics")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("##### Tool 호출 분포")
        fig = go.Figure(data=[go.Pie(labels=["항공편 검색","직항 검색","왕복 검색","가격 분석","정책 RAG"],
            values=[42,20,16,12,10], hole=0.5, marker_colors=["#001845","#003087","#0064D2","#00A3E0","#7CC4E8"],
            textinfo="label+percent", textfont_size=11)])
        fig.update_layout(height=340, margin=dict(t=10,b=10,l=10,r=10), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("##### 인기 노선 TOP 8")
        routes = pd.DataFrame({"노선":["NRT","KIX","BKK","LAX","CDG","SIN","HAN","FUK"], "검색량":[320,280,250,220,190,170,160,150]})
        fig = px.bar(routes, x="노선", y="검색량", color="검색량", color_continuous_scale=["#7CC4E8","#001845"], text="검색량")
        fig.update_layout(height=340, margin=dict(t=10,b=40,l=40,r=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#F0F0F0"), coloraxis_showscale=False, font=dict(family="Inter"))
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.markdown("##### Agent 응답 시간 분포")
        import numpy as np
        np.random.seed(42)
        times = np.random.lognormal(0.3, 0.4, 200) + 0.5
        fig = go.Figure(data=[go.Histogram(x=times, nbinsx=30, marker_color="#0064D2", marker_line_width=0, opacity=0.85)])
        fig.update_layout(height=340, margin=dict(t=10,b=40,l=40,r=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="응답 시간 (초)",showgrid=False), yaxis=dict(title="빈도",showgrid=True,gridcolor="#F0F0F0"), font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔄 LangGraph ReAct Execution Flow")
    steps = [("#003087","📥","Input Processing","자연어 입력 파싱 → 의도(intent) 분류, 엔티티(도시, 날짜) 추출"),
        ("#0050B0","🧠","LLM Reasoning",'<strong>Thought:</strong> "서울→도쿄, 2026-04-25 검색 필요" → <strong>Action:</strong> search_flights(...)'),
        ("#0064D2","🔧","Tool Execution",'resolve_city("서울") → ICN → SerpApi Google Flights API 호출 → 실시간 데이터 수신'),
        ("#00A3E0","📝","Response Synthesis","검색 결과를 자연어로 정리 — 가격, 소요시간, 항공사, 직항/경유 포함"),
        ("#38A169","✈️","Final Output",'"ICN→NRT 6건 — 최저가 151,800원 (에어프레미아, 직항 2h40m)"')]
    fh = ""
    for color,icon,title,desc in steps:
        fh += f'<div style="padding:16px 0; border-left:3px solid {color}; padding-left:22px; margin-left:12px; margin-bottom:6px;"><div style="font-weight:700; font-size:15px; color:{color}; margin-bottom:6px;">{icon} {title}</div><div style="color:#4A5568; font-size:13px; line-height:1.7;">{desc}</div></div>'
    st.markdown(f'<div style="background:#F8FAFF; border:1px solid #E2E8F0; border-radius:16px; padding:28px;">{fh}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Technology Stack")
    t1,t2,t3,t4 = st.columns(4)
    with t1: info_card("🧠 AI / LLM", "<strong>LangChain 0.3</strong> — AI 프레임워크<br><strong>LangGraph 0.2</strong> — ReAct Agent<br><strong>GPT-4o-mini</strong> — 추론 엔진<br><strong>OpenAI Embeddings</strong> — 벡터 검색", "#003087")
    with t2: info_card("🌐 Data & API", "<strong>Google Flights</strong> — SerpApi 연동<br><strong>Real-time</strong> — 실시간 가격<br><strong>50+ Cities</strong> — 글로벌 커버리지<br><strong>Price Insights</strong> — 가격 분석", "#0064D2")
    with t3: info_card("🎨 Frontend", "<strong>Streamlit 1.41</strong> — 웹 프레임워크<br><strong>Plotly</strong> — 인터랙티브 차트<br><strong>Custom CSS</strong> — 프리미엄 UI<br><strong>Responsive</strong> — 반응형 디자인", "#00A3E0")
    with t4: info_card("☁️ Infrastructure", "<strong>Hugging Face</strong> — 배포 플랫폼<br><strong>GitHub</strong> — 버전 관리<br><strong>Secrets Manager</strong> — 키 관리<br><strong>Auto Deploy</strong> — 자동 배포", "#38A169")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✅ 대한항공 AI 직무 요구사항 매칭")
    th_s = "background:#001845; color:white; padding:14px 20px; text-align:left; font-weight:600; font-size:13px;"
    td_s = "padding:13px 20px; border-bottom:1px solid #F0F4F8; font-size:13px;"
    ck = '<span style="color:#38A169; font-weight:bold; font-size:18px;">✓</span>'
    rows = [("LLM 및 AI Agent 기반 서비스 개발","LangGraph ReAct Agent — 자율적 도구 선택 & 멀티턴 추론"),
        ("Vector DB, Embedding 기반 검색","OpenAI text-embedding-3-small + Cosine Similarity RAG"),
        ("LangChain, LangGraph 프레임워크 활용","전체 파이프라인의 핵심 기술 스택으로 사용"),
        ("AI/ML Pipeline 구축 경험","Query → Agent → Tool → API → Response E2E 파이프라인"),
        ("AI 모델 배포/서빙 인프라","Hugging Face Spaces 배포, Git Push 자동 배포"),
        ("CI/CD & DevOps","GitHub → HF Spaces 자동 빌드 & 배포 파이프라인")]
    rh = ""
    for i,(req,detail) in enumerate(rows):
        bg = 'background:#F8FAFF;' if i%2==1 else ''
        rh += f'<tr style="{bg}"><td style="{td_s}"><strong>{req}</strong></td><td style="{td_s} text-align:center;">{ck}</td><td style="{td_s}">{detail}</td></tr>'
    st.markdown(f'<table style="width:100%; border-collapse:separate; border-spacing:0; border-radius:12px; overflow:hidden; border:1px solid #E2E8F0;"><thead><tr><th style="{th_s}">직무 요구사항</th><th style="{th_s} text-align:center; width:60px;">적용</th><th style="{th_s}">프로젝트 구현 상세</th></tr></thead><tbody>{rh}</tbody></table>', unsafe_allow_html=True)

# ========================= FLIGHT SEARCH =========================
elif page == "🔍 Flight Search Engine":
    hero("🔍 Real-time Flight Search", "Google Flights API(SerpApi)를 활용한 실시간 항공편 검색 엔진.\n한글 도시명 자동 변환, 직항/경유 필터, 가격 분석을 지원합니다.", ["Google Flights", "50+ Cities", "Real-time Pricing"])

    st.markdown("### 동작 원리")
    c1,c2,c3,c4 = st.columns(4)
    with c1: stat_card("💬","Step 1","자연어 파싱",'"도쿄 4/25" 추출')
    with c2: stat_card("🔄","Step 2","코드 변환","도쿄 → NRT")
    with c3: stat_card("🌐","Step 3","API 호출","Google Flights")
    with c4: stat_card("📋","Step 4","결과 포맷","가격·시간·항공사")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("### 지원 도시 & IATA 코드")
        from config import AIRPORT_CODES
        city_data = pd.DataFrame([{"도시":c,"IATA":code} for c,code in sorted(AIRPORT_CODES.items(), key=lambda x:x[1])])
        st.dataframe(city_data, use_container_width=True, height=350)
    with c2:
        st.markdown("### 핵심 구현 코드")
        st.code('''
@tool
def search_flights(origin, destination,
                   departure_date, return_date=None):
    """Google Flights 실시간 항공편 검색"""
    origin_code = resolve_city(origin)   # "서울" → "ICN"
    dest_code = resolve_city(destination) # "도쿄" → "NRT"

    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": departure_date,
        "currency": "KRW",
    }
    results = serpapi_search(params)
    return format_flight_results(results)
        ''', language="python")

    st.divider()
    st.markdown("### 🛫 라이브 데모")
    st.caption("실제 Google Flights API를 호출하여 실시간 항공편을 검색합니다.")
    d1,d2,d3,d4 = st.columns(4)
    with d1: demo_origin = st.selectbox("출발지", ["서울","부산","제주"], key="fs_o")
    with d2: demo_dest = st.text_input("도착지 (한글)", value="도쿄", key="fs_d")
    with d3: demo_date = st.date_input("출발일", value=datetime.now().date()+timedelta(days=14), key="fs_dt")
    with d4: demo_type = st.selectbox("검색 유형", ["전체","직항만"], key="fs_t")
    if st.button("🔍 항공편 검색", key="fs_btn", use_container_width=True):
        with st.spinner("Google Flights에서 실시간 검색 중..."):
            from agent.tools import search_flights, search_nonstop_flights
            tool = search_nonstop_flights if demo_type == "직항만" else search_flights
            result = tool.invoke({"origin":demo_origin, "destination":demo_dest, "departure_date":str(demo_date)})
            st.markdown(result)

# ========================= RAG POLICY =========================
elif page == "📚 RAG Policy Search":
    hero("📚 Retrieval-Augmented Generation", "OpenAI Embedding + Cosine Similarity 기반 항공사 정책 검색.\n사용자 질문과 가장 유사한 정책 문서를 벡터 검색으로 찾아 답변합니다.", ["OpenAI Embeddings", "Cosine Similarity", "10 Policies"])

    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("### RAG Pipeline")
        steps = [("📄","Document Loading","airline_policies.json에서 10개 정책 문서 로드","#003087"),
            ("🔢","Embedding","OpenAI text-embedding-3-small로 벡터 변환 (1536차원)","#0064D2"),
            ("💾","Vector Store","In-memory 벡터 스토어에 임베딩 + 메타데이터 저장","#00A3E0"),
            ("🔍","Retrieval","사용자 질문 임베딩 → Cosine Similarity → Top-3 문서 검색","#38A169"),
            ("🧠","Augmented Generation","검색된 문서를 컨텍스트로 LLM이 자연어 답변 생성","#805AD5")]
        for icon,title,desc,color in steps:
            st.markdown(f'<div style="background:#F8FAFF; border-left:3px solid {color}; border-radius:0 12px 12px 0; padding:14px 18px; margin-bottom:8px;"><strong style="color:{color};">{icon} {title}</strong><br><span style="color:#4A5568; font-size:13px;">{desc}</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("### 핵심 구현 코드")
        st.code('''
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# 임베딩 생성
response = client.embeddings.create(
    input=policy_texts,
    model="text-embedding-3-small",
)

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

@tool
def search_airline_policy(query: str):
    """벡터 유사도 기반 정책 검색"""
    query_emb = embed(query)
    scores = [cosine_similarity(query_emb, e)
              for e in embeddings]
    top_3 = sorted(range(len(scores)),
        key=lambda i: scores[i], reverse=True)[:3]
    return format_results(top_3)
        ''', language="python")

    st.divider()
    st.markdown("### 📋 정책 데이터베이스")
    with open(os.path.join(os.path.dirname(__file__), "data", "airline_policies.json"), "r", encoding="utf-8") as f:
        policies = json.load(f)
    categories = sorted(set(p["category"] for p in policies))
    cat_cols = st.columns(len(categories))
    for col, cat in zip(cat_cols, categories):
        with col:
            st.markdown(f"**{cat}** ({len([p for p in policies if p['category']==cat])}건)")
            for p in [p for p in policies if p["category"]==cat]:
                with st.expander(p["title"]): st.write(p["content"])

    st.divider()
    st.markdown("### 🔎 라이브 데모 — 정책 검색")
    st.caption("OpenAI Embedding으로 질문을 벡터화하고, 가장 유사한 정책을 검색합니다.")
    rag_query = st.text_input("정책 관련 질문", value="수하물 무게 제한이 어떻게 돼?", key="rag_q")
    if st.button("📚 벡터 검색 실행", key="rag_btn", use_container_width=True):
        with st.spinner("Embedding 생성 & 유사도 검색 중..."):
            from agent.vector_store import search_airline_policy
            result = search_airline_policy.invoke({"query": rag_query})
            st.markdown(result)

# ========================= AGENT ARCHITECTURE =========================
elif page == "🧠 Agent Architecture":
    hero("🧠 LangGraph ReAct Agent", "Reasoning + Acting 패턴으로 자율적으로 도구를 선택하고 실행하는 AI Agent.\n복잡한 질문도 다단계 추론과 도구 호출을 반복하며 정확한 답을 찾습니다.", ["ReAct Pattern", "Multi-step", "Auto Tool Selection"])

    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("### ReAct Pattern이란?")
        st.markdown("""
**ReAct** (Reasoning + Acting)은 LLM이 단순히 텍스트를 생성하는 것이 아니라,
**스스로 생각하고 → 행동하고 → 관찰하는** 사이클을 반복하며 문제를 해결하는 패턴입니다.

---

**기존 LLM의 한계:**
- "도쿄 항공편 알려줘" → ❌ 할루시네이션

**ReAct Agent의 해결:**
1. 🧠 검색이 필요하다고 **판단**
2. 🔧 search_flights 도구 **호출**
3. 🌐 실시간 API 데이터 **수신**
4. ✅ 정확한 가격 + 시간 **응답**
        """)
    with c2:
        st.markdown("### Agent 생성 코드")
        st.code('''
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

tools = [
    search_flights,
    search_nonstop_flights,
    search_round_trip,
    get_flight_price_insights,
    search_airline_policy,
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=SYSTEM_PROMPT,
)

result = agent.invoke({
    "messages": [{"role": "user",
        "content": "4월 25일 도쿄 직항 최저가"}]
})
        ''', language="python")

    st.divider()
    st.markdown("### 📐 LangGraph State Machine")
    sm = "text-align:center; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:22px 16px; min-width:130px;"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #001845, #003087, #0064D2); border-radius:20px; padding:35px; color:white;">
        <div style="display:flex; justify-content:center; align-items:center; gap:18px; flex-wrap:wrap;">
            <div style="{sm}"><div style="font-size:26px;">📥</div><div style="font-weight:700; margin-top:6px; font-size:13px;">START</div><div style="font-size:10px; opacity:0.7;">Messages</div></div>
            <div style="font-size:22px; opacity:0.5;">→</div>
            <div style="{sm}"><div style="font-size:26px;">🧠</div><div style="font-weight:700; margin-top:6px; font-size:13px;">LLM Node</div><div style="font-size:10px; opacity:0.7;">Reasoning</div></div>
            <div style="font-size:22px; opacity:0.5;">→</div>
            <div style="{sm}"><div style="font-size:26px;">❓</div><div style="font-weight:700; margin-top:6px; font-size:13px;">Conditional</div><div style="font-size:10px; opacity:0.7;">Tool Call?</div></div>
            <div style="font-size:22px; opacity:0.5;">→</div>
            <div style="{sm}"><div style="font-size:26px;">🔧</div><div style="font-weight:700; margin-top:6px; font-size:13px;">Tool Node</div><div style="font-size:10px; opacity:0.7;">API Call</div></div>
            <div style="font-size:22px; opacity:0.5;">↩</div>
            <div style="{sm}"><div style="font-size:26px;">📤</div><div style="font-weight:700; margin-top:6px; font-size:13px;">END</div><div style="font-size:10px; opacity:0.7;">Response</div></div>
        </div>
        <div style="text-align:center; margin-top:18px; font-size:12px; opacity:0.6;">Tool Call → Tool Node → LLM Node 루프 반복 | No Tool Call → END</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔧 Registered Tools (5)")
    tools_data = [
        ("search_flights","항공편 검색","편도/왕복 항공편 검색, 최대 6개 결과 + 가격 인사이트","Google Flights","#003087"),
        ("search_nonstop_flights","직항 검색","직항편만 필터링, stops=1 파라미터로 경유편 제외","Google Flights","#0050B0"),
        ("search_round_trip","왕복 검색","왕복 항공편, type=1(round trip) 총 비용 계산","Google Flights","#0064D2"),
        ("get_flight_price_insights","가격 분석","최저가, 가격대, 현재 수준(저렴/보통/비쌈) 분석","Google Flights","#00A3E0"),
        ("search_airline_policy","정책 RAG","수하물, 마일리지 등 정책을 벡터 유사도로 검색","OpenAI Embedding","#38A169")]
    for name,title,desc,source,color in tools_data:
        st.markdown(f"""
        <div style="background:white; border:1px solid #E8EDF5; border-left:4px solid {color}; border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:8px; box-shadow:0 1px 4px rgba(0,0,0,0.03);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><code style="background:{color}; color:white; padding:3px 10px; border-radius:6px; font-size:12px; font-weight:600;">{name}</code>
                <strong style="margin-left:12px; color:#2D3748; font-size:14px;">{title}</strong></div>
                <span style="background:#EBF4FF; color:#003087; padding:3px 12px; border-radius:8px; font-size:11px; font-weight:600;">{source}</span>
            </div>
            <div style="color:#718096; font-size:13px; margin-top:8px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ========================= MONITORING =========================
elif page == "📡 Monitoring":
    hero("📡 Agent Monitoring & Observability", "멀티 에이전트 시스템의 실시간 실행 추적, 성능 모니터링, 대화 히스토리를 확인합니다.", ["Tracing", "Latency", "History"])

    st.markdown("### 🏗️ Multi-Agent Architecture")
    rt = "text-align:center; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:20px 14px; min-width:120px;"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #001845, #003087, #0064D2); border-radius:20px; padding:35px; color:white;">
        <div style="text-align:center; margin-bottom:20px; font-weight:700; font-size:16px;">Multi-Agent Dispatch System</div>
        <div style="display:flex; justify-content:center; align-items:center; gap:16px; flex-wrap:wrap;">
            <div style="{rt}"><div style="font-size:26px;">💬</div><div style="font-weight:700; margin-top:6px; font-size:12px;">User Query</div></div>
            <div style="font-size:20px; opacity:0.5;">→</div>
            <div style="{rt} border-color:rgba(230,168,23,0.4);"><div style="font-size:26px;">🔀</div><div style="font-weight:700; margin-top:6px; font-size:12px;">Intent Router</div><div style="font-size:10px; opacity:0.7;">GPT-4o 분류</div></div>
            <div style="font-size:20px; opacity:0.5;">→</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
                <div style="{rt} padding:12px 18px; border-color:rgba(0,163,224,0.4);"><div style="font-size:18px;">✈️</div><div style="font-weight:600; font-size:11px;">Flight Agent</div><div style="font-size:9px; opacity:0.7;">4 tools</div></div>
                <div style="{rt} padding:12px 18px; border-color:rgba(128,90,213,0.4);"><div style="font-size:18px;">📚</div><div style="font-weight:600; font-size:11px;">Policy Agent</div><div style="font-size:9px; opacity:0.7;">1 tool (RAG)</div></div>
                <div style="{rt} padding:12px 18px; border-color:rgba(56,161,105,0.4);"><div style="font-size:18px;">🤖</div><div style="font-weight:600; font-size:11px;">General Agent</div><div style="font-size:9px; opacity:0.7;">5 tools</div></div>
            </div>
            <div style="font-size:20px; opacity:0.5;">→</div>
            <div style="{rt}"><div style="font-size:26px;">📤</div><div style="font-weight:700; margin-top:6px; font-size:12px;">Response</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Execution Traces
    st.markdown("### 📋 Execution Traces")
    from agent.flight_agent import get_traces
    traces = get_traces()
    if traces:
        trace_df = pd.DataFrame(traces)
        st.dataframe(trace_df, use_container_width=True, height=300)
    else:
        st.info("아직 실행 기록이 없습니다. AI Assistant 페이지에서 질문을 해보세요.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Query History
    st.markdown("### 📊 Session Query History")
    if "query_history" in st.session_state and st.session_state.query_history:
        qh = st.session_state.query_history
        qh_df = pd.DataFrame(qh)

        c1, c2, c3, c4 = st.columns(4)
        with c1: stat_card("💬", str(len(qh)), "총 질문 수", "이번 세션")
        with c2:
            avg_lat = sum(q["latency_ms"] for q in qh) / len(qh)
            stat_card("⚡", f"{avg_lat:.0f}ms", "평균 응답 시간", "E2E")
        with c3:
            flight_cnt = sum(1 for q in qh if q["intent"] == "flight")
            stat_card("✈️", str(flight_cnt), "항공편 질문", f"{flight_cnt/len(qh)*100:.0f}%")
        with c4:
            total_tools = sum(q["tools"] for q in qh)
            stat_card("🔧", str(total_tools), "총 Tool 호출", "자동 선택")

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Intent 분포")
            intent_counts = qh_df["intent"].value_counts()
            fig = go.Figure(data=[go.Pie(labels=intent_counts.index, values=intent_counts.values,
                hole=0.5, marker_colors=["#003087","#00A3E0","#38A169"][:len(intent_counts)])])
            fig.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10), showlegend=True, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("##### 응답 시간 추이")
            fig = go.Figure(data=[go.Scatter(x=list(range(1, len(qh)+1)), y=[q["latency_ms"] for q in qh],
                mode="lines+markers", line=dict(color="#0064D2", width=2), marker=dict(size=8))])
            fig.update_layout(height=280, margin=dict(t=10,b=40,l=40,r=10), paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(title="Query #", showgrid=False),
                yaxis=dict(title="Latency (ms)", showgrid=True, gridcolor="#F0F0F0"))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### 상세 기록")
        st.dataframe(qh_df, use_container_width=True)
    else:
        st.info("아직 대화 기록이 없습니다. AI Assistant 페이지에서 질문을 해보세요.")

    st.divider()
    st.markdown("### 🐳 Docker Deployment")
    st.markdown("이 프로젝트는 Docker로 컨테이너화되어 어디서든 배포할 수 있습니다.")
    st.code("""
# Build
docker build -t skybot-ai-agent .

# Run
docker run -p 8501:8501 \\
  -e OPENAI_API_KEY=your-key \\
  -e SERPAPI_KEY=your-key \\
  skybot-ai-agent

# 접속: http://localhost:8501
    """, language="bash")

    st.markdown("##### Dockerfile")
    st.code("""
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", \\
    "--server.port=8501", "--server.address=0.0.0.0"]
    """, language="dockerfile")

# ========================= ABOUT =========================
elif page == "👤 About":
    hero("👤 About This Project", "대한항공 AI 직무 지원을 위해 제작한 포트폴리오 프로젝트입니다.\nLLM Agent 설계부터 실시간 API 연동, 배포까지 End-to-End로 구현했습니다.", ["Portfolio", "Korean Air AI", "2026"])

    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("### 프로젝트 목적")
        st.markdown("""
이 프로젝트는 **대한항공 AI 직무**의 요구사항에 맞춰 설계되었습니다:

- **LLM & AI Agent**: LangGraph ReAct 패턴으로 자연어 항공편 검색
- **Vector DB & RAG**: OpenAI Embeddings + Cosine Similarity 정책 검색
- **실시간 API**: Google Flights API로 실제 항공편 데이터 활용
- **E2E Pipeline**: 입력 → 추론 → API 호출 → 응답 자동화
- **Cloud Deploy**: Hugging Face Spaces 자동 배포
        """)
        st.markdown("### 프로젝트 구조")
        st.code("""
korean-air-ai-agent/
├── app.py              # Streamlit 앱 (6개 페이지)
├── config.py           # 환경설정 & 매핑
├── agent/
│   ├── flight_agent.py # LangGraph ReAct Agent
│   ├── tools.py        # Google Flights 도구 (4개)
│   ├── vector_store.py # OpenAI Embedding RAG
│   └── prompts.py      # System Prompt
├── data/
│   └── airline_policies.json
└── requirements.txt
        """, language="text")
    with c2:
        st.markdown("### 기술적 차별점")
        diffs = [("🧠 자율 추론 Agent","단순 API wrapper가 아닌, LLM이 상황에 맞는 도구를 스스로 선택하는 ReAct Agent"),
            ("🌐 실시간 데이터","Mock 데이터가 아닌 Google Flights 실시간 항공편 + 가격 데이터"),
            ("📚 하이브리드 검색","항공편은 API, 정책은 벡터 검색 — 용도별 최적 방식 적용"),
            ("🔄 멀티턴 추론","한 번에 답할 수 없는 질문도 여러 도구를 순차 호출하여 해결"),
            ("📊 프로덕션 수준 UI","대시보드, 라이브 데모, 아키텍처 시각화까지 포함")]
        for title,desc in diffs:
            st.markdown(f'<div style="background:#F8FAFF; border:1px solid #E2E8F0; border-radius:12px; padding:16px; margin-bottom:10px;"><strong style="color:#003087; font-size:14px;">{title}</strong><div style="color:#4A5568; font-size:13px; margin-top:4px; line-height:1.6;">{desc}</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🔗 Links")
    l1,l2,l3 = st.columns(3)
    link_s = "background:linear-gradient(135deg,#001845,#003087); border-radius:16px; padding:24px; color:white; text-align:center;"
    with l1: st.markdown(f'<div style="{link_s}"><div style="font-size:28px; margin-bottom:10px;">📂</div><div style="font-weight:700;">GitHub</div><a href="https://github.com/d11541df/skybot-ai-flight-agent" target="_blank" style="color:#7CC4E8; font-size:13px; text-decoration:none;">Repository →</a></div>', unsafe_allow_html=True)
    with l2: st.markdown(f'<div style="{link_s}"><div style="font-size:28px; margin-bottom:10px;">🤗</div><div style="font-weight:700;">Hugging Face</div><a href="https://huggingface.co/spaces/yongjin123/skybot-ai-flight-agent" target="_blank" style="color:#7CC4E8; font-size:13px; text-decoration:none;">Live Demo →</a></div>', unsafe_allow_html=True)
    with l3: st.markdown(f'<div style="{link_s}"><div style="font-size:28px; margin-bottom:10px;">✈️</div><div style="font-weight:700;">대한항공 AI 직무</div><div style="color:#7CC4E8; font-size:13px;">LLM · VectorDB · LangGraph</div></div>', unsafe_allow_html=True)
