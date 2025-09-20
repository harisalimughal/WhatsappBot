from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from datetime import datetime
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
# from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Print upload folder for debugging
print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# WhatsApp configuration
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

# Azure Blob Storage configuration (commented out)
# AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "unifonicbot-files")

# Initialize Azure Blob Storage client (commented out)
# blob_service_client = None
# if AZURE_STORAGE_CONNECTION_STRING:
#     try:
#         blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#         print("✅ Azure Blob Storage connected")
#     except Exception as e:
#         print(f"❌ Azure Blob Storage error: {e}")
#         blob_service_client = None
# else:
#     print("⚠️ Azure Blob Storage not configured - using local storage")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def upload_to_azure_blob(file_path, filename):
#     """Upload file to Azure Blob Storage"""
#     try:
#         if not blob_service_client:
#             return None, "Azure Blob Storage not configured"
#         
#         # Create container if it doesn't exist
#         container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
#         try:
#             container_client.create_container()
#         except:
#             pass  # Container already exists
#         
#         # Upload file
#         blob_client = blob_service_client.get_blob_client(
#             container=AZURE_CONTAINER_NAME, 
#             blob=filename
#         )
#         
#         with open(file_path, "rb") as data:
#             blob_client.upload_blob(data, overwrite=True)
#         
#         # Get the blob URL
#         blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{filename}"
#         return blob_url, "Success"
#     
#     except Exception as e:
#         return None, f"Azure upload error: {str(e)}"

def process_uploaded_file(file_path, file_type, filename):
    """Process uploaded file and extract basic info"""
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Simple local storage (Azure commented out)
        return f"File saved locally: {filename} ({file_size_mb} MB)"
    
    except Exception as e:
        return f"Error processing file: {str(e)}"

def send_whatsapp_message(phone_number, message):
    """Send message via WhatsApp API"""
    try:
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def chatbot(question, context=""):
    """Function for chatbot interaction"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot for Unifonic. Respond in a friendly and helpful manner."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """Main page with chat interface"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Admin dashboard for company file management"""
    return render_template('admin.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get bot response
        bot_response = chatbot(user_message)
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads from company"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file
            file_type = filename.rsplit('.', 1)[1].lower()
            content = process_uploaded_file(file_path, file_type, filename)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'content': content[:500] + '...' if len(content) > 500 else content
            })
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """WhatsApp webhook for receiving messages"""
    if request.method == 'GET':
        # WhatsApp verification
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        print(f"🔍 WhatsApp verification attempt - Token: {verify_token}")
        
        if verify_token == WHATSAPP_VERIFY_TOKEN:
            print("✅ WhatsApp webhook verified successfully!")
            return challenge
        else:
            print("❌ WhatsApp webhook verification failed!")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        try:
            data = request.get_json()
            print(f"📨 Received WhatsApp webhook: {json.dumps(data, indent=2)}")
            
            if data.get('object') == 'whatsapp_business_account':
                for entry in data.get('entry', []):
                    for change in entry.get('changes', []):
                        if change.get('field') == 'messages':
                            for message in change.get('value', {}).get('messages', []):
                                phone_number = message.get('from')
                                message_text = message.get('text', {}).get('body', '')
                                
                                print(f"💬 Message from {phone_number}: {message_text}")
                                
                                if message_text:
                                    # Get bot response
                                    print("🤖 Getting bot response...")
                                    bot_response = chatbot(message_text)
                                    print(f"🤖 Bot response: {bot_response}")
                                    
                                    # Send response back to WhatsApp
                                    print("📤 Sending response to WhatsApp...")
                                    result = send_whatsapp_message(phone_number, bot_response)
                                    print(f"📤 WhatsApp API result: {result}")
                                else:
                                    print("⚠️ No text message found")
            
            return jsonify({'status': 'success'})
        
        except Exception as e:
            print(f"❌ WhatsApp webhook error: {str(e)}")
            return jsonify({'error': str(e)}), 500

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp message (for testing)"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({'error': 'Phone number and message required'}), 400
        
        result = send_whatsapp_message(phone_number, message)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting UnifonicBot Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    
    # Run in production mode when deployed
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    # Use gunicorn in production, Flask dev server in development
    if os.environ.get('FLASK_ENV') == 'production':
        print("Running in production mode with gunicorn")
        # This will be handled by gunicorn command in Dockerfile
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("Running in development mode")
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
