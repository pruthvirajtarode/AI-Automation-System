# 🚂 Railway Deployment Guide: Digital Dada Agent™

Follow these steps to deploy your **Digital Dada AI Operations Agent™** to Railway. This is faster and more flexible than Render.

## 1. Login to Railway
1. Go to [Railway.app](https://railway.app) and log in with your GitHub account.

## 2. Create the Database
1. Click **New Project** -> **Provision PostgreSQL**.
2. Railway will create a database in seconds.

## 3. Deploy the Backend (FastAPI)
1. In the same project, click **New** -> **GitHub Repo**.
2. Select your `AI-Automation-System` repository.
3. **Important Configuration**:
   - Go to the **Settings** tab of this new service.
   - Set **Service Name** to `digital-dada-backend`.
   - Set **Root Directory** to `backend`.
   - Railway will automatically detect the `requirements.txt` and `main:app`.
4. **Environment Variables**:
   - Go to the **Variables** tab.
   - Click **New Variable** -> **Reference Variable**.
   - Select your Postgres Database and choose `DATABASE_URL`.
   - Manually add `OPENAI_API_KEY` with your key.
   - Add `CORS_ORIGINS` = `["*"]`.

## 4. Deploy the Frontend (React)
1. Click **New** -> **GitHub Repo** again.
2. Select the same `AI-Automation-System` repository.
3. **Important Configuration**:
   - Go to the **Settings** tab.
   - Set **Service Name** to `digital-dada-frontend`.
   - Set **Root Directory** to `frontend`.
4. **Networking**:
   - Go to **Settings** -> **Networking**.
   - Click **Generate Domain** to get your public URL.
5. **Environment Variables**:
   - Add `REACT_APP_API_URL` = `https://your-backend-url.up.railway.app/api` (get this from the backend service networking tab).

## 5. Deployment is Live!
Railway will automatically build and deploy both services. You can monitor the logs in the **Deployments** tab of each service.

---
**Sir, Railway is much more powerful for this setup. You will not face the "one database" limit here.**
