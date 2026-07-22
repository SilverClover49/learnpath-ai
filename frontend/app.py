# LearnPath AI - Streamlit Frontend (Sprint 4)
import streamlit as st
import sys
import os

# Add parent to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from backend.agent import create_agent
from langchain_core.messages import HumanMessage

# Page config
st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes celebrate {
    0% { transform: scale(1) rotate(0deg); }
    25% { transform: scale(1.1) rotate(-5deg); }
    50% { transform: scale(1.2) rotate(5deg); }
    75% { transform: scale(1.1) rotate(-5deg); }
    100% { transform: scale(1) rotate(0deg); }
}

.main-header {
    font-size: 4rem;
    color: #4CAF50;
    text-align: center;
    padding: 2rem;
    animation: fadeIn 1s ease-out, pulse 2s infinite;
}

.sub-header {
    font-size: 1.5rem;
    color: #666;
    text-align: center;
    animation: fadeIn 1.5s ease-out;
}

.welcome-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin: 2rem 0;
    animation: fadeIn 2s ease-out;
}

.step-indicator {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
}

.step {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    transition: all 0.3s;
}

.step.active {
    background: #4CAF50;
    color: white;
    transform: scale(1.1);
}

.step.completed {
    background: #2196F3;
    color: white;
}

.code-block {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 1rem;
    border-radius: 10px;
    font-family: 'Consolas', monospace;
    overflow-x: auto;
}

.celebration {
    animation: celebrate 1s ease-in-out;
    text-align: center;
    font-size: 4rem;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "user_name": "",
        "user_age": 0,
        "goal": "",
        "timeframe": "",
        "session_id": f"session_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "phase": "start",
        "resources": [],
        "checklist": []
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "onboarding_complete" not in st.session_state:
    st.session_state.onboarding_complete = False

# Welcome screen
if not st.session_state.onboarding_complete:
    st.markdown('<div class="welcome-box"><h1>Welcome to LearnPath AI</h1><p>Your Personalized Learning Companion</p></div>', unsafe_allow_html=True)
    
    steps = ["Name", "Age", "Goal", "Timeframe", "Resources", "Plan", "Code", "Whiteboard"]
    current_step = 0
    if st.session_state.state.get("user_name"):
        current_step = 1
    if st.session_state.state.get("user_age"):
        current_step = 2
    if st.session_state.state.get("goal"):
        current_step = 3
    if st.session_state.state.get("timeframe"):
        current_step = 4
    
    st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
    for i, step in enumerate(steps):
        if i < current_step:
            st.markdown(f'<div class="step completed">v</div>', unsafe_allow_html=True)
        elif i == current_step:
            st.markdown(f'<div class="step active">{i+1}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step">{i+1}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">LearnPath AI</h1>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.divider()
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Tell me about yourself..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        if not st.session_state.state.get("user_name"):
            st.session_state.state["user_name"] = prompt
        elif not st.session_state.state.get("user_age"):
            try:
                st.session_state.state["user_age"] = int(prompt)
            except:
                st.session_state.state["user_age"] = 20
        elif not st.session_state.state.get("goal"):
            st.session_state.state["goal"] = prompt
        elif not st.session_state.state.get("timeframe"):
            st.session_state.state["timeframe"] = prompt
        
        st.session_state.state["messages"].append(HumanMessage(content=prompt))
        
        with st.spinner("Thinking..."):
            st.session_state.state = st.session_state.agent.invoke(st.session_state.state)
        
        response = st.session_state.state["messages"][-1].content
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.write(response)
        
        if (st.session_state.state.get("user_name") and 
            st.session_state.state.get("goal") and 
            st.session_state.state.get("timeframe")):
            st.session_state.onboarding_complete = True

with col2:
    st.header("Session Info")
    
    st.subheader("Your Profile")
    st.write("**Name:**", st.session_state.state.get("user_name", "Not set"))
    st.write("**Age:**", st.session_state.state.get("user_age", "Not set"))
    st.write("**Goal:**", st.session_state.state.get("goal", "Not set"))
    st.write("**Timeframe:**", st.session_state.state.get("timeframe", "Not set"))
    st.write("**Phase:**", st.session_state.state.get("phase", "start"))
    
    st.divider()
    
    st.subheader("Checklist")
    checklist = st.session_state.state.get("checklist", [])
    if checklist:
        for item in checklist:
            st.write(f"[{'x' if item.get('completed') else ' '}] {item['task']}")
    else:
        st.write("No checklist yet")
    
    st.divider()
    
    st.subheader("Session Files")
    session_dir = os.path.join(parent_dir, "sessions", st.session_state.state.get("session_id", ""))
    if os.path.exists(session_dir):
        files = os.listdir(session_dir)
        for f in files:
            if f.endswith(('.md', '.html', '.json')):
                st.write(f"📄 {f}")
    else:
        st.write("No session files yet")
    
    st.divider()
    
    st.subheader("Actions")
    if st.button("Start New Session"):
        st.session_state.state = {
            "messages": [],
            "user_name": "",
            "user_age": 0,
            "goal": "",
            "timeframe": "",
            "session_id": f"session_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "phase": "start",
            "resources": [],
            "checklist": []
        }
        st.session_state.chat_history = []
        st.session_state.onboarding_complete = False
        st.rerun()
