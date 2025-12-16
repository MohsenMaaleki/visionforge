"""Test Gemini API connection"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_gemini_connection():
    """Test basic Gemini API connection"""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ GOOGLE_API_KEY not configured in .env file")
        print("   Get your key from: https://aistudio.google.com/apikey")
        return False

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Say 'Gemini is working!' in a fun way")
        print("✅ Gemini API Connected!")
        print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False


def test_gemini_json_output():
    """Test Gemini JSON output mode"""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ GOOGLE_API_KEY not configured")
        return False

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        response = model.generate_content(
            "Return a JSON object with keys 'name' and 'status'. Name should be 'VisionForge' and status should be 'ready'.",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        import json
        result = json.loads(response.text)
        print("✅ Gemini JSON Mode Working!")
        print(f"   Response: {result}")
        return True
    except Exception as e:
        print(f"❌ Gemini JSON Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Gemini API Connection")
    print("=" * 50)

    print("\n1. Testing basic connection...")
    test_gemini_connection()

    print("\n2. Testing JSON output mode...")
    test_gemini_json_output()

    print("\n" + "=" * 50)
