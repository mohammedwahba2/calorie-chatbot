# AI Nutrition Coach

Production-style AI nutrition coaching app built with FastAPI + Nuxt 3.

## What It Does

- JWT auth (`register` / `login`)
- AI chat coaching with Ollama (`llama3`/`mistral`)
- Arabic + English language-aware replies
- Persistent user profile memory
- Meal logging and progress tracking
- Dashboard + profile + meals + progress pages

## Tech Stack

- Backend: FastAPI, SQLAlchemy, JWT, Ollama API
- Frontend: Nuxt 3, Vue 3, Tailwind CSS
- DB: SQLite by default (`app.db` in project root)

## Requirements

Install these tools before running the project:

- Python `3.10+`
- Node.js `18+` (LTS recommended)
- `pnpm`
- Ollama

### Install Tooling (Windows - Recommended)

```bash
winget install Python.Python.3.11
winget install OpenJS.NodeJS.LTS
npm install -g pnpm
winget install Ollama.Ollama
```

If `winget` is not available, install manually:

- Python: https://www.python.org/downloads/windows/
- Node.js LTS: https://nodejs.org/
- Ollama: https://ollama.com/download/windows
- Then run: `npm install -g pnpm`

### Install Tooling (macOS)

```bash
brew install python node pnpm ollama
```

### Install Tooling (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm curl
sudo npm install -g pnpm
curl -fsSL https://ollama.com/install.sh | sh
```

## Backend Libraries

Backend Python dependencies are installed from `requirements.txt`:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `psycopg2-binary`
- `python-dotenv`
- `passlib[bcrypt]`
- `python-jose`
- `requests`
- `email-validator`
- `httpx`
- `pytest`

Install all backend libraries with (PowerShell or CMD):

```bash
pip install -r requirements.txt
```

## Frontend Libraries

Install frontend dependencies from `apps/frontend/package.json`:

```bash
cd apps/frontend
pnpm install
```

Main frontend packages include Nuxt, Vue, Vue Router, Tailwind CSS, PostCSS, and Autoprefixer.

## Ollama Model Download

Start Ollama and download a model:

```bash
ollama pull llama3
```

If Ollama app is already running on Windows, you can skip `ollama serve`.

You can also use `mistral` by changing `OLLAMA_MODEL` in `.env`.

## Project Structure

```text
calorie-chatbot/
├── app.db
├── .env
├── requirements.txt
├── services/
│   └── api-gateway/
│       ├── main.py
│       └── app/
│           ├── main.py
│           ├── models.py
│           ├── schemas.py
│           ├── core/
│           │   ├── config.py
│           │   ├── database.py
│           │   └── security.py
│           ├── routers/
│           │   ├── auth.py
│           │   ├── chat.py
│           │   ├── meals.py
│           │   ├── progress.py
│           │   └── profile.py
│           └── services/
│               ├── ai_service.py
│               ├── authz.py
│               ├── nutrition_service.py
│               └── session_store.py
└── apps/
    └── frontend/
        ├── nuxt.config.ts
        ├── postcss.config.js
        ├── tailwind.config.js
        └── app/
            ├── components/Chat/
            ├── composables/
            ├── layouts/
            └── pages/
```

## API Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /chat` (requires `Authorization: Bearer <token>`)
- `GET /me`
- `POST /meals/log`
- `GET /meals/log`
- `POST /progress`
- `GET /progress`
- `GET /health`

## Environment

Create `.env` in the root:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3
```

## Run Commands

### 1) Run Backend

```bash
pip install -r requirements.txt
cd services/api-gateway
python -m uvicorn main:app --reload --port 8000
```

### 2) Run Frontend

```bash
cd apps/frontend
pnpm install
pnpm dev
```

### 3) Access App

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

## Notes

- Chat state is isolated per user and session.
- Main database file is `app.db` in the project root.
- Ollama is used dynamically; if unavailable, safe fallback replies are used.

## Developer Onboarding

See `docs/DEVELOPER_ONBOARDING.md` for a full engineer onboarding guide.
