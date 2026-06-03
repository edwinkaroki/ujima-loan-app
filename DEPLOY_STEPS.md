# Quick Deployment Guide for Ujima Loan App

Your repo: `https://github.com/edwinkaroki/ujima-loan-app.git`

## Quickest Path: Vercel (Frontend) + Render (Backend)

### Step 1: Deploy Frontend to Vercel
1. Go to [vercel.com](https://vercel.com) and log in with GitHub.
2. Click "New Project" → Import your repo `edwinkaroki/ujima-loan-app`.
3. Framework preset: "Other" (it's just HTML). Configure as needed.
4. Click "Deploy". Vercel will build and deploy `index.html` automatically.
5. **Note the Vercel URL** (e.g., `https://ujima-loan-app.vercel.app`).

### Step 2: Deploy Backend to Render
1. Go to [render.com](https://render.com) and log in with GitHub.
2. Click "New +" → "Web Service" → Connect your GitHub repo.
3. Fill in:
   - **Name**: `ujima-backend`
   - **Root Directory**: `backend/`
   - **Runtime**: Docker
   - **Branch**: `main`
4. Scroll down to **Environment** section and add:
   - `FRONTEND_ORIGIN` = `https://ujima-loan-app.vercel.app` (your Vercel domain)
   - `GEMINI_API_KEY` = (paste your API key, or leave blank for now)
5. Click "Create Web Service". Render will build the Docker image and deploy.
6. **Note the Render backend URL** (e.g., `https://ujima-backend.onrender.com`).

### Step 3: Update CORS on Backend (if needed)
If the frontend makes requests to a different domain, ensure `backend/main.py` allows it. In Render dashboard:
- Go to your backend service → Settings → Environment
- Ensure `FRONTEND_ORIGIN` is set to your Vercel domain.

### Done!
- Frontend accessible at Vercel domain (e.g., `https://ujima-loan-app.vercel.app`).
- Backend API at Render domain (e.g., `https://ujima-backend.onrender.com/api/process`).
- The frontend will call `/api/process` which is proxied by the frontend's reverse proxy layer or directly to the backend.

---

## Alternative: Netlify (Frontend) + Railway/Fly.io (Backend)

**Frontend on Netlify**:
1. Go to [netlify.com](https://netlify.com).
2. "Add new site" → Import from Git → select your repo.
3. Set build directory to `/` (root, since we have `index.html` in root).
4. Deploy.

**Backend on Railway or Fly**:
- Railway: Go to [railway.app](https://railway.app) → "New Project" → GitHub repo → select `backend/` folder → deploy.
- Fly: Go to [fly.io](https://fly.io) → `flyctl launch` from project root, configure `fly.toml`.

---

## Self-Hosted (VPS + Docker Compose)

If you have a VPS (DigitalOcean, AWS, Linode):

1. SSH into your server.
2. Clone the repo:
   ```bash
   git clone https://github.com/edwinkaroki/ujima-loan-app.git
   cd ujima-loan-app
   ```
3. Run with Docker Compose:
   ```bash
   docker compose up --build -d
   ```
4. Configure nginx/TLS on your server to expose port 80/443.

---

## GitHub Actions (Auto-Deploy)

You can trigger auto-deploys on push to `main` using `.github/workflows/deploy_render.yml`. To enable:

1. In GitHub repo → Settings → Secrets and variables → Actions.
2. Add secrets:
   - `RENDER_API_KEY`: Get from [render.com/account/api-tokens](https://render.com/account/api-tokens).
   - `RENDER_BACKEND_SERVICE_ID`: From Render service dashboard URL (look for `/srv/...`).
   - `RENDER_FRONTEND_SERVICE_ID`: Same as above.
3. On next push to `main`, the workflow will trigger Render deploys automatically.

---

## Troubleshooting

- **"Backend connection refused"**: Ensure `FRONTEND_ORIGIN` matches your frontend domain in the backend environment.
- **"CORS error"**: Update `FRONTEND_ORIGIN` in backend to allow frontend domain.
- **"Docker not found"**: Install Docker Desktop or use managed hosting (Render, Railway, etc.).
- **"Port 80 in use"**: Change `docker-compose.yml` port mapping (e.g., `8001:80`).

---

## Next Steps

1. ✅ Repo pushed to GitHub.
2. ⏭ Deploy frontend to Vercel (5 mins).
3. ⏭ Deploy backend to Render (5 mins).
4. ⏭ Test at your Vercel domain.
5. ⏭ Set up GitHub Actions for auto-deploy (optional).
