# Crops Library

Live URL: (Replace this with the public frontend URL once deployed)


## 1) App name and purpose
Crops Library — an image-first crop identification and disease diagnosis app for farmers, agronomists and researchers. It helps non-experts identify plant species and common diseases from photos (leaf, stem, fruit) and provides concise, actionable next steps.

Who benefits
- Smallholder farmers who need fast guidance about crop problems.
- Extension agents & agronomists triaging field samples.
- Researchers and students who want a quick image-based lookup.

Real problem solved
- Reduces time and uncertainty when diagnosing crop problems from images by providing an AI-assisted identification and short practical recommendations.


## 2) Live deployed URL
You must deploy the backend and frontend and then paste the public frontend URL here. Make sure the URL is publicly accessible (open in an incognito window to verify). Example placeholder:

https://crops-library.example


## 3) Features
- Web frontend (Next.js): upload an image and receive species and disease predictions with confidence scores and recommended actions.
- Mobile demo (Expo): pick from gallery or take a photo, upload to backend, view results and browse built-in Crops library.
- Backend (FastAPI): endpoints:
  - POST /identify — image upload => AI-powered identification (OpenAI) or deterministic fallback when key is missing
  - POST /diagnose — stubbed disease diagnosis
  - CRUD endpoints for /crops (list, create, read, update, delete)
- AI-powered feature: multimodal image → reasoning using OpenAI (strict JSON output schema), with explanation and suggested actions.
- Dev-friendly: local SQLite fallback, Dockerfile for the backend, and a Next.js web app for grading accessibility.


## 4) The AI feature (exact system prompt and behavior)
The app uses OpenAI’s image-capable chat model (configured by the environment variable `OPENAI_MODEL`, default `gpt-4o-mini-vision`) to perform identification and diagnosis.

System prompt (exact text used by the backend — included verbatim):

```
You are an expert plant identification and disease diagnosis assistant for farmers and researchers.
Given a single image (provided as a base64 data URL), return a concise JSON object with the following schema:
{
  "predictions": [
    {"name": "Common or scientific name of species or disease", "type": "species|disease", "confidence": float (0-1) }
  ],
  "explanation": "short explanation of how you reached the conclusion",
  "suggested_actions": "practical next steps for the farmer/researcher"
}
Only output valid JSON. If you are uncertain, produce low confidence values and state uncertainty in the explanation.
Use no additional prose outside the JSON block. Keep responses compact.
```

How it works (backend flow)
- The frontend sends the uploaded image to the backend `/identify` endpoint as `multipart/form-data` (field `file`).
- If `OPENAI_API_KEY` is present in environment variables, the backend will base64-encode the image and send it to the OpenAI chat completions endpoint with the system prompt above.
- The model is required to return strict JSON. The backend parses this JSON and converts predictions into the response schema consumed by the frontend.
- If OpenAI fails (or no API key is set), the backend returns a deterministic fallback so the app remains usable for grading.

Example AI output (normalized into the API response):
```
{
  "predictions": [
    {"name": "Zea mays (Maize)", "type":"species", "confidence":0.87},
    {"name": "Northern leaf blight", "type":"disease", "confidence":0.12}
  ],
  "explanation":"Leaf lesions and long streaks consistent with northern leaf blight; overall leaf shape matches maize.",
  "suggested_actions":"Remove severely infected leaves, avoid overhead irrigation, and consult local extension for fungicide options. Collect sample if needed."
}
```


## 5) Tools, services and models used
- Backend: Python, FastAPI, Uvicorn, SQLModel (SQLite / Postgres-compatible)
- Frontend: Next.js (React)
- Mobile: Expo-managed React Native app (mobile/)
- AI: OpenAI (image-capable chat completion model, configured by `OPENAI_MODEL` env var)
- Optional: Hugging Face helper remains in repo if you prefer HF inference instead
- Hosting recommendations: Render (backend) and Vercel (frontend). Dockerfile included for backend.


## 6) Screenshots (add 3 or more)
Place screenshots in `docs/screenshots/` and name them `screenshot-1.png`, `screenshot-2.png`, `screenshot-3.png`. After you add real screenshots, replace the placeholder links below with the file paths.

- Screenshot 1: Upload screen and file chooser — docs/screenshots/screenshot-1.png
- Screenshot 2: Results view with predictions and explanation — docs/screenshots/screenshot-2.png
- Screenshot 3: Mobile app camera upload or crops list — docs/screenshots/screenshot-3.png

