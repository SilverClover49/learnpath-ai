# LearnPath AI - Premium UI
import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from backend.agent import create_agent
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS - Ethereal Glass + Double Bezel Architecture
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #050505;
    --bg-secondary: #0a0a0a;
    --bg-card: rgba(255,255,255,0.03);
    --bg-card-hover: rgba(255,255,255,0.06);
    --border-subtle: rgba(255,255,255,0.06);
    --border-accent: rgba(255,255,255,0.12);
    --text-primary: #fafafa;
    --text-secondary: rgba(255,255,255,0.6);
    --text-muted: rgba(255,255,255,0.4);
    --accent-green: #00d4aa;
    --accent-purple: #a855f7;
    --accent-blue: #3b82f6;
    --glow-green: rgba(0,212,170,0.15);
    --glow-purple: rgba(168,85,247,0.15);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0,212,170,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 60%, rgba(168,85,247,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

.stApp > * {
    position: relative;
    z-index: 1;
}

/* Hide Streamlit defaults */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Premium Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

/* Hero Section */
.hero-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 4rem 2rem;
    text-align: center;
    position: relative;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--accent-green);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
    animation: fadeInDown 0.8s cubic-bezier(0.32,0.72,0,1) both;
}

.hero-title {
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
    margin-bottom: 1.5rem;
    animation: fadeInUp 0.8s cubic-bezier(0.32,0.72,0,1) 0.1s both;
}

.hero-title .gradient-text {
    background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-purple) 50%, var(--accent-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 600px;
    line-height: 1.6;
    animation: fadeInUp 0.8s cubic-bezier(0.32,0.72,0,1) 0.2s both;
}

/* Double Bezel Card Architecture */
.dual-bezel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 24px;
    padding: 2px;
    transition: all 0.4s cubic-bezier(0.32,0.72,0,1);
}

.dual-bezel:hover {
    border-color: var(--border-accent);
    background: var(--bg-card-hover);
}

.dual-bezel-inner {
    background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
    border-radius: 22px;
    padding: 2rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}

/* Step Indicator - Premium */
.steps-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 3rem 0;
    animation: fadeInUp 0.8s cubic-bezier(0.32,0.72,0,1) 0.3s both;
}

.step-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 100px;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-muted);
    transition: all 0.4s cubic-bezier(0.32,0.72,0,1);
}

.step-pill.active {
    background: rgba(0,212,170,0.15);
    border-color: rgba(0,212,170,0.3);
    color: var(--accent-green);
    box-shadow: 0 0 20px rgba(0,212,170,0.2);
}

.step-pill.completed {
    background: rgba(0,212,170,0.1);
    border-color: rgba(0,212,170,0.2);
    color: var(--accent-green);
}

.step-number {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 600;
}

.step-pill.active .step-number {
    background: var(--accent-green);
    color: var(--bg-primary);
}

/* Chat Interface */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

.message {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    animation: fadeInUp 0.5s cubic-bezier(0.32,0.72,0,1) both;
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
}

.message-avatar.user {
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
}

.message-avatar.assistant {
    background: linear-gradient(135deg, var(--accent-green), #00b894);
}

.message-content {
    flex: 1;
    padding: 1.25rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: var(--text-primary);
}

.message-content.user {
    background: rgba(59,130,246,0.08);
    border-color: rgba(59,130,246,0.15);
}

/* Sidebar Panel */
.sidebar-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.sidebar-panel h3 {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}

.profile-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border-subtle);
}

.profile-item:last-child {
    border-bottom: none;
}

.profile-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.profile-value {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
}

/* Checklist */
.checklist-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    margin-bottom: 8px;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1);
}

.checklist-item:hover {
    background: rgba(255,255,255,0.04);
    border-color: var(--border-accent);
}

.checklist-checkbox {
    width: 20px;
    height: 20px;
    border: 2px solid var(--border-accent);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: transparent;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1);
}

.checklist-item.completed .checklist-checkbox {
    background: var(--accent-green);
    border-color: var(--accent-green);
    color: var(--bg-primary);
}

/* File Cards */
.file-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    margin-bottom: 8px;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1);
}

.file-card:hover {
    background: rgba(255,255,255,0.04);
    border-color: var(--border-accent);
    transform: translateX(4px);
}

.file-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(168,85,247,0.1);
    border-radius: 10px;
    font-size: 1rem;
}

.file-name {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
}

/* Button Styles */
.premium-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 14px 24px;
    background: linear-gradient(135deg, var(--accent-green), #00b894);
    border: none;
    border-radius: 12px;
    color: var(--bg-primary);
    font-size: 0.9375rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1);
}

.premium-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,212,170,0.3);
}

.premium-button:active {
    transform: translateY(0) scale(0.98);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(0,212,170,0.2);
    }
    50% {
        box-shadow: 0 0 40px rgba(0,212,170,0.4);
    }
}

.pulse-glow {
    animation: pulse-glow 3s ease-in-out infinite;
}

