# 🚀 Standalone Deployment Guide (GitHub Pages)

This repository contains the standalone personal portfolio and research web application for **Reyhane Javidi Alsaadi**.

---

## 🛠️ Local Development & Build

```bash
# 1. Install dependencies
npm install

# 2. Run local development server
npm run dev
# Open http://localhost:3000

# 3. Test static production export
npm run build
```

---

## 🌐 Deploying to GitHub Pages (Step-by-Step)

### Step 1: Create a GitHub Repository
1. In Reyhane's GitHub account ([github.com/reyhane-code](https://github.com/reyhane-code)), create a new public repository.
2. **Recommended Name:** `reyhane-code.github.io`
   *(Using this exact name deploys your website directly to `https://reyhane-code.github.io/` without any subfolder).*

### Step 2: Push this repository
Open terminal inside this project folder:
```bash
git init
git branch -M main
git add .
git commit -m "feat: initial release of academic portfolio and research website"
git remote add origin https://github.com/reyhane-code/reyhane-code.github.io.git
git push -u origin main
```

### Step 3: Enable GitHub Pages Action
1. Go to repository **Settings** -> **Pages**.
2. Under **Build and deployment** -> **Source**, select **GitHub Actions**.
3. Done! The workflow `.github/workflows/deploy.yml` will automatically build and publish the site.