How to capture screenshots
- Web: open the deployed frontend or `http://localhost:3000` during local testing. Use your OS screenshot tool to capture pages and save into `docs/screenshots/`.


## 7) How to run the project locally (full commands)
Prerequisites:
- Git, Node.js (18+), npm, Python 3.11+, pip
- (Optional) Docker for containerized dev

A. Clone and switch to the working branch
```bash
git clone https://github.com/mairaazam399/Crops-Library.git
cd Crops-Library
git checkout feature/mobile-fastapi-scaffold
```

B. Backend (dev with SQLite fallback)
```bash
python3 -m venv .venv
source .venv/bin/activate     # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
# (Optional) set OPENAI_API_KEY to enable real AI calls
uvicorn backend.app.main:app --reload --port 8000
```
Open http://127.0.0.1:8000/docs to explore the API.

C. Web frontend (Next.js)
```bash
cd web
npm install
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 npm run dev
# Open http://localhost:3000 in a browser
```

D. Mobile (Expo) — optional
```bash
cd mobile
npm install
npx expo start
# Edit mobile/App.js BACKEND_URL to point at your backend (see file comment)
```


## 8) How to deploy (recommended providers)

A. Deploy backend to Render (quick)
1. Create a Render account and connect your GitHub repo.
2. New -> Web Service -> Select `mairaazam399/Crops-Library`, branch `feature/mobile-fastapi-scaffold`.
3. Choose the Dockerfile in `backend/Dockerfile` OR use the Python build/start commands:
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Create a managed Postgres on Render (optional but recommended) and copy the `DATABASE_URL`.
5. In your Render service settings, set the Environment Variables:
   - OPENAI_API_KEY = <your OpenAI key>
   - OPENAI_MODEL = (optional) e.g. `gpt-4o-mini-vision`
   - DATABASE_URL = <postgres url> (or omit to use SQLite fallback)
6. Deploy and wait. The service will have a public HTTPS URL (e.g., `https://your-backend.onrender.com`). Test the `/docs` endpoint.

B. Deploy frontend to Vercel (quick)
1. Create a Vercel account and connect your GitHub repo.
2. Create a new project and set the Root Directory to `/web`.
3. Add Environment Variable:
   - NEXT_PUBLIC_BACKEND_URL = https://<your-backend-url>
4. Deploy and fetch the public frontend URL (e.g., `https://crops-library.vercel.app`).
5. Open the URL to verify the upload flow.


## 9) Environment variables (summary)
- OPENAI_API_KEY — required for AI-powered identification (set on backend host). DO NOT commit.
- OPENAI_MODEL — optional (defaults to `gpt-4o-mini-vision` in code)
- DATABASE_URL — optional for production Postgres; if omitted, backend will use local SQLite file at `backend/db/crops.db`.
- NEXT_PUBLIC_BACKEND_URL — set on Vercel for the frontend to call the deployed backend.


## 10) API examples
List crops:
```
curl https://<your-backend>/crops
```
Identify an image (example):
```
curl -X POST "https://<your-backend>/identify" -F "file=@test.jpg"
```


## 11) Grading checklist (for you to verify before submission)
- [ ] Repo is public and the submitted link is accessible in an incognito window.
- [ ] Frontend is deployed and the public URL is working.
- [ ] README contains the AI system prompt (it does, above) and the live URL.
- [ ] At least 3 screenshots are present in `docs/screenshots/`.
- [ ] No API keys or secrets are committed.


## 12) Where I put important files in the repo
- backend/ — FastAPI backend and AI integration
- mobile/ — Expo app (mobile demo)
- web/ — Next.js frontend
- backend/AI_PROMPT.md — exact system prompt used by OpenAI
- .env.example — example environment file


## 13) Support & next steps I can do for you (optional)
If you want I can:
- Produce 3 real screenshots by running the deployed app and committing them to `docs/screenshots/` (I will need the live deployed URL and permission to use my hosting if you pick that option).
- Create a GitHub Actions workflow to run backend tests and optionally deploy to Render via CLI.
- Add CI/CD to auto-deploy both backend and frontend when you push to `main`.

If you want me to add the final README text above to the repo (I just did) and then prepare any additional polished assets or push screenshots, tell me which of the optional tasks you want.


---

If anything is unclear or you want me to proceed with deployment for you (I can deploy using my accounts and provide the live URLs), reply and I’ll continue. Otherwise, follow the deploy steps above and then paste the live frontend URL into this README where indicated so graders can access it.
