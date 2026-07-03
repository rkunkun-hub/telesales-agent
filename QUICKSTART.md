# 🚀 Quick Start Guide - IntelliTrac Telesales Agent V1.1

**Updated Version with General Purpose Lead Qualification**

---

## ⚡ 5-Minute Quick Start

### Step 1: Download & Setup
```bash
# Create folder
mkdir telesales-agent && cd telesales-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Get API Keys (5 minutes)

**Anthropic API:**
1. Go to https://console.anthropic.com
2. Create API key
3. Copy to `.env`: `ANTHROPIC_API_KEY=sk-ant-xxx`

**Google Sheets:**
1. Go to Google Cloud Console
2. Create Service Account
3. Download JSON
4. Save as `google-credentials.json`
5. Share Google Sheet with service account email

### Step 3: Test Locally (2 minutes)
```bash
python 04_test_harness.py
```

**Expected output:**
```
🚀 IntelliTrac AI Telesales Agent - Test Suite
Starting 5 test scenarios...

🧪 TEST: Qualified Hot Lead - Clear Use Case & Pain Points
📝 Customer with clear delivery use case and urgent problems

Agent: Halo! 👋 Terima kasih sudah menghubungi IntelliTrac...
Customer: Kami butuh GPS tracking untuk fleet delivery kami
Agent: Bagus! Delivery untuk industri apa...
...
📊 Lead Score: 78/100 | HOT

✅ All tests completed! Results saved to test_results.json
```

### Step 4: Run Server (1 minute)
```bash
uvicorn 03_fastapi_webhook:app --reload --port 8000
```

Visit: http://localhost:8000/docs (API documentation)

### Step 5: Deploy (5 minutes)
See [SETUP_GUIDE.md](SETUP_GUIDE.md) for Railway/Heroku deployment

---

## 💡 What's New in V1.1?

### **Better Discovery Process**
```
OLD: "Berapa jumlah truk pendingin?"
NEW: "Untuk apa Anda membutuhkan GPS tracking?"

OLD: Assumes refrigerated transportation
NEW: Works for ANY fleet management (delivery, mining, logistics, etc)
```

### **New Data Fields**
- ✅ `use_case` - What they need GPS for
- ✅ `vehicle_type` - Type of vehicles/assets
- ❌ Removed `temperature_requirements` (too specific)

### **Better Scoring**
```
Now: Use Case (20) + Pain Points (25) + Fleet Size (20) + ...
Before: Fleet Size (30) + Temperature (15) + ...

Result: More balanced scoring, not biased to one industry
```

### **5 Real-World Scenarios**
- E-commerce delivery (HOT)
- Mining equipment (WARM)
- Early exploration (COLD)
- Enterprise logistics (HOT)
- Wrong fit detection (COLD)

---

## 📋 File Overview

| File | Purpose | Run With |
|------|---------|----------|
| `01_telesales_agent.py` | Core agent logic | (imported) |
| `02_google_sheets_integration.py` | Data storage | (imported) |
| `03_fastapi_webhook.py` | REST API server | `uvicorn` |
| `04_test_harness.py` | Automated testing | `python` |
| `CHANGELOG.md` | What changed (this file) | (read) |

---

## 🎯 Conversation Flow

**New improved flow:**

```
1️⃣ Greeting
   Agent: "Untuk apa Anda membutuhkan GPS tracking?"
   
2️⃣ Use Case Discovery
   Agent: "Delivery untuk industri apa? Berapa kendaraan?"
   
3️⃣ Pain Points
   Agent: "Apa masalah utama yang dihadapi?"
   
4️⃣ Current Solution
   Agent: "Sistem apa yang sedang digunakan?"
   
5️⃣ Fleet Size (confirm)
   Agent: "Jumlah aset yang perlu ditrack?"
   
6️⃣ Timeline
   Agent: "Kapan target implementasi?"
   
7️⃣ Budget
   Agent: "Sudah ada budget approval?"
   
8️⃣ Contact
   Agent: "Nama, company, email, phone?"

✅ Lead Score Calculated
✅ Saved to Google Sheets
✅ Ready for follow-up
```

---

## 🧪 Test Different Scenarios

Try these messages to test different industries:

### **Scenario: E-commerce Delivery (HOT)**
```
Customer: Kami butuh GPS tracking untuk fleet delivery
Agent: Delivery untuk industri apa - e-commerce, food, retail?
Customer: E-commerce - kami punya 20 kendaraan
Agent: Apa masalah utama dengan tracking sekarang?
Customer: Driver tracking tidak real-time
Agent: (Score: 78/100 - HOT ✅)
```

### **Scenario: Mining Equipment (WARM)**
```
Customer: Kami punya mining operation, pengen track equipment
Agent: Berapa equipment yang perlu ditrack?
Customer: Kira-kira 18 heavy equipment
Agent: Apa masalah utama saat ini?
Customer: Manual checklist - banyak human error
Agent: Kapan implementasi?
Customer: Mungkin quarter depan
Agent: (Score: 55/100 - WARM 🟡)
```

### **Scenario: Early Stage (COLD)**
```
Customer: Saya explore tentang GPS solutions
Agent: Apa use case Anda?
Customer: Belum tahu exactly, mungkin vehicle tracking
Agent: Ini prioritas sekarang?
Customer: Belum, mungkin next year
Agent: (Score: 25/100 - COLD ❄️)
```

---

## 📊 Google Sheets Format

Each lead gets saved with these columns:

```
Timestamp | Name | Company | Phone | Email | Use Case | Vehicle Type | 
Fleet Size | Current Solution | Pain Points | Timeline | Budget Awareness | 
Lead Score | Qualification Level | Conversation Turns | Source | Status
```

**Example:**
```
2024-01-15 | Ahmad | PT Delivery | 0812-xxx | ahmad@... | 
Delivery | Light trucks | 20 | Manual phone | Real-time tracking | 
2-3 months | Need proposal | 78 | HOT | 8 | whatsapp_google_ads | New
```

---

## 🔧 Common Tasks

### **Test Agent Locally**
```bash
python 04_test_harness.py
```

### **Check API is Running**
```bash
curl http://localhost:8000/health
```

### **Test Webhook Manually**
```bash
curl -X POST http://localhost:8000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from_number": "6281234567890",
    "message_text": "Kami butuh GPS tracking untuk delivery fleet",
    "conversation_id": "test-123"
  }'
