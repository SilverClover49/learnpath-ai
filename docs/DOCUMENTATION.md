# LearnPath AI - Complete Documentation

## Overview

LearnPath AI is an AI-powered personalized learning platform that creates custom curricula, tracks progress, and guides users through their learning journey.

## Features

### Core Features
- **Animated Onboarding** - Fun, engaging welcome experience
- **Personalized Curriculum** - AI-generated learning plans
- **Resource Collection** - Find free learning materials
- **Thinking Board** - AI-powered learning insights
- **Dynamic Checklist** - Track progress
- **Code Examples** - Beginner-friendly code snippets
- **Whiteboard** - Visual learning paths
- **End Credits** - Celebration on completion

### Technical Features
- **LangGraphs** - Agent orchestration
- **Streamlit** - Modern web UI
- **OpenRouter API** - LLM integration
- **Session Persistence** - Save progress to files

## Architecture

```
learnpath-ai/
├── backend/
│   └── agent.py          # LangGraph agent (9 nodes)
├── frontend/
│   └── app.py            # Streamlit UI
├── sessions/             # User sessions
├── requirements.txt      # Dependencies
├── .env.example          # API key template
└── README.md             # Project overview
```

## Agent Flow

```
Onboard → Plan → Resources → Thinking Board → Checklist → Code → Whiteboard → Learn
```

### Node Descriptions

1. **Onboard** - Collects user info (name, age, goal, timeframe)
2. **Plan** - Generates personalized curriculum
3. **Ask Resources** - Asks about learning materials
4. **Find Resources** - Discovers free resources
5. **Thinking Board** - Creates learning insights
6. **Create Checklist** - Builds task list
7. **Code Examples** - Generates code snippets
8. **Whiteboard** - Creates visual learning path
9. **Learn** - Interactive learning with celebration

## Session Files

Each session creates:

| File | Description |
|------|-------------|
| `profile.md` | User information |
| `curriculum.md` | Learning plan |
| `thinking_board.md` | AI insights |
| `checklist.md` | Task list |
| `checklist.json` | Machine-readable tasks |
| `resources.md` | Learning materials |
| `code_examples.md` | Code snippets |
| `whiteboard.html` | Visual learning path |
| `end_credits.html` | Completion celebration |

## API Integration

### OpenRouter
- Model: Llama 3.3 70B
- Used for: All LLM calls
- Rate limit: Varies by plan

### Environment Variables

```bash
OPENROUTER_API_KEY=your_key_here
```

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env with your API key

# Run backend test
python backend/agent.py

# Run frontend
python -m streamlit run frontend/app.py
```

### Production

1. Set environment variables
2. Deploy to your platform
3. Configure reverse proxy
4. Enable HTTPS

## Testing

### Backend Test
```bash
python backend/agent.py
```

### Frontend Test
```bash
python -m streamlit run frontend/app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

- GitHub Issues: https://github.com/SilverClover49/learnpath-ai/issues
- Email: mdrumaan12345@gmail.com
