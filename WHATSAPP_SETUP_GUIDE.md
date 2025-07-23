# WhatsApp Integration Setup Guide for Chronicler of the Nile

## Overview

This guide provides step-by-step instructions for setting up WhatsApp integration with the Chronicler of the Nile application. The integration allows users to interact with the AI historian directly through WhatsApp messages, making Egyptian history accessible through one of the world's most popular messaging platforms.

## Prerequisites

Before setting up WhatsApp integration, ensure you have:

1. A Facebook Business Account
2. A WhatsApp Business Account
3. A verified phone number for WhatsApp Business
4. Access to Facebook Developer Console
5. A publicly accessible webhook URL (for production deployment)

## Step 1: Create a Facebook App

1. **Go to Facebook Developers Console**
   - Visit [https://developers.facebook.com/](https://developers.facebook.com/)
   - Log in with your Facebook account

2. **Create a New App**
   - Click "Create App"
   - Select "Business" as the app type
   - Fill in the app details:
     - App Name: "Chronicler of the Nile WhatsApp"
     - App Contact Email: Your email address
     - Business Account: Select your business account

3. **Add WhatsApp Product**
   - In your app dashboard, click "Add Product"
   - Find "WhatsApp" and click "Set Up"

## Step 2: Configure WhatsApp Business API

1. **Get Started with WhatsApp**
   - In the WhatsApp product section, you'll see the "Getting Started" page
   - Note down the following important values:
     - **App ID**: Found in app settings
     - **App Secret**: Found in app settings (keep this secure)
     - **Phone Number ID**: Provided in the WhatsApp setup
     - **Business Account ID**: Provided in the WhatsApp setup

2. **Generate Access Token**
   - In the WhatsApp setup page, you'll see a temporary access token
   - For production, you'll need to generate a permanent access token
   - Copy the access token (this will be your `WHATSAPP_ACCESS_TOKEN`)

3. **Add Phone Number**
   - Verify your phone number in the WhatsApp Business API setup
   - This number will be used to send messages from your application

## Step 3: Configure Webhook

1. **Set Webhook URL**
   - In the WhatsApp configuration, find the "Webhook" section
   - Set the webhook URL to: `https://your-domain.com/api/whatsapp/webhook`
   - Replace `your-domain.com` with your actual domain

2. **Set Verify Token**
   - Create a secure verify token (e.g., `chronicler_webhook_verify_2024`)
   - This will be your `WHATSAPP_VERIFY_TOKEN`

3. **Subscribe to Webhook Events**
   - Subscribe to the following webhook fields:
     - `messages`
     - `message_deliveries`
     - `message_reads`

## Step 4: Update Environment Variables

Add the following environment variables to your `.env` file in the backend directory:

```env
# Existing variables
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-here

# WhatsApp Integration
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=chronicler_webhook_verify_2024
WHATSAPP_APP_SECRET=your-app-secret
```

## Step 5: Install Dependencies

Install the required Python packages:

```bash
cd backend
pip install wikipedia python-dotenv
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Step 6: Deploy Your Application

For WhatsApp webhooks to work, your application must be publicly accessible. You have several options:

### Option A: Using ngrok (for testing)

1. Install ngrok: [https://ngrok.com/](https://ngrok.com/)
2. Run your Flask application locally:
   ```bash
   python src/main.py
   ```
3. In another terminal, expose your local server:
   ```bash
   ngrok http 5000
   ```
4. Use the ngrok HTTPS URL as your webhook URL in Facebook Developer Console

### Option B: Deploy to Production

Deploy your application to a cloud service like:
- Heroku
- AWS
- Google Cloud Platform
- DigitalOcean
- Any VPS with a domain name

## Step 7: Test the Integration

1. **Verify Webhook**
   - Facebook will send a verification request to your webhook
   - Check your application logs to ensure verification succeeds

2. **Send Test Message**
   - Send a message to your WhatsApp Business number
   - Check the application logs to see if the message is received
   - Verify that the AI responds correctly

3. **Test Different Languages**
   - Send messages in both English and Arabic
   - Verify that the AI responds in the same language

## Step 8: Production Considerations

### Security

1. **Webhook Signature Verification**
   - The application automatically verifies webhook signatures using `WHATSAPP_APP_SECRET`
   - Never expose your app secret in client-side code

2. **Rate Limiting**
   - Implement rate limiting to prevent abuse
   - WhatsApp has its own rate limits that you should respect

3. **Error Handling**
   - Monitor application logs for errors
   - Implement proper error responses for users

### Monitoring

1. **Logging**
   - The application includes comprehensive logging
   - Monitor logs for webhook delivery issues

2. **Database**
   - All WhatsApp conversations are stored in the database
   - Monitor database size and performance

3. **API Quotas**
   - Monitor your Gemini API usage
   - Monitor WhatsApp API quotas and billing

## API Endpoints

The WhatsApp integration adds the following endpoints:

### Webhook Endpoints

- `GET /api/whatsapp/webhook` - Webhook verification
- `POST /api/whatsapp/webhook` - Receive WhatsApp messages

### Management Endpoints

- `POST /api/whatsapp/send` - Send manual WhatsApp message (for testing)
- `GET /api/whatsapp/status` - Check WhatsApp integration status

### Example: Send Manual Message

```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "message": "Hello from Chronicler of the Nile!"
  }'
