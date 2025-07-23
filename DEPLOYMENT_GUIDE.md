# Deployment Guide: The Chronicler of the Nile

## Overview

This comprehensive deployment guide covers multiple deployment scenarios for The Chronicler of the Nile application, from local development to production environments. The application consists of a Flask backend, React frontend, and requires external API access to Google Gemini.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Deployment](#local-development-deployment)
3. [Production Deployment Options](#production-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Security Considerations](#security-considerations)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)
10. [Backup and Recovery](#backup-and-recovery)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB available space
- Network: Stable internet connection for API calls

**Recommended Requirements:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 20GB+ SSD
- Network: High-speed internet connection

### Software Dependencies

**Backend Requirements:**
- Python 3.11 or higher
- pip package manager
- Virtual environment support

**Frontend Requirements:**
- Node.js 20.x or higher
- pnpm package manager (recommended) or npm

**External Services:**
- Google Gemini API key
- Domain name (for production)
- SSL certificate (for production)

### API Keys and Credentials

1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Store securely for environment configuration

2. **Secret Keys**
   - Generate a strong secret key for Flask sessions
   - Use tools like `python -c "import secrets; print(secrets.token_hex(32))"`

## Local Development Deployment

### Step 1: Clone and Setup Project

```bash
# Clone the project
git clone <repository-url>
cd chronicler_of_the_nile

# Verify project structure
ls -la
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 3: Environment Configuration

Create a `.env` file in the backend directory:

```bash
# backend/.env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 4: Database Initialization

```bash
# From backend directory with activated virtual environment
python src/main.py

# This will automatically create the SQLite database
# Check for database creation
ls src/database/
```

### Step 5: Frontend Setup

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Verify installation
pnpm list
```

### Step 6: Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python src/main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm run dev --host
```

### Step 7: Verify Local Deployment

1. **Backend Health Check:**
   - Visit `http://localhost:5000/api/knowledge/periods`
   - Should return JSON with available periods

2. **Frontend Access:**
   - Visit `http://localhost:5173`
   - Should display the Chronicler interface

3. **Full Integration Test:**
   - Send a test message through the interface
   - Verify AI response and conversation storage

## Production Deployment Options

### Option 1: Traditional VPS/Server Deployment

#### Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm nginx supervisor

# Install pnpm globally
sudo npm install -g pnpm

# Create application user
sudo useradd -m -s /bin/bash chronicler
sudo usermod -aG sudo chronicler
```

#### Application Deployment

```bash
# Switch to application user
sudo su - chronicler

# Clone application
git clone <repository-url> /home/chronicler/chronicler_of_the_nile
cd /home/chronicler/chronicler_of_the_nile

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Frontend build
cd ../frontend
pnpm install
pnpm run build
```

#### Environment Configuration

```bash
# Create production environment file
sudo nano /home/chronicler/chronicler_of_the_nile/backend/.env
```

```env
GEMINI_API_KEY=your_production_gemini_api_key
SECRET_KEY=your_production_secret_key
FLASK_ENV=production
DATABASE_URL=sqlite:////home/chronicler/chronicler_of_the_nile/backend/src/database/app.db
CORS_ORIGINS=https://yourdomain.com
```

#### Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/chronicler
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Frontend static files
    location / {
        root /home/chronicler/chronicler_of_the_nile/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API proxy to Flask backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/chronicler /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Supervisor Configuration

```bash
# Create supervisor configuration
sudo nano /etc/supervisor/conf.d/chronicler.conf
```

```ini
[program:chronicler]
command=/home/chronicler/chronicler_of_the_nile/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 src.main:app
directory=/home/chronicler/chronicler_of_the_nile/backend
user=chronicler
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/chronicler.log
environment=PATH="/home/chronicler/chronicler_of_the_nile/backend/venv/bin"
```

```bash
# Update supervisor and start service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start chronicler
```

### Option 2: Docker Deployment

#### Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY knowledge_base/ ./knowledge_base/

# Create database directory
RUN mkdir -p src/database

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "src/main.py"]
```

#### Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN npm install -g pnpm && pnpm install

# Copy source code
COPY . .

# Build application
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/src/database
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  data:
```

#### Docker Deployment Commands

```bash
# Create environment file
echo "GEMINI_API_KEY=your_api_key" > .env
echo "SECRET_KEY=your_secret_key" >> .env

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Cloud Platform Deployment

#### Heroku Deployment

**Backend (Heroku):**

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create chronicler-backend

# Set environment variables
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key
heroku config:set FLASK_ENV=production

# Create Procfile
echo "web: gunicorn src.main:app" > backend/Procfile

# Deploy
cd backend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a chronicler-backend
git push heroku main
```

**Frontend (Netlify/Vercel):**

```bash
# Build for production
cd frontend
pnpm run build

# Deploy to Netlify (using CLI)
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

#### AWS Deployment

**Using AWS Elastic Beanstalk:**

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
cd backend
eb init chronicler-backend

# Create environment
eb create production

# Set environment variables
eb setenv GEMINI_API_KEY=your_api_key SECRET_KEY=your_secret_key

# Deploy
eb deploy
```

## Environment Configuration

### Development Environment

```env
# backend/.env.development
GEMINI_API_KEY=your_development_api_key
SECRET_KEY=dev_secret_key_not_for_production
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
AI_TEMPERATURE=0.7
AI_TOP_P=0.8
AI_TOP_K=40
AI_MAX_OUTPUT_TOKENS=1024
MAX_CONVERSATION_TOKENS=4000
MAX_HISTORY_LENGTH=50
```

### Production Environment

```env
# backend/.env.production
GEMINI_API_KEY=your_production_api_key
SECRET_KEY=strong_production_secret_key_32_chars_min
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/chronicler_db
CORS_ORIGINS=https://yourdomain.com
AI_TEMPERATURE=0.7
AI_TOP_P=0.8
AI_TOP_K=40
AI_MAX_OUTPUT_TOKENS=1024
MAX_CONVERSATION_TOKENS=4000
MAX_HISTORY_LENGTH=50
```

### Environment Variable Security

1. **Never commit .env files to version control**
2. **Use environment-specific configurations**
3. **Rotate API keys regularly**
4. **Use secrets management services in production**

## Database Setup

### SQLite (Development)

SQLite is automatically configured for development:

```python
# Automatic database creation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
```

### PostgreSQL (Production)

For production, consider PostgreSQL:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE chronicler_db;
CREATE USER chronicler_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE chronicler_db TO chronicler_user;
\q

# Update environment configuration
DATABASE_URL=postgresql://chronicler_user:secure_password@localhost/chronicler_db
```

### Database Migration

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## Security Considerations

### API Security

1. **API Key Protection:**
   - Store in environment variables
   - Never expose in client-side code
   - Rotate regularly
   - Monitor usage

2. **Rate Limiting:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Chat endpoint implementation
    pass
```

3. **Input Validation:**
```python
from flask import request
from marshmallow import Schema, fields, ValidationError

class ChatSchema(Schema):
    message = fields.Str(required=True, validate=lambda x: len(x) <= 1000)
    session_id = fields.Str(validate=lambda x: len(x) <= 100)

@app.route('/api/chat', methods=['POST'])
def chat():
    schema = ChatSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
```

### HTTPS Configuration

1. **SSL Certificate:**
   - Use Let's Encrypt for free certificates
   - Configure automatic renewal
   - Implement HSTS headers

2. **Nginx SSL Configuration:**
```nginx
# Strong SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Application Security

1. **CORS Configuration:**
```python
from flask_cors import CORS

CORS(app, origins=['https://yourdomain.com'])
```

2. **Content Security Policy:**
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

## Monitoring and Maintenance

### Application Monitoring

1. **Health Check Endpoint:**
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })
```

2. **Logging Configuration:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/chronicler.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

3. **Performance Monitoring:**
```python
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        app.logger.info(f'{f.__name__} took {end_time - start_time:.2f} seconds')
        return result
    return decorated_function
```

### System Monitoring

1. **Server Monitoring:**
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

2. **Log Monitoring:**
```bash
# Monitor application logs
tail -f /var/log/chronicler.log

# Monitor Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Automated Backups

1. **Database Backup Script:**
```bash
#!/bin/bash
# backup_db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/chronicler/backups"
DB_PATH="/home/chronicler/chronicler_of_the_nile/backend/src/database/app.db"

mkdir -p $BACKUP_DIR
cp $DB_PATH $BACKUP_DIR/app_db_backup_$DATE.db

# Keep only last 30 backups
find $BACKUP_DIR -name "app_db_backup_*.db" -mtime +30 -delete
```

2. **Cron Job Setup:**
```bash
# Add to crontab
crontab -e

# Backup database daily at 2 AM
0 2 * * * /home/chronicler/scripts/backup_db.sh
```

## Troubleshooting

### Common Issues

1. **API Key Issues:**
```bash
# Check environment variables
echo $GEMINI_API_KEY

# Test API key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
     https://generativelanguage.googleapis.com/v1/models
```

2. **Database Connection Issues:**
```python
# Test database connection
from src.models.conversation import db
try:
    db.create_all()
    print("Database connection successful")
except Exception as e:
    print(f"Database error: {e}")
```

3. **CORS Issues:**
```javascript
// Check browser console for CORS errors
// Verify CORS_ORIGINS environment variable
// Test with curl:
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://localhost:5000/api/chat
```

### Debug Mode

1. **Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Frontend Debug:**
```javascript
// Add to React component
console.log('API Response:', response);
console.log('Current State:', state);
```

### Performance Issues

1. **Database Query Optimization:**
```python
# Add database indexes
class Conversation(db.Model):
    session_id = db.Column(db.String(100), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

2. **API Response Caching:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/knowledge')
@cache.cached(timeout=3600)  # Cache for 1 hour
def get_knowledge():
    return jsonify(load_knowledge_base())
```

## Performance Optimization

### Backend Optimization

1. **Gunicorn Configuration:**
```python
# gunicorn.conf.py
bind = "127.0.0.1:5000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

2. **Database Connection Pooling:**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```

### Frontend Optimization

1. **Build Optimization:**
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@/components/ui']
        }
      }
    }
  }
}
```

2. **Code Splitting:**
```javascript
// Lazy load components
const ChatInterface = lazy(() => import('./components/ChatInterface'));
```

### Nginx Optimization

```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Backup and Recovery

