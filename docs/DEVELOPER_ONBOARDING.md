# Developer Onboarding

This guide helps new engineers run and understand the AI Nutrition Coach quickly.

## 1) What this project is

AI Nutrition Coach app with:
- chat-based coaching (Arabic + English)
- auth (JWT)
- meal logging
- progress tracking
- session-based chat history

## 2) Tech stack

- Backend: FastAPI + SQLAlchemy
- Frontend: Nuxt 3 + Tailwind CSS
- AI: Ollama local models (`llama3` / `mistral`)
- DB: SQLite by default (`app.db` in project root)

## 3) Repo layout (important)

```text
services/api-gateway/
  main.py
  app/
    main.py
    core/
    models.py
    schemas.py
    routers/
    services/

apps/frontend/
  nuxt.config.ts
  app/
    pages/
    components/
    composables/
```

## 4) Environment setup

Create `.env` in root:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3
```

## 5) Install dependencies

Backend:

```bash
pip install -r requirements.txt
```

Frontend:

```bash
cd apps/frontend
pnpm install
```

## 6) Run locally

### Start backend

```bash
cd services/api-gateway
python3 -m uvicorn main:app --reload --port 8000
```

### Start frontend

```bash
cd apps/frontend
pnpm dev
```

### Start Ollama (if not already running)

```bash
ollama serve
ollama run llama3
```

## 7) Main API endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Chat
- `POST /chat`
- `GET /chat/sessions`
- `POST /chat/sessions`
- `GET /chat/history/{session_id}`

### User/Profile
- `GET /me`

### Meals
- `POST /meals/log`
- `GET /meals/log`

### Progress
- `POST /progress`
- `GET /progress`

## 8) Typical chat lifecycle

1. User logs in and gets JWT.
2. Frontend stores token in localStorage.
3. User opens chat page.
4. Frontend loads session list and chat history.
5. Sending message calls `POST /chat` with `session_id`.
6. Backend saves messages and updates profile memory.
7. Frontend renders response and keeps session continuity.

## 9) Frontend behavior notes

- Chat supports session switch + new chat creation.
- New chat creates session row immediately (`POST /chat/sessions`).
- Message history reloads automatically on session change.
- Language direction (`rtl`/`ltr`) is inferred from text.

## 10) Backend behavior notes

- Router organization:
  - `routers/auth.py`
  - `routers/chat.py`
  - `routers/meals.py`
  - `routers/progress.py`
  - `routers/profile.py`
- DB models are in `app/models.py`.
- AI orchestration is in `services/ai_service.py`.
- Session runtime memory uses key: `user_id:session_id`.

## 11) Troubleshooting

### Frontend shows no styles
- check `tailwind.config.js` content paths
- check `postcss.config.js`
- restart `pnpm dev`

### Auth works but chat fails with 401
- verify `Authorization: Bearer <token>` is being sent
- clear localStorage and login again

### History not loading
- check `GET /chat/history/{session_id}` response in browser network tab
- ensure selected session belongs to current logged-in user

### AI responses fallback too often
- verify Ollama server is up on `OLLAMA_URL`
- verify selected model exists (`ollama list`)

## 12) Recommended next engineering tasks

- add Alembic migrations
- add Docker Compose (frontend + api + ollama)
- add structured logging + request IDs
- add automated tests for chat sessions + pagination + auth guards
