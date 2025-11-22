# HR Recruitment Assistant 🎯

A production-ready web application for HR recruitment with AI-powered CV analysis, candidate scoring, and job description optimization.

## Features

- 📄 **CV Upload & Processing**: Upload single or multiple CVs (PDF) for automatic extraction
- 👥 **Candidate Dashboard**: View, filter, and manage all candidates in one place
- 📊 **Analytics**: Visual insights on candidates, scores, and recruitment trends
- ✍️ **JD Rewriting**: AI-powered job description improvement and optimization
- 🎯 **Smart Scoring**: Automatic candidate scoring against job requirements
- 💾 **PostgreSQL Database**: Production-grade data persistence
- ⚡ **Redis Caching**: Fast agent memory and result caching
- 🐳 **Docker Deployment**: Easy deployment with docker-compose

## Tech Stack

- **Backend**: FastAPI, Langchain, Langgraph
- **Frontend**: Gradio
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **LLM**: Groq (llama-3.3-70b)
- **Deployment**: Docker + docker-compose

## Quick Start

### Prerequisites

- Docker & docker-compose
- Groq API key ([Get one here](https://console.groq.com/))

### Setup

1. **Clone and navigate**:
   ```bash
   cd /home/baobao/Projects/HR-Agents/jd_assistants
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Start services**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Web UI: http://localhost:7860
   - Check logs: `docker-compose logs -f app`

### Development Mode

For local development without Docker:

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Start PostgreSQL and Redis** (via Docker):
   ```bash
   docker-compose up -d postgres redis
   ```

3. **Set environment variables**:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://hr_user:hr_password@localhost:5432/hr_db"
   export REDIS_URL="redis://localhost:6379/0"
   export GROQ_API_KEY="your_api_key_here"
   ```

4. **Run application**:
   ```bash
   python -m jd_assistants.app
   ```

## Usage Guide

### 1. Upload CVs
- Go to "📄 Upload CVs" tab
- Select one or multiple PDF files
- Click "Process CVs"
- View extracted candidate information

### 2. Create Job Description
- Go to "📋 Job Description" tab
- Enter job title, description, and required skills
- Click "Save Job Description"

### 3. Score Candidates
- Go to "👥 Candidates Dashboard" tab
- Click "Score All Candidates"
- View ranked candidates with scores and reasons

### 4. View Analytics
- Go to "📊 Analytics" tab
- Click "Generate Analytics"
- View score distributions and trends

### 5. Improve Job Descriptions
- Go to "✍️ JD Rewriting" tab
- Paste your JD
- Click "Analyze & Suggest Improvements" for feedback
- Click "Rewrite Complete JD" for a complete rewrite

## Architecture

```
┌─────────────┐
│   Gradio    │ ← User Interface
│   Frontend  │
└──────┬──────┘
       │
┌──────┴────────────────────────┐
│   Application Layer           │
│  - CV Processing              │
│  - Candidate Scoring          │
│  - JD Rewriting               │
│  - Analytics                  │
└───────┬───────────────────────┘
        │
   ┌────┴────┐
   │         │
┌──┴──┐  ┌──┴───┐
│ DB  │  │Redis │
│(PG) │  │Cache │
└─────┘  └──────┘
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://hr_user:hr_password@localhost:5432/hr_db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `GROQ_API_KEY` | Groq API key | *Required* |
| `APP_HOST` | Application host | `0.0.0.0` |
| `APP_PORT` | Application port | `7860` |

## Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View database
docker-compose exec postgres psql -U hr_user -d hr_db

# Redis CLI
docker-compose exec redis redis-cli
```

## Project Structure

```
jd_assistants/
├── Dockerfile                 # Application container
├── docker-compose.yml        # Service orchestration
├── .env.example              # Environment variables template
├── src/jd_assistants/
│   ├── agent/                # AI agents
│   │   ├── base.py          # Base agent class
│   │   ├── read_cv.py       # CV extraction
│   │   ├── summarization.py # Bio generation
│   │   ├── score.py         # Candidate scoring
│   │   ├── response.py      # Email generation
│   │   └── jd_rewriter.py   # JD improvement
│   ├── database.py          # PostgreSQL models & CRUD
│   ├── cache.py             # Redis operations
│   ├── app.py               # Main Gradio application
│   ├── models.py            # Pydantic models
│   └── tools/               # Utilities
└── pyproject.toml           # Dependencies
```

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running: `docker-compose ps postgres`
- Check credentials in `.env`
- Verify database URL format

### Redis connection errors
- Ensure Redis is running: `docker-compose ps redis`
- Check Redis URL in `.env`

### API rate limits
- Groq has rate limits on free tier
- Add delays between batch operations
- Consider upgrading Groq plan

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request