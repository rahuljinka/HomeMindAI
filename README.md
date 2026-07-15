# HomeMind AI - Phase 1 MVP

Personal AI memory assistant that remembers where physical objects are located inside your home.

## Features
- **AI Memory Pipeline:** Natural language intent detection and entity extraction.
- **Hierarchical Locations:** Objects are stored in Room -> Furniture -> Container.
- **Mobile First:** React Native app for seamless interaction.
- **Clean Architecture:** Modular backend with provider abstraction for AI.
- **History Tracking:** Automatic logging of object movements and storage reasons.

## Tech Stack
- **Backend:** FastAPI, PostgreSQL (pgvector), Redis, SQLAlchemy, Google Gemini API (gemini-3.1-flash-lite)
- **Frontend:** React Native (Expo), TypeScript, React Query, Axios
- **Infrastructure:** Docker, Docker Compose

## AI Provider:
- **Google Gemini**
- **Development Model:** Gemini 3.1 Flash Lite

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Gemini API Key

### Installation & Setup
1. Clone the repository.
2. Create a `.env` file in the root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@db/homemind
   REDIS_URL=redis://redis:6379/0
   GEMINI_API_KEY=your_key_here
   AI_MODEL=gemini-3.1-flash-lite
   JWT_SECRET=your_secret_here
   ALGORITHM=HS256
   ```
3. Launch everything:
   ```bash
   docker compose up --build
   ```

## Development Workflow
- **Backend:** Located in `backend/app/`. Run tests with `pytest`.
- **Frontend:** Located in `frontend/mobile/`.
- **Database:** Migrations handled by Alembic in `backend/migrations/`.

## API Documentation
Once running, visit `http://localhost:8000/docs` for the interactive Swagger API documentation.

## Phase 2 Roadmap
- Voice conversations (STT/TTS)
- Camera scanning and Object Detection
- Indoor mapping
- Shared household support
