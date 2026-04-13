import streamlit as st

api_key = st.secrets["GROQ_API_KEY"]

import streamlit as st
import json
from agents.planner import planner_agent
from agents.architect import architect_agent
from agents.coder import coder_agent

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Project Builder", layout="wide")

# =========================
# STYLE (SaaS Level)
# =========================

st.markdown("""
<style>

/* BACKGROUND (AI + GRADIENT BLEND) */
.stApp {
    background:
        linear-gradient(rgba(15,23,42,0.45), rgba(15,23,42,0.45)),
        url("https://orca.security/wp-content/uploads/2024/10/top-10-ai-model-blog.png?resize=1044,620");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* GLASS EFFECT FOR CONTENT */
.card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(6px);
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* Improve text readability */
.title {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
}


/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
    color: white;
}

/* Title */
.title {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
}
/* Cards */
.card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(6px);
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
            
/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #3b82f6);
    color: white;
    border-radius: 10px;
    height: 42px;
    width: 180px;
    border: none;
}

/* Input */
textarea {
    border-radius: 12px !important;
}

/* Step badges */
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background: #e0e7ff;
    color: #3730a3;
    margin-right: 8px;
    font-size: 13px;
}

h3 {
    color: #e2e8f0 !important;
    text-shadow: 0px 1px 6px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "plan" not in st.session_state:
    st.session_state.plan = None
    st.session_state.arch = None
    st.session_state.done = False

if "step" not in st.session_state:
    st.session_state.step = "idle"

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("🚀 AI Builder")
    st.write("Build AI projects automatically")

    st.divider()

    st.markdown("### Workflow")
    def highlight(step, current):
        return "🟢 " + step if current == step.lower() else "⚪ " + step

    current = st.session_state.get("step", "idle")

    st.markdown(highlight("Planner", current))
    st.markdown(highlight("Architect", current))
    st.markdown(highlight("Coder", current))

    st.divider()
    st.caption("v1.0 • Multi-Agent System")

# =========================
# HEADER
# =========================
st.markdown('<div class="title">AI Project Builder</div>', unsafe_allow_html=True)


# =========================
# INPUT SECTION
# =========================
st.markdown("### 🧠 Describe Your Project")

user_input = st.text_area(
    "",
    height=100,
    placeholder="Example: Build a RAG system for answering questions from PDFs..."
)

run = st.button("Generate Project")


# =========================
# RUN PIPELINE
# =========================
if run and user_input:

    # STEP 1
    st.session_state.plan = planner_agent(user_input, api_key)
    st.rerun()

# HANDLE EACH STEP SEPARATELY

if st.session_state.step == "planner":
    with st.spinner("🧠 Planning..."):
        st.session_state.plan = planner_agent(user_input)

    st.session_state.step = "architect"
    st.rerun()


elif st.session_state.step == "architect":
    with st.spinner("🏗 Designing Architecture..."):
        st.session_state.arch = architect_agent(st.session_state.plan)

    st.session_state.step = "coder"
    st.rerun()


elif st.session_state.step == "coder":
    with st.spinner("⚡ Generating Code..."):
        coder_agent(st.session_state.plan, st.session_state.arch)

    st.session_state.step = "done"
    st.session_state.done = True
    st.rerun()

# =========================
# OUTPUT SECTION
# =========================
if st.session_state.done:

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Planner", "🏗 Architecture", "📁 Files"])

    # ---- Planner ----
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.json(st.session_state.plan)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Architect ----
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.json(st.session_state.arch)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Files ----
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        files = st.session_state.arch.get("files", [])

        for f in files:
            with st.expander(f"📄 {f}"):
                try:
                    with open(f"{st.session_state.plan['project_name'].lower().replace(' ','_')}/{f}", "r", encoding="utf-8") as file:
                        st.code(file.read(), language="python")
                except:
                    st.write("File content not available")

        st.markdown('</div>', unsafe_allow_html=True)
