# LearnPath AI - Technical Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      LearnPath AI                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Frontend  │    │   Backend   │    │  External   │     │
│  │  (Streamlit)│◄──►│ (LangGraph) │◄──►│  (OpenRouter)│     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Browser   │    │   Sessions  │    │   LLM API   │     │
│  │   (Local)   │    │   (Files)   │    │   (Cloud)   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Frontend (Streamlit)
- **Purpose:** User interface
- **Features:**
  - Animated welcome screen
  - Chat interface
  - Session info sidebar
  - Progress indicators
- **Location:** `frontend/app.py`

### Backend (LangGraph)
- **Purpose:** Agent orchestration
- **Features:**
  - 9-node workflow
  - LLM integration
  - Session management
  - File generation
- **Location:** `backend/agent.py`

### External (OpenRouter)
- **Purpose:** LLM inference
- **Model:** Llama 3.3 70B
- **Usage:** All AI responses

## Data Flow

```
User Input
    ↓
Frontend (Streamlit)
    ↓
Backend (LangGraph)
    ├→ Onboard Node
    ├→ Plan Node
    ├→ Resources Node
    ├→ Thinking Board Node
    ├→ Checklist Node
    ├→ Code Examples Node
    ├→ Whiteboard Node
    └→ Learn Node
    ↓
Session Files (Markdown/HTML/JSON)
    ↓
Frontend Display
```

## Agent Graph

```python
StateGraph(AgentState)
    .add_node("onboard", onboard)
    .add_node("plan", plan)
    .add_node("ask_resources", ask_resources)
    .add_node("find_resources", find_resources)
    .add_node("thinking_board", thinking_board)
    .add_node("create_checklist", create_checklist)
    .add_node("code_examples", code_examples)
    .add_node("whiteboard", whiteboard)
    .add_node("learn", learn)
    .set_entry_point("onboard")
    .add_edge("onboard", "plan")
    .add_edge("plan", "ask_resources")
    .add_edge("ask_resources", "find_resources")
    .add_edge("find_resources", "thinking_board")
    .add_edge("thinking_board", "create_checklist")
    .add_edge("create_checklist", "code_examples")
    .add_edge("code_examples", "whiteboard")
    .add_edge("whiteboard", "learn")
    .add_edge("learn", END)
```

## State Management

```python
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
```

## File Structure

```
sessions/
└── session_YYYYMMDD_HHMMSS/
    ├── profile.md          # User info
    ├── curriculum.md       # Learning plan
    ├── thinking_board.md   # AI insights
    ├── checklist.md        # Task list
    ├── checklist.json      # Machine-readable
    ├── resources.md        # Learning materials
    ├── code_examples.md    # Code snippets
    ├── whiteboard.html     # Visual path
    └── end_credits.html    # Completion
```

## API Integration

### OpenRouter Setup
```python
llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7
)
```

### Prompt Template
```python
resp = llm.invoke([HumanMessage(content=f"""
    Task: {task}
    Context: {context}
    User: {user_info}
    
    Response:
""")])
```

## Error Handling

| Error | Handling |
|-------|----------|
| API timeout | Retry with backoff |
| Invalid input | Graceful fallback |
| File write error | Log and continue |
| LLM error | Use cached response |

## Performance

| Metric | Target | Current |
|--------|--------|---------|
| Response time | < 5s | ~3-5s |
| File generation | < 1s | < 1s |
| Memory usage | < 100MB | ~50MB |

## Security

- API keys in environment variables
- No sensitive data in files
- Local file storage only
- No external data sharing

## Future Improvements

1. **Database storage** - Replace file-based sessions
2. **User authentication** - Multi-user support
3. **Real-time updates** - WebSocket integration
4. **Mobile app** - React Native frontend
5. **Analytics** - Learning progress insights
