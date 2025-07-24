# The Chronicler of the Nile: A Comprehensive Egyptian History AI

## Overview

The Chronicler of the Nile is a sophisticated conversational AI system designed to engage users in detailed discussions across the entire span of Egyptian history, from the Pharaonic era through the Roman, Islamic, Ottoman, and modern periods. This project demonstrates advanced prompt engineering, conversational memory management, robust handling of diverse user queries, WhatsApp integration, and dynamic Wikipedia content enhancement while providing accurate historical information, explanations of complex events, and contextual insights.

## Project Description

Egypt's history spans over 5,000 years, featuring pharaohs, conquerors, caliphs, sultans, and revolutionaries. The Chronicler of the Nile brings this vast narrative to life as a digital entity that users can consult for information, explanations, and contextual understanding of any period in Egyptian history. Now enhanced with WhatsApp integration and real-time Wikipedia content retrieval.

### Key Features

- **Multilingual Support**: Responds in the same language as the user's query (Arabic and English)
- **Comprehensive Historical Coverage**: Spans from Ancient Egypt to modern times
- **Conversational Memory**: Maintains context throughout sessions
- **Advanced AI Integration**: Powered by Google's Gemini API
- **WhatsApp Integration**: Direct messaging through WhatsApp Business API
- **Wikipedia Enhancement**: Real-time retrieval of relevant Wikipedia content
- **Responsive Web Interface**: Modern React frontend with mobile support
- **RESTful API**: Flask backend with well-structured endpoints
- **Historical Knowledge Base**: Structured JSON data covering all major periods

## New Features

### WhatsApp Integration
- **Direct Messaging**: Users can interact with the Chronicler directly through WhatsApp
- **Webhook Support**: Real-time message processing via WhatsApp Business API
- **Multi-platform Conversations**: Seamless experience across web and WhatsApp
- **Phone Number Management**: Individual conversation histories per WhatsApp number

### Wikipedia Enhancement
- **Dynamic Content Retrieval**: Real-time Wikipedia searches for enhanced responses
- **Egyptian History Filtering**: Intelligent filtering for Egypt-related content
- **Contextual Integration**: Wikipedia content seamlessly integrated into AI responses
- **Multi-language Support**: Wikipedia searches in both English and Arabic contexts

## Architecture

The system follows a modern full-stack architecture:

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite for conversation storage with WhatsApp support
- **AI Integration**: Google Gemini API for natural language processing
- **WhatsApp API**: Integration with WhatsApp Business Cloud API
- **Wikipedia API**: Dynamic content retrieval and enhancement
- **API Design**: RESTful endpoints for chat, history, knowledge access, and WhatsApp
- **CORS Support**: Enabled for frontend-backend communication

### Frontend (React)
- **Framework**: React with modern hooks
- **UI Library**: Shadcn/ui components with Tailwind CSS
- **State Management**: React hooks for local state
- **Responsive Design**: Mobile-first approach
- **Real-time Chat**: Interactive conversation interface

### Knowledge Base
- **Format**: Structured JSON files enhanced with Wikipedia integration
- **Coverage**: Four major historical periods plus real-time Wikipedia content
- **Content**: Detailed information on rulers, events, culture, and society
- **Accessibility**: API endpoints for programmatic access
- **Dynamic Enhancement**: Real-time Wikipedia content integration

## Historical Periods Covered

### 1. Ancient Egypt (c. 3100 BCE - 30 BCE)
- Early Dynastic Period
- Old Kingdom (Pyramid Age)
- Middle Kingdom
- New Kingdom (Egyptian Empire)
- Late Period
- Pharaohs, gods, monuments, and daily life

### 2. Graeco-Roman Egypt (332 BCE - 641 CE)
- Ptolemaic Dynasty
- Roman Province
- Alexandria as center of learning
- Rise of Christianity
- Intellectual achievements

### 3. Islamic and Ottoman Egypt (641 CE - 1805 CE)
- Arab Conquest
- Fatimid Caliphate
- Ayyubid Dynasty
- Mamluk Sultanate
- Ottoman Period
- Cultural and religious developments

### 4. Modern Egypt (1805 CE - Present)
- Muhammad Ali Dynasty
- British Occupation
- Independence and Revolution
- Nasser, Sadat, and Mubarak eras
- Arab Spring and contemporary Egypt

