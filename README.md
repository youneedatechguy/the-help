# WhatsApp-Todoist Bot (Baileys)

Self-hosted WhatsApp bot with LLM-powered Todoist integration.

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and add your API keys
3. Run with Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
```

4. Scan QR code from logs to link WhatsApp

## Environment Variables

- `TODOIST_API_TOKEN` - From todoist.com/prefs/integrations
- `OPENAI_API_KEY` - From platform.openai.com/api-keys
- `WHATSAPP_SESSION_PATH` - Where to store WhatsApp auth (default: ./auth)

## Commands

Send WhatsApp messages:
- "Create a task to buy milk" - Create a task
- "Show my tasks" - List tasks
- "Complete [task name]" - Mark task done
- "Move [task] to [project]" - Move task

## API Endpoints

- `GET /health` - Health check
- `GET /tasks` - List tasks (HTTP)