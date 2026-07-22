# LearnPath AI - Optimized Premium UI
import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load agent lazily
@st.cache_resource
def load_agent():
    from backend.agent import create_agent
    return create_agent()

# Premium CSS - Optimized for Performance
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-primary: #050505;
    --bg-card: rgba(255,255,255,0.03);
    --border-subtle: rgba(255,255,255,0.06);
    --border-accent: rgba(255,255,255,0.12);
    --text-primary: #fafafa;
    --text-secondary: rgba(255,255,255,0.6);
    --text-muted: rgba(255,255,255,0.4);
    --accent-green: #00d4aa;
    --accent-purple: #a855f7;
    --accent-blue: #3b82f6;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: 
        radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0,212,170,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 60%, rgba(168,85,247,0.06) 0%, transparent 60%);
    pointer-events: none;
}

#MainMenu, footer, header, .stDeployButton {visibility: hidden;}

/* Hero */
.hero {
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 4rem 2rem;
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
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 2rem;
    animation: fadeDown 0.6s ease-out both;
}

.hero-title {
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    animation: fadeUp 0.6s ease-out 0.1s both;
}

.gradient-text {
    background: linear-gradient(135deg, var(--accent-green), var(--accent-purple), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 1.125rem;
    color: var(--text-secondary);
    max-width: 500px;
    line-height: 1.6;
    animation: fadeUp 0.6s ease-out 0.2s both;
}

/* Steps */
.steps {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 2rem 0;
    flex-wrap: wrap;
    animation: fadeUp 0.6s ease-out 0.3s both;
}

.step {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 100px;
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--text-muted);
    transition: all 0.3s ease;
}

.step.active {
    background: rgba(0,212,170,0.15);
    border-color: rgba(0,212,170,0.3);
    color: var(--accent-green);
}

.step.done {
    background: rgba(0,212,170,0.1);
    border-color: rgba(0,212,170,0.2);
    color: var(--accent-green);
}

.step-num {
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    font-size: 0.6875rem;
    font-weight: 600;
}

.step.active .step-num {
    background: var(--accent-green);
    color: var(--bg-primary);
}

/* Messages */
.msg {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: fadeUp 0.4s ease-out both;
}

.msg-av {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.125rem;
    flex-shrink: 0;
}

.msg-av.user { background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); }
.msg-av.ai { background: linear-gradient(135deg, var(--accent-green), #00b894); }

.msg-body {
    flex: 1;
    padding: 1rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    font-size: 0.9375rem;
    line-height: 1.6;
}

.msg-body.user {
    background: rgba(59,130,246,0.08);
    border-color: rgba(59,130,246,0.15);
}

/* Panel */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.panel-title {
    font-size: 0.6875rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}

.prof-row {
    display: flex;
    justify-content: space-between;
    padding: 0.625rem 0;
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.875rem;
}

.prof-row:last-child { border: none; }
.prof-label { color: var(--text-secondary); }
.prof-val { font-weight: 500; }

/* Checklist */
.chk {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}

.chk:hover { background: rgba(255,255,255,0.04); }

.chk-box {
    width: 18px;
    height: 18px;
    border: 2px solid var(--border-accent);
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.625rem;
}

.chk.done .chk-box {
    background: var(--accent-green);
    border-color: var(--accent-green);
    color: var(--bg-primary);
}

/* File */
.file {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}

.file:hover { transform: translateX(4px); border-color: var(--border-accent); }

.file-ico {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(168,85,247,0.1);
    border-radius: 8px;
}

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Streamlit Overrides */
.stChatMessage { background: transparent !important; border: none !important; }

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 14px 18px !important;
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
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0,212,170,0.25);
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Session state
if "agent" not in st.session_state:
    st.session_state.agent = load_agent()
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

# Hero (when empty)
if not st.session_state.onboarding_complete and not st.session_state.chat_history:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ AI-Powered Learning</div>
        <h1 class="hero-title">Your Personal<br><span class="gradient-text">Learning Companion</span></h1>
        <p class="hero-sub">Tell us what you want to learn, and we'll create a personalized curriculum and guide you every step.</p>
    </div>
    """, unsafe_allow_html=True)

# Steps
if st.session_state.chat_history:
    steps = ["Name", "Age", "Goal", "Timeframe", "Learn"]
    cur = 0
    if st.session_state.state.get("user_name"): cur = 1
    if st.session_state.state.get("user_age"): cur = 2
    if st.session_state.state.get("goal"): cur = 3
    if st.session_state.state.get("timeframe"): cur = 4
    
    h = '<div class="steps">'
    for i, s in enumerate(steps):
        cls = "done" if i < cur else "active" if i == cur else ""
        num = "✓" if i < cur else str(i+1)
        h += f'<div class="step {cls}"><div class="step-num">{num}</div>{s}</div>'
    h += '</div>'
    st.markdown(h, unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    for msg in st.session_state.chat_history:
        r = msg["role"]
        av = "🎓" if r == "assistant" else "👤"
        cls = "ai" if r == "assistant" else "user"
        bc = "user" if r == "user" else ""
        st.markdown(f'<div class="msg"><div class="msg-av {cls}">{av}</div><div class="msg-body {bc}">{msg["content"]}</div></div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("Type your message..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        if not st.session_state.state.get("user_name"):
            st.session_state.state["user_name"] = prompt
        elif not st.session_state.state.get("user_age"):
            try: st.session_state.state["user_age"] = int(prompt)
            except: st.session_state.state["user_age"] = 20
        elif not st.session_state.state.get("goal"):
            st.session_state.state["goal"] = prompt
        elif not st.session_state.state.get("timeframe"):
            st.session_state.state["timeframe"] = prompt
        
        st.session_state.state["messages"].append(HumanMessage(content=prompt))
        
        with st.spinner("Thinking..."):
            st.session_state.state = st.session_state.agent.invoke(st.session_state.state)
        
        response = st.session_state.state["messages"][-1].content
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        if all([st.session_state.state.get("user_name"), st.session_state.state.get("goal"), st.session_state.state.get("timeframe")]):
            st.session_state.onboarding_complete = True
        st.rerun()

with col2:
    # Profile
    p = st.session_state.state
    items = [("Name", p.get("user_name","—")), ("Age", p.get("user_age","—")), ("Goal", p.get("goal","—")), ("Timeframe", p.get("timeframe","—")), ("Phase", p.get("phase","start"))]
    ph = '<div class="panel"><div class="panel-title">Your Profile</div>'
    for l,v in items: ph += f'<div class="prof-row"><span class="prof-label">{l}</span><span class="prof-val">{v}</span></div>'
    ph += '</div>'
    st.markdown(ph, unsafe_allow_html=True)
    
    # Checklist
    cl = p.get("checklist", [])
    if cl:
        ch = '<div class="panel"><div class="panel-title">Checklist</div>'
        for item in cl:
            cls = "done" if item.get("completed") else ""
            chk = "✓" if item.get("completed") else ""
            ch += f'<div class="chk {cls}"><div class="chk-box">{chk}</div>{item["task"]}</div>'
        ch += '</div>'
        st.markdown(ch, unsafe_allow_html=True)
    
    # Files
    sd = os.path.join(parent_dir, "sessions", p.get("session_id",""))
    if os.path.exists(sd):
        fs = [f for f in os.listdir(sd) if f.endswith(('.md','.html','.json'))]
        if fs:
            fh = '<div class="panel"><div class="panel-title">Session Files</div>'
            for f in fs:
                i = "📄" if f.endswith('.md') else "🌐" if f.endswith('.html') else "📊"
                fh += f'<div class="file"><div class="file-ico">{i}</div>{f}</div>'
            fh += '</div>'
            st.markdown(fh, unsafe_allow_html=True)
    
    # Button
    if st.button("✨ Start New Session", use_container_width=True):
        st.session_state.state = {"messages":[],"user_name":"","user_age":0,"goal":"","timeframe":"","session_id":f"session_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}","phase":"start","resources":[],"checklist":[]}
        st.session_state.chat_history = []
        st.session_state.onboarding_complete = False
        st.rerun()