/* Streamlit Overrides */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.stChatMessage[data-testid="stChatMessage"] {
    background: transparent !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 14px 18px !important;
    font-size: 0.9375rem !important;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-green), #00b894) !important;
    border: none !important;
    border-radius: 12px !important;
    color: var(--bg-primary) !important;
    font-weight: 600 !important;
    padding: 14px 24px !important;
    transition: all 0.3s cubic-bezier(0.32,0.72,0,1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,212,170,0.3) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255,255,255,0.2);
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

# Hero Section (when not chatting)
if not st.session_state.onboarding_complete and not st.session_state.chat_history:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span>✦</span>
            <span>AI-Powered Learning</span>
        </div>
        <h1 class="hero-title">
            Your Personal<br>
            <span class="gradient-text">Learning Companion</span>
        </h1>
        <p class="hero-subtitle">
            Tell us what you want to learn, and we'll create a personalized 
            curriculum, track your progress, and guide you every step of the way.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Step Indicator
if st.session_state.chat_history:
    steps = ["Name", "Age", "Goal", "Timeframe", "Learn"]
    current_step = 0
    if st.session_state.state.get("user_name"):
        current_step = 1
    if st.session_state.state.get("user_age"):
        current_step = 2
    if st.session_state.state.get("goal"):
        current_step = 3
    if st.session_state.state.get("timeframe"):
        current_step = 4
    
    steps_html = '<div class="steps-container">'
    for i, step in enumerate(steps):
        if i < current_step:
            steps_html += f'<div class="step-pill completed"><div class="step-number">✓</div>{step}</div>'
        elif i == current_step:
            steps_html += f'<div class="step-pill active"><div class="step-number">{i+1}</div>{step}</div>'
        else:
            steps_html += f'<div class="step-pill"><div class="step-number">{i+1}</div>{step}</div>'
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

# Main Content
col1, col2 = st.columns([2, 1], gap="2rem")

with col1:
    # Chat Messages
    for msg in st.session_state.chat_history:
        role = msg["role"]
        avatar = "🎓" if role == "assistant" else "👤"
        avatar_class = "assistant" if role == "assistant" else "user"
        content_class = "user" if role == "user" else ""
        
        st.markdown(f"""
        <div class="message">
            <div class="message-avatar {avatar_class}">{avatar}</div>
            <div class="message-content {content_class}">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat Input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
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
        
        if (st.session_state.state.get("user_name") and 
            st.session_state.state.get("goal") and 
            st.session_state.state.get("timeframe")):
            st.session_state.onboarding_complete = True
        
        st.rerun()

with col2:
    # Profile Panel
    st.markdown("""
    <div class="sidebar-panel">
        <h3>Your Profile</h3>
    </div>
    """, unsafe_allow_html=True)
    
    profile_items = [
        ("Name", st.session_state.state.get("user_name", "—")),
        ("Age", st.session_state.state.get("user_age", "—")),
        ("Goal", st.session_state.state.get("goal", "—")),
        ("Timeframe", st.session_state.state.get("timeframe", "—")),
        ("Phase", st.session_state.state.get("phase", "start")),
    ]
    
    profile_html = '<div class="sidebar-panel">'
    for label, value in profile_items:
        profile_html += f'''
        <div class="profile-item">
            <span class="profile-label">{label}</span>
            <span class="profile-value">{value}</span>
        </div>'''
    profile_html += '</div>'
    st.markdown(profile_html, unsafe_allow_html=True)
    
    # Checklist Panel
    checklist = st.session_state.state.get("checklist", [])
    if checklist:
        checklist_html = '<div class="sidebar-panel"><h3>Checklist</h3>'
        for item in checklist:
            status_class = "completed" if item.get("completed") else ""
            check = "✓" if item.get("completed") else ""
            checklist_html += f'''
            <div class="checklist-item {status_class}">
                <div class="checklist-checkbox">{check}</div>
                <span>{item['task']}</span>
            </div>'''
        checklist_html += '</div>'
        st.markdown(checklist_html, unsafe_allow_html=True)
    
    # Session Files Panel
    session_dir = os.path.join(parent_dir, "sessions", st.session_state.state.get("session_id", ""))
    if os.path.exists(session_dir):
        files = [f for f in os.listdir(session_dir) if f.endswith(('.md', '.html', '.json'))]
        if files:
            files_html = '<div class="sidebar-panel"><h3>Session Files</h3>'
            for f in files:
                icon = "📄" if f.endswith('.md') else "🌐" if f.endswith('.html') else "📊"
                files_html += f'''
                <div class="file-card">
                    <div class="file-icon">{icon}</div>
                    <span class="file-name">{f}</span>
                </div>'''
            files_html += '</div>'
            st.markdown(files_html, unsafe_allow_html=True)
    
    # Actions Panel
    st.markdown("""
    <div class="sidebar-panel">
        <h3>Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✨ Start New Session", use_container_width=True):
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
