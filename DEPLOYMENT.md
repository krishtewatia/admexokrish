# Automated Lead Management & Email Tracking System — Deployment Guide

This guide details the step-by-step process of deploying the entire application stack: database on MongoDB Atlas, backend on Render, and frontend on Vercel.

---

## 1. Database Deployment (MongoDB Atlas)

MongoDB Atlas is a fully managed cloud database service. We will deploy a free M0 tier cluster.

### Step 1: Create an Account and Cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up/log in.
2. Click **Create** to create a new cluster.
3. Select the **M0 (Free)** tier.
4. Select a Cloud Provider (e.g., AWS, Google Cloud) and a region closest to your target audience.
5. Click **Create Deployment**.

### Step 2: Configure Database Access (User)
1. In the security section of the sidebar, go to **Database Access**.
2. Click **Add New Database User**.
3. Set the authentication method to **Password**.
4. Enter a username (e.g., `lead_user`) and a secure password. Keep these handy.
5. Set database user privileges to **Read and write to any database**.
6. Click **Add User**.

### Step 3: Configure Network Access (IP Access List)
Since Render backend services run on dynamic IPs, we need to allow access from any IP.
1. Go to **Network Access** in the sidebar.
2. Click **Add IP Address**.
3. Select **Allow Access From Anywhere** (this will add `0.0.0.0/0`).
4. Click **Confirm**.

### Step 4: Get Connection String
1. Go to the **Database** section (Clusters overview) under Deployment.
2. Click **Connect** on your cluster.
3. Choose **Drivers** (under "Connect to your application").
4. Copy the connection string. It will look like:
   `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`
5. Replace `<username>` and `<password>` with the credentials created in Step 2.
6. The name of the database is appended right before `?` or specified inside environment variables. (e.g., database name `adh_leads_db` -> `...mongodb.net/adh_leads_db?retryWrites=true...`).

---

## 2. Backend Deployment (Render)

Render is a unified platform to build and run apps. We will deploy the FastAPI backend.

### Step 1: Push Project to GitHub
1. Render deploys directly from a Git repository. Make sure the backend code is committed to a GitHub repository.

### Step 2: Create a Web Service
1. Sign in to [Render](https://render.com/).
2. Click **New** -> **Web Service**.
3. Connect your GitHub repository.
4. Configure the Web Service settings:
   - **Name**: `lead-management-api`
   - **Region**: Select the same region or nearest region to your MongoDB Atlas cluster.
   - **Runtime**: `Python 3` (Render supports Python standard versions).
   - **Build Command**: `pip install -r requirements.txt` (Make sure your current folder is set to `backend` or use Root Directory configuration: `backend`).
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
Go to the **Environment** tab of your service settings and add the following environment variables:

| Variable | Value | Description |
|---|---|---|
| `MONGODB_URI` | `mongodb+srv://lead_user:PASSWORD@cluster...` | From MongoDB Atlas Connection (Step 4 above) |
| `MONGODB_DB_NAME` | `adh_leads_db` | Name of the database to use |
| `BREVO_API_KEY` | `xkeysib-...` | Your Brevo API key for sending emails |
| `SENDER_EMAIL` | `sender@yourdomain.com` | Email address registered on Brevo as sender |
| `SENDER_NAME` | `Lead Team` | Display name of the email sender |
| `BACKEND_BASE_URL` | `https://your-render-url.onrender.com` | The public URL Render gives you (required for tracking links/pixels) |
| `OPENAI_API_KEY` | `sk-...` | (Optional) OpenAI API Key for lead classification |

### Step 4: Deploy
1. Click **Create Web Service**.
2. Once the deploy succeeds, copy your Web Service URL (e.g., `https://lead-management-api.onrender.com`). This will be used as the backend API URL.

---

## 3. Frontend Deployment (Vercel)

Vercel is optimized for frontend deployments. We will deploy the React/Vite app.

### Step 1: Prepare the Frontend config
Ensure you have the following file in `frontend/vercel.json` if you want clean client-side routing (fallback to `index.html`):
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Step 2: Import Project in Vercel
1. Go to [Vercel](https://vercel.com/) and sign up/log in.
2. Click **Add New...** -> **Project**.
3. Connect your GitHub account and import your repository.

### Step 3: Configure Build & Development Settings
If your repo has `frontend` in a subdirectory:
1. Set the **Root Directory** to `frontend`.
2. Vercel will automatically detect **Vite** as the framework.
3. Keep default Build Command (`npm run build`) and Output Directory (`dist`).

### Step 4: Configure Environment Variables
Expand the **Environment Variables** section and add:

| Key | Value | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `https://your-render-url.onrender.com` | The URL of your live Render backend (from Step 4 of Render guide) |

### Step 5: Deploy
1. Click **Deploy**.
2. Once complete, Vercel will provide a production URL (e.g., `https://your-project.vercel.app`).

---

## 4. Final verification and connection

1. Once the frontend is live, copy its Vercel URL (e.g., `https://your-project.vercel.app`).
2. Go back to **Render** -> **Web Service** -> **Environment** and add or update:
   - `CORS_ORIGINS`: `["https://your-project.vercel.app"]`
3. Render will redeploy automatically.
4. Try creating a lead using the Lead Capture Form on the frontend.
5. Check if the lead appears in your dashboard.
6. Verify that the welcome email is received, and when opened or clicked, the dashboard totals increment!
