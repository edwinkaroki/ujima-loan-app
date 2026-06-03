Hosting & Deployment Guide

Overview
- The project has a static frontend (`index.html`) and a FastAPI backend in `backend/main.py`.
- You can host the frontend as a static site (Vercel, Netlify, Render Static) and the backend as a Docker web service (Render, Fly, Railway), or run both behind an nginx reverse proxy using Docker Compose.

Render (recommended quick path)
1. In Render, create a new Static Site service for the frontend, point to the repo root and set `publishPath` to `/`.
2. Create a new Web Service for the backend using the Dockerfile at `backend/Dockerfile` (env: Docker).
3. Add the following environment secrets in Render for the backend:
   - `GEMINI_API_KEY` (Secret)
   - `FRONTEND_ORIGIN` (e.g. https://your-domain.com)
4. Set `FRONTEND_ORIGIN` in `backend` to your production domain.
5. If you use a custom domain, configure DNS and enable TLS in Render.

Vercel + Render (alternate)
- Deploy frontend to Vercel by connecting your GitHub repo; it will serve `index.html`.
- Deploy backend to Render as above.
- Set `FRONTEND_ORIGIN` on the backend to your Vercel domain.

Vercel-specific steps
1. Add `vercel.json` (provided) to the repo root to declare a static build for `index.html`.
2. Connect your GitHub repo to Vercel and import the project — Vercel will auto-deploy on push to `main`.
3. Configure a custom domain in Vercel if desired; Vercel manages TLS automatically.
4. Point the backend `FRONTEND_ORIGIN` to the Vercel domain (for example `https://your-app.vercel.app`) in Render environment variables.

Notes on routing
- When using Vercel for frontend and Render for backend, the frontend will call the public backend endpoint (for example `https://api.yourdomain.com/api/process`). Ensure CORS on the backend allows your frontend domain.
- Alternatively, host both frontend and backend behind a single nginx reverse proxy (Docker Compose example) so the frontend can use relative API paths (`/api/process`).

Self-hosted with Docker + nginx
- Use `docker-compose.yml` (provided) to run `backend` and `web` (nginx). nginx serves `index.html` and proxies `/api/` to `backend`.
- In production, run behind a reverse proxy with TLS (nginx + Certbot) and ensure `FRONTEND_ORIGIN` matches your domain.

GitHub Actions (Render auto-deploy trigger)
- You can trigger Render deploys from a workflow using Render API. Use the template `.github/workflows/deploy_render.yml` and set secrets:
  - `RENDER_API_KEY`
  - `RENDER_BACKEND_SERVICE_ID`
  - `RENDER_FRONTEND_SERVICE_ID`

Security & Good Practices
- Never commit `.env` or secrets.
- Store API keys in the host's secret manager (Render environment secrets, Vercel env vars).
- Limit CORS to your frontend domain in `backend/main.py`.

Need help applying these to your Render account or setting up CI? I can:
- Fill `render.yaml` with your repo URL and apply it (if you give repo URL),
- Create the GitHub Actions workflow file to trigger Render deploys (requires adding secrets in GitHub), or
- Run `docker compose up --build` here if Docker is available to test locally.
