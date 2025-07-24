
### Option 1: Render.com 

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

### Option 2: Vercel 

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

