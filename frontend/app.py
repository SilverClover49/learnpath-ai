# LearnPath AI - Unified Experience
import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from langchain_core.messages import HumanMessage

st.set_page_config(page_title="LearnPath AI", page_icon="🎓", layout="wide")

# Single CSS block - no imports, no animations, just clean
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { background: #0a0a0a; font-family: 'Inter', sans-serif; }
#MainMenu, footer, header, .stDeployButton { display: none; }

/* Clean chat styling */
.stChatMessage { background: transparent !important; border: none !important; padding: 0.5rem 0 !important; }
.stChatMessage[data-testid="stChatMessage"] { background: transparent !important; }

/* Input styling */
.stTextInput > div > div > input {
    background: #141414 !important;
    border: 1px solid #262626 !important;
    border-radius: 10px !important;
    color: #fff !important;
}
.stTextInput > div > div > input:focus { border-color: #00d4aa !important; }

/* Button */
.stButton > button {
    background: #00d4aa !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton > button:hover { background: #00b894 !important; }
</style>
""", unsafe_allow_html=True)

# Agent with proper caching
@st.cache_resource
def get_agent():
    from backend.agent import create_agent
    return create_agent()

# Init state
if "agent" not in st.session_state:
    st.session_state.agent = get_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state.user = {"name": "", "age": 0, "goal": "", "timeframe": "", "phase": "start"}
if "step" not in st.session_state:
    st.session_state.step = 0

# Simple header
st.markdown("# LearnPath AI")

# Step indicator
steps = ["Name", "Age", "Goal", "Timeframe", "Done"]
step_cols = st.columns(5)
for i, (col, step) in enumerate(zip(step_cols, steps)):
    with col:
        if i < st.session_state.step:
            st.success(f"✓ {step}")
        elif i == st.session_state.step:
            st.info(f"→ {step}")
        else:
            st.caption(step)

st.divider()

# Chat area
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Type here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Update user state based on step
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
    
    # Build state for agent
    agent_state = {
        "messages": [HumanMessage(content=p) for p in [m["content"] for m in st.session_state.messages if m["role"] == "user"]],
        "user_name": st.session_state.user["name"],
        "user_age": st.session_state.user["age"],
        "goal": st.session_state.user["goal"],
        "timeframe": st.session_state.user["timeframe"],
        "session_id": f"session_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "phase": "learn",
        "resources": [],
        "checklist": []
    }
    
    # Get response (this is the blocking part)
    with st.spinner("Thinking..."):
        result = st.session_state.agent.invoke(agent_state)
    
    response = result["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.user["phase"] = result.get("phase", "learn")
    
    st.rerun()

# Sidebar
with st.sidebar:
    st.header("Session")
    for k, v in st.session_state.user.items():
        st.write(f"**{k.title()}:** {v}")
    
    if st.button("New Session"):
        st.session_state.messages = []
        st.session_state.user = {"name": "", "age": 0, "goal": "", "timeframe": "", "phase": "start"}
        st.session_state.step = 0
        st.rerun()
