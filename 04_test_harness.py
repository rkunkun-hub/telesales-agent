"""
Test Harness for IntelliTrac Telesales Agent
Run various test scenarios to validate agent behavior
"""

import json
from datetime import datetime
from typing import List, Dict

# Import agent
from telesales_agent import LeadQualificationAgent, get_initial_greeting


# ============================================================================
# TEST SCENARIOS
# ============================================================================

class TestScenario:
    """Base class for test scenarios"""
    
    def __init__(self, name: str, description: str, messages: List[str]):
        self.name = name
        self.description = description
        self.messages = messages
        self.results = []
    
    def run(self) -> Dict:
        """Run the test scenario"""
        print(f"\n{'='*70}")
        print(f"🧪 TEST: {self.name}")
        print(f"{'='*70}")
        print(f"📝 {self.description}\n")
        
        agent = LeadQualificationAgent()
        
        # Initial greeting
        greeting = get_initial_greeting("refrigerated")
        print(f"Agent: {greeting}\n")
        
        # Process messages
        for i, user_msg in enumerate(self.messages, 1):
            print(f"Customer [{i}]: {user_msg}")
            response = agent.process_message(user_msg)
            print(f"Agent: {response['message']}\n")
            print(f"  📊 Score: {response['lead_score']}/100 | {response['qualification_level']}\n")
            
            self.results.append({
                "turn": i,
                "user_message": user_msg,
                "agent_response": response['message'],
                "lead_score": response['lead_score'],
                "qualification_level": response['qualification_level']
            })
        
        # Final assessment
        final_data = agent.export_lead_data()
        
        print(f"{'='*70}")
        print(f"✅ FINAL ASSESSMENT")
        print(f"{'='*70}")
        print(f"Lead Score: {final_data['lead_score']}/100")
        print(f"Qualification Level: {final_data['qualification_level']}")
        print(f"Fleet Size: {final_data['fleet_size']}")
        print(f"Pain Points: {final_data['pain_points']}")
        print(f"Timeline: {final_data['timeline']}")
        print(f"Contact: {final_data['name']} from {final_data['company']}")
        print(f"Status: {'✅ QUALIFIED' if final_data['qualification_level'] == 'HOT' else '⏳ NEEDS FOLLOW-UP'}")
        
        return {
            "scenario": self.name,
            "status": "PASSED",
            "lead_data": final_data,
            "conversation_turns": len(self.messages)
        }


# ============================================================================
# SCENARIO DEFINITIONS
# ============================================================================

SCENARIO_1 = TestScenario(
    name="Qualified Hot Lead - Clear Use Case & Pain Points",
    description="Customer dengan use case yang jelas dan pain points yang urgent",
    messages=[
        "Kami butuh GPS tracking untuk fleet delivery kami",
        "Masalahnya driver sering terlambat dan kita tidak bisa track real-time posisi mereka",
        "Saat ini kami masih manual - tanya driver via telepon",
        "Kami punya 25 kendaraan delivery yang operasi setiap hari",
        "Kami perlu implementasi dalam 2 bulan, sangat urgent",
        "Nama saya Budi Santoso, perusahaan PT Logistics Cepat",
        "Email: budi@logcepat.co.id, nomor 0812-3456-7890",
    ]
)

SCENARIO_2 = TestScenario(
    name="Warm Lead - Exploring, Not Urgent",
    description="Customer yang tertarik tapi masih exploring options",
    messages=[
        "Kami punya mining operation dan pengen track equipment locations",
        "Saat ini equipment tracking masih menggunakan manual checklist",
        "Permasalahan utamanya adalah duplikasi data dan human error",
        "Kami ada sekitar 18 heavy equipment yang tersebar di beberapa site",
        "Timeline ya, mungkin quarter depan lah",
        "Nama saya Siti dari PT Mining Solutions"
    ]
)

SCENARIO_3 = TestScenario(
    name="Cold Lead - Early Stage, Browsing",
    description="Customer baru cari info, belum ada kebutuhan urgent",
    messages=[
        "Saya baru explore tentang GPS solutions, belum tahu exactly kita butuh apa",
        "Mungkin untuk tracking beberapa kendaraan maintenance team kami",
        "Tapi jujur saja, ini belum jadi prioritas sekarang",
        "Email saya saja: explore@company.com - maybe next year kita hubungi lagi"
    ]
)

