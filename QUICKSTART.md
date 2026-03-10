# Quick Start Guide

## 1. Setup (First Time)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

## 2. Run the Gateway

```bash
# Start the gateway server
python gateway.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 3. Test It

### Option A: Use the test script
In a new terminal:
```bash
python test_gateway.py
```

### Option B: Use curl
```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "channel": "cli"}'
```

### Option C: Use the example client
```bash
python example_client.py "What is Python?"
```

## 4. Continue Conversation

The gateway maintains conversation history per session. Send another message with the same account_id to continue:

```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What was my previous question?",
    "channel": "cli",
    "account_id": "my_user"
  }'
```

## 5. Check Active Sessions

```bash
curl http://localhost:8000/sessions
```

## Architecture Overview

```
┌─────────────┐
│   Message   │
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Gateway API    │ (gateway.py)
│  /message       │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    Routing      │ (routing.py)
│  Resolve Agent  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Session Store   │ (session.py)
│ Load/Create     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Agent Processor │ (agent.py)
│  Call OpenAI    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Response      │
│   to Client     │
└─────────────────┘
```

## What's Next?

- Add more channels (Telegram, Discord, Slack)
- Add more AI providers (Anthropic, Cohere, etc.)
- Add authentication
- Add rate limiting
- Add streaming responses

See README.md for details on extending the gateway.
