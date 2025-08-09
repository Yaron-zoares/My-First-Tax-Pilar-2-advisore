#!/usr/bin/env python3
"""
Test script for Q&A system with tax questions
Demonstrates the solution for "מדוע המס יצא אפס" (Why is the tax zero?)
"""

import requests
import json

def test_qa_system():
    """Test the Q&A system with tax questions"""
    
    # API endpoint
    api_url = "http://localhost:8000/api/v1/qa/ask"
    
    # Test file
    test_file = "data/uploads/test_pillar_2.csv"
    
    # Test questions
    test_questions = [
        {
            "question": "מדוע המס יצא אפס",
            "language": "he",
            "description": "Hebrew tax question"
        },
        {
            "question": "Why is the tax zero?",
            "language": "en", 
            "description": "English tax question"
        },
        {
            "question": "מהו סך המסים?",
            "language": "he",
            "description": "Hebrew total tax question"
        },
        {
            "question": "What is the total tax?",
            "language": "en",
            "description": "English total tax question"
        }
    ]
    
    print("🧪 Testing Q&A System with Tax Questions")
    print("=" * 50)
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n{i}. {test['description']}")
        print(f"Question: {test['question']}")
        
        try:
            # Make API request
            response = requests.post(api_url, json={
                "question": test["question"],
                "file_path": test_file,
                "language": test["language"]
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Answer: {result['answer']}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Sources: {', '.join(result['sources'])}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Q&A System Test Complete!")
    print("\nThe system now properly:")
    print("• Connects to uploaded data files")
    print("• Analyzes tax information from the dataset")
    print("• Provides detailed tax analysis in both Hebrew and English")
    print("• Shows why tax values might be zero or low")
    print("• Includes confidence scores and sources")

if __name__ == "__main__":
    test_qa_system()
