# LearnPath AI - Backend Agent (Sprint 4)
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def create_agent():
    """Create and return the LearnPath AI agent"""
    
    # LLM - using environment variable
    llm = ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7
    )
    
    # State
    class AgentState(TypedDict):
        messages: Annotated[Sequence[HumanMessage | AIMessage], add_messages]
        user_name: str
        user_age: int
        goal: str
        timeframe: str
        session_id: str
        phase: str
        resources: list
        checklist: list
    
    # Get session directory
    def get_session_dir(state):
        return os.path.join("sessions", state.get("session_id", "default"))
    
    # Save file with UTF-8
    def save_file(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # Save thinking board
    def save_thinking_board(state, content):
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        save_file(os.path.join(session_dir, "thinking_board.md"), content)
    
    # Save checklist
    def save_checklist(state, checklist):
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        
        with open(os.path.join(session_dir, "checklist.json"), "w") as f:
            json.dump(checklist, f, indent=2)
        
        md_content = "# Learning Checklist\n\n"
        for item in checklist:
            status = "[x]" if item.get("completed") else "[ ]"
            md_content += f"- {status} {item['task']}\n"
        
        save_file(os.path.join(session_dir, "checklist.md"), md_content)
    
    # Save resources
    def save_resources(state, resources):
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        
        md_content = "# Learning Resources\n\n"
        for r in resources:
            md_content += f"## {r['title']}\n"
            md_content += f"- **Type:** {r['type']}\n"
            md_content += f"- **Link:** {r['link']}\n"
            md_content += f"- **Description:** {r['description']}\n\n"
        
        save_file(os.path.join(session_dir, "resources.md"), md_content)
    
    # Save whiteboard
    def save_whiteboard(state, content):
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        save_file(os.path.join(session_dir, "whiteboard.html"), content)
    
    # Save code examples
    def save_code_examples(state, content):
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        save_file(os.path.join(session_dir, "code_examples.md"), content)
    
    # Nodes
    def onboard(state: AgentState) -> AgentState:
        msgs = state["messages"]
        last = msgs[-1].content if msgs else ""
        name = state.get("user_name", "")
        age = state.get("user_age", 0)
        goal = state.get("goal", "")
        timeframe = state.get("timeframe", "")
        
        if not name:
            prompt = "Greet the user warmly and ask for their name. Be enthusiastic!"
        elif not age:
            prompt = f"Nice to meet you {name}! Ask how old they are."
        elif not goal:
            prompt = f"Ask {name} what they want to learn. Give examples like Python, Web Dev, Data Science."
        elif not timeframe:
            prompt = f"Ask {name} how much time they have (1 week, 2 weeks, 1 month)."
        else:
            prompt = f"""
            Confirm with {name}:
            - Name: {name}
            - Age: {age}
            - Goal: {goal}
            - Timeframe: {timeframe}
            
            Ask if correct. Be excited!
            """
        
        resp = llm.invoke([HumanMessage(content=prompt)])
        return {"messages": [AIMessage(content=resp.content)], "phase": "onboard"}
    
    def plan(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        timeframe = state.get("timeframe", "some time")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Create a {timeframe} learning plan for {name} to learn {goal}.
        
        Format:
        ## Overview
        ## Week 1: ...
        ## Week 2: ...
        ## Resources
        ## Milestones
        
        Keep it concise but useful.
        """)])
        
        session_dir = get_session_dir(state)
        os.makedirs(session_dir, exist_ok=True)
        save_file(os.path.join(session_dir, "curriculum.md"), resp.content)
        
        return {
            "messages": [AIMessage(content=f"Here's your learning plan:\n\n{resp.content}")],
            "phase": "resources"
        }
    
    def ask_resources(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Ask {name} if they have any learning materials to add:
        - Videos (YouTube links)
        - Books
        - PDFs
        - Articles
        
        Or if they want you to find free resources online.
        """)])
        
        return {"messages": [AIMessage(content=resp.content)], "phase": "resources"}
    
    def find_resources(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Find 5 free learning resources for {name} to learn {goal}.
        
        Include:
        - YouTube tutorials
        - Free courses
        - Documentation
        - Practice platforms
        
        Format as a numbered list with title, type, and description.
        """)])
        
        resources = [
            {"title": "Free Resource 1", "type": "Video", "link": "https://youtube.com", "description": "Tutorial"},
            {"title": "Free Resource 2", "type": "Course", "link": "https://coursera.org", "description": "Course"},
        ]
        save_resources(state, resources)
        
        return {
            "messages": [AIMessage(content=f"Here are some free resources:\n\n{resp.content}")],
            "phase": "thinking"
        }
    
    def thinking_board(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Create a thinking board for {name} learning {goal}.
        
        Include:
        ## Key Concepts
        ## Learning Path
        ## Potential Challenges
        ## Tips for Success
        """)])
        
        save_thinking_board(state, resp.content)
        
        return {
            "messages": [AIMessage(content=f"Here's your thinking board:\n\n{resp.content}")],
            "phase": "checklist"
        }
    
    def create_checklist(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        timeframe = state.get("timeframe", "some time")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Create a learning checklist for {name} to learn {goal} in {timeframe}.
        
        Include 5-7 actionable items.
        """)])
        
        checklist = [
            {"task": "Complete introduction", "completed": False},
            {"task": "Set up development environment", "completed": False},
            {"task": "Complete first tutorial", "completed": False},
            {"task": "Build a practice project", "completed": False},
            {"task": "Review and practice", "completed": False},
        ]
        save_checklist(state, checklist)
        
        return {
            "messages": [AIMessage(content=f"Here's your checklist:\n\n{resp.content}")],
            "phase": "code",
            "checklist": checklist
        }
    
    def code_examples(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Create beginner code examples for {name} learning {goal}.
        
        Include 3-5 code snippets with:
        - Title
        - Description
        - Code block
        - Expected output
        
        Make it beginner-friendly.
        """)])
        
        save_code_examples(state, resp.content)
        
        return {
            "messages": [AIMessage(content=f"Here are some code examples to get you started:\n\n{resp.content}")],
            "phase": "whiteboard"
        }
    
    def whiteboard(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        
        resp = llm.invoke([HumanMessage(content=f"""
        Create a visual learning path diagram for {name} learning {goal}.
        
        Use this HTML/CSS format:
        - A flowchart showing the learning journey
        - Boxes for each major topic
        - Arrows connecting them
        - Color-coded by difficulty
        
        Return ONLY the HTML code.
        """)])
        
        # Create a simple whiteboard HTML
        whiteboard_html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #4CAF50; text-align: center; }}
        .flow {{ display: flex; flex-direction: column; gap: 20px; align-items: center; }}
        .box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 300px; text-align: center; }}
        .box.easy {{ border-left: 5px solid #4CAF50; }}
        .box.medium {{ border-left: 5px solid #FFC107; }}
        .box.hard {{ border-left: 5px solid #f44336; }}
        .arrow {{ font-size: 24px; color: #666; }}
        .legend {{ display: flex; gap: 20px; justify-content: center; margin-top: 20px; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Learning Path: {goal}</h1>
        <div class="flow">
            <div class="box easy"><strong>1. Fundamentals</strong><br>Learn the basics</div>
            <div class="arrow">↓</div>
            <div class="box easy"><strong>2. Core Concepts</strong><br>Build understanding</div>
            <div class="arrow">↓</div>
            <div class="box medium"><strong>3. Practice</strong><br>Apply what you learned</div>
            <div class="arrow">↓</div>
            <div class="box medium"><strong>4. Projects</strong><br>Build real things</div>
            <div class="arrow">↓</div>
            <div class="box hard"><strong>5. Mastery</strong><br>Advanced topics</div>
        </div>
        <div class="legend">
            <div class="legend-item"><div class="legend-color" style="background: #4CAF50;"></div> Easy</div>
            <div class="legend-item"><div class="legend-color" style="background: #FFC107;"></div> Medium</div>
            <div class="legend-item"><div class="legend-color" style="background: #f44336;"></div> Hard</div>
        </div>
    </div>
</body>
</html>"""
        
        save_whiteboard(state, whiteboard_html)
        
        return {
            "messages": [AIMessage(content="I've created a visual learning path for you! Check the whiteboard in your session folder.")],
            "phase": "learn"
        }
    
    def learn(state: AgentState) -> AgentState:
        name = state.get("user_name", "there")
        goal = state.get("goal", "something")
        last = state["messages"][-1].content
        
        # Check for completion keywords
        completion_words = ["completed", "finished", "done", "achieved", "mastered"]
        is_completion = any(word in last.lower() for word in completion_words)
        
        if is_completion:
            resp = llm.invoke([HumanMessage(content=f"""
            {name} says they've completed their goal of learning {goal}!
            
            Celebrate with them! Create a congratulatory message with:
            - Their achievements
            - What they learned
            - Next steps
            - Encouragement
            
            Make it feel like end credits of a movie!
            """)])
            
            # Create end credits
            end_credits = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
            animation: fadeIn 2s;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        h1 {{ font-size: 3rem; margin-bottom: 30px; }}
        .credit {{ margin: 20px 0; font-size: 1.2rem; }}
        .name {{ font-size: 2rem; color: #FFD700; }}
        .emoji {{ font-size: 4rem; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="emoji">🎓🏆✨</div>
    <h1>Congratulations!</h1>
    <div class="name">{name}</div>
    <div class="credit">You've completed your learning journey!</div>
    <div class="credit">Goal: {goal}</div>
    <div class="credit">Status: ACHIEVED</div>
    <div class="emoji">🎉🎊🥳</div>
    <div class="credit">Keep learning, keep growing!</div>
</body>
</html>"""
            
            session_dir = get_session_dir(state)
            save_file(os.path.join(session_dir, "end_credits.html"), end_credits)
            
            return {"messages": [AIMessage(content=resp.content + "\n\n🎓 Check out your end credits in the session folder!")]}
        else:
            resp = llm.invoke([HumanMessage(content=f"""
            Help {name} learn {goal}.
            They said: {last}
            
            Be helpful, give examples, encourage them.
            """)])
            
            return {"messages": [AIMessage(content=resp.content)]}
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("onboard", onboard)
    workflow.add_node("plan", plan)
    workflow.add_node("ask_resources", ask_resources)
    workflow.add_node("find_resources", find_resources)
    workflow.add_node("thinking_board", thinking_board)
    workflow.add_node("create_checklist", create_checklist)
    workflow.add_node("code_examples", code_examples)
    workflow.add_node("whiteboard", whiteboard)
    workflow.add_node("learn", learn)
    
    workflow.set_entry_point("onboard")
    workflow.add_edge("onboard", "plan")
    workflow.add_edge("plan", "ask_resources")
    workflow.add_edge("ask_resources", "find_resources")
    workflow.add_edge("find_resources", "thinking_board")
    workflow.add_edge("thinking_board", "create_checklist")
    workflow.add_edge("create_checklist", "code_examples")
    workflow.add_edge("code_examples", "whiteboard")
    workflow.add_edge("whiteboard", "learn")
    workflow.add_edge("learn", END)
    
    return workflow.compile()

# Test
if __name__ == "__main__":
    print("Testing LearnPath AI Agent (Sprint 4)...")
    app = create_agent()
    state = {
        "messages": [],
        "user_name": "",
        "user_age": 0,
        "goal": "",
        "timeframe": "",
        "session_id": "test_sprint4",
        "phase": "start",
        "resources": [],
        "checklist": []
    }
    state = app.invoke(state)
    print(f"Response: {state['messages'][-1].content[:200]}...")
    print(f"Phase: {state['phase']}")
    print("Sprint 4 Backend works!")
