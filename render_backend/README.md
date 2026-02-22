# Render Backend - Deploy Təlimatı

## Dəstəklənən formatlar
PDF, DOCX, PPTX, XLS, PNG, JPG, JPEG

## Render-də deploy

### 1. GitHub-a yüklə
git init
git add .
git commit -m "Initial commit"
git push

### 2. Render.com-da Web Service yarat
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Instance Type: Free

### 3. Deploy gözlə
3-5 dəqiqə

### İstifadə
Ana səhifə: https://your-app.onrender.com/
API: https://your-app.onrender.com/api/files
