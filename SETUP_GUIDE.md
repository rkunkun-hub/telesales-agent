# 🚀 IntelliTrac AI Telesales Agent - Setup & Integration Guide

## Daftar Isi
1. [Setup Lokal](#setup-lokal)
2. [Google Sheets Setup](#google-sheets-setup)
3. [Make.com Integration](#makecom-integration)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

---

## Setup Lokal

### 1. Clone/Extract Project
```bash
# Pindahkan ke folder project Anda
cd C:\Data\Me\Claude AI\learn-agents\telesales-agent

# Atau gunakan folder baru
mkdir telesales-agent
cd telesales-agent
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy template
copy .env.template .env

# Edit .env dengan nilai Anda
# - ANTHROPIC_API_KEY
# - GOOGLE_SHEETS_CREDENTIALS_PATH
```

### 5. Verify Installation
```bash
python 01_telesales_agent.py
```

Jika output menunjukkan test conversation dengan lead score, selamat! ✅

---

## Google Sheets Setup

### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Click "Select a Project" → "NEW PROJECT"
3. Name it: `IntelliTrac-Telesales`
4. Click "CREATE"

### Step 2: Enable Google Sheets API
1. In Google Cloud Console, search "Google Sheets API"
2. Click "ENABLE"
3. Wait a few seconds for activation

### Step 3: Create Service Account
1. Go to "Credentials" (left menu)
2. Click "CREATE CREDENTIALS" → "Service Account"
3. Fill in:
   - Service account name: `intellitrac-telesales`
   - Description: "AI Telesales Agent for WhatsApp"
4. Click "CREATE AND CONTINUE"
5. Skip optional steps, click "DONE"

### Step 4: Create JSON Key
1. In "Service Accounts", click the account you just created
2. Go to "KEYS" tab
3. Click "ADD KEY" → "Create new key" → "JSON"
4. JSON file will auto-download
5. **Save as `google-credentials.json` in your project folder**
6. Update `.env`:
   ```
   GOOGLE_SHEETS_CREDENTIALS_PATH=google-credentials.json
   ```

### Step 5: Share Sheet with Service Account
1. Create new Google Sheet: https://sheets.google.com
2. Name it: `IntelliTrac Leads`
3. Get the Service Account email from JSON file (key: `client_email`)
4. Share the sheet with this email
5. Grant "Editor" access

### Step 6: Initialize Sheet Structure (Optional)
```bash
# Run this to auto-create headers
python -c "from google_sheets_integration import create_sheets_template; create_sheets_template('google-credentials.json')"
```

---

## Make.com Integration

Make.com adalah platform no-code yang menghubungkan WhatsApp → FastAPI → Claude → Google Sheets.

### Prerequisites
- Make.com account (free tier OK)
- WhatsApp Business Account
- FastAPI server running (deployed di cloud)

### Step 1: Deploy FastAPI to Cloud

**Option A: Railway.app (Recommended - Easiest)**
```bash
# 1. Sign up di railway.app
# 2. Connect GitHub account
# 3. Fork/push project ke GitHub
# 4. Di Railway: New Project → Deploy from GitHub
# 5. Set environment variables:
#    - ANTHROPIC_API_KEY
#    - GOOGLE_SHEETS_CREDENTIALS_PATH (base64 encode the JSON)
# 6. Deploy

# FastAPI akan accessible di: https://your-app.railway.app
```

**Option B: Heroku**
```bash
# 1. Install Heroku CLI
# 2. heroku login
# 3. heroku create intellitrac-telesales
# 4. heroku config:set ANTHROPIC_API_KEY=xxx
# 5. git push heroku main
```

**Option C: Replit (Fastest for Testing)**
```
1. Go to replit.com
2. "Create Repl" → "Import from GitHub"
3. Paste this repo
4. Set secrets (ANTHROPIC_API_KEY, etc)
5. Click "Run"
```

### Step 2: Create Make.com Scenario

**Flow Overview:**
```
WhatsApp Message → Make Webhook → FastAPI → Claude → Google Sheets
                                      ↓
                          Make Webhook → WhatsApp Response
```

**Setup Steps:**

#### A. Create WhatsApp Trigger in Make
1. Open Make.com → Create New Scenario
2. Add Module: "WhatsApp Business" → "Webhooks" → "Instant"
3. Click "Save" (don't need to configure yet)

#### B. Add Custom Webhook Module (for testing)
1. Add new module: "Webhooks" → "Custom Webhook"
2. Set as trigger
3. Copy webhook URL (you'll use this later)

#### C. Add FastAPI Call
1. Add module: "HTTP" → "Make a request"
2. **Method:** POST
3. **URL:** `https://your-app.railway.app/webhook/whatsapp`
4. **Headers:**
   ```
   Content-Type: application/json
   Authorization: Bearer your_webhook_secret_token
   ```
5. **Body:**
   ```json
   {
     "from_number": "{{1.phone}}",
     "message_text": "{{1.text}}",
     "conversation_id": "{{1.id}}"
   }
   ```

#### D. Parse Response
1. Add module: "JSON" → "Parse JSON"
2. Map the response from FastAPI

#### E. Send WhatsApp Response Back
1. Add module: "WhatsApp Business" → "Send a Text Message"
2. **Recipient:** `{{4.to_number}}`
3. **Message:** `{{4.message}}`

#### F. Save to Google Sheets (Optional - Already done by FastAPI)
- Skipped karena FastAPI sudah save to Sheets

### Step 3: Test Make Scenario

```bash
# 1. Run FastAPI lokal dulu:
uvicorn 03_fastapi_webhook:app --reload --port 8000

# 2. Di Make, use ngrok untuk expose lokal server:
# Terminal: ngrok http 8000
# Dapatkan URL seperti: https://xxxx-xx-xxx-xx.ngrok.io

# 3. Update FastAPI URL di Make: https://xxxx-xx-xxx-xx.ngrok.io/webhook/whatsapp

# 4. Di Make, click "Test" button
# 5. Pilih WhatsApp message yang sebelumnya diterima
# 6. Lihat jika response berhasil
```

---

## Testing

### Test 1: Local Agent Test
```bash
python 01_telesales_agent.py
```
Expected: Shows conversation flow with lead score

### Test 2: Webhook Test
```bash
python -m pytest test_webhook.py -v
```

### Test 3: Google Sheets Connection
```bash
python -c "from google_sheets_integration import GoogleSheetsLeadStorage; gs = GoogleSheetsLeadStorage('google-credentials.json'); print('✅ Connected!')"
```

### Test 4: End-to-End dengan FastAPI
```bash
# Terminal 1: Start server
uvicorn 03_fastapi_webhook:app --reload

# Terminal 2: Test request
curl -X POST http://localhost:8000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from_number": "6281234567890",
    "message_text": "Halo, saya punya 15 truk pendingin"
  }'
```

---

## Deployment

### Production Checklist

- [ ] ANTHROPIC_API_KEY set di production environment
- [ ] Google credentials properly configured
- [ ] WhatsApp Business Account verified
- [ ] Make.com scenario tested and activated
- [ ] Error logging configured
- [ ] Rate limiting implemented
- [ ] Conversation storage (optional: upgrade to Redis)
- [ ] SSL/TLS enabled
- [ ] API monitoring setup

### Scale Considerations

**Current Setup Supports:**
- ~1000 concurrent conversations
- ~10,000 messages/day
- Cost: ~$0.30/day (Anthropic Haiku)

**For Higher Volume:**
- Switch to Haiku model (already configured)
- Add Redis for conversation storage
- Implement message queue (RabbitMQ/Kafka)
- Use database instead of memory for leads
- Add API Gateway for rate limiting

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"
**Solution:**
```bash
# 1. Check .env file exists
ls -la .env

# 2. Reload environment
deactivate
venv\Scripts\activate

# 3. Verify key
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Issue: "Google Sheets connection failed"
**Solution:**
```bash
# 1. Check credentials file
ls -la google-credentials.json

# 2. Verify permissions (sheet must be shared with service account email)

# 3. Test connection
python 02_google_sheets_integration.py
```

### Issue: Make webhook not receiving responses
**Solution:**
1. Check FastAPI is running: `curl http://localhost:8000/health`
2. Check Make webhook URL is correct
3. Look at Make execution history for errors
4. Verify JSON format in Make request body

### Issue: Claude returning empty responses
**Solution:**
1. Check API quota at https://console.anthropic.com/
2. Verify model name is correct: `claude-haiku-4-5-20251001`
3. Check message length (system prompt + history)

---

## File Structure

```
telesales-agent/
├── 01_telesales_agent.py          # Core agent logic
├── 02_google_sheets_integration.py # Sheets module
├── 03_fastapi_webhook.py          # Webhook server
├── requirements.txt               # Dependencies
├── .env.template                  # Environment template
├── .env                           # Your actual config
├── google-credentials.json        # Google auth (secret!)
├── test_webhook.py               # Tests
└── README.md                      # This file
```

---

## Next Steps

1. ✅ Setup lokal dan test agent
2. ✅ Deploy ke cloud (Railway/Heroku)
3. ✅ Setup Make.com scenario
4. ✅ Connect WhatsApp Business
5. ✅ Monitor leads di Google Sheets
6. ✅ Train sales team on lead qualification levels

---

## Support & Questions

Untuk questions atau issues:
1. Check Anthropic docs: https://docs.anthropic.com
2. Check Make docs: https://make.com/docs
3. Check WhatsApp API docs: https://developers.facebook.com/docs/whatsapp

Good luck! 🚀
