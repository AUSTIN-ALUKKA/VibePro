## Corporate Voice-Verification Call Interceptor — Docker-first student demo

This prototype demonstrates a call-interceptor service for voice verification. It's designed to be fully portable and run using Docker and Docker Compose.

Demo in 15 minutes (mock-mode):

1. Copy example env: `cp .env.example .env` and optionally edit values.
2. Build & run the stack: `make up` (or `docker compose up --build`).
3. Wait for backend to become healthy (`docker compose ps` or `docker compose logs -f backend`).
4. Open docs: `http://localhost:8000/docs`.

If you want ngrok public URL (optional): set `NGROK_AUTH_TOKEN` in `.env` and run: `docker compose up ngrok` — or run ngrok locally and point to `http://localhost:8000`.

Testing:
- Run `make test` (this runs pytest inside the `tests` service against the `backend` service).

Enabling real providers:
- Set provider credentials (for example `AI_PROVIDER_API_KEY`, `TWILIO_AUTH_TOKEN`) in `.env` and restart: `make down && make up`.

Cleaning up:
- `make down` will stop containers and remove volumes (including dev DB).

Files of interest:
- `backend/` — FastAPI backend
- `scripts/seed_db.py` — idempotent seeding for mock enrollments
- `tests/` — pytest tests that run inside Docker
- `docker-compose.yml`, `Dockerfile`, `Makefile`, `.env.example`

Notes & design decisions:
- Default mode is `MOCK_MODE=true`. All external provider integrations are optional and mocked when credentials are missing.
- The backend enforces `MAX_CONCURRENT_CALLS` via an in-memory async semaphore. This state is not persisted across restarts; see `scripts/seed_db.py` and `backend/app/README` for more.
- Logging is JSON to stdout and optionally to a rotating file inside the container.

Have fun experimenting. See `CONTRIBUTING.md` for how to extend the prototype.
