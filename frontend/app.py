# LearnPath AI - Redesigned
import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from langchain_core.messages import HumanMessage

st.set_page_config(page_title="LearnPath AI", page_icon="🎓", layout="wide")

# Redesigned CSS - Premium but minimal
st.markdown("""
<style>
/* Font: Geist instead of generic Inter */
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0c0c0c;
    --surface: #141414;
    --surface-hover: #1a1a1a;
    --border: #222;
    --text: #e5e5e5;
    --text-dim: #737373;
    --accent: #22c55e;
    --accent-dim: rgba(34,197,94,0.12);
}

.stApp {
    background: var(--bg);
    font-family: 'Geist', system-ui, sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none; }

/* Typography */
h1, h2, h3 { color: var(--text); letter-spacing: -0.02em; }

/* Chat messages - clean, no borders */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 1rem 0 !important;
}

.stChatMessage[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: transparent;
}

.stChatMessage[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: transparent;
}

/* Input - refined */
.stChatInput {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

.stChatInput:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}

/* Buttons - proper states */
.stButton > button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Geist', sans-serif !important;
    font-weight: 500 !important;
    transition: all 150ms ease !important;
}

.stButton > button:hover {
    background: var(--surface-hover) !important;
    border-color: #333 !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}

.stButton > button:focus-visible {
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #444; }

/* Dividers */
hr { border-color: var(--border) !important; opacity: 1 !important; }

/* Status indicators */
.stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# Agent
@st.cache_resource
def get_agent():
    from backend.agent import create_agent
    return create_agent()

# State
if "agent" not in st.session_state:
    st.session_state.agent = get_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state.user = {"name": "", "age": 0, "goal": "", "timeframe": ""}
if "step" not in st.session_state:
    st.session_state.step = 0

# Header with proper typography
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2rem; font-weight: 600; letter-spacing: -0.03em; margin-bottom: 0.5rem;">LearnPath AI</h1>
    <p style="color: var(--text-dim); font-size: 0.9375rem;">Your personalized learning companion</p>
</div>
""", unsafe_allow_html=True)

# Step indicator - proper visual hierarchy
steps = ["Name", "Age", "Goal", "Timeframe", "Done"]
cols = st.columns([1] * 5)
for i, (col, step) in enumerate(zip(cols, steps)):
    with col:
        if i < st.session_state.step:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.75rem; background: var(--accent-dim); border-radius: 8px; border: 1px solid rgba(34,197,94,0.2);">
                <div style="font-size: 0.75rem; color: var(--accent); font-weight: 500;">✓ {step}</div>
            </div>
            """, unsafe_allow_html=True)
        elif i == st.session_state.step:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.75rem; background: var(--surface); border-radius: 8px; border: 1px solid var(--border);">
                <div style="font-size: 0.75rem; color: var(--text); font-weight: 500;">→ {step}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.75rem; color: var(--text-dim); font-weight: 400;">{step}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Update step
    if st.session_state.step == 0:
        st.session_state.user["name"] = prompt
        st.session_state.step = 1
    elif st.session_state.step == 1:
        try: st.session_state.user["age"] = int(prompt)
        except: st.session_state.user["age"] = 20
        st.session_state.step = 2
    elif st.session_state.step == 2:
        st.session_state.user["goal"] = prompt
        st.session_state.step = 3
    elif st.session_state.step == 3:
        st.session_state.user["timeframe"] = prompt
        st.session_state.step = 4
    
    # Agent state
    agent_state = {
        "messages": [HumanMessage(content=m["content"]) for m in st.session_state.messages if m["role"] == "user"],
        "user_name": st.session_state.user["name"],
        "user_age": st.session_state.user["age"],
        "goal": st.session_state.user["goal"],
        "timeframe": st.session_state.user["timeframe"],
        "session_id": f"session_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "phase": "learn",
        "resources": [],
        "checklist": []
    }
    
    with st.spinner("Thinking..."):
        result = st.session_state.agent.invoke(agent_state)
    
    st.session_state.messages.append({"role": "assistant", "content": result["messages"][-1].content})
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### Session")
    
    for k, v in st.session_state.user.items():
        if v:
            st.markdown(f"""
            <div style="padding: 0.75rem; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); margin-bottom: 0.5rem;">
                <div style="font-size: 0.6875rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">{k.title()}</div>
                <div style="font-size: 0.875rem; color: var(--text); font-weight: 500;">{v}</div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("New Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user = {"name": "", "age": 0, "goal": "", "timeframe": ""}
        st.session_state.step = 0
        st.rerun()