```

### **Check Conversation Status**
```bash
curl http://localhost:8000/conversations/test-123
```

### **View Active Conversations** (debug)
```bash
curl http://localhost:8000/debug/conversations
```

---

## 🚀 Deploy to Cloud (5 minutes)

### **Option 1: Railway (Easiest)**
```bash
# 1. Go to railway.app
# 2. Connect GitHub
# 3. New Project → Deploy from GitHub
# 4. Set environment variables:
#    - ANTHROPIC_API_KEY
#    - GOOGLE_SHEETS_CREDENTIALS_PATH
# 5. Deploy

# Your URL: https://your-app.railway.app
```

### **Option 2: Heroku**
```bash
heroku login
heroku create intellitrac-telesales
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxx
git push heroku main
```

### **Option 3: Replit (Testing Only)**
```bash
# 1. Go to replit.com
# 2. Create from GitHub
# 3. Set secrets
# 4. Run
```

---

## 🔌 Connect to Make.com

### **Quick Setup**
1. Create Make scenario
2. Add Custom Webhook trigger
3. Copy webhook URL from Make
4. Add HTTP module:
   ```
   POST: https://your-app.railway.app/webhook/whatsapp
   ```
5. Add WhatsApp response module
6. Test & activate

See [MAKE_INTEGRATION_GUIDE.md](MAKE_INTEGRATION_GUIDE.md) for details

---

## 💰 Cost Estimate

**Monthly for 1000 inquiries/day:**
- Anthropic Haiku: ~$9
- Hosting: $7
- Make.com: $10
- WhatsApp API: $50
- **Total: ~$76/month**

**If 1% convert to customers at $1000 ARR = $300/month revenue** 🎉

---

## 📈 Performance Metrics

**Expected:**
- Response time: 2-3 seconds
- Success rate: >99%
- HOT leads: 15-25%
- WARM leads: 30-40%
- COLD leads: 35-55%

**Monitor in Google Sheets:**
- Daily inquiry count
- HOT leads per day
- Average lead score
- Conversion rate (inquiry → demo)

---

## ⚠️ Troubleshooting

### **Agent not responding**
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Check server running
curl http://localhost:8000/health

# Restart server
```

### **Google Sheets not saving**
```bash
# Check credentials
ls -la google-credentials.json

# Verify sheet is shared with service account email
# Check in Google Sheets: Share → get email
```

### **Make webhook not triggering**
```
1. Check webhook URL in Make is correct
2. Click "Test" in Make
3. Check FastAPI logs for incoming requests
4. Verify JSON format in Make body
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more

---

## 📞 Support

**Documentation:**
- README.md - Overview
- SETUP_GUIDE.md - Detailed setup
- MAKE_INTEGRATION_GUIDE.md - Make.com workflow
- DEPLOYMENT_CHECKLIST.md - Launch checklist
- CHANGELOG.md - What changed (this document)

**External Resources:**
- Anthropic: https://docs.anthropic.com
- FastAPI: https://fastapi.tiangolo.com
- Make.com: https://www.make.com/docs

---

## ✅ Launch Checklist

- [ ] Files downloaded & extracted
- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] API keys obtained (Anthropic + Google)
- [ ] `.env` file configured
- [ ] Test harness passes
- [ ] Local server runs
- [ ] Cloud deployment ready
- [ ] Make scenario created
- [ ] WhatsApp Business API configured
- [ ] Google Ads campaigns ready
- [ ] Sales team trained
- [ ] Google Sheets monitoring setup

---

## 🎉 You're Ready!

```
✅ Agent is general purpose (not just refrigerated)
✅ Conversation flow is natural (discovery-first)
✅ Scoring is balanced (use case → 20 points)
✅ Multiple industries supported (delivery, mining, logistics, etc)
✅ Tests pass with 5 real-world scenarios
✅ Production-ready code
✅ Comprehensive documentation

Ready to launch! 🚀
```

---

**Version:** 1.1  
**Status:** ✅ Tested & Ready  
**Last Updated:** January 2024

Quick questions? Check CHANGELOG.md for what changed from V1.0 to V1.1