## Installation and Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- pnpm package manager
- Google Gemini API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
export SECRET_KEY="your-secret-key-here"
```

5. Run the Flask application:
```bash
python src/main.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm run dev
```

The frontend will be available at `http://localhost:5173`

## API Documentation

### Chat Endpoints

#### POST /api/chat
Send a message to the Chronicler and receive a response.

**Request Body:**
```json
{
  "message": "Tell me about the pyramids of Giza",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "The pyramids of Giza...",
  "session_id": "session_12345",
  "language": "en",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET /api/history/{session_id}
Retrieve conversation history for a specific session.

**Response:**
```json
{
  "session_id": "session_12345",
  "history": [
    {
      "user_message": "Tell me about the pyramids",
      "ai_response": "The pyramids of Giza...",
      "timestamp": "2024-01-01T12:00:00Z",
      "language": "en"
    }
  ]
}
```

#### GET /api/sessions
Get list of all conversation sessions.

**Response:**
```json
{
  "sessions": ["session_12345", "session_67890"]
}
```

### Knowledge Base Endpoints

#### GET /api/knowledge
Retrieve all historical knowledge.

**Response:**
```json
{
  "ancient_egypt": { ... },
  "graeco_roman": { ... },
  "islamic_ottoman": { ... },
  "modern_egypt": { ... }
}
```

#### GET /api/knowledge/{period}
Get knowledge for a specific historical period.

**Response:**
```json
{
  "period": "ancient_egypt",
  "data": { ... }
}
```

#### GET /api/knowledge/periods
Get list of available historical periods.

**Response:**
```json
{
  "periods": ["ancient_egypt", "graeco_roman", "islamic_ottoman", "modern_egypt"],
  "count": 4
}
```

## Usage Examples

### Basic Conversation
```
User: "Tell me about Cleopatra"
Chronicler: "Cleopatra VII Philopator (69-30 BCE) was the last active pharaoh of Ptolemaic Egypt..."
```

### Arabic Language Support
```
User: "أخبرني عن الأهرامات"
Chronicler: "أهرامات الجيزة هي من أعظم الإنجازات المعمارية في التاريخ القديم..."
```

### Cross-Period Context
```
User: "How did Islamic conquest change Egypt?"
Chronicler: "The Arab conquest of Egypt in 641 CE marked a fundamental transformation from the Graeco-Roman period..."
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### AI Model Parameters

The system uses the following Gemini API parameters:
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **Top P**: 0.8 (nucleus sampling)
- **Top K**: 40 (token selection)
- **Max Output Tokens**: 1024 (response length limit)

### Conversation Management

- **Max Conversation Tokens**: 4000 (context window management)
- **Max History Length**: 50 messages per session
- **Session Timeout**: No automatic timeout (persistent until cleared)

## Development

### Project Structure
```
chronicler_of_the_nile/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   └── conversation.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   └── knowledge.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── node_modules/
├── knowledge_base/
│   ├── ancient_egypt.json
│   ├── graeco_roman.json
│   ├── islamic_ottoman.json
│   └── modern_egypt.json
├── README.md
└── GHANGELOG.md
```

### Adding New Historical Periods

1. Create a new JSON file in `knowledge_base/`
2. Follow the existing structure with period, timeframe, overview, etc.
3. Update the knowledge route to include the new period
4. Test the API endpoints

### Extending AI Capabilities

1. Modify the prompt in `src/routes/chat.py`
2. Adjust Gemini API parameters in `src/config.py`
3. Update conversation memory management as needed
4. Test with various query types

## Testing

### Backend Testing
```bash
cd backend
source venv/bin/activate
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
pnpm test
```

### Integration Testing
1. Start both backend and frontend
2. Test conversation flow
3. Verify language detection
4. Check knowledge base access
5. Test session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- **Backend**: Follow PEP 8 for Python code
- **Frontend**: Use ESLint and Prettier for JavaScript/React
- **Documentation**: Update README and API docs for changes

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- Google Gemini API for natural language processing
- React and Flask communities for excellent frameworks
- Historical sources and academic research on Egyptian history
- Shadcn/ui for beautiful React components

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation and deployment guide



---

*The Chronicler of the Nile - Bringing Egyptian history to life through AI*

