# LearnPath AI 🎓

An AI-powered personalized learning platform that creates custom curricula, tracks progress, and guides you through your learning journey.

## Features

- **Animated Onboarding** - Fun, engaging welcome experience
- **Personalized Curriculum** - AI-generated learning plans
- **Resource Collection** - Find free learning materials
- **Thinking Board** - AI-powered learning insights
- **Dynamic Checklist** - Track your progress
- **Chat Interface** - Natural conversation with your AI tutor

## Tech Stack

- **Backend:** Python, LangGraphs, OpenRouter API
- **Frontend:** Streamlit
- **AI:** Llama 3.3 70B via OpenRouter

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create `.env` file:
```
OPENROUTER_API_KEY=your_key_here
```

### 3. Run Backend Test
```bash
python backend/agent.py
```

### 4. Run Frontend
```bash
python -m streamlit run frontend/app.py
```

Open http://localhost:8501

## Project Structure

```
learnpath-ai/
├── backend/
│   └── agent.py          # LangGraph agent
├── frontend/
│   └── app.py            # Streamlit UI
├── sessions/             # User sessions (gitignored)
├── requirements.txt      # Dependencies
├── .env                  # API keys (gitignored)
└── README.md             # This file
```

## How It Works

1. **Onboarding** - Tell the AI your name, age, goal, and timeframe
2. **Curriculum** - AI generates a personalized learning plan
3. **Resources** - Find free learning materials
4. **Learning** - Chat with your AI tutor, track progress

## License

MIT
