from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import uuid
from datetime import datetime
from src.models.conversation import db, Conversation, ConversationHistory
from src.utils.wikipedia_search import wikipedia_searcher
import json

chat_bp = Blueprint("chat", __name__)

# Configure Gemini API
print(f" GEMINI_API_KEY from environment variables: {os.getenv("GEMINI_API_KEY")[:10] if os.getenv("GEMINI_API_KEY") else "Not found"}...")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Store conversation histories in memory (in production, use Redis or database)
conversation_sessions = {}

def get_chronicler_prompt():
    """Get the base prompt for the Chronicler of the Nile"""
    return """You are "The Chronicler of the Nile," a sophisticated AI embodying the vast knowledge of Egyptian history spanning millennia. You are an authoritative, knowledgeable, and objective historical expert who can discuss any period of Egyptian history with depth and nuance.\n\nYour knowledge encompasses:\n- Ancient Egypt: Pharaohs, gods, monuments, daily life, dynasties\n- Graeco-Roman Egypt: Ptolemaic dynasty, Roman rule, early Christianity\n- Islamic Egypt: Arab conquest, Fatimid, Ayyubid, Mamluk periods\n- Ottoman Egypt: Ottoman rule, cultural developments\n- Modern Egypt: Muhammad Ali dynasty, British occupation, 1952 Revolution, Nasser, Sadat, Mubarak, and significant events\n\nGuidelines for your responses:\n1. Maintain an authoritative yet accessible tone - knowledgeable but not overly archaic\n2. Provide factual accuracy and balanced perspectives where historical debate exists\n3. Offer explanations of causes, effects, social impacts, and cultural significance\n4. Draw connections across different periods when relevant\n5. Use the conversation history to provide contextual understanding\n6. If uncertain about specific details, acknowledge limitations gracefully\n7. Avoid speculation about future events or current political opinions\n8. Structure responses clearly with paragraphs, bullet points, or headings as appropriate\n\nRespond in the same language as the user's query. If the user asks in Arabic, respond in Arabic. If in English, respond in English. Maintain this language consistency throughout the conversation unless explicitly asked to switch."""

def detect_language(text):
    """Simple language detection - can be enhanced with proper language detection library"""
    # Check for Arabic characters
    arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
    if arabic_chars > len(text) * 0.3:  # If more than 30% Arabic characters
        return 'ar'
    return 'en'

def get_chronicler_response(user_message, conversation, language):
    """
    Generate a response from the Chronicler using Gemini AI with Wikipedia enhancement.\n    \n    Args:\n        user_message (str): User's message\n        conversation (ConversationHistory): Conversation history\n        language (str): Detected language\n        \n    Returns:\n        str: AI response\n    """
    print(f" Generating Chronicler response for: {user_message[:50]}...")
    
    # Get Wikipedia contextual information
    print(" Searching Wikipedia for additional context...")
    wikipedia_context = wikipedia_searcher.get_contextual_information(user_message, language)
    
    # Prepare context for AI
    context = conversation.get_context_for_ai()
    
    # Create the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prepare the full prompt with context and Wikipedia information
    full_prompt = get_chronicler_prompt()
    
    # Add Wikipedia context if available
    if wikipedia_context:
        full_prompt += f"\n\n{wikipedia_context}"
        print(" Wikipedia context added to prompt")
    
    if context:
        full_prompt += "\n\nConversation History:\n"
        for msg in context:
            role = "User" if msg['role'] == 'user' else "Chronicler"
            full_prompt += f"{role}: {msg['content']}\n"
    
    full_prompt += f"\nUser: {user_message}\nChronicler:"
    
    print(f" Full prompt length: {len(full_prompt)} characters")
    
    # Generate response
    print(" Generating AI response...")
    response = model.generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=1024,
        )
    )
    
    ai_response = response.text
    print(f" AI response generated: {len(ai_response)} characters")
    
    return ai_response

@chat_bp.route('/chat', methods=['POST'])
def chat():
    print("=== Starting chat request processing ===")
    try:
        print("1. Receiving data...")
        data = request.get_json()
        print(f"Received data: {data}")
        
        user_message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        print(f"2. User message: {user_message}")
        print(f"3. Session ID: {session_id}")
        
        if not user_message:
            print("Error: Empty message")
            return jsonify({'error': 'Message is required'}), 400
        
        # Detect language
        language = detect_language(user_message)
        print(f"4. Detected language: {language}")
        
        # Get or create conversation history for this session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = ConversationHistory()
            print(f"5. New conversation session created for {session_id}")
        else:
            print(f"5. Existing conversation session found for {session_id}")
        
        conversation = conversation_sessions[session_id]
        
        # Add user message to history
        conversation.add_message('user', user_message)
        print("6. Added user message to history")
        
        # Generate AI response with Wikipedia enhancement
        print("7. Generating AI response with Wikipedia context...")
        ai_response = get_chronicler_response(user_message, conversation, language)
        print(f"8. AI response: {ai_response[:100]}...")
        
        # Add AI response to history
        conversation.add_message('assistant', ai_response)
        print("9. Added AI response to history")
        
        # Save to database
        print("10. Saving to database...")
        conv_record = Conversation(
            session_id=session_id,
            user_message=user_message,
            ai_response=ai_response,
            language=language
        )
        db.session.add(conv_record)
        db.session.commit()
        print("11. Saved to database successfully")
        
        print("=== Chat request completed successfully ===")
        return jsonify({
            'response': ai_response,
            'session_id': session_id,
            'language': language,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        print(f" Error occurred in chat(): {str(e)}")
        print(f" Error type: {type(e).__name__}")
        import traceback
        print(f" Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    print(f"=== Starting get_history request for session: {session_id} ===")
    try:
        conversations = Conversation.query.filter_by(session_id=session_id).order_by(Conversation.timestamp).all()
        history = []
        
        for conv in conversations:
            history.append({
                'user_message': conv.user_message,
                'ai_response': conv.ai_response,
                'timestamp': conv.timestamp.isoformat(),
                'language': conv.language
            })
        print(f" Retrieved {len(history)} history records for session {session_id}")
        return jsonify({
            'session_id': session_id,
            'history': history
        })
        
    except Exception as e:
        print(f" Error occurred in get_history(): {str(e)}")
        print(f" Error type: {type(e).__name__}")
        import traceback
        print(f" Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/sessions', methods=['GET'])
def get_sessions():
    print("=== Starting get_sessions request ===")
    try:
        # Get unique session IDs from database
        sessions = db.session.query(Conversation.session_id).distinct().all()
        session_list = [session[0] for session in sessions]
        print(f" Retrieved {len(session_list)} unique sessions")
        return jsonify({
            'sessions': session_list
        })
        
    except Exception as e:
        print(f" Error occurred in get_sessions(): {str(e)}")
        print(f" Error type: {type(e).__name__}")
        import traceback
        print(f" Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500