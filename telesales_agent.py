"""
IntelliTrac AI Telesales Agent
Lead Qualification for Logistics & Refrigerated Transportation

Main module: Handles WhatsApp inquiries and qualifies leads using Claude AI
"""

import anthropic
import json
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from typing import Optional

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# SYSTEM PROMPT - Agent Personality & Behavior
# ============================================================================

SYSTEM_PROMPT = """Anda adalah IntelliTrac Sales Agent yang profesional dan ramah. 
Tugas Anda adalah melakukan lead qualification untuk solusi GPS Tracking 
untuk berbagai kebutuhan Logistics & Transportation.

INFORMASI PRODUK:
- GPS Fleet Tracker untuk fleet management
- Real-time tracking untuk semua jenis kendaraan
- Support untuk: Logistics, Cold Chain, Delivery, Construction, Mining, dll
- Features: live location, temperature alerts (if needed), geofencing, speed monitoring, reports
- Harga: customized berdasarkan kebutuhan dan fleet size

CONVERSATION FLOW (Natural & Discovery-Focused):
1. GREETING - Sambutan hangat, terbuka untuk semua kebutuhan
2. USE CASE DISCOVERY - Tanya: jenis kendaraan, kebutuhan GPS untuk apa (delivery tracking, asset monitoring, etc)
3. PAIN POINTS - Tanya: apa masalah yang mereka hadapi saat ini
4. CURRENT SOLUTION - Tanya: solusi apa yang sedang digunakan
5. FLEET SIZE - Tanya: berapa jumlah kendaraan/asset
6. TIMELINE - Tanya: kapan target implementasi
7. BUDGET - Tanya: ada budget approval atau perlu proposal
8. CONTACT INFO - Kumpulkan nama, company, email, phone

LEAD QUALIFICATION CRITERIA:
Kualifikasi lead berdasarkan:
1. Use Case Clarity (jelas/tidak jelas kebutuhannya)
2. Pain Points (ada masalah urgent atau exploring)
3. Fleet Size (skala bisnis)
4. Current Solution (ada sistem atau manual)
5. Timeline (urgent atau future)
6. Budget (approved atau need approval)

CONVERSATION RULES:
1. Mulai dengan greeting hangat, tidak assume use case
2. Tanya satu pertanyaan utama per response (jangan overload)
3. Dengarkan dengan aktif, referensikan jawaban mereka
4. Jangan langsung jualan - fokus discovery kebutuhan
5. Validasi pemahaman Anda tentang kebutuhan mereka
6. Jika pain point jelas dan timeline urgent → suggest demo
7. Gunakan bahasa Indonesia yang natural dan friendly
8. Keep conversation singkat, fokus, dan value-driven

RESPONSE FORMAT:
Selalu respond dengan JSON structure ini:
{
    "message": "Pesan ke customer (natural, 1-2 sentences)",
    "qualification_status": "initial|discovery|ongoing|qualified",
    "qualification_data": {
        "use_case": null,
        "vehicle_type": null,
        "pain_points": [],
        "current_solution": null,
        "fleet_size": null,
        "timeline": null,
        "budget_awareness": null
    },
    "next_action": "continue|schedule_demo|send_brochure"
}

JANGAN tambahkan text lain selain JSON object di atas."""

# ============================================================================
# QUALIFICATION LOGIC
# ============================================================================

