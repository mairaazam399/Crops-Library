Updated backend README: added DB and CRUD instructions.

Running the backend now will create a SQLite DB at backend/db/crops.db and seed it with sample crops on first startup.

Quick start (local):

1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r backend/requirements.txt
4. Run: uvicorn backend.app.main:app --reload --port 8000

Endpoints:
- POST /identify  (form multipart, field name `file`) -> returns stubbed species list
- POST /diagnose   (form multipart, field name `file`) -> returns stubbed disease label
- CRUD for crops:
  - GET /crops
  - POST /crops
  - GET /crops/{id}
  - PUT /crops/{id}
  - DELETE /crops/{id}

Notes:
- The current database is a local SQLite file. For production, switch the connection URL in backend/app/db.py to a managed RDS/Postgres instance.
- The app seeds three sample crops (Maize, Tomato, Wheat) if the table is empty on startup.
