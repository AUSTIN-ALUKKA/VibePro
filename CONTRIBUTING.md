Thanks for contributing!

This prototype is intended for educational use. If you want to add features or fix bugs:

1. Fork and open a PR.
2. Keep changes small and testable via Docker Compose.
3. Update tests in `tests/` and ensure `make test` passes.

Architecture notes:
- Keep the backend Dockerfile small & use Python 3.11-slim.
- Avoid embedding secrets in images; use environment variables.