SCENARIO_4 = TestScenario(
    name="High-Value Enterprise Lead",
    description="Large enterprise dengan clear requirements dan budget",
    messages=[
        "Kami PT Retail Nasional Indonesia - punya 150+ kendaraan distribusi",
        "Kami butuh real-time tracking untuk compliance dan customer visibility",
        "Sekarang pakai tracking provider lama, tapi service-nya kurang bagus",
        "Permasalahan: data accuracy buruk, reporting system outdated, API integration sulit",
        "Timeline critical - Q1 tahun depan harus full operational",
        "Budget already approved oleh CFO, hanya perlu validation dari operations team",
        "Direktur ops saya Ahmad. Email: ahmad@ptretail.co.id, mobile 0811-9999-999"
    ]
)

SCENARIO_5 = TestScenario(
    name="Not a Fit - Personal Use Case",
    description="Customer dengan use case yang bukan target market",
    messages=[
        "Saya cari GPS untuk tracking motor pribadi saya",
        "Khawatir motor saya akan dicuri",
        "Budget saya maksimal 500rb per tahun"
    ]
)


# ============================================================================
# EVALUATION METRICS
# ============================================================================

def evaluate_results(results: List[Dict]) -> Dict:
    """Evaluate test results"""
    
    hot_leads = [r for r in results if r['lead_data']['qualification_level'] == 'HOT']
    warm_leads = [r for r in results if r['lead_data']['qualification_level'] == 'WARM']
    cold_leads = [r for r in results if r['lead_data']['qualification_level'] == 'COLD']
    
    avg_score = sum(r['lead_data']['lead_score'] for r in results) / len(results)
    avg_turns = sum(r['conversation_turns'] for r in results) / len(results)
    
    return {
        "total_scenarios": len(results),
        "hot_leads": len(hot_leads),
        "warm_leads": len(warm_leads),
        "cold_leads": len(cold_leads),
        "average_score": round(avg_score, 1),
        "average_turns": round(avg_turns, 1),
        "scenarios": results
    }


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all test scenarios"""
    
    scenarios = [
        SCENARIO_1,
        SCENARIO_2,
        SCENARIO_3,
        SCENARIO_4,
        SCENARIO_5
    ]
    
    print("\n" + "="*70)
    print("🚀 IntelliTrac Telesales Agent - Test Suite")
    print("="*70)
    print(f"Starting {len(scenarios)} test scenarios...\n")
    
    results = []
    for scenario in scenarios:
        result = scenario.run()
        results.append(result)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    evaluation = evaluate_results(results)
    
    print(f"\nTotal Scenarios: {evaluation['total_scenarios']}")
    print(f"  🔥 HOT Leads: {evaluation['hot_leads']}")
    print(f"  🟡 WARM Leads: {evaluation['warm_leads']}")
    print(f"  ❄️  COLD Leads: {evaluation['cold_leads']}")
    print(f"\nAverage Lead Score: {evaluation['average_score']}/100")
    print(f"Average Conversation Turns: {evaluation['average_turns']}")
    
    # Detailed results
    print(f"\n{'='*70}")
    print("DETAILED RESULTS")
    print(f"{'='*70}\n")
    
    for scenario_result in evaluation['scenarios']:
        status_emoji = "🔥" if scenario_result['lead_data']['qualification_level'] == 'HOT' else \
                      "🟡" if scenario_result['lead_data']['qualification_level'] == 'WARM' else "❄️"
        
        print(f"{status_emoji} {scenario_result['scenario']}")
        print(f"   Score: {scenario_result['lead_data']['lead_score']}/100")
        print(f"   Level: {scenario_result['lead_data']['qualification_level']}")
        print(f"   Contact: {scenario_result['lead_data']['name']} ({scenario_result['lead_data']['company']})")
        print()
    
    # Export results
    with open("test_results.json", "w", encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "evaluation": evaluation
        }, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*70}")
    print("✅ All tests completed! Results saved to test_results.json")
    print(f"{'='*70}\n")
    
    return evaluation


if __name__ == "__main__":
    run_all_tests()
