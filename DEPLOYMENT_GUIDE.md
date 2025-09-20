# UnifonicBot Deployment Guide

## 🚀 **Deploy to Railway (Recommended)**

### **Step 1: Prepare Your Code**
✅ All files are ready for deployment

### **Step 2: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub account

### **Step 3: Deploy Your App**
1. **Create new project** in Railway
2. **Connect GitHub repository** (or upload files)
3. **Railway will automatically detect** it's a Python app
4. **Add environment variables:**
   - `OPENAI_API_KEY` = your OpenAI key
   - `WHATSAPP_TOKEN` = your WhatsApp token
   - `WHATSAPP_PHONE_NUMBER_ID` = your phone number ID
   - `WHATSAPP_VERIFY_TOKEN` = mybot2024
   - `FLASK_ENV` = production

### **Step 4: Get Your Deployed URL**
Railway will give you a URL like:
```
https://unifonicbot-production.up.railway.app
```

### **Step 5: Update WhatsApp Webhook**
1. Go to WhatsApp dashboard
2. Update webhook URL to: `https://your-railway-url.railway.app/whatsapp`
3. Keep verify token: `mybot2024`

## 🌐 **Alternative: Deploy to Render**

### **Step 1: Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### **Step 2: Deploy**
1. **New Web Service**
2. **Connect GitHub repository**
3. **Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. **Add environment variables** (same as Railway)

## 🔧 **After Deployment:**

### **Your app will be available at:**
```
https://your-app-name.railway.app
```

### **Admin dashboard:**
```
https://your-app-name.railway.app/admin
```

### **WhatsApp webhook:**
```
https://your-app-name.railway.app/whatsapp
```

## ✅ **Benefits of Deployment:**

- ✅ **24/7 running** - No need to keep your computer on
- ✅ **Public URL** - Accessible from anywhere
- ✅ **Automatic restarts** - If app crashes, it restarts
- ✅ **HTTPS** - Secure connection for WhatsApp
- ✅ **No ngrok needed** - Direct public access

## 🧪 **Test After Deployment:**

1. **Visit your deployed URL**
2. **Test admin dashboard** - Upload files
3. **Test customer chat** - Send messages
4. **Test WhatsApp** - Send message to your WhatsApp number
5. **Update webhook** in WhatsApp dashboard

Your bot will now run 24/7 in the cloud! 🎉
