"""
PDF Generation Testing Script
Tests all 6 FastSewa services with sample data
"""

import pdf_generator
from datetime import datetime

# =============================================
# TEST DATA
# =============================================

test_users = [
    {
        'full_name': 'Amit Sharma',
        'phone': '+91-9876543210',
        'address': 'Sector 22, Noida, UP'
    },
    {
        'full_name': 'Priya Singh',
        'phone': '+91-9123456789',
        'address': 'Koramangala, Bangalore'
    },
    {
        'full_name': 'Rajesh Kumar',
        'phone': '+91-9988776655',
        'address': 'Civil Lines, Delhi'
    }
]

test_enquiries = [
    # Test 1: Construction
    {
        'id': 1001,
        'service_type': 'FS_BUILD',
        'form_data': {
            'requirements': 'Modern 3BHK Residential House with 2-floor design',
            'budget_range': '₹50-60 Lakhs',
            'plot_area': '2000 sqft'
        }
    },
    
    # Test 2: Security
    {
        'id': 1002,
        'service_type': 'FS_SECURE',
        'form_data': {
            'requirements': 'Round-the-clock security for residential society',
            'budget_range': '₹30,000/month',
            'property_type': 'Residential Society',
            'guard_count': '3'
        }
    },
    
    # Test 3: Medical
    {
        'id': 1003,
        'service_type': 'FS_MEDICAL',
        'form_data': {
            'requirements': 'Home nursing care for elderly patient',
            'budget_range': 'As per consultation',
            'symptoms': 'Post-surgery recovery care needed'
        }
    },
    
    # Test 4: Legal & GST
    {
        'id': 1004,
        'service_type': 'FS_LEGAL',
        'form_data': {
            'requirements': 'GST Registration for new startup',
            'budget_range': '₹5,000-8,000'
        }
    },
    
    # Test 5: Land Verification
    {
        'id': 1005,
        'service_type': 'FS_LAND',
        'form_data': {
            'requirements': 'Complete legal verification of agricultural land',
            'budget_range': '₹15,000-20,000'
        }
    },
    
    # Test 6: Repair
    {
        'id': 1006,
        'service_type': 'FS_REPAIR',
        'form_data': {
            'requirements': 'AC repair and electrical wiring check',
            'budget_range': 'Inspection free, repair charges as applicable'
        }
    }
]

# =============================================
# RUN TESTS
# =============================================

def run_all_tests():
    print("\n" + "="*60)
    print("🧪 FASTSEWA PDF GENERATION - COMPREHENSIVE TEST")
    print("="*60 + "\n")
    
    results = {"success": 0, "failed": 0}
    
    for idx, (user, enquiry) in enumerate(zip(test_users * 2, test_enquiries), 1):
        service_name = pdf_generator.get_service_name(enquiry['service_type'])
        
        print(f"Test {idx}: {service_name}")
        print("-" * 60)
        
        result = pdf_generator.generate_invoice(user, enquiry)
        print(result)
        
        if "✅" in result:
            results["success"] += 1
        else:
            results["failed"] += 1
        
        print("\n")
    
    # Summary
    print("="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Successful: {results['success']}/{len(test_enquiries)}")
    print(f"❌ Failed: {results['failed']}/{len(test_enquiries)}")
    
    if results['failed'] == 0:
        print("\n🎉 All tests passed! PDF generation is working perfectly.")
    else:
        print("\n⚠️ Some tests failed. Check error messages above.")
    
    print("="*60 + "\n")

# =============================================
# INTERACTIVE TEST MODE
# =============================================

def interactive_test():
    print("\n🔧 INTERACTIVE PDF TEST MODE")
    print("Enter custom data or type 'auto' for automated test\n")
    
    choice = input("Choice (auto/custom): ").strip().lower()
    
    if choice == 'auto':
        run_all_tests()
    else:
        print("\n📝 Enter Customer Details:")
        user = {
            'full_name': input("Name: "),
            'phone': input("Phone: "),
            'address': input("Address: ")
        }
        
        print("\n📋 Enter Service Details:")
        enquiry = {
            'id': input("Quote ID (e.g., 1001): "),
            'service_type': input("Service Code (FS_BUILD/FS_SECURE/etc.): "),
            'form_data': {
                'requirements': input("Requirements: "),
                'budget_range': input("Budget: ")
            }
        }
        
        result = pdf_generator.generate_invoice(user, enquiry)
        print("\n" + result)

# =============================================
# MAIN EXECUTION
# =============================================

if __name__ == "__main__":
    try:
        run_all_tests()
        
        # Optional: Uncomment for interactive mode
        # interactive_test()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
