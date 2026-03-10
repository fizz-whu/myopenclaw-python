# myopenclaw-python

A simple Python implementation of OpenClaw's gateway architecture that receives messages and sends them to AI for processing.

## Architecture

This implementation follows OpenClaw's message flow:

1. **Gateway** (`gateway.py`) - HTTP server that receives messages
2. **Routing** (`routing.py`) - Determines which agent handles the message
3. **Agent Processor** (`agent.py`) - Sends message to AI (OpenAI)
4. **Session Store** (`session.py`) - Manages conversation history

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Running

Start the gateway server:
```bash
python gateway.py
```

The gateway will run on `http://localhost:8000` by default.

## Usage

### HTTP API

Send a message:
```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "channel": "api"
  }'
```

Response:
```json
{
  "response": "I'm doing well, thank you for asking!...",
  "success": true,
  "error": null,
  "session_key": "default:api:default",
  "agent_id": "default"
}
```

### CLI Client

```bash
python example_client.py "Hello, how are you?"
```

### Python Code

```python
import requests

response = requests.post(
    "http://localhost:8000/message",
    json={
        "message": "Hello!",
        "channel": "python",
    }
)

print(response.json())
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Health check
- `POST /message` - Send a message to AI
- `GET /sessions` - List all active sessions

## Message Request Format

```json
{
  "message": "Your message here",
  "channel": "api",           // Optional: channel identifier
  "account_id": "user123",    // Optional: account identifier
  "peer_kind": "direct",      // Optional: peer type (direct/group/channel)
  "peer_id": "12345",         // Optional: peer identifier
  "images": []                // Optional: list of image URLs
}
```

## Configuration

Edit `config.py` or use environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key
- `DEFAULT_MODEL` - Model to use (default: gpt-4o-mini)
- `DEFAULT_PROVIDER` - Provider to use (default: openai)
- `GATEWAY_PORT` - Gateway server port (default: 8000)

## How It Works

1. **Message Reception**: Gateway receives HTTP POST with message
2. **Routing**: Based on channel/account/peer, determines which agent to use
3. **Session Management**: Loads or creates conversation session
4. **AI Processing**: Sends message + history to OpenAI
5. **Response**: Returns AI response and updates session

## Comparison with OpenClaw

| OpenClaw (TypeScript) | myopenclaw-python |
|-----------------------|-------------------|
| `src/gateway/server.ts` | `gateway.py` |
| `src/routing/resolve-route.ts` | `routing.py` |
| `src/commands/agent.ts` | `agent.py` |
| `src/config/sessions.ts` | `session.py` |

## Extending

### Add a new channel

Create a new file like `telegram_channel.py`:

```python
from gateway import send_message_logic

async def handle_telegram_message(update):
    # Extract message from Telegram update
    message = update.message.text
    
    # Process through gateway
    result = await process_message(
        message=message,
        channel="telegram",
        account_id=str(update.message.chat.id),
        peer=RoutePeer(kind="direct", id=str(update.message.from_user.id))
    )
    
    # Send response back to Telegram
    await send_to_telegram(result.response)
```

### Add a new AI provider

Extend `agent.py`:

```python
def _get_client(self, provider: str):
    if provider == "anthropic":
        import anthropic
        return anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # ... handle other providers
```

## License

MIT