### Backup Strategy

1. **Database Backups:**
   - Daily automated backups
   - Weekly full system backups
   - Monthly off-site backups

2. **Application Code:**
   - Version control (Git)
   - Tagged releases
   - Configuration backups

3. **SSL Certificates:**
   - Certificate backup
   - Private key backup
   - Renewal automation

### Recovery Procedures

1. **Database Recovery:**
```bash
# Stop application
sudo supervisorctl stop chronicler

# Restore database
cp /home/chronicler/backups/app_db_backup_YYYYMMDD.db \
   /home/chronicler/chronicler_of_the_nile/backend/src/database/app.db

# Start application
sudo supervisorctl start chronicler
```

2. **Full System Recovery:**
```bash
# Restore from backup
tar -xzf system_backup_YYYYMMDD.tar.gz -C /

# Restore permissions
chown -R chronicler:chronicler /home/chronicler/chronicler_of_the_nile

# Restart services
sudo systemctl restart nginx
sudo supervisorctl restart chronicler
```

## Conclusion

This deployment guide provides comprehensive instructions for deploying The Chronicler of the Nile in various environments. Choose the deployment method that best fits your requirements:

- **Local Development**: Use the simple setup for development and testing
- **VPS/Server**: Use traditional server deployment for full control
- **Docker**: Use containerization for consistency and scalability
- **Cloud Platforms**: Use managed services for ease of maintenance

Remember to:
- Secure your API keys and environment variables
- Implement proper monitoring and logging
- Set up automated backups
- Keep your system updated
- Monitor performance and optimize as needed

For additional support or questions, refer to the main README.md file or contact the development team.

---

*Last updated: January 2024*
*Version: 1.0.0*

