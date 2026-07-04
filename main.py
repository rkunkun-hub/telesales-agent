"""
FastAPI Webhook Handler for Make/Zapier Integration
Receives WhatsApp messages from Make and processes them with Claude AI
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict
import os
import json
import uuid
from datetime import datetime
import asyncio

# Import our custom modules
from telesales_agent import LeadQualificationAgent, get_initial_greeting
from google_sheets_integration import GoogleSheetsLeadStorage

# ============================================================================
# FASTAPI SETUP
# ============================================================================

app = FastAPI(title="IntelliTrac Telesales Webhook")

# Store active conversations in memory (or use Redis for production)
active_conversations: Dict[str, LeadQualificationAgent] = {}

# Initialize Google Sheets (set environment variables)
SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "google-credentials.json")
SHEETS_STORAGE = None

try:
    SHEETS_STORAGE = GoogleSheetsLeadStorage(SHEETS_CREDENTIALS)
    print("✅ Google Sheets connected")
except Exception as e:
    print(f"⚠️  Google Sheets not available: {e}")


# ============================================================================
# MODELS
# ============================================================================

class WhatsAppMessage(BaseModel):
    """Incoming WhatsApp message from Make/Zapier"""
    from_number: str  # Customer phone number
    message_text: str  # Customer message
    message_id: Optional[str] = None  # Unique message ID
    timestamp: Optional[str] = None  # Message timestamp
    conversation_id: Optional[str] = None  # Optional conversation ID


class WhatsAppResponse(BaseModel):
    """Response to send back via Make/Zapier to WhatsApp"""
    to_number: str
    message: str
    conversation_id: str
    lead_score: int
    qualification_level: str
    status: str


# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Make/Zapier"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": len(active_conversations)
    }


@app.post("/webhook/whatsapp")
async def handle_whatsapp_message(message: WhatsAppMessage):
    """
    Main webhook endpoint - receives WhatsApp messages from Make/Zapier
    
    Flow:
    1. Receive message from Make
    2. Find or create agent conversation
    3. Process message with Claude
    4. Save to Google Sheets
    5. Return response for WhatsApp
    """
    
    try:
        # Generate or use provided conversation ID
        conversation_id = message.conversation_id or str(uuid.uuid4())
        customer_number = message.from_number
        user_message = message.message_text
        
        print(f"📨 Incoming: {customer_number} | Conv: {conversation_id}")
        print(f"   Message: {user_message[:100]}...")
        
        # ====== STEP 1: Get or create agent for this conversation ======
        
        if conversation_id not in active_conversations:
            # New conversation
            agent = LeadQualificationAgent()
            active_conversations[conversation_id] = agent
            
            # Send initial greeting
            initial_message = get_initial_greeting("refrigerated")
            response_message = initial_message
            
            # Add to conversation history
            agent.add_message("assistant", initial_message)
            
        else:
            # Existing conversation
            agent = active_conversations[conversation_id]
            
            # ====== STEP 2: Process message with Claude ======
            response_data = agent.process_message(user_message)
            response_message = response_data.get("message", "")
        
        # ====== STEP 3: Extract qualification info ======
        
        lead_score = agent.calculate_lead_score()
        qualification_level = agent.get_qualification_level()
        
        print(f"   Score: {lead_score}/100 | Level: {qualification_level}")
        
        # ====== STEP 4: Save lead if qualification complete ======
        
        if agent.is_qualification_complete() and SHEETS_STORAGE:
            lead_data = agent.export_lead_data()
            SHEETS_STORAGE.save_lead(lead_data)
            SHEETS_STORAGE.save_conversation_log(
                lead_data, 
                agent.conversation_history,
                conversation_id
            )
            
            # Update conversation status (optional: move to closed after saving)
            # active_conversations.pop(conversation_id)
        
        # ====== STEP 5: Prepare response ======
        
        response = WhatsAppResponse(
            to_number=customer_number,
            message=response_message,
            conversation_id=conversation_id,
            lead_score=lead_score,
            qualification_level=qualification_level,
            status="sent"
        )
        
        print(f"   ✅ Response ready: {response_message[:50]}...")
        return response
        
    except Exception as e:
        print(f"❌ Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/whatsapp/start")
async def start_conversation(phone_number: str, landing_page: Optional[str] = "refrigerated"):
    """
    Start a new conversation (called when customer first clicks WhatsApp link from Google Ads)
    
    Args:
        phone_number: Customer phone number
        landing_page: Which landing page they came from (refrigerated/logistics/general)
    """
    
    try:
        conversation_id = str(uuid.uuid4())
        
        # Create new agent
        agent = LeadQualificationAgent()
        active_conversations[conversation_id] = agent
        
        # Get greeting
        greeting = get_initial_greeting(landing_page)
        
        response = {
            "conversation_id": conversation_id,
            "phone_number": phone_number,
            "message": greeting,
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"🎯 New conversation started: {conversation_id}")
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{conversation_id}")
async def get_conversation_status(conversation_id: str):
    """Get current status of a conversation"""
    
    if conversation_id not in active_conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    agent = active_conversations[conversation_id]
    
    return {
        "conversation_id": conversation_id,
        "conversation_turns": len(agent.conversation_history),
        "lead_score": agent.calculate_lead_score(),
        "qualification_level": agent.get_qualification_level(),
        "qualification_data": agent.qualification_data,
        "is_complete": agent.is_qualification_complete()
    }


@app.delete("/conversations/{conversation_id}")
async def close_conversation(conversation_id: str):
    """Close a conversation and clean up"""
    
    if conversation_id not in active_conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    agent = active_conversations.pop(conversation_id)
    
    return {
        "conversation_id": conversation_id,
        "status": "closed",
        "lead_score": agent.calculate_lead_score(),
        "qualification_level": agent.get_qualification_level()
    }


# ============================================================================
# DEBUG ENDPOINTS (remove in production)
# ============================================================================

@app.get("/debug/conversations")
async def debug_conversations():
    """List all active conversations"""
    return {
        "total": len(active_conversations),
        "conversations": list(active_conversations.keys())
    }


@app.post("/debug/test-message")
async def debug_test_message(phone: str = "6281234567890", text: str = "Halo, saya punya 20 truk pendingin"):
    """Test message processing without Make/Zapier"""
    
    test_msg = WhatsAppMessage(
        from_number=phone,
        message_text=text,
        conversation_id=None
    )
    
    return await handle_whatsapp_message(test_msg)


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    print("🚀 IntelliTrac Telesales Webhook Server Started")
    print(f"📍 Listening on: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Server shutting down...")
    # Save any open conversations before shutdown (optional)
    if SHEETS_STORAGE:
        for conv_id, agent in active_conversations.items():
            if agent.qualification_data["contact_info"]["name"]:
                lead_data = agent.export_lead_data()
                SHEETS_STORAGE.save_lead(lead_data)
    print("✅ Shutdown complete")


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run with: python 03_fastapi_webhook.py
    # Or: uvicorn 03_fastapi_webhook:app --reload --port 8000
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
