# Deployment Instructions for Chronicler of the Nile

## Free Deployment Options (No Credit Card Required)

### Option 1: Render.com (Recommended)

1. **Create a GitHub Repository**
   - Upload your project to GitHub
   - Make sure all files are committed

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub (free)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python src/main.py`
     - **Environment**: Python 3
   - Add environment variables from your `.env` file

3. **Configure Webhook**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Set WhatsApp webhook to: `https://your-app-name.onrender.com/whatsapp/webhook`

### Option 2: Vercel (Alternative)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create vercel.json**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

### Option 3: PythonAnywhere (Free Tier)

1. **Sign up at pythonanywhere.com**
2. **Upload your files**
3. **Create a web app**
4. **Configure WSGI file**

### Option 4: Glitch.com

1. **Go to glitch.com**
2. **Import from GitHub**
3. **Add environment variables**
4. **Your app will be live automatically**

## WhatsApp Business API Configuration

### Step 1: Facebook Developer Account
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create a new app
3. Add "WhatsApp Business API" product

### Step 2: Get Credentials
- **Access Token**: From WhatsApp → API Setup
- **Phone Number ID**: From WhatsApp → API Setup  
- **Verify Token**: Create your own (use: `rahmaebrahimZC4`)
- **App Secret**: From App Settings → Basic

### Step 3: Configure Webhook
1. In WhatsApp → Configuration
2. Set Webhook URL: `https://your-deployed-app.com/whatsapp/webhook`
3. Set Verify Token: `rahmaebrahimZC4`
4. Subscribe to `messages` events

### Step 4: Add Phone Number
1. Go to WhatsApp → Phone Numbers
2. Add your phone number: `01031279115`
3. Verify the number

## Testing Your Deployment

1. **Check Status**
   ```bash
   curl https://your-app.com/whatsapp/status
   ```

2. **Test Webhook**
   ```bash
   curl -X GET "https://your-app.com/whatsapp/webhook?hub.mode=subscribe&hub.challenge=test&hub.verify_token=rahmaebrahimZC4"
   ```

3. **Send Test Message**
   Send a WhatsApp message to your business number and check for responses.

## Troubleshooting

### Common Issues:

1. **Webhook Verification Failed**
   - Check your verify token matches
   - Ensure your app is accessible publicly

2. **No Response to Messages**
   - Check your access token is valid
   - Verify phone number ID is correct
   - Check app logs for errors

3. **Database Errors**
   - Ensure `init_db.py` runs during deployment
   - Check database permissions

### Logs and Debugging:

- **Render**: Check logs in dashboard
- **Vercel**: Use `vercel logs`
- **Local**: Run `python src/main.py` and check console

## Security Notes

- Keep your tokens secure
- Use environment variables, never hardcode credentials
- Enable webhook signature verification in production
- Consider using HTTPS for all communications

## Scaling Considerations

- Free tiers have limitations (requests/month, uptime)
- For production use, consider paid plans
- Use PostgreSQL instead of SQLite for better performance
- Implement proper logging and monitoring

