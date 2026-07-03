# 🚀 IntelliTrac AI Telesales Agent

**Automated Lead Qualification for Logistics & Refrigerated Transportation**

Intelligent WhatsApp chatbot powered by Claude AI that qualifies leads from Google Ads, scores them automatically, and saves qualified prospects to Google Sheets.

---

## 🎯 What This Does

```
Customer clicks Google Ads → Lands on product page → Clicks WhatsApp → AI Agent qualifies lead → Data saved to Sheets
                                                                                ↓
                                                               Sales team gets prioritized leads ready for follow-up
```

**Key Features:**
- ✅ **Natural Conversations** - Claude AI handles open-ended responses
- ✅ **Smart Qualification** - Automatically scores leads (0-100)
- ✅ **Data Collection** - Gathers company, fleet size, pain points, timeline
- ✅ **Google Sheets Integration** - Leads auto-saved for CRM/follow-up
- ✅ **Scalable** - Handles hundreds of concurrent conversations
- ✅ **Cost Efficient** - Uses Haiku model (~$0.30/day for 1000+ inquiries)

---

## 📊 Lead Scoring System

| Score | Level | Action | Example |
|-------|-------|--------|---------|
| 70-100 | 🔥 HOT | Call immediately | 25+ trucks, clear pain points, budget ready |
| 40-69 | 🟡 WARM | Schedule follow-up | 10-20 trucks, some pain points, timeline unclear |
| 0-39 | ❄️ COLD | Add to nurture | 1-5 trucks, exploring only, budget not approved |

---

## 📁 Project Structure

```
telesales-agent/
│
├── 📄 01_telesales_agent.py
│   └── Core agent with lead qualification logic
│       - LeadQualificationAgent class
│       - Claude API integration
│       - Scoring algorithm
│       - Test mode included
│
├── 📄 02_google_sheets_integration.py
│   └── Save leads to Google Sheets
│       - GoogleSheetsLeadStorage class
│       - Auto-append rows
│       - Lead status tracking
│       - Conversation logging
│
├── 📄 03_fastapi_webhook.py
│   └── REST API server for WhatsApp/Make integration
│       - /webhook/whatsapp endpoint
│       - Conversation management
│       - Health check
│       - Debug endpoints
│
├── 📄 04_test_harness.py
│   └── Automated testing with 5 scenarios
│       - Qualified hot lead
│       - Medium lead
│       - Cold lead
│       - Enterprise lead
│       - Not-a-fit scenario
│
├── 📄 requirements.txt
│   └── Python dependencies
│
├── 📄 .env.template
│   └── Environment variables template
│       - API keys
│       - Google credentials path
│       - Server config
│
├── 📄 SETUP_GUIDE.md
│   └── Step-by-step setup instructions
│       - Local development
│       - Google Sheets configuration
│       - Deployment options
│       - Troubleshooting
│
├── 📄 MAKE_INTEGRATION_GUIDE.md
│   └── Make.com workflow setup
│       - Webhook configuration
│       - WhatsApp Business API
│       - Testing procedures
│       - Advanced scenarios
│
└── 📄 README.md (this file)
    └── Project overview and quick start
```

---

## 🚀 Quick Start (15 Minutes)

### Step 1: Setup Environment
```bash
# Clone or download this project
cd telesales-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get API Keys
```bash
# 1. Get Anthropic API key from https://console.anthropic.com
# 2. Get Google credentials from Google Cloud Console (see SETUP_GUIDE.md)

# Create .env file
copy .env.template .env

# Edit .env and add your keys:
# ANTHROPIC_API_KEY=sk-ant-xxx...
# GOOGLE_SHEETS_CREDENTIALS_PATH=google-credentials.json
```

### Step 3: Test Locally
```bash
# Run test agent (includes 5 sample conversations)
python 04_test_harness.py

# Expected output: Summary of lead scoring, results saved to test_results.json
```

### Step 4: Start Server
```bash
# Run FastAPI server
uvicorn 03_fastapi_webhook:app --reload --port 8000

# Test endpoint
curl http://localhost:8000/health
```

### Step 5: Connect to Make/Zapier
See [MAKE_INTEGRATION_GUIDE.md](MAKE_INTEGRATION_GUIDE.md) for detailed setup

---

## 💬 Conversation Flow Example

```
Agent: Halo! 👋 Terima kasih sudah menghubungi IntelliTrac. 
       Saya siap membantu Anda menemukan solusi GPS tracking yang tepat. 
       Untuk memulai, bisa saya tahu apa kebutuhan GPS Anda?

Customer: Kami butuh tracking untuk fleet delivery kami

