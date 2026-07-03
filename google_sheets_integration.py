"""
Google Sheets Integration Module
Saves qualified leads to Google Sheets automatically
"""

import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class GoogleSheetsLeadStorage:
    """Handle lead data storage in Google Sheets"""
    
    def __init__(self, credentials_path: str, spreadsheet_name: str = "IntelliTrac Leads"):
        """
        Initialize Google Sheets connection
        
        Args:
            credentials_path: Path to Google Service Account JSON
            spreadsheet_name: Name of the spreadsheet to use
        """
        try:
            self.credentials = Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets', 
                       'https://www.googleapis.com/auth/drive']
            )
            self.client = gspread.authorize(self.credentials)
            self.spreadsheet = self.client.open(spreadsheet_name)
            self.worksheet = self.spreadsheet.worksheet("Leads")
        except Exception as e:
            raise Exception(f"Failed to connect to Google Sheets: {str(e)}")
    
    def save_lead(self, lead_data: Dict) -> bool:
        """
        Save a single lead to Google Sheets
        
        Args:
            lead_data: Dictionary with lead information (from export_lead_data)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare row data - order harus match dengan header
            row = [
                lead_data.get("timestamp", ""),
                lead_data.get("name", ""),
                lead_data.get("company", ""),
                lead_data.get("phone", ""),
                lead_data.get("email", ""),
                lead_data.get("use_case", ""),
                lead_data.get("vehicle_type", ""),
                lead_data.get("fleet_size", ""),
                lead_data.get("current_solution", ""),
                lead_data.get("pain_points", ""),
                lead_data.get("timeline", ""),
                lead_data.get("budget_awareness", ""),
                lead_data.get("lead_score", 0),
                lead_data.get("qualification_level", ""),
                lead_data.get("conversation_turns", 0),
                lead_data.get("source", ""),
                "New"  # Status
            ]
            
            # Append to worksheet
            self.worksheet.append_row(row, value_input_option='RAW')
            print(f"✅ Lead saved: {lead_data.get('name')} from {lead_data.get('company')}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving lead: {str(e)}")
            return False
    
    def save_conversation_log(self, lead_data: Dict, conversation_history: List[Dict], 
                              conversation_id: str) -> bool:
        """
        Save conversation logs to separate sheet for analysis
        
        Args:
            lead_data: Lead information
            conversation_history: List of conversation turns
            conversation_id: Unique conversation ID
            
        Returns:
            True if successful
        """
        try:
            # Create or get Conversations sheet
            try:
                conversations_sheet = self.spreadsheet.worksheet("Conversations")
            except gspread.exceptions.WorksheetNotFound:
                conversations_sheet = self.spreadsheet.add_worksheet("Conversations", 1000, 10)
                # Add headers
                conversations_sheet.append_row([
                    "Conversation ID", "Lead Name", "Company", "Turn #", 
                    "Role", "Message", "Timestamp"
                ])
            
            # Save each message
            for i, msg in enumerate(conversation_history):
                row = [
                    conversation_id,
                    lead_data.get("name", ""),
                    lead_data.get("company", ""),
                    i + 1,
                    msg.get("role", "").upper(),
                    msg.get("content", ""),
                    datetime.now().isoformat()
                ]
                conversations_sheet.append_row(row, value_input_option='RAW')
            
            print(f"✅ Conversation log saved: {conversation_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving conversation: {str(e)}")
            return False
    
    def get_hot_leads(self) -> List[Dict]:
        """Get all HOT leads (score >= 70)"""
        try:
            all_records = self.worksheet.get_all_records()
            hot_leads = [r for r in all_records if r.get("Qualification Level") == "HOT"]
            return hot_leads
        except Exception as e:
            print(f"Error fetching hot leads: {str(e)}")
            return []
    
    def update_lead_status(self, lead_name: str, new_status: str) -> bool:
        """
        Update lead status (e.g., "New" → "Contacted" → "Demo Scheduled" → "Qualified")
        
        Args:
            lead_name: Name of the lead
            new_status: New status value
            
        Returns:
            True if successful
        """
        try:
            all_records = self.worksheet.get_all_records()
            for i, record in enumerate(all_records):
                if record.get("Name") == lead_name:
                    # Row index is i+2 (header is row 1, data starts at row 2)
                    self.worksheet.update_cell(i + 2, 16, new_status)  # Column 16 = Status
                    print(f"✅ Status updated: {lead_name} → {new_status}")
                    return True
            
            print(f"❌ Lead not found: {lead_name}")
            return False
            
        except Exception as e:
            print(f"Error updating lead status: {str(e)}")
            return False


# ============================================================================
# SETUP HELPER
# ============================================================================

def create_sheets_template(credentials_path: str):
    """
    Create a new Google Sheet with proper headers
    Run this once to set up the spreadsheet
    """
    try:
        credentials = Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets', 
                   'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(credentials)
        
        # Create new spreadsheet
        spreadsheet = client.create("IntelliTrac Leads")
        print(f"📊 New spreadsheet created: {spreadsheet.url}")
        
        # Add worksheet and headers
        worksheet = spreadsheet.sheet1
        worksheet.title = "Leads"
        
        headers = [
            "Timestamp",
            "Name",
            "Company",
            "Phone",
            "Email",
            "Use Case",
            "Vehicle Type",
            "Fleet Size",
            "Current Solution",
            "Pain Points",
            "Timeline",
            "Budget Awareness",
            "Lead Score",
            "Qualification Level",
            "Conversation Turns",
            "Source",
            "Status"
        ]
        
        worksheet.append_row(headers)
        print("✅ Headers created in 'Leads' sheet")
        
        # Create Conversations sheet
        conversations = spreadsheet.add_worksheet("Conversations", 1000, 7)
        conv_headers = [
            "Conversation ID",
            "Lead Name",
            "Company",
            "Turn #",
            "Role",
            "Message",
            "Timestamp"
        ]
        conversations.append_row(conv_headers)
        print("✅ 'Conversations' sheet created")
        
        return spreadsheet
        
    except Exception as e:
        print(f"❌ Error creating sheets: {str(e)}")
        return None


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Example usage
    print("Google Sheets Integration Test\n")
    print("⚠️  Note: You need Google Service Account credentials\n")
    
    # To use this:
    # 1. Go to Google Cloud Console
    # 2. Create Service Account
    # 3. Download JSON credentials
    # 4. Update credentials_path below
    
    # credentials_path = "path/to/google-credentials.json"
    # sheets = GoogleSheetsLeadStorage(credentials_path)
    # 
    # hot_leads = sheets.get_hot_leads()
    # print(f"Found {len(hot_leads)} HOT leads")