```

### Example: Check Status

```bash
curl http://localhost:5000/api/whatsapp/status
```

Response:
```json
{
  "whatsapp_token_configured": true,
  "phone_number_id_configured": true,
  "verify_token_configured": true,
  "app_secret_configured": true,
  "active_conversations": 5
}
```

## Troubleshooting

### Common Issues

1. **Webhook Verification Fails**
   - Check that `WHATSAPP_VERIFY_TOKEN` matches the token in Facebook Developer Console
   - Ensure your webhook URL is publicly accessible
   - Check application logs for error messages

2. **Messages Not Received**
   - Verify webhook subscription includes `messages` field
   - Check that your webhook URL is correct
   - Ensure your application is running and accessible

3. **Cannot Send Messages**
   - Verify `WHATSAPP_ACCESS_TOKEN` is correct and not expired
   - Check `WHATSAPP_PHONE_NUMBER_ID` is correct
   - Ensure the recipient number is in the correct format (+country_code_number)

4. **AI Not Responding**
   - Check `GEMINI_API_KEY` is configured correctly
   - Verify Wikipedia integration is working
   - Check application logs for AI generation errors

### Debug Mode

Enable debug logging by setting Flask debug mode:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Log Analysis

The application provides detailed logging for WhatsApp integration:

- `🔍` - Webhook verification
- `📨` - Message received
- `🔄` - Processing message
- `📱` - Message details
- `🌐` - Language detection
- `🤖` - AI response generation
- `✅` - Success operations
- `❌` - Error operations

## Features

### Automatic Language Detection

The system automatically detects whether messages are in Arabic or English and responds in the same language.

### Wikipedia Integration

All WhatsApp conversations benefit from enhanced Wikipedia context, providing richer and more accurate historical information.

### Conversation History

Each WhatsApp number maintains its own conversation history, allowing for contextual conversations across multiple messages.

### Database Storage

All WhatsApp conversations are stored in the database with the following additional fields:
- `platform`: Set to "whatsapp"
- `phone_number`: The sender's WhatsApp number
- `session_id`: Formatted as "whatsapp_{phone_number}"

## Limitations

1. **WhatsApp Business API Limits**
   - Free tier has limited message quotas
   - Some features require WhatsApp Business verification

2. **Message Types**
   - Currently supports text messages only
   - Media messages (images, documents) are not processed

3. **Group Messages**
   - The integration is designed for individual conversations
   - Group message handling would require additional development

## Next Steps

After successful setup, consider these enhancements:

1. **Rich Media Support**
   - Add support for sending images of historical artifacts
   - Handle document uploads for historical analysis

2. **Interactive Features**
   - Implement quick reply buttons
   - Add interactive message templates

3. **Analytics**
   - Track popular historical topics
   - Monitor user engagement metrics

4. **Multi-language Support**
   - Add support for more languages
   - Implement automatic translation features

## Support

For technical support or questions about the WhatsApp integration:

1. Check the application logs for detailed error messages
2. Verify all environment variables are correctly set
3. Test the webhook URL independently
4. Consult Facebook's WhatsApp Business API documentation

Remember that WhatsApp Business API is a production service with real costs and rate limits. Always test thoroughly in a development environment before deploying to production.

