from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    platform = db.Column(db.String(20), default='web')  # 'web' or 'whatsapp'
    phone_number = db.Column(db.String(20), nullable=True)  # For WhatsApp integration
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_message': self.user_message,
            'ai_response': self.ai_response,
            'language': self.language,
            'platform': self.platform,
            'phone_number': self.phone_number,
            'timestamp': self.timestamp.isoformat()
        }

class ConversationHistory:
    def __init__(self):
        self.history = []
    
    def add_message(self, role, content):
        self.history.append({
            'role': role,
            'content': content
        })
    
    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []
    
    def get_context_for_ai(self, max_tokens=4000):
        """Get conversation history formatted for AI, with token management"""
        if not self.history:
            return []
        
        # Simple token estimation 
        total_tokens = 0
        context = []
        
        # Start from the most recent messages and work backwards
        for message in reversed(self.history):
            estimated_tokens = len(message['content']) // 4  # Rough estimation
            if total_tokens + estimated_tokens > max_tokens:
                break
            context.insert(0, message)
            total_tokens += estimated_tokens
        
        return context

