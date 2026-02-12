# 🚀 Render Deployment Guide: Digital Dada Agent™

Follow these steps to get your **Digital Dada AI Operations Agent™** live for your client demo.

## 1. Prepare Your GitHub Repository
1. Create a new **Private** repository on GitHub.
2. Run these commands in your project root:
   ```bash
   git init
   git add .
   git commit -m "Initialize Digital Dada SaaS"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## 2. Deploy via Render Blueprint (Recommended)
1. Log in to [Render.com](https://render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file and show you the plan:
   - **Database**: digital-dada-db (PostgreSQL)
   - **Backend**: digital-dada-backend (FastAPI)
   - **Frontend**: digital-dada-frontend (React Static)
5. Click **Apply**.

## 3. Critical: Set Your API Keys
Once the deployment starts, you **must** manually add your API keys in the Render Dashboard:
1. Go to the `digital-dada-backend` service.
2. Go to **Environment**.
3. Add the following:
   - `OPENAI_API_KEY`: `your_key_here`
   - `TWILIO_ACCOUNT_SID`: `your_sid_here` (Optional for demo)
   - `TWILIO_AUTH_TOKEN`: `your_token_here` (Optional for demo)
   - `SENDGRID_API_KEY`: `your_key_here` (Optional for demo)

## 4. Final Verification
1. Wait for all 3 services to show a green **Live** status.
2. Open the **Frontend URL** (e.g., `https://digital-dada-frontend.onrender.com`).
3. Log in and test the AI response—it will now identify as **Digital Dada**.

---
**Sir, your system is now configured for a single-click deployment.** After you push to GitHub and click 'Apply' on Render, you will have a live URL to show your client.