class LeadQualificationAgent:
    def __init__(self):
        self.conversation_history = []
        self.qualification_data = {
            "use_case": None,
            "vehicle_type": None,
            "pain_points": [],
            "current_solution": None,
            "fleet_size": None,
            "timeline": None,
            "budget_awareness": None,
            "contact_info": {
                "name": None,
                "company": None,
                "phone": None,
                "email": None
            }
        }
        self.lead_score = 0
        self.source = "whatsapp_google_ads"
        
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def calculate_lead_score(self) -> int:
        """Calculate lead qualification score (0-100)"""
        score = 0
        
        # Use case clarity: clear use case = strong signal
        if self.qualification_data["use_case"]:
            score += 20
        
        # Pain points: has urgent problems
        if self.qualification_data["pain_points"]:
            score += 25
        
        # Fleet size: business potential
        if self.qualification_data["fleet_size"]:
            try:
                fleet = int(self.qualification_data["fleet_size"])
                score += min(20, fleet // 5)  # Max 20 points
            except:
                pass
        
        # Current solution: has existing system (upgrade potential)
        if self.qualification_data["current_solution"]:
            score += 15
        
        # Has timeline: buying signal
        if self.qualification_data["timeline"] and self.qualification_data["timeline"].lower() not in ["belum", "tidak", "entahlah"]:
            score += 15
        
        # Budget aware: buying power
        if self.qualification_data["budget_awareness"]:
            score += 10
        
        return min(100, score)
    
    def get_qualification_level(self) -> str:
        """Determine qualification level: HOT, WARM, or COLD"""
        score = self.calculate_lead_score()
        
        if score >= 70:
            return "HOT"
        elif score >= 40:
            return "WARM"
        else:
            return "COLD"
    
    def is_qualification_complete(self) -> bool:
        """Check if we have enough data to move to next stage"""
        required_fields = [
            self.qualification_data["use_case"],
            self.qualification_data["pain_points"],
            self.qualification_data["fleet_size"],
            self.qualification_data["timeline"],
            self.qualification_data["contact_info"]["name"],
            self.qualification_data["contact_info"]["company"]
        ]
        return all(required_fields)
    
    def process_message(self, user_message: str) -> dict:
        """Process user message and return AI response"""
        
        # Add user message to history
        self.add_message("user", user_message)
        
        # Call Claude API
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Cost-efficient for high volume
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=self.conversation_history
        )
        
        # Extract response
        assistant_message = response.content[0].text
        self.add_message("assistant", assistant_message)
        
        # Parse JSON response
        try:
            response_data = json.loads(assistant_message)
        except json.JSONDecodeError:
            # Fallback jika response bukan valid JSON
            return {
                "message": assistant_message,
                "qualification_status": "ongoing",
                "qualification_data": self.qualification_data,
                "lead_score": self.calculate_lead_score(),
                "qualification_level": self.get_qualification_level(),
                "next_action": "continue",
                "error": "Response parsing failed"
            }
        
        # Update qualification data dari response
        if response_data.get("qualification_data"):
            for key, value in response_data["qualification_data"].items():
                if value is not None:
                    self.qualification_data[key] = value
        
        # Enrich response dengan internal data
        response_data["qualification_data"] = self.qualification_data
        response_data["lead_score"] = self.calculate_lead_score()
        response_data["qualification_level"] = self.get_qualification_level()
        response_data["timestamp"] = datetime.now().isoformat()
        
        return response_data
    
    def export_lead_data(self) -> dict:
        """Export lead data for Google Sheets"""
        return {
            "timestamp": datetime.now().isoformat(),
            "lead_score": self.calculate_lead_score(),
            "qualification_level": self.get_qualification_level(),
            "use_case": self.qualification_data["use_case"],
            "vehicle_type": self.qualification_data["vehicle_type"],
            "fleet_size": self.qualification_data["fleet_size"],
            "current_solution": self.qualification_data["current_solution"],
            "pain_points": "; ".join(self.qualification_data["pain_points"]),
            "timeline": self.qualification_data["timeline"],
            "budget_awareness": self.qualification_data["budget_awareness"],
            "name": self.qualification_data["contact_info"]["name"],
            "company": self.qualification_data["contact_info"]["company"],
            "phone": self.qualification_data["contact_info"]["phone"],
            "email": self.qualification_data["contact_info"]["email"],
            "conversation_turns": len(self.conversation_history),
            "source": self.source
        }


# ============================================================================
# CONVERSATION STARTERS
# ============================================================================

def get_initial_greeting(landing_page: Optional[str] = None) -> str:
    """Generate initial greeting based on landing page"""
    greetings = {
        "refrigerated": "Halo! 👋 Terima kasih sudah tertarik dengan solusi GPS tracking kami. Saya di sini untuk membantu Anda menemukan sistem yang perfect untuk bisnis Anda. Bisa saya tahu, untuk apa Anda membutuhkan GPS tracking?",
        "logistics": "Halo! 👋 Senang bertemu! Saya adalah sales assistant IntelliTrac. Kami punya solusi GPS tracking yang flexible untuk berbagai kebutuhan logistik. Bisa cerita sedikit tentang operasi Anda?",
        "general": "Halo! 👋 Terima kasih sudah menghubungi IntelliTrac. Saya siap membantu Anda menemukan solusi GPS tracking yang tepat. Untuk memulai, bisa saya tahu apa kebutuhan GPS Anda?"
    }
    return greetings.get(landing_page, greetings["general"])


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test agent
    print("🚀 IntelliTrac AI Telesales Agent - Test Mode\n")
    
    agent = LeadQualificationAgent()
    
    # Start conversation
    initial_message = get_initial_greeting("general")
    print(f"Agent: {initial_message}\n")
    
    # Simulate conversation
    test_messages = [
        "Kami butuh GPS tracking untuk fleet delivery kami",
        "E-commerce - kami punya 20 kendaraan",
        "Masalahnya driver sering terlambat dan kita tidak bisa track real-time",
        "Saat ini masih manual - tanya driver via telepon",
        "Timeline 2-3 bulan, cukup urgent",
        "Nama saya Ahmad dari PT Logistics Cepat",
        "Email: ahmad@logcepat.co.id, nomor 0812-3456-7890"
    ]
    
    for user_msg in test_messages:
        print(f"Customer: {user_msg}")
        response = agent.process_message(user_msg)
        print(f"Agent: {response['message']}\n")
        print(f"📊 Lead Score: {response['lead_score']}/100 | Level: {response['qualification_level']}\n")
    
    # Export lead data
    print("\n✅ Lead Data Ready for Google Sheets:")
    print(json.dumps(agent.export_lead_data(), indent=2, ensure_ascii=False))
