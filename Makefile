.PHONY: up down test demo

up:
	docker compose up --build

down:
	docker compose down --volumes

test:
	docker compose run --rm tests

demo:
	@echo "Building and bringing up the stack (mock-mode)"
	@docker compose up --build -d backend
	@sleep 3
	@echo "Waiting for backend to become healthy..."
	@docker compose ps backend
	@echo "If you have NGROK_AUTHTOKEN set in .env, run: docker compose up ngrok" \
		|| true
	@echo "Tail backend logs: docker compose logs -f backend"