Agent: Bagus! Jadi Anda punya delivery fleet. Delivery untuk industri apa - 
       e-commerce, food, retail, atau yang lain? Dan kira-kira berapa 
       kendaraan yang perlu ditrack?

Customer: E-commerce, kami punya 20 kendaraan

Agent: Perfect! 20 kendaraan untuk e-commerce delivery - skalanya cukup signifikan. 
       Sekarang, apa sih masalah utama yang Anda hadapi dengan delivery tracking 
       saat ini?

Customer: Masalahnya driver sering terlambat dan kita tidak bisa track real-time

Agent: Saya paham - visibility real-time memang critical untuk customer satisfaction 
       dan efficiency. Sekarang, untuk melacak driver sebelumnya, Anda pakai sistem 
       apa? Ada GPS system lama, atau masih manual?

Customer: Masih manual - tanya driver via telepon

Agent: Okay, jadi completely manual tracking. Itu memang challenging dengan 20 vehicles. 
       Sekarang timeline-nya gimana? Kapan Anda ingin implement solution baru?

Customer: 2-3 bulan ke depan, cukup urgent

Agent: 2-3 bulan - baik, itu reasonable timeline. Terakhir, agar saya bisa prepare 
       proposal yang tepat, bisa saya tahu nama Anda dan perusahaan?

Customer: Saya Ahmad dari PT Logistics Cepat

Agent: Ahmad dari PT Logistics Cepat - sempurna! 🎯 Berdasarkan yang kita diskusi, 
       Anda butuh real-time tracking untuk 20 delivery vehicles dengan implementasi 
       dalam 2-3 bulan. Kami punya solution yang perfect untuk ini. 
       
       Bisa saya minta email dan nomor HP untuk follow-up lebih detail?

Customer: Email saya ahmad@logcepat.co.id, nomor 0812-3456-7890

[Lead Score: 78/100 - HOT ✅ - Automatically saved to Google Sheets]
```

**Key Flow:**
1. ✅ **Greeting** (terbuka, tidak assume)
2. ✅ **Use Case Discovery** (delivery untuk apa, berapa kendaraan)
3. ✅ **Pain Points** (apa masalah current)
4. ✅ **Current Solution** (sistem apa yang sekarang)
5. ✅ **Timeline** (kapan mau implementasi)
6. ✅ **Contact Info** (nama, company, email, phone)

---

## 📊 Lead Data Saved to Google Sheets

Each qualified lead creates a row with:

| Field | Example |
|-------|---------|
| Timestamp | 2024-01-15 14:32:00 |
| Name | Ahmad Wijaya |
| Company | PT Fresh Indonesia |
| Phone | +6281234567890 |
| Email | ahmad@freshindo.id |
| Fleet Size | 15 |
| Current Solution | Manual GPS tracking |
| Pain Points | Delay in real-time data; temperature monitoring errors |
| Temperature Requirements | Real-time monitoring; alerts at ±2°C |
| Timeline | 3 months |
| Budget Awareness | Approved by management |
| Lead Score | 75 |
| Qualification Level | HOT |
| Conversation Turns | 8 |
| Source | whatsapp_google_ads |
| Status | New → Contacted → Demo Scheduled |

---

## 🔌 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Google Ads Landing Page                     │
│              (intellitrac.co.id/gps-solutions/)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
                    WhatsApp CTA Button
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    WhatsApp Business API                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                 Make.com Webhook Automation                       │
│  (Receives message → Calls FastAPI → Sends response back)       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Server (03_fastapi_webhook.py)              │
│  - Handles concurrent conversations                             │
│  - Routes to Claude AI                                          │
│  - Saves to Google Sheets                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ↓                     ↓
        ┌──────────────────┐   ┌────────────────────┐
        │   Claude API     │   │  Google Sheets     │
        │  (Qualification) │   │  (Lead Storage)    │
        └──────────────────┘   └────────────────────┘
```

---

## 🎓 Qualification Criteria

Agent asks about dalam urutan natural:

1. **Use Case** (business understanding)
   - "Untuk apa Anda membutuhkan GPS tracking?"
   - Delivery, Logistics, Mining, Construction, Cold Chain, etc

2. **Vehicle Type** (scope clarity)
   - "Kendaraan apa yang perlu ditrack?"
   - Delivery trucks, heavy equipment, motorcycles, etc

3. **Pain Points** (urgency & motivation)
   - "Apa sih masalah utama saat ini?"
   - Real-time visibility, driver accountability, efficiency, security, etc

4. **Current Solution** (replacement potential)
   - "Sistem apa yang sedang Anda gunakan?"
   - Manual, competitor system, outdated solution, nothing

5. **Fleet Size** (business potential)
   - "Berapa jumlah kendaraan/asset yang perlu ditrack?"
   - 5-20 = Small, 20-50 = Medium, 50+ = Enterprise

