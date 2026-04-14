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

## Run Backend

```bash
pip install -r requirements.txt
cd services/api-gateway
python3 -m uvicorn main:app --reload --port 8000
```

## Run Frontend

```bash
cd apps/frontend
pnpm install
pnpm dev
```

## Notes

- Chat state is isolated per user and session.
- Main database file is `app.db` in the project root.
- Ollama is used dynamically; if unavailable, safe fallback replies are used.

## Developer Onboarding

See `docs/DEVELOPER_ONBOARDING.md` for a full engineer onboarding guide.
