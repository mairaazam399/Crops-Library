# Crops-Library

Scaffolded a mobile-first (React Native / Expo) client and a FastAPI backend stub on branch feature/mobile-fastapi-scaffold.

What's included:
- backend/: FastAPI app with /identify and /diagnose endpoints that accept image uploads and return deterministic stub responses.
- mobile/: Minimal Expo app (App.js) that lets you pick an image and upload it to the backend.

How I scaffolded this
- Created branch feature/mobile-fastapi-scaffold.
- Added backend and mobile scaffold files with run instructions.

Next suggested steps (I can do these):
- Integrate a real ML model for identification (TensorFlow/PyTorch) and wire it into /identify.
- Add authentication and a simple crops database (SQLite) with CRUD endpoints.
- Add CI (GitHub Actions) and Docker Compose to run mobile/backend together.

To run locally (backend):
- See backend/README.md

To run locally (mobile):
- See mobile/README.md