6. **Timeline** (buying signal)
   - "Kapan Anda target untuk implementasi?"
   - Next 1-3 months = HOT, 3-6 months = WARM, Future = COLD

7. **Budget** (closing probability)
   - "Sudah ada budget approval?"
   - Approved = ready to buy, Need proposal = considering

8. **Contact Info** (follow-up ability)
   - Name, Company, Email, Phone

---

## 🛠️ Customization Guide

### Change Qualification Criteria

Edit `01_telesales_agent.py`:

```python
def calculate_lead_score(self) -> int:
    """Customize scoring weights"""
    score = 0
    
    # Adjust these weights based on your priorities
    if self.qualification_data["fleet_size"]:
        score += 40  # Changed from 30
    
    if self.qualification_data["pain_points"]:
        score += 25  # Changed from 20
    
    # ... more criteria
```

### Change Agent Personality

Edit `SYSTEM_PROMPT` in `01_telesales_agent.py`:

```python
SYSTEM_PROMPT = """Anda adalah [YOUR_CUSTOM_PERSONALITY]
Produk Anda: [YOUR_PRODUCTS]
Target Market: [YOUR_MARKET]
Tone: [PROFESSIONAL|FRIENDLY|CASUAL]
...
"""
```

### Add More Qualifying Questions

Edit `get_initial_greeting()` function:

```python
def get_initial_greeting(landing_page: Optional[str] = None) -> str:
    """Add or modify greeting messages"""
    greetings = {
        "your_new_page": "Custom greeting for specific landing page",
        # ... more pages
    }
```

---

## 📈 Metrics & KPIs

Track these in your Google Sheets dashboard:

```
Daily Metrics:
- Total inquiries received
- Leads qualified (by level: HOT/WARM/COLD)
- Average lead score
- Average conversation length

Conversion Metrics:
- HOT lead → Demo booked rate
- Demo → Close rate
- Average deal value by source

Cost Metrics:
- Cost per inquiry
- Cost per qualified lead
- Cost per customer acquired
```

---

## 🔐 Security Best Practices

- ✅ Store API keys in `.env` (never commit!)
- ✅ Use HTTPS only in production
- ✅ Validate webhook requests in Make
- ✅ Implement rate limiting
- ✅ Don't log PII (personal info)
- ✅ Regular credential rotation
- ✅ Monitor API usage

---

## 💰 Cost Breakdown

**Monthly Estimate (1000 inquiries/day):**

| Component | Cost | Notes |
|-----------|------|-------|
| Anthropic Haiku | ~$9 | $0.80/$0.24 per M tokens |
| Hosting (Railway) | $7 | Basic dyno |
| Make.com | $10 | Pro plan for reliability |
| WhatsApp API | $50 | Pay-per-message outbound |
| Google Suite | $6 | Business account (if needed) |
| **TOTAL** | **~$82/month** | Full automation for 30k inquiries |

**ROI:** If even 1% convert to customers at $1000 ARR = $300/month revenue 🎉

---

## 🐛 Troubleshooting

### Agent doesn't respond
- Check `ANTHROPIC_API_KEY` in `.env`
- Verify API quota at console.anthropic.com
- Check internet connection

### Leads not saving to Sheets
- Verify Google credentials file
- Check sheet is shared with service account email
- Run: `python 02_google_sheets_integration.py`

### Make webhook not triggering
- Verify webhook URL in Make
- Test with "Make a test request"
- Check FastAPI server is running
- Review Make execution history

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

---

## 📚 Learning Resources

- **Anthropic API**: https://docs.anthropic.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Make.com**: https://www.make.com/docs
- **Google Sheets API**: https://developers.google.com/sheets
- **WhatsApp Business API**: https://developers.facebook.com/docs/whatsapp

---

## 🤝 Support

If you need help:

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Review your Make.com execution history
3. Test with [04_test_harness.py](04_test_harness.py)
4. Check FastAPI logs: `uvicorn ... --log-level=debug`

---

## 📝 Next Steps

- [ ] Setup local environment
- [ ] Get API credentials
- [ ] Run test suite
- [ ] Deploy to Railway
- [ ] Setup Make.com scenario
- [ ] Configure WhatsApp Business
- [ ] Test end-to-end
- [ ] Launch to Google Ads
- [ ] Monitor & optimize

---

## 📄 License

Internal use for IntelliTrac GPS only.

---

## 🎉 Good Luck!

You're now ready to automate lead qualification and focus your sales team on closing deals instead of data entry.

Happy selling! 🚀

---

**Version:** 1.0  
**Last Updated:** January 2024  
**Author:** IntelliTrac Engineering  
**Support:** engineering@intellitrac.co.id
