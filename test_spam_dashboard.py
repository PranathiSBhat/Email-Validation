#!/usr/bin/env python3
"""
Test script for the spam detection dashboard
"""

import requests
import json
import time

# Test data
test_texts = [
    "Congratulations! You've won $1000! Click here to claim your prize now!",
    "Hi, how are you doing today? I hope you're having a great week.",
    "URGENT: Your account will be suspended unless you verify your information immediately!",
    "Thanks for your email. I'll get back to you by tomorrow.",
    "FREE MONEY! No strings attached! Get rich quick with this amazing opportunity!"
]

def test_spam_prediction():
    """Test the spam prediction API"""
    print("🧪 Testing Spam Prediction API...")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text[:50]}...")
        
        try:
            response = requests.post(
                f"{base_url}/api/spam/predict",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"]
                confidence = result["confidence"]
                is_spam = result["is_spam"]
                
                print(f"✅ Prediction: {prediction}")
                print(f"   Confidence - Ham: {confidence['ham']}%, Spam: {confidence['spam']}%")
                print(f"   Is Spam: {is_spam}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the Flask app is running on http://127.0.0.1:5000")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            
        time.sleep(0.5)  # Small delay between requests
    
    return True

def test_metrics_api():
    """Test the metrics API"""
    print("\n\n📊 Testing Metrics API...")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        response = requests.get(f"{base_url}/api/spam/metrics")
        
        if response.status_code == 200:
            metrics = response.json()
            print("✅ Metrics loaded successfully:")
            print(f"   Accuracy: {metrics['accuracy']:.4f}")
            print(f"   Precision: {metrics['precision']:.4f}")
            print(f"   Recall: {metrics['recall']:.4f}")
            print(f"   F1 Score: {metrics['f1_score']:.4f}")
            print(f"   Total Samples: {metrics['total_samples']}")
            print(f"   Confusion Matrix: {metrics['confusion_matrix']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        
    return True

def test_results_api():
    """Test the results API"""
    print("\n\n📋 Testing Results API...")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        response = requests.get(f"{base_url}/api/spam/results")
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Results loaded successfully: {len(results)} records found")
            
            if results:
                print("\nRecent results:")
                for i, result in enumerate(results[:3], 1):  # Show first 3 results
                    text_preview = result['email_text'][:50] + "..." if len(result['email_text']) > 50 else result['email_text']
                    prediction = "Spam" if result['xgboost_pred'] == 1 else "Ham"
                    print(f"   {i}. {text_preview} -> {prediction}")
            else:
                print("   No results found. Make some predictions first.")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        
    return True

def main():
    """Run all tests"""
    print("🚀 Spam Detection Dashboard Test Suite")
    print("=" * 60)
    print("Make sure the Flask app is running before running these tests!")
    print("Run: python run_app.py")
    print("=" * 60)
    
    # Test all APIs
    success = True
    
    success &= test_spam_prediction()
    success &= test_metrics_api()
    success &= test_results_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests completed! Check the dashboard at http://127.0.0.1:5000/spam-dashboard")
    else:
        print("❌ Some tests failed. Check the Flask app logs for errors.")
    print("=" * 60)

if __name__ == "__main__":
    main()

