# Chronicler of the Nile - WhatsApp Chatbot

A sophisticated AI chatbot that embodies the vast knowledge of Egyptian history, integrated with WhatsApp Cloud API and enhanced with Wikipedia search functionality.

## Features

- **WhatsApp Integration**: Responds to messages sent to your WhatsApp Business number
- **Wikipedia Enhancement**: Uses Wikipedia search chains to provide accurate historical information
- **Multi-language Support**: Supports both English and Arabic
- **Egyptian History Expertise**: Specialized knowledge spanning all periods of Egyptian history
- **Conversation Memory**: Maintains context across conversations

## Setup Instructions

### 1. WhatsApp Business API Setup

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app and add WhatsApp Business API
3. Get your credentials:
   - Access Token
   - Phone Number ID
   - Verify Token
   - App Secret

### 2. Environment Variables

Update the `.env` file with your credentials:

```
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_APP_SECRET=your_app_secret
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python src/main.py
```

### 4. Deployment Options

#### Option A: Render.com (Free)
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Use the provided `render.yaml` configuration
4. Deploy automatically

#### Option B: Docker
```bash
docker build -t chronicler-nile .
docker run -p 5000:5000 chronicler-nile
```

### 5. WhatsApp Webhook Configuration

1. Set your webhook URL to: `https://your-domain.com/whatsapp/webhook`
2. Use your verify token for webhook verification
3. Subscribe to message events

## API Endpoints

- `GET /whatsapp/webhook` - Webhook verification
- `POST /whatsapp/webhook` - Receive WhatsApp messages
- `POST /whatsapp/send` - Send messages (testing)
- `GET /whatsapp/status` - Check integration status
- `POST /chat` - Web chat interface
- `GET /history/<session_id>` - Get conversation history

## Usage

Once deployed and configured, users can:

1. Send messages to your WhatsApp Business number
2. Ask questions about Egyptian history in English or Arabic
3. Receive detailed, contextual responses enhanced with Wikipedia information

## Example Conversations

**English:**
- User: "Tell me about Cleopatra"
- Bot: Provides detailed information about Cleopatra with Wikipedia context

**Arabic:**
- User: "أخبرني عن الأهرامات"
- Bot: يقدم معلومات مفصلة عن الأهرامات مع السياق من ويكيبيديا

## Technical Details

- **Backend**: Flask with SQLAlchemy
- **AI Model**: Google Gemini 1.5 Flash
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Wikipedia Integration**: Custom search chains for contextual enhancement
- **Language Detection**: Automatic detection and response in user's language

## Support

For issues or questions, check the logs in your deployment platform or run locally for debugging.

