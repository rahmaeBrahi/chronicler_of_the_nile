from flask import Blueprint, request, jsonify
import os
import requests
import hmac
import hashlib
from datetime import datetime
from src.models.conversation import db, Conversation, ConversationHistory
from src.routes.chat import get_chronicler_response, detect_language
import uuid

whatsapp_bp = Blueprint("whatsapp", __name__)

# WhatsApp Cloud API configuration
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")  
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")  
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN") 
WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET")  
# Store conversation histories for WhatsApp sessions
whatsapp_conversations = {}

def verify_webhook_signature(payload, signature):
    """Verify the webhook signature from WhatsApp"""
    # For local testing without a domain, we will bypass signature verification.
    # In a production environment, this MUST be enabled and properly configured.
    print(" Webhook signature verification bypassed for local testing.")
    return True

def send_whatsapp_message(phone_number, message):
    """Send a message via WhatsApp Cloud API"""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID or WHATSAPP_TOKEN == "YOUR_WHATSAPP_ACCESS_TOKEN" or WHATSAPP_PHONE_NUMBER_ID == "YOUR_WHATSAPP_PHONE_NUMBER_ID":
        print(" WhatsApp credentials not configured or are default placeholders. Please set WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID.")
        return False
    
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers )
        response.raise_for_status()
        print(f" Message sent to {phone_number}")
        return True
    except requests.exceptions.RequestException as e:
        print(f" Failed to send WhatsApp message: {e}")
        return False

@whatsapp_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    """Verify webhook endpoint for WhatsApp"""
    print(" WhatsApp webhook verification request received")
    
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    print(f"Mode: {mode}, Token: {token}, Challenge: {challenge}")
    
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        print(" Webhook verified successfully.")
        return challenge, 200
    else:
        print(" Webhook verification failed. Invalid mode or token.")
        return "Verification failed", 403

@whatsapp_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle incoming WhatsApp messages"""
    print(" WhatsApp webhook message received")
    
    try:
        # Verify signature (bypassed for local testing)
        signature = request.headers.get("X-Hub-Signature-256")
        if signature and not verify_webhook_signature(request.data, signature):
            print(" Invalid webhook signature")
            return "Invalid signature", 403
        
        data = request.get_json()
        print(f" Webhook data: {data}")
        
        # Process webhook data
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        process_message(change.get("value", {}))
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f" Error processing webhook: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

def process_message(message_data):
    """Process incoming WhatsApp message"""
    print(f" Processing message data: {message_data}")
    
    try:
        messages = message_data.get("messages", [])
        
        for message in messages:
            if message.get("type") != "text":
                print(f" Skipping non-text message: {message.get("type")}")
                continue
            
            # Extract message details
            from_number = message.get("from")
            message_id = message.get("id")
            text_body = message.get("text", {}).get("body", "")
            timestamp = message.get("timestamp")
            
            print(f" Message from {from_number}: {text_body}")
            
            if not text_body:
                print(" Empty message body, skipping")
                continue
            
            # Generate session ID for this phone number
            session_id = f"whatsapp_{from_number}"
            
            # Get or create conversation history
            if session_id not in whatsapp_conversations:
                whatsapp_conversations[session_id] = ConversationHistory()
            
            conversation = whatsapp_conversations[session_id]
            
            # Detect language
            language = detect_language(text_body)
            print(f" Detected language: {language}")
            
            # Add user message to history
            conversation.add_message("user", text_body)
            
            # Get AI response using the same logic as web chat
            ai_response = get_chronicler_response(text_body, conversation, language)
            
            # Add AI response to history
            conversation.add_message("assistant", ai_response)
            
            # Send response back via WhatsApp
            if send_whatsapp_message(from_number, ai_response):
                print(f" Response sent to {from_number}")
            else:
                print(f" Failed to send response to {from_number}")
            
            # Save to database
            try:
                conv_record = Conversation(
                    session_id=session_id,
                    user_message=text_body,
                    ai_response=ai_response,
                    language=language,
                    platform="whatsapp",
                    phone_number=from_number
                )
                db.session.add(conv_record)
                db.session.commit()
                print(" Conversation saved to database")
            except Exception as db_error:
                print(f" Database error: {db_error}")
                db.session.rollback()
    
    except Exception as e:
        print(f" Error processing message: {str(e)}")
        import traceback
        print(f" Traceback: {traceback.format_exc()}")

@whatsapp_bp.route("/send", methods=["POST"])
def send_message():
    """Manual endpoint to send WhatsApp messages (for testing)"""
    try:
        data = request.get_json()
        phone_number = data.get("phone_number")
        message = data.get("message")
        
        if not phone_number or not message:
            return jsonify({"error": "phone_number and message are required"}), 400
        
        success = send_whatsapp_message(phone_number, message)
        
        if success:
            return jsonify({"status": "Message sent successfully"})
        else:
            return jsonify({"error": "Failed to send message"}), 500
            
    except Exception as e:
        print(f" Error in send_message: {str(e)}")
        return jsonify({"error": str(e)}), 500

@whatsapp_bp.route("/status", methods=["GET"])
def whatsapp_status():
    """Check WhatsApp integration status"""
    status = {
        "whatsapp_token_configured": bool(WHATSAPP_TOKEN) and WHATSAPP_TOKEN != "YOUR_WHATSAPP_ACCESS_TOKEN",
        "phone_number_id_configured": bool(WHATSAPP_PHONE_NUMBER_ID) and WHATSAPP_PHONE_NUMBER_ID != "YOUR_WHATSAPP_PHONE_NUMBER_ID",
        "verify_token_configured": bool(WHATSAPP_VERIFY_TOKEN) and WHATSAPP_VERIFY_TOKEN != "YOUR_WHATSAPP_VERIFY_TOKEN",
        "app_secret_configured": bool(WHATSAPP_APP_SECRET) and WHATSAPP_APP_SECRET != "YOUR_WHATSAPP_APP_SECRET",
        "active_conversations": len(whatsapp_conversations)
    }
    
    return jsonify(status)
