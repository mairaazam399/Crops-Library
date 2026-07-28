# Backend README

This is a minimal FastAPI backend for the Crops Library mobile demo.

Quick start (local):

1. Create a virtualenv: python -m venv .venv
2. Activate it: source .venv/bin/activate
3. Install deps: pip install -r backend/requirements.txt
4. Run: uvicorn backend.app.main:app --reload --port 8000

Endpoints:
- POST /identify  (form multipart, field name `file`) -> returns stubbed species list
- POST /diagnose   (form multipart, field name `file`) -> returns stubbed disease label

Notes:
- The current implementation is a deterministic stub for quick testing. Replace the stub logic in backend/app/main.py with actual model loading and inference.
