# WhatsApp-Todoist Bot (Baileys) - Documentation

Self-hosted WhatsApp bot with LLM-powered Todoist integration using Baileys (pyaileys).

## ⚠️ Required Environment Variables

Before running the bot, you **must** set these environment variables:

| Variable | Description | Example | Required? |
|----------|-------------|---------|-----------|
| `TODOIST_API_TOKEN` | Get from [Todoist Integrations](https://todoist.com/prefs/integrations) | `todoist_api_token_here` | ✅ Yes |
| `OPENAI_API_KEY` | Get from [OpenAI API Keys](https://platform.openai.com/api-keys) | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | ✅ Yes |
| `WHATSAPP_SESSION_PATH` | Directory to store WhatsApp auth session (used with Docker volume) | `/app/auth` | ✅ Yes (for persistence) |

## 🔧 Optional Configuration

| Variable | Description | Example | Required? |
|----------|-------------|---------|-----------|
| `MODEL_PROVIDER` | LLM provider: `openai` or `openrouter` (default: `openai`) | `openai` | No |
| `MODEL_NAME` | Model to use (default: `gpt-4o-mini`) | `gpt-4o-mini` | No |
| `REDIS_URL` | Redis URL for conversation context (optional) | `redis://localhost:6379` | No |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/youneedatechguy/the-help.git
cd the-help
```

### 2. Environment Variables
Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
# Edit .env with your values (at minimum, set the required variables above)
nano .env
```

### 3. Run with Docker Compose
```bash
# Build and start the service
docker-compose up -d

# View logs to see QR code for WhatsApp linking
docker-compose logs -f
```

## QR Code Display & Device Onboarding

### Where the QR Code Appears
The QR code is displayed in the container logs when:
1. Starting the container for the first time
2. No existing WhatsApp session is found in the auth directory
3. The bot needs to link to a WhatsApp number

### How to View the QR Code
1. Start the container: `docker-compose up -d`
2. Follow the logs: `docker-compose logs -f`
3. Look for an ASCII QR code in the output (appears as block characters)
4. The logs will contain text like: `Scan this QR code with WhatsApp to link your device`

### Device Onboarding Process
1. **First-time setup**: When no session exists, the bot generates a QR code in logs
2. **Link your device**:
   - Open WhatsApp on your phone
   - Go to Settings → Linked Devices → Link a Device
   - Scan the QR code from the Docker logs
3. **Session persistence**: The WhatsApp session is saved to the Docker volume (`whatsapp-auth`)
4. **Subsequent startups**: Bot reuses existing session (no QR needed unless session is cleared)

### To Link a New Device or Reset
```bash
# Remove existing auth session
docker-compose down
docker volume rm the-help_whatsapp-auth  # Volume name may vary

# Restart to generate new QR code
docker-compose up -d
docker-compose logs -f
```

## Model Configuration

### Available Configuration Options
The bot supports both OpenAI and OpenRouter providers with flexible model selection:

**Environment Variables:**
- `MODEL_PROVIDER`: `openai` or `openrouter` (defaults to `openai`)
- `MODEL_NAME`: Specific model identifier (defaults to `gpt-4o-mini`)

**Examples:**
```bash
# Use OpenAI GPT-4o
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o

# Use OpenRouter with a different model
MODEL_PROVIDER=openrouter
MODEL_NAME=anthropic/claude-3-haiku

# Use OpenAI GPT-3.5 Turbo (cost-effective)
MODEL_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
```

**Note**: The default model is `gpt-4o-mini` with OpenAI provider, as specified in the requirements.

## Commands

Send WhatsApp messages to your linked number:

| Command | Description |
|---------|-------------|
| `Create a task to buy milk` | Create a new Todoist task |
| `Show my tasks` | List your Todoist tasks |
| `Complete [task name]` | Mark a task as completed |
| `Move [task] to [project]` | Move task between projects |
| `Help` | Show available commands |

## API Endpoints

The bot exposes these HTTP endpoints for testing and monitoring:

- `GET /health` - Health check (returns WhatsApp connection status)
- `GET /tasks` - List tasks via HTTP (for testing only)

## Logging & Monitoring

### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail 50

# Specific service
docker-compose logs -f whatsapp-todoist-bot
```

### Health Check
```bash
curl http://localhost:8001/health
# Returns: {"status":"healthy","service":"whatsapp-todoist-bot","whatsapp_connected":true}
```

## Directory Structure

```
the-help/
├── app/
│   ├── __init__.py
│   ├── agent.py          # LLM-powered Todoist agent
│   ├── config.py         # Environment configuration
│   ├── main.py           # FastAPI application
│   ├── redis_conversation.py  # Conversation memory (optional)
│   ├── todoist_client.py # Todoist API client
│   └── whatsapp_handler.py # Baileys WhatsApp integration
├── Dockerfile            # Container build instructions
├── docker-compose.yml    # Deployment configuration
├── requirements.txt      # Python dependencies
└── .env.example          # Environment template
```

## Deployment Notes

### Persistent Storage
- WhatsApp auth session is stored in Docker volume (`whatsapp-auth`)
- This preserves your device linking across container restarts
- To reset linking, remove the volume as described above

### Resource Usage
- Memory: ~150-256MB (depending on model usage)
- CPU: Minimal when idle, increases during LLM processing
- Network: Only when sending/receiving WhatsApp messages

## Troubleshooting

### Common Issues

**QR Code Not Visible in Logs**
- Ensure you're following logs with `docker-compose logs -f`
- Check if a session already exists (no QR needed if linked)
- Verify container is running: `docker-compose ps`

**WhatsApp Not Connecting**
- Check logs for connection errors
- Verify internet connectivity from container
- Ensure port 8001 is accessible if testing externally

**Model Loading Errors**
- Verify API key is valid and has credit
- Check model name spelling and availability
- Try switching providers (openai ↔ openrouter)

**Rate Limiting**
- OpenAI/OpenRouter have usage limits
- Monitor usage in respective provider dashboards
- Consider adding caching or request throttling if needed

## Security Notes

- Never commit your `.env` file with real API keys
- The WhatsApp session contains authentication tokens - treat as sensitive
- Consider using Docker secrets for production deployments
- Regularly rotate API keys if security is a concern

## Support

For issues or questions, check:
1. Container logs: `docker-compose logs -f`
2. Environment variables: Check your `.env` file or Portainer config
3. WhatsApp connection: Verify via `/health` endpoint
4. API credentials: Validate with respective provider services

---
**Ready for deployment via Portainer or Docker Compose.**