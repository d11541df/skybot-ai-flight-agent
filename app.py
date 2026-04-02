"""SkyBot - Korean Air AI Flight Assistant (Portfolio Demo)"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="SkyBot | AI Flight Assistant",
    page_icon="https://www.koreanair.com/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* 메인 헤더 */
    .hero-section {
        background: linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%);
        border-radius: 20px;
        padding: 40px 50px;
        color: white;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-section h1 {
        margin: 0;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
    }
    .hero-section .subtitle {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 16px;
        font-weight: 300;
    }
    .hero-section .badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 12px;
        margin-top: 12px;
        backdrop-filter: blur(10px);
    }

    /* 카드 스타일 */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(0, 100, 210, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 48, 135, 0.06);
        backdrop-filter: blur(10px);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 48, 135, 0.12);
    }

    /* 메트릭 카드 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%);
        border: 1px solid rgba(0, 100, 210, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0, 48, 135, 0.05);
    }
    [data-testid="stMetricValue"] {
        color: #003087;
        font-weight: 700;
    }

    /* 채팅 */
    .stChatMessage {
        border-radius: 16px !important;
        border: 1px solid rgba(0,100,210,0.06) !important;
    }
    .stChatInputContainer {
        border-radius: 16px !important;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8faff 0%, #eef4ff 100%);
    }

    /* 탭 */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
    }

    /* 쿼리 카드 */
    .query-card {
        background: linear-gradient(135deg, #EBF4FF 0%, #F0F7FF 100%);
        border: 1px solid #BEE3F8;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        font-size: 14px;
        color: #1A365D;
        cursor: pointer;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
        font-weight: 500;
    }
    .query-card:hover {
        background: linear-gradient(135deg, #D6E8FF 0%, #E6F0FF 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,100,210,0.15);
    }

    /* 아키텍처 */
    .arch-container {
        background: linear-gradient(135deg, #003087 0%, #0064D2 50%, #00A3E0 100%);
        border-radius: 20px;
        padding: 35px;
        color: white;
    }
    .arch-node {
        text-align: center;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 16px;
        padding: 24px 16px;
        min-width: 150px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .arch-node:hover { transform: scale(1.05); }
    .arch-node .icon { font-size: 32px; margin-bottom: 10px; }
    .arch-node .title { font-weight: 700; font-size: 15px; }
    .arch-node .desc { font-size: 12px; opacity: 0.8; margin-top: 4px; }

    .tech-badge {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: 500;
    }

    /* 플로우 */
    .flow-container {
        background: linear-gradient(135deg, #f8faff 0%, #fff 100%);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 30px;
    }
    .flow-step {
        padding: 12px 0;
        border-left: 3px solid;
        padding-left: 20px;
        margin-left: 10px;
    }
    .flow-step .label {
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 6px;
    }
    .flow-step .detail {
        color: #4A5568;
        font-size: 14px;
        line-height: 1.6;
    }

    /* 매칭 테이블 */
    .match-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    .match-table th {
        background: #003087;
        color: white;
        padding: 14px 20px;
        text-align: left;
        font-weight: 600;
        font-size: 14px;
    }
    .match-table td {
        padding: 12px 20px;
        border-bottom: 1px solid #F0F4F8;
        font-size: 14px;
    }
    .match-table tr:nth-child(even) { background: #F8FAFF; }
    .match-table tr:hover { background: #EBF4FF; }
    .match-check { color: #38A169; font-weight: bold; font-size: 18px; }

    /* 사이드바 버튼 */
    [data-testid="stSidebar"] div.stButton > button {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        color: #2D3748;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 12px;
        text-align: left;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: #EBF4FF;
        border-color: #90CDF4;
        color: #003087;
        transform: translateX(4px);
    }

    /* Hide branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 스크롤바 */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: #0064D2; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div style="
            width: 80px; height: 80px; margin: 0 auto;
            background: linear-gradient(135deg, #003087, #00A3E0);
            border-radius: 20px;
            display: flex; align-items: center; justify-content: center;
            font-size: 36px;
            box-shadow: 0 8px 24px rgba(0,48,135,0.25);
        ">✈️</div>
        <h2 style="color: #003087; margin: 15px 0 0 0; font-weight: 800; letter-spacing: -0.5px;">SkyBot</h2>
        <p style="color: #718096; font-size: 13px; font-weight: 400;">AI Flight Assistant</p>
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, #003087, #0064D2);
            color: white;
            border-radius: 20px;
            padding: 4px 16px;
            font-size: 11px;
            font-weight: 600;
            margin-top: 4px;
        ">PORTFOLIO PROJECT</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        ["💬 AI Chat", "📊 Dashboard",
         "🔍 실시간 항공편 검색", "💰 최저가 비교 분석",
         "📚 항공사 정책 RAG", "🧠 Agent 아키텍처"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("""
    <div style="padding: 0 5px;">
        <h4 style="color: #003087; font-weight: 700; margin-bottom: 12px;">Tech Stack</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">LangChain</span>
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">LangGraph</span>
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">GPT-4o</span>
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">ChromaDB</span>
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">Google Flights</span>
            <span style="background: #EBF4FF; color: #003087; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;">Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="text-align: center; font-size: 11px; color: #A0AEC0; line-height: 1.6;">
        Built for <strong>Korean Air</strong> AI Position<br>
        Portfolio Project 2026
    </div>
    """, unsafe_allow_html=True)


# ==================== AI CHAT PAGE ====================
if page == "💬 AI Chat":
    hero = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px; position:relative; overflow:hidden;"
    badge = "display:inline-block; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); border-radius:20px; padding:4px 14px; font-size:12px; margin-top:12px; margin-right:6px;"
    st.markdown(f"""
    <div style="{hero}">
        <h1 style="margin:0; font-size:42px; font-weight:800; letter-spacing:-1px;">✈️ SkyBot</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">
            대한항공 AI 항공편 어시스턴트 — LangChain + LangGraph + Google Flights API
        </p>
        <span style="{badge}">🟢 Real-time Flight Data</span>
        <span style="{badge}">🤖 AI Agent (ReAct)</span>
        <span style="{badge}">📚 RAG Policy Search</span>
    </div>
    """, unsafe_allow_html=True)

    # 예시 쿼리 (클릭 가능)
    st.markdown("#### 이런 질문을 해보세요")
    examples = [
        ("🇯🇵", "4월 25일에 도쿄 가는 비행기 있어?"),
        ("🇹🇭", "서울에서 방콕 직항 최저가 알려줘"),
        ("🧳", "수하물 무게 제한이 어떻게 돼?"),
        ("🇺🇸", "인천-LA 왕복 5월 1일~8일"),
        ("💳", "비즈니스석 마일리지 얼마야?"),
    ]

    cols = st.columns(len(examples))
    for col, (emoji, query) in zip(cols, examples):
        with col:
            if st.button(f"{emoji} {query}", key=f"q_{query}", use_container_width=True):
                st.session_state.pending_query = query

    # 메인 영역 버튼 스타일
    st.markdown("""
    <style>
        [data-testid="stMain"] div.stButton > button {
            background: linear-gradient(135deg, #EBF4FF 0%, #F0F7FF 100%);
            border: 1px solid #BEE3F8;
            border-radius: 12px;
            color: #1A365D;
            font-size: 13px;
            font-weight: 500;
            padding: 12px 8px;
            min-height: 70px;
            white-space: normal;
            line-height: 1.4;
            transition: all 0.2s;
        }
        [data-testid="stMain"] div.stButton > button:hover {
            background: linear-gradient(135deg, #D6E8FF 0%, #E6F0FF 100%);
            border-color: #90CDF4;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,100,210,0.15);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "tool_log" not in st.session_state:
        st.session_state.tool_log = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="✈️" if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    # 버튼 클릭 or 직접 입력 처리
    prompt = st.chat_input("항공편을 검색해보세요... (예: 4월 25일 도쿄 가는 비행기 있어?)")

    if st.session_state.pending_query and not prompt:
        prompt = st.session_state.pending_query
        st.session_state.pending_query = None

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="✈️"):
            with st.spinner("SkyBot이 항공편을 검색하고 있습니다..."):
                try:
                    if st.session_state.agent is None:
                        from agent.flight_agent import create_flight_agent
                        st.session_state.agent = create_flight_agent()

                    from agent.flight_agent import run_agent
                    result = run_agent(
                        st.session_state.agent,
                        prompt,
                        st.session_state.messages[:-1],
                    )

                    response = result["response"]
                    st.markdown(response)

                    if result["tool_calls"]:
                        st.session_state.tool_log.extend(result["tool_calls"])
                        with st.expander("🔧 Agent Tool Calls (디버그)", expanded=False):
                            for tc in result["tool_calls"]:
                                st.code(f"{tc['name']}({tc['args']})", language="python")

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    error_msg = f"오류가 발생했습니다: {str(e)}"
                    st.error(error_msg)
                    st.info("💡 .env 파일에 OPENAI_API_KEY와 SERPAPI_KEY가 설정되어 있는지 확인해주세요.")


# ==================== DASHBOARD PAGE ====================
elif page == "📊 Dashboard":
    hero2 = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px;"
    badge2 = "display:inline-block; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); border-radius:20px; padding:4px 14px; font-size:12px; margin-top:12px; margin-right:6px;"
    st.markdown(f"""
    <div style="{hero2}">
        <h1 style="margin:0; font-size:42px; font-weight:800; letter-spacing:-1px;">📊 System Dashboard</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">SkyBot 시스템 아키텍처, 성능 메트릭 & 기술 스택</p>
        <span style="{badge2}">Architecture</span>
        <span style="{badge2}">Performance</span>
        <span style="{badge2}">Tech Details</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Metrics ---
    st.markdown("### 📈 Core Metrics")
    cols = st.columns(5)
    metrics = [
        ("지원 도시", "50+", "40개국 커버"),
        ("API 응답 속도", "~1.5s", "Google Flights"),
        ("정책 DB", "10건", "ChromaDB RAG"),
        ("AI Tools", "5개", "Tool Calling"),
        ("LLM", "GPT-4o", "OpenAI"),
    ]
    for col, (label, value, sub) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value, delta=sub)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Architecture ---
    st.markdown("### 🏗️ System Architecture")

    arch_node_style = "text-align:center; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:24px 16px; min-width:150px; backdrop-filter:blur(10px);"
    badge_style = "background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:10px 20px; font-size:13px; font-weight:500;"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #003087 0%, #0064D2 50%, #00A3E0 100%); border-radius:20px; padding:35px; color:white;">
        <div style="display:flex; justify-content:space-around; align-items:center; flex-wrap:wrap; gap:15px;">
            <div style="{arch_node_style}">
                <div style="font-size:32px; margin-bottom:10px;">💬</div>
                <div style="font-weight:700; font-size:15px;">User Query</div>
                <div style="font-size:12px; opacity:0.8; margin-top:4px;">자연어 입력<br>"도쿄 가는 비행기"</div>
            </div>
            <div style="font-size:28px; opacity:0.6;">→</div>
            <div style="{arch_node_style}">
                <div style="font-size:32px; margin-bottom:10px;">🧠</div>
                <div style="font-weight:700; font-size:15px;">LangGraph Agent</div>
                <div style="font-size:12px; opacity:0.8; margin-top:4px;">ReAct Pattern<br>Reasoning + Acting</div>
            </div>
            <div style="font-size:28px; opacity:0.6;">→</div>
            <div style="{arch_node_style}">
                <div style="font-size:32px; margin-bottom:10px;">🔧</div>
                <div style="font-weight:700; font-size:15px;">Tool Router</div>
                <div style="font-size:12px; opacity:0.8; margin-top:4px;">5개 도구 자동 선택<br>Flight · RAG · Insight</div>
            </div>
            <div style="font-size:28px; opacity:0.6;">→</div>
            <div style="{arch_node_style}">
                <div style="font-size:32px; margin-bottom:10px;">🌐</div>
                <div style="font-weight:700; font-size:15px;">Google Flights</div>
                <div style="font-size:12px; opacity:0.8; margin-top:4px;">SerpApi 연동<br>Real-time Data</div>
            </div>
            <div style="font-size:28px; opacity:0.6;">→</div>
            <div style="{arch_node_style}">
                <div style="font-size:32px; margin-bottom:10px;">✈️</div>
                <div style="font-weight:700; font-size:15px;">Response</div>
                <div style="font-size:12px; opacity:0.8; margin-top:4px;">구조화된 응답<br>가격·시간·항공사</div>
            </div>
        </div>
        <div style="margin-top:30px; display:flex; justify-content:center; gap:15px; flex-wrap:wrap;">
            <div style="{badge_style}">🐍 Python 3.11</div>
            <div style="{badge_style}">🦜 LangChain 0.3</div>
            <div style="{badge_style}">📊 LangGraph 0.2</div>
            <div style="{badge_style}">🔍 SerpApi</div>
            <div style="{badge_style}">💾 ChromaDB</div>
            <div style="{badge_style}">🤖 GPT-4o-mini</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts ---
    st.markdown("### 📊 Analytics")

    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Tool Usage Distribution")
        fig = go.Figure(data=[go.Pie(
            labels=["항공편 검색", "직항 검색", "왕복 검색", "가격 분석", "정책 RAG"],
            values=[40, 20, 18, 12, 10],
            hole=0.45,
            marker_colors=["#003087", "#0064D2", "#00A3E0", "#6B9FD7", "#B8D4F0"],
            textinfo="label+percent",
            textfont_size=12,
        )])
        fig.update_layout(
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Popular Routes from ICN")
        routes = pd.DataFrame({
            "노선": ["NRT", "KIX", "BKK", "LAX", "CDG", "SIN", "HAN", "FUK"],
            "검색량": [320, 280, 250, 220, 190, 170, 160, 150],
        })
        fig = px.bar(
            routes, x="노선", y="검색량",
            color="검색량",
            color_continuous_scale=["#B8D4F0", "#003087"],
            text="검색량",
        )
        fig.update_layout(
            height=380,
            margin=dict(t=20, b=40, l=40, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
            coloraxis_showscale=False,
            font=dict(family="Inter"),
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Agent Flow ---
    st.markdown("### 🔄 LangGraph Agent Flow")

    step_base = "padding:14px 0; border-left:3px solid; padding-left:20px; margin-left:10px; margin-bottom:4px;"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #f8faff 0%, #fff 100%); border:1px solid #E2E8F0; border-radius:16px; padding:30px;">
        <div style="{step_base} border-color:#0064D2;">
            <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#0064D2;">📥 Step 1 — Input Processing</div>
            <div style="color:#4A5568; font-size:14px; line-height:1.6;">
                사용자 입력: <code>"4월 25일 도쿄 가는 비행기 있어?"</code><br>
                자연어를 분석하여 의도(intent)와 엔티티(entity) 추출
            </div>
        </div>
        <div style="{step_base} border-color:#E6A817;">
            <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#E6A817;">🧠 Step 2 — LLM Reasoning (ReAct)</div>
            <div style="color:#4A5568; font-size:14px; line-height:1.6;">
                <strong>Thought:</strong> 서울→도쿄, 2026-04-25 항공편 검색이 필요<br>
                <strong>Action:</strong> search_flights(origin="서울", destination="도쿄", departure_date="2026-04-25")
            </div>
        </div>
        <div style="{step_base} border-color:#38A169;">
            <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#38A169;">🔧 Step 3 — Tool Execution</div>
            <div style="color:#4A5568; font-size:14px; line-height:1.6;">
                resolve_city("서울") → <code>ICN</code> | resolve_city("도쿄") → <code>NRT</code><br>
                Google Flights API 호출 → 실시간 항공편 데이터 수신 (가격, 시간, 항공사)
            </div>
        </div>
        <div style="{step_base} border-color:#805AD5;">
            <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#805AD5;">📝 Step 4 — Response Synthesis</div>
            <div style="color:#4A5568; font-size:14px; line-height:1.6;">
                검색 결과를 자연어로 정리 — 가격, 소요시간, 항공사, 직항/경유 정보 포함
            </div>
        </div>
        <div style="{step_base} border-color:#E53E3E;">
            <div style="font-weight:700; font-size:15px; margin-bottom:6px; color:#E53E3E;">✈️ Step 5 — Output</div>
            <div style="color:#4A5568; font-size:14px; line-height:1.6;">
                "4월 25일 인천→나리타 항공편 6건을 찾았습니다! 최저가 151,800원 (에어프레미아)..."
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tech Stack Cards ---
    st.markdown("### 🛠️ Technology Stack")
    cols = st.columns(4)
    stacks = [
        ("🧠 AI / LLM", "#003087", [
            ("LangChain", "AI 프레임워크"),
            ("LangGraph", "ReAct Agent"),
            ("GPT-4o-mini", "언어모델"),
            ("ChromaDB", "Vector DB (RAG)"),
        ]),
        ("🌐 Data API", "#0064D2", [
            ("Google Flights", "SerpApi 연동"),
            ("Real-time", "실시간 데이터"),
            ("50+ Cities", "글로벌 커버리지"),
            ("Price Insights", "가격 분석"),
        ]),
        ("🎨 Frontend", "#00A3E0", [
            ("Streamlit", "웹 프레임워크"),
            ("Plotly", "인터랙티브 차트"),
            ("Custom CSS", "프리미엄 UI"),
            ("Responsive", "반응형 디자인"),
        ]),
        ("☁️ Infrastructure", "#38A169", [
            ("Streamlit Cloud", "배포 플랫폼"),
            ("GitHub", "버전 관리"),
            ("python-dotenv", "환경변수 관리"),
            ("CI/CD Ready", "자동 배포"),
        ]),
    ]

    for col, (title, color, items) in zip(cols, stacks):
        with col:
            items_html = "".join(
                f'<div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F0F4F8;">'
                f'<span style="font-weight: 600; color: #2D3748; font-size: 13px;">{name}</span>'
                f'<span style="color: #718096; font-size: 12px;">{desc}</span></div>'
                for name, desc in items
            )
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.95); border:1px solid rgba(0,100,210,0.08); border-radius:16px; padding:24px; box-shadow:0 4px 20px rgba(0,48,135,0.06); height:280px;">
                <div style="
                    font-size:18px; font-weight:700; color:{color};
                    margin-bottom:16px; padding-bottom:12px;
                    border-bottom:2px solid {color}20;
                ">{title}</div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Job Requirement Matching ---
    st.markdown("### ✅ 대한항공 AI 직무 요구사항 매칭")
    th_style = "background:#003087; color:white; padding:14px 20px; text-align:left; font-weight:600; font-size:14px;"
    td_style = "padding:12px 20px; border-bottom:1px solid #F0F4F8; font-size:14px;"
    check = '<span style="color:#38A169; font-weight:bold; font-size:18px;">✓</span>'

    st.markdown(f"""
    <table style="width:100%; border-collapse:separate; border-spacing:0; border-radius:12px; overflow:hidden; border:1px solid #E2E8F0;">
        <thead>
            <tr>
                <th style="{th_style}">직무 요구사항</th>
                <th style="{th_style}">적용</th>
                <th style="{th_style}">상세</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="{td_style}"><strong>LLM 및 AI Agent 기반 서비스 개발</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">LangGraph ReAct Agent로 자연어 항공편 검색 구현</td>
            </tr>
            <tr style="background:#F8FAFF;">
                <td style="{td_style}"><strong>Vector DB, Embedding 기반 검색</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">ChromaDB로 항공사 정책 RAG 검색 구현</td>
            </tr>
            <tr>
                <td style="{td_style}"><strong>LangChain, LangGraph 프레임워크</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">핵심 기술 스택으로 전체 파이프라인 구축</td>
            </tr>
            <tr style="background:#F8FAFF;">
                <td style="{td_style}"><strong>AI/ML Pipeline 구축</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">Query → Agent → Tool → API → Response 파이프라인</td>
            </tr>
            <tr>
                <td style="{td_style}"><strong>AI 모델 배포/서빙 인프라</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">Streamlit Cloud 배포, 실시간 서빙</td>
            </tr>
            <tr style="background:#F8FAFF;">
                <td style="{td_style}"><strong>CI/CD & DevOps</strong></td>
                <td style="{td_style}">{check}</td>
                <td style="{td_style}">GitHub + Streamlit Cloud 자동 배포 파이프라인</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Project Structure ---
    st.markdown("### 📁 Project Structure")
    st.code("""
korean-air-ai-agent/
├── app.py                  # Streamlit 메인 앱 (Chat + Dashboard)
├── config.py               # 환경 설정 & 도시/항공사 매핑
│
├── agent/
│   ├── flight_agent.py     # LangGraph ReAct Agent 생성 & 실행
│   ├── tools.py            # Google Flights API 도구 (SerpApi)
│   ├── vector_store.py     # ChromaDB 벡터 스토어 (RAG)
│   └── prompts.py          # System Prompt 관리
│
├── dashboard/
│   └── components.py       # 대시보드 UI 컴포넌트
│
├── data/
│   └── airline_policies.json  # 항공사 정책 데이터 (10건)
│
├── .streamlit/
│   └── config.toml         # Streamlit 테마 설정
│
├── requirements.txt        # Python 의존성
├── .env                    # API Keys (gitignore)
└── .gitignore
    """, language="text")


# ==================== FEATURE: 실시간 항공편 검색 ====================
elif page == "🔍 실시간 항공편 검색":
    hero_s = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px;"
    st.markdown(f"""
    <div style="{hero_s}">
        <h1 style="margin:0; font-size:38px; font-weight:800;">🔍 실시간 항공편 검색</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">
            Google Flights API를 활용한 실시간 항공편 데이터 검색
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 기능 설명
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 어떻게 동작하나요?")
        st.markdown("""
        1. **자연어 입력 파싱** — "4월 25일 도쿄" → 날짜, 도시 자동 추출
        2. **도시명 → IATA 코드 변환** — "도쿄" → `NRT`, "서울" → `ICN`
        3. **SerpApi Google Flights 호출** — 실시간 항공편 + 가격 데이터
        4. **결과 포맷팅** — 항공사, 시간, 가격, 직항/경유 정리
        """)

        st.markdown("### 지원 도시 (50+)")
        st.markdown("""
        **일본** — 도쿄(NRT), 오사카(KIX), 후쿠오카(FUK), 삿포로(CTS)
        **동남아** — 방콕(BKK), 싱가포르(SIN), 하노이(HAN), 다낭(DAD)
        **미주** — 뉴욕(JFK), LA(LAX), 샌프란시스코(SFO)
        **유럽** — 파리(CDG), 런던(LHR), 프랑크푸르트(FRA)
        **기타** — 시드니(SYD), 두바이(DXB), 괌(GUM), 하와이(HNL)
        """)

    with col2:
        st.markdown("### 핵심 코드")
        st.code('''
@tool
def search_flights(origin, destination,
                   departure_date, return_date=None):
    """Google Flights 실시간 항공편 검색"""
    origin_code = resolve_city(origin)    # "서울" → "ICN"
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

    # 라이브 데모
    st.markdown("### 🛫 라이브 데모")
    demo_col1, demo_col2, demo_col3 = st.columns(3)
    with demo_col1:
        demo_origin = st.selectbox("출발지", ["서울", "부산", "제주"], key="demo_origin")
    with demo_col2:
        demo_dest = st.text_input("도착지 (한글)", value="도쿄", key="demo_dest")
    with demo_col3:
        demo_date = st.date_input("출발일", key="demo_date")

    if st.button("🔍 항공편 검색", key="demo_search", use_container_width=True):
        with st.spinner("Google Flights에서 검색 중..."):
            from dotenv import load_dotenv
            load_dotenv()
            from agent.tools import search_flights
            result = search_flights.invoke({
                "origin": demo_origin,
                "destination": demo_dest,
                "departure_date": str(demo_date),
            })
            st.markdown(result)


# ==================== FEATURE: 최저가 비교 분석 ====================
elif page == "💰 최저가 비교 분석":
    hero_s = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px;"
    st.markdown(f"""
    <div style="{hero_s}">
        <h1 style="margin:0; font-size:38px; font-weight:800;">💰 최저가 비교 분석</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">
            Google Flights Price Insights를 활용한 가격 분석 & 최적 시점 안내
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 제공 정보")
        st.markdown("""
        - **최저가** — 해당 노선의 현재 최저 가격
        - **일반 가격대** — 이 노선의 통상적인 가격 범위
        - **가격 수준** — 현재 가격이 저렴/보통/비쌈인지 판단
        - **직항 vs 경유** — 직항과 경유편 가격 비교
        - **항공사별 비교** — 대한항공, LCC 등 가격 차이
        """)

        st.markdown("### Price Insights 활용")
        st.markdown("""
        Google Flights는 과거 가격 데이터를 기반으로
        현재 가격이 평소 대비 저렴한지 분석합니다.

        이 데이터를 AI Agent가 자연어로 해석하여
        사용자에게 **"지금 사는 게 좋다"** 또는
        **"좀 더 기다려보라"** 등의 조언을 제공합니다.
        """)

    with col2:
        st.markdown("### 핵심 코드")
        st.code('''
@tool
def get_flight_price_insights(origin, destination,
                              departure_date):
    """가격 분석 정보 제공"""
    results = serpapi_search(params)
    insights = results.get("price_insights", {})

    lowest = insights.get("lowest_price")
    typical = insights.get("typical_price_range")
    level = insights.get("price_level")
    # → "저렴" / "보통" / "비쌈"

    return format_price_analysis(insights)
        ''', language="python")

    st.divider()

    # 라이브 데모
    st.markdown("### 📊 라이브 데모 — 가격 분석")
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        p_origin = st.selectbox("출발지", ["서울", "부산"], key="p_origin")
    with p_col2:
        p_dest = st.text_input("도착지 (한글)", value="방콕", key="p_dest")
    with p_col3:
        p_date = st.date_input("출발일", key="p_date")

    if st.button("💰 가격 분석", key="price_search", use_container_width=True):
        with st.spinner("가격 데이터 분석 중..."):
            from dotenv import load_dotenv
            load_dotenv()
            from agent.tools import get_flight_price_insights
            result = get_flight_price_insights.invoke({
                "origin": p_origin,
                "destination": p_dest,
                "departure_date": str(p_date),
            })
            st.markdown(result)


# ==================== FEATURE: 항공사 정책 RAG ====================
elif page == "📚 항공사 정책 RAG":
    hero_s = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px;"
    st.markdown(f"""
    <div style="{hero_s}">
        <h1 style="margin:0; font-size:38px; font-weight:800;">📚 항공사 정책 RAG</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">
            ChromaDB Vector Store 기반 항공사 정책 검색 (Retrieval-Augmented Generation)
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### RAG 파이프라인")
        node_s = "background:#F8FAFF; border:1px solid #E2E8F0; border-radius:12px; padding:16px; margin-bottom:12px;"
        st.markdown(f"""
        <div style="{node_s}">
            <strong style="color:#0064D2;">1. Document Loading</strong><br>
            <span style="color:#4A5568;">airline_policies.json → 10개 정책 문서 로드</span>
        </div>
        <div style="{node_s}">
            <strong style="color:#0064D2;">2. Embedding & Indexing</strong><br>
            <span style="color:#4A5568;">ChromaDB에 벡터 임베딩 저장 (cosine similarity)</span>
        </div>
        <div style="{node_s}">
            <strong style="color:#0064D2;">3. Query → Retrieval</strong><br>
            <span style="color:#4A5568;">"수하물 무게" → 유사도 기반 상위 3개 문서 검색</span>
        </div>
        <div style="{node_s}">
            <strong style="color:#0064D2;">4. LLM Augmented Response</strong><br>
            <span style="color:#4A5568;">검색된 문서 + 사용자 질문 → LLM이 자연어 답변 생성</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 정책 데이터 (10건)")
        import json
        with open("data/airline_policies.json", "r", encoding="utf-8") as f:
            policies = json.load(f)
        for p in policies:
            with st.expander(f"📄 [{p['category']}] {p['title']}"):
                st.write(p["content"])

    st.divider()

    st.markdown("### 핵심 코드")
    st.code('''
# ChromaDB Vector Store 초기화
client = chromadb.Client()
collection = client.create_collection(
    name="airline_policies",
    metadata={"hnsw:space": "cosine"},
)

# 정책 문서 임베딩 & 저장
collection.add(
    documents=[p["content"] for p in policies],
    metadatas=[{"category": p["category"],
                "title": p["title"]} for p in policies],
    ids=[f"policy_{i}" for i in range(len(policies))],
)

@tool
def search_airline_policy(query: str) -> str:
    """항공사 정책을 벡터 검색합니다"""
    results = collection.query(
        query_texts=[query], n_results=3
    )
    return format_results(results)
    ''', language="python")

    st.divider()

    # 라이브 데모
    st.markdown("### 🔎 라이브 데모 — 정책 검색")
    rag_query = st.text_input("정책 질문 입력", value="수하물 무게 제한이 어떻게 돼?", key="rag_q")
    if st.button("📚 정책 검색", key="rag_search", use_container_width=True):
        with st.spinner("ChromaDB에서 검색 중..."):
            from dotenv import load_dotenv
            load_dotenv()
            from agent.vector_store import search_airline_policy
            result = search_airline_policy.invoke({"query": rag_query})
            st.markdown(result)


# ==================== FEATURE: Agent 아키텍처 ====================
elif page == "🧠 Agent 아키텍처":
    hero_s = "background:linear-gradient(135deg, #003087 0%, #0064D2 40%, #00A3E0 100%); border-radius:20px; padding:40px 50px; color:white; margin-bottom:30px;"
    st.markdown(f"""
    <div style="{hero_s}">
        <h1 style="margin:0; font-size:38px; font-weight:800;">🧠 LangGraph ReAct Agent</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:16px; font-weight:300;">
            Reasoning + Acting 패턴 기반 자율적 도구 선택 & 실행 에이전트
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ReAct 설명
    st.markdown("### ReAct Pattern이란?")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        ReAct (Reasoning + Acting)는 LLM이 **생각하고(Thought)**
        **행동하고(Action)** **관찰(Observation)** 하는 사이클을
        반복하며 복잡한 질문에 답하는 패턴입니다.

        **기존 방식과의 차이:**
        - ❌ 단순 프롬프트: "도쿄 항공편 알려줘" → 할루시네이션
        - ✅ ReAct Agent: 도구를 직접 호출하여 실제 데이터 반환

        **SkyBot의 ReAct 사이클:**
        1. **Thought** — "서울→도쿄, 4/25 항공편을 검색해야 한다"
        2. **Action** — `search_flights("서울", "도쿄", "2026-04-25")`
        3. **Observation** — API 결과: 6건, 최저 151,800원
        4. **Thought** — "결과를 정리해서 답변하자"
        5. **Response** — 자연어로 정리된 항공편 정보
        """)

    with col2:
        st.markdown("### Agent 생성 코드")
        st.code('''
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 5개 도구 등록
tools = [
    search_flights,        # 항공편 검색
    search_nonstop_flights,# 직항 검색
    search_round_trip,     # 왕복 검색
    get_flight_price_insights, # 가격 분석
    search_airline_policy, # 정책 RAG
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=SYSTEM_PROMPT,
)

# 실행
result = agent.invoke({
    "messages": [{"role": "user",
                  "content": user_query}]
})
        ''', language="python")

    st.divider()

    # Tool 상세
    st.markdown("### 🔧 등록된 Tools (5개)")
    tool_data = [
        ("search_flights", "항공편 검색", "출발지, 도착지, 날짜로 실시간 검색", "Google Flights"),
        ("search_nonstop_flights", "직항 검색", "직항편만 필터링하여 검색", "Google Flights"),
        ("search_round_trip", "왕복 검색", "왕복 항공편 검색 + 총 비용", "Google Flights"),
        ("get_flight_price_insights", "가격 분석", "최저가, 가격대, 현재 수준 분석", "Google Flights"),
        ("search_airline_policy", "정책 RAG", "수하물, 마일리지 등 정책 검색", "ChromaDB"),
    ]
    for name, title, desc, source in tool_data:
        card_s = "background:#F8FAFF; border:1px solid #E2E8F0; border-radius:12px; padding:16px; margin-bottom:10px;"
        st.markdown(f"""
        <div style="{card_s}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <code style="background:#003087; color:white; padding:2px 8px; border-radius:6px; font-size:13px;">{name}</code>
                    <strong style="margin-left:10px; color:#2D3748;">{title}</strong>
                </div>
                <span style="background:#EBF4FF; color:#003087; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600;">{source}</span>
            </div>
            <div style="color:#718096; font-size:13px; margin-top:6px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # LangGraph 상태 머신
    st.markdown("### 📐 LangGraph State Machine")
    sm_node = "text-align:center; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:20px 16px; min-width:120px;"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #003087, #0064D2, #00A3E0); border-radius:20px; padding:30px; color:white;">
        <div style="display:flex; justify-content:center; align-items:center; gap:20px; flex-wrap:wrap;">
            <div style="{sm_node}">
                <div style="font-size:28px;">📥</div>
                <div style="font-weight:700; margin-top:8px;">START</div>
                <div style="font-size:11px; opacity:0.8;">Messages Input</div>
            </div>
            <div style="font-size:24px; opacity:0.6;">→</div>
            <div style="{sm_node} border-color:rgba(230,168,23,0.5);">
                <div style="font-size:28px;">🧠</div>
                <div style="font-weight:700; margin-top:8px;">LLM Node</div>
                <div style="font-size:11px; opacity:0.8;">Reasoning</div>
            </div>
            <div style="font-size:24px; opacity:0.6;">→</div>
            <div style="{sm_node}">
                <div style="font-size:28px;">❓</div>
                <div style="font-weight:700; margin-top:8px;">Should Continue?</div>
                <div style="font-size:11px; opacity:0.8;">Tool Call 여부</div>
            </div>
            <div style="font-size:24px; opacity:0.6;">→</div>
            <div style="{sm_node} border-color:rgba(56,161,105,0.5);">
                <div style="font-size:28px;">🔧</div>
                <div style="font-weight:700; margin-top:8px;">Tool Node</div>
                <div style="font-size:11px; opacity:0.8;">API 호출</div>
            </div>
            <div style="font-size:24px; opacity:0.6;">↩️</div>
            <div style="{sm_node}">
                <div style="font-size:28px;">📤</div>
                <div style="font-weight:700; margin-top:8px;">END</div>
                <div style="font-size:11px; opacity:0.8;">Final Response</div>
            </div>
        </div>
        <div style="text-align:center; margin-top:20px; font-size:13px; opacity:0.7;">
            Tool Call이 있으면 Tool Node → LLM Node 반복 | 없으면 END로 종료
        </div>
    </div>
    """, unsafe_allow_html=True)
