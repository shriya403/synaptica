import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Synaptica",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub {
        font-size: 18px;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🧠 Synaptica</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">Self-Evolving Multi-Agent Intelligence Platform</div>',
    unsafe_allow_html=True,
)

st.sidebar.header("📊 System Status")

try:
    health = requests.get(f"{API_URL}/health", timeout=5).json()
    st.sidebar.success("Backend Connected")
    st.sidebar.metric("Agents Active", health.get("agents", 5))
except Exception:
    st.sidebar.error("Backend Not Connected")
    st.sidebar.info("Run: python -m uvicorn api.main:app --reload")

st.sidebar.header("🤖 Agents")
try:
    agents = requests.get(f"{API_URL}/agents", timeout=5).json()["agents"]
    for agent in agents:
        st.sidebar.write(f"✅ {agent['name']}")
except Exception:
    st.sidebar.write("Agents unavailable")

st.header("🎯 Enter Your Task")

examples = [
    "Launch Synaptica AI Platform",
    "Plan a product launch for an AI study planner",
    "Create a go-to-market strategy for a fitness app",
]

selected = st.selectbox("Choose example task", examples)

task_input = st.text_area(
    "Task",
    value=selected,
    height=120,
)

if st.button("🚀 Execute Multi-Agent Workflow", type="primary"):
    if not task_input.strip():
        st.warning("Please enter a task.")
    else:
        with st.spinner("Running 5-agent collaboration..."):
            try:
                response = requests.post(
                    f"{API_URL}/execute",
                    json={
                        "task": task_input,
                        "context": {},
                    },
                    timeout=300,
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success(f"Task completed in {data['execution_time']} seconds")

                    result = data["result"]

                    st.subheader("🧩 Subtasks")
                    st.json(result["subtasks"])

                    st.subheader("🤖 Agent Results")

                    results = result["results"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 🔍 Market Researcher")
                        st.json(results["market_researcher"]["result"])

                        st.markdown("### 📅 Timeline Planner")
                        st.json(results["timeline_planner"]["result"])

                        st.markdown("### 💰 Budget Optimizer")
                        st.json(results["budget_optimizer"]["result"])

                    with col2:
                        st.markdown("### ✍️ Content Creator")
                        st.json(results["content_creator"]["result"])

                        st.markdown("### ⚠️ Risk Analyst")
                        st.json(results["risk_analyst"]["result"])

                    st.subheader("🎯 Final Synthesized Plan")
                    st.markdown(result["synthesized"]["final_plan"])

                    st.subheader("📈 Orchestrator Critique")
                    st.json(result["critique"])

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                st.error("Could not connect to backend.")
                st.code(str(e))

st.markdown("---")
st.caption("Built by Shriya Shinde | Synaptica AI Platform")