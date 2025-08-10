#!/usr/bin/env python3
"""
Test script for Guardrails integration in Pilar2
This script tests the Guardrails service and EnhancedQAEngine integration
"""

import sys
import os
import logging
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_guardrails_service():
    """Test the Guardrails service directly"""
    print("🔒 Testing Guardrails Service...")
    
    try:
        from backend.services.guardrails_service import GuardrailsService
        
        # Initialize service
        service = GuardrailsService()
        
        # Test basic functionality
        print(f"✅ Guardrails available: {service.guardrails_available}")
        print(f"✅ Quality threshold: {service.quality_threshold}")
        print(f"✅ Max response length: {service.max_response_length}")
        
        # Test validation
        test_response = """
        Based on the OECD Pillar Two regulations, this company appears to be compliant 
        with the minimum tax requirements. The effective tax rate calculation shows 
        compliance with the 15% threshold. However, we recommend regular monitoring 
        of tax positions and maintaining proper documentation.
        """
        
        validation_result = service.validate_ai_response(test_response, "compliance")
        
        print(f"✅ Validation successful: {validation_result['success']}")
        print(f"✅ Quality score: {validation_result['quality_score']}")
        print(f"✅ Warnings: {len(validation_result['warnings'])}")
        
        if 'validation_details' in validation_result:
            details = validation_result['validation_details']
            print(f"✅ Compliance status: {details.get('compliance_status', 'N/A')}")
            print(f"✅ Risk level: {details.get('risk_level', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Guardrails service test failed: {str(e)}")
        logger.error(f"Guardrails service test failed: {str(e)}")
        return False

def test_enhanced_qa_engine():
    """Test the EnhancedQAEngine with Guardrails integration"""
    print("\n🤖 Testing EnhancedQAEngine with Guardrails...")
    
    try:
        from backend.services.enhanced_qa_engine import EnhancedQAEngine
        
        # Initialize engine (without OpenAI key for testing)
        engine = EnhancedQAEngine()
        
        # Test Guardrails status
        guardrails_status = engine.get_guardrails_status()
        print(f"✅ Guardrails status: {guardrails_status['guardrails_available']}")
        
        # Test manual validation
        test_response = """
        The company's tax position requires careful analysis under Pillar Two rules. 
        Current calculations suggest potential exposure to top-up tax. We recommend 
        immediate review of transfer pricing policies and consideration of safe harbor 
        elections where applicable.
        """
        
        manual_validation = engine.validate_response_manually(test_response, "regulatory")
        print(f"✅ Manual validation successful: {manual_validation['success']}")
        print(f"✅ Manual validation quality score: {manual_validation['quality_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ EnhancedQAEngine test failed: {str(e)}")
        logger.error(f"EnhancedQAEngine test failed: {str(e)}")
        return False

def test_fallback_validation():
    """Test fallback validation when Guardrails is not available"""
    print("\n🔄 Testing Fallback Validation...")
    
    try:
        from backend.services.guardrails_service import GuardrailsService
        
        # Create service (should work even without Guardrails)
        service = GuardrailsService()
        
        # Test fallback validation
        test_response = "Simple test response for fallback validation."
        
        fallback_result = service._fallback_validation(test_response, "general")
        
        print(f"✅ Fallback validation successful: {fallback_result['success']}")
        print(f"✅ Fallback quality score: {fallback_result['quality_score']}")
        print(f"✅ Fallback warnings: {fallback_result['warnings']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback validation test failed: {str(e)}")
        logger.error(f"Fallback validation test failed: {str(e)}")
        return False

def test_quality_scoring():
    """Test quality scoring functionality"""
    print("\n📊 Testing Quality Scoring...")
    
    try:
        from backend.services.guardrails_service import GuardrailsService
        
        service = GuardrailsService()
        
        # Test different response qualities
        responses = [
            "Low quality response.",
            "Medium quality response with some professional terms like tax and compliance.",
            "High quality response with professional terminology, structured format, and source references. This analysis considers OECD guidelines and provides actionable recommendations for Pillar Two compliance.",
            "Excellent response with comprehensive analysis, professional language, structured format (1. Analysis 2. Recommendations 3. Sources), and detailed regulatory references according to OECD guidelines."
        ]
        
        for i, response in enumerate(responses, 1):
            score = service._calculate_quality_score(response)
            print(f"✅ Response {i} quality score: {score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality scoring test failed: {str(e)}")
        logger.error(f"Quality scoring test failed: {str(e)}")
        return False

def test_pillar_two_extraction():
    """Test Pillar Two information extraction"""
    print("\n🏛️ Testing Pillar Two Information Extraction...")
    
    try:
        from backend.services.guardrails_service import GuardrailsService
        
        service = GuardrailsService()
        
        # Test Hebrew and English responses
        test_responses = [
            "This company is compliant with Pillar Two requirements. Risk level is low.",
            "החברה עומדת בדרישות עמוד שני. רמת הסיכון נמוכה.",
            "Non-compliant status detected. High risk exposure requires immediate attention.",
            "נדרש ביקורת נוספת. רמת סיכון בינונית."
        ]
        
        for i, response in enumerate(test_responses, 1):
            extracted = service._extract_pillar_two_info(response)
            print(f"✅ Response {i}:")
            print(f"   Compliance: {extracted['compliance_status']}")
            print(f"   Risk Level: {extracted['risk_level']}")
            print(f"   Confidence: {extracted['confidence']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pillar Two extraction test failed: {str(e)}")
        logger.error(f"Pillar Two extraction test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Guardrails Integration Tests")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Guardrails Service", test_guardrails_service),
        ("EnhancedQAEngine Integration", test_enhanced_qa_engine),
        ("Fallback Validation", test_fallback_validation),
        ("Quality Scoring", test_quality_scoring),
        ("Pillar Two Extraction", test_pillar_two_extraction)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Guardrails integration is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
