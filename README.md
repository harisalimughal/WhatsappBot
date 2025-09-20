# UnifonicBot - WhatsApp AI Assistant

A powerful WhatsApp bot with AI capabilities, file upload management, and admin dashboard.

## 🚀 Features

- **WhatsApp Integration** - Chat with customers via WhatsApp
- **AI-Powered Responses** - Uses OpenAI GPT for intelligent responses
- **File Upload System** - Company can upload training files
- **Admin Dashboard** - Manage files and monitor bot performance
- **Docker Support** - Easy deployment with Docker

## 🐳 Docker Deployment

### Local Development
```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t unifonicbot .
docker run -p 5000:5000 --env-file .env unifonicbot
```

### Production Deployment
1. **Build Docker image:**
   ```bash
   docker build -t unifonicbot .
   ```

2. **Push to registry:**
   ```bash
   docker tag unifonicbot your-registry/unifonicbot:latest
   docker push your-registry/unifonicbot:latest
   ```

3. **Deploy to Railway:**
   - Select "Deploy from Docker image"
   - Use your Docker image URL
   - Add environment variables

## 🔧 Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=mybot2024
FLASK_ENV=production
```

## 📱 Usage

1. **Admin Dashboard:** `https://your-app.com/admin`
2. **Customer Chat:** `https://your-app.com/`
3. **WhatsApp Webhook:** `https://your-app.com/whatsapp`

## 🛠️ Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Run with Docker
docker-compose up
```

## 📁 Project Structure

```
UnifonicBot/
├── app.py                 # Main Flask application
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Local Docker setup
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html       # Customer chat interface
│   └── admin.html       # Admin dashboard
└── uploads/             # File upload directory
```

## 🔒 Security

- Environment variables are not committed to git
- File uploads are validated
- WhatsApp webhook verification
- Production-ready configuration

## 📞 Support

For issues or questions, please check the deployment guide or contact support.
