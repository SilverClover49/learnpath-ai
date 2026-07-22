# LearnPath AI - Sprint 2 Progress

## What's Working Now

### Backend
✅ Optimized agent with 3 nodes (onboard, plan, learn)
✅ User state management (name, age, goal, timeframe)
✅ Session folder creation
✅ Curriculum generation
✅ LLM integration

### Frontend
✅ Animated welcome screen
✅ Step indicator (Name → Age → Goal → Timeframe → Plan)
✅ Chat interface
✅ Session info sidebar
✅ Reset session button
✅ Custom CSS animations

## How to Run

### Backend Test
```powershell
cd D:\AICTE-AI-Internship\learnpath-ai
python backend\agent.py
```

### Frontend
```powershell
cd D:\AICTE-AI-Internship\learnpath-ai
python -m streamlit run frontend\app.py --server.port 8502
```

Then open **http://localhost:8502**

## Test Flow
1. Open the app
2. See animated welcome screen
3. Type your name → Agent asks for age
4. Type your age → Agent asks for goal
5. Type your goal → Agent asks for timeframe
6. Type your timeframe → Agent generates curriculum
7. Curriculum saved to `sessions/` folder

## Session Files Created
```
sessions/
└── session_YYYYMMDD_HHMMSS/
    ├── profile.md        # User info
    └── curriculum.md     # Learning plan
```

## Next Steps (Sprint 3)
- Resource collection (user upload + AI find)
- Thinking board
- Dynamic checklist
- Better UI polish
