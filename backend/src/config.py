import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS')  
    
    # AI Model settings
    AI_MODEL_NAME = 'gemini-pro'
    AI_TEMPERATURE = 0.7
    AI_TOP_P = 0.8
    AI_TOP_K = 40
    AI_MAX_OUTPUT_TOKENS = 1024
    
    # Conversation settings
    MAX_CONVERSATION_TOKENS = 4000
    MAX_HISTORY_LENGTH = 50

