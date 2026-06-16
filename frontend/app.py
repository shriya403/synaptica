import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Synaptica Pro",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: #F7F5F0; }
    .hero {
        padding: 4rem 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #FFFFFF, #EEF2FF);
        border: 1px solid #E5E7EB;
    }
    .title { font-size: 56px; font-weight: 800; color: #1F2937; }
    .subtitle { font-size: 20px; color: #6B7280; max-width: 760px; }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"


def landing_page():
    st.markdown(
        """
        <div class="hero">
            <div class="title">🧠 Synaptica Pro</div>
            <p class="subtitle">
                Premium AI workflow platform for research, document intelligence,
                and multi-agent execution.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="card"><h3>🤖 Multi-Agent AI</h3><p>Specialized agents collaborate for research, planning, and execution.</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="card"><h3>📚 Multi-Document RAG</h3><p>Upload PDFs, create separate knowledge bases, and ask grounded questions.</p></div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="card"><h3>📄 Persistent Reports</h3><p>Save document Q&A history and generate structured outputs.</p></div>',
            unsafe_allow_html=True,
        )

    if st.button("Get Started", type="primary"):
        st.session_state.page = "Login"
        st.rerun()


def login_page():
    st.title("Welcome back")
    st.caption("Login to access your Synaptica workspace.")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")

    if submit:
        if email and password:
            st.session_state.logged_in = True
            st.session_state.page = "Dashboard"
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Please enter email and password.")


def dashboard_page():
    with st.sidebar:
        st.title("Synaptica Pro")

        page = st.radio(
            "Workspace",
            [
                "🏠 Overview",
                "📚 Knowledge Base",
                "🤖 Agent Studio",
                "⚡ Workflows",
                "📊 Analytics",
                "📄 Reports",
                "⚙️ Settings",
            ],
        )

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Home"
            st.rerun()

    if page == "🏠 Overview":
        st.title("Dashboard Overview")

        try:
            health = requests.get(f"{API_URL}/health", timeout=5).json()
            st.success("Backend Connected")
            st.metric("Agents Active", health.get("agents", 5))
            st.metric("RAG Enabled", str(health.get("rag", False)))
        except Exception:
            st.error("Backend not connected. Start FastAPI first.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Workflows", "12")
        col2.metric("Reports", "8")
        col3.metric("Quality Score", "8.5/10")
        col4.metric("Knowledge Bases", "Multi-PDF")

    elif page == "📚 Knowledge Base":
        st.title("📚 Knowledge Base")
        st.caption("Upload PDFs, create separate knowledge bases, and chat with selected documents.")

        uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

        if uploaded_file is not None:
            if st.button("Upload & Index PDF", type="primary"):
                with st.spinner("Uploading and indexing document..."):
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/upload-pdf",
                        files=files,
                        timeout=300,
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.success(
                            f"Uploaded {data['filename']} | "
                            f"Chunks: {data['chunks_stored']} | "
                            f"Collection: {data['collection_name']}"
                        )
                        st.json(data)
                    else:
                        st.error(response.text)

        st.markdown("---")
        st.subheader("Available Knowledge Bases")

        collections = []

        try:
            response = requests.get(f"{API_URL}/knowledge-bases", timeout=10)

            if response.status_code == 200:
                collections = response.json().get("collections", [])
            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))

        if collections:
            selected_collection = st.selectbox(
                "Select a knowledge base",
                collections,
            )

            st.markdown("---")
            st.subheader("Ask Selected Document")

            question = st.text_input(
                "Question",
                placeholder="Example: What is this document about?",
            )

            if st.button("Ask Synaptica RAG", type="primary"):
                if not question.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Searching selected document and generating answer..."):
                        response = requests.post(
                            f"{API_URL}/ask-docs",
                            json={
                                "question": question,
                                "collection_name": selected_collection,
                            },
                            timeout=300,
                        )

                        if response.status_code == 200:
                            data = response.json()["result"]

                            st.success("Answer generated")

                            st.markdown("### Answer")
                            st.write(data["answer"])

                            st.markdown("### Sources")
                            st.json(data["sources"])

                        else:
                            st.error(response.text)
        else:
            st.info("No knowledge bases found. Upload a PDF first.")

        st.markdown("---")
        st.subheader("Persistent Chat History")

        try:
            history_response = requests.get(f"{API_URL}/rag-history", timeout=10)
            history = history_response.json().get("history", [])

            if history:
                if st.button("Clear Persistent History"):
                    delete_response = requests.delete(
                        f"{API_URL}/rag-history",
                        timeout=10,
                    )

                    if delete_response.status_code == 200:
                        st.success("History cleared")
                        st.rerun()

                for chat in reversed(history):
                    with st.expander(f"{chat['collection']} | {chat['question']}"):
                        st.caption(chat["timestamp"])
                        st.write(chat["answer"])
                        st.json(chat["sources"])
            else:
                st.info("No persistent document chat history yet.")

        except Exception as e:
            st.error(str(e))

    elif page == "🤖 Agent Studio":
        st.title("🤖 Agent Studio")

        agents = [
            ("Planner Agent", "Plans and decomposes user tasks"),
            ("Research Agent", "Finds and analyzes information"),
            ("RAG Agent", "Answers using selected document knowledge bases"),
            ("Validator Agent", "Checks factual grounding"),
            ("Critic Agent", "Reviews and improves outputs"),
        ]

        for name, role in agents:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{name}</h3>
                    <p>{role}</p>
                    <p><b>Status:</b> Active</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

    elif page == "⚡ Workflows":
        st.title("⚡ Run Agent Workflow")

        task = st.text_area(
            "Enter task",
            value="Launch Synaptica AI Platform",
            height=120,
        )

        if st.button("Execute Workflow", type="primary"):
            with st.spinner("Running multi-agent workflow..."):
                response = requests.post(
                    f"{API_URL}/execute",
                    json={"task": task, "context": {}},
                    timeout=300,
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Completed in {data['execution_time']} seconds")
                    result = data["result"]

                    st.subheader("Final Report")
                    st.markdown(result["synthesized"]["final_plan"])

                    st.subheader("Agent Results")
                    st.json(result["results"])
                else:
                    st.error(response.text)

    elif page == "📊 Analytics":
        st.title("📊 Analytics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Latency", "4.2s")
        col2.metric("Grounding Score", "8.6/10")
        col3.metric("Success Rate", "92%")

        st.info("Real analytics will be connected after task history storage is added.")

    elif page == "📄 Reports":
        st.title("📄 Reports")
        st.info("Generated workflow and RAG reports will appear here.")

    elif page == "⚙️ Settings":
        st.title("⚙️ Settings")
        st.write("Profile, theme, API keys, and workspace settings will appear here.")


if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        login_page()
    else:
        landing_page()
else:
    dashboard_page()