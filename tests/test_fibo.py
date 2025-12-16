"""Test FIBO API via Bria"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import requests

load_dotenv()

BRIA_API_URL = "https://engine.prod.bria-api.com/v2/image/generate"


def test_bria_connection():
    """Test FIBO API connection via Bria"""
    api_token = os.getenv("BRIA_API_TOKEN")

    if not api_token or api_token == "your_bria_api_token_here":
        print("❌ BRIA_API_TOKEN not configured in .env file")
        print("   Get your token from: https://platform.bria.ai/")
        return False

    try:
        print("🎨 Generating test image with FIBO via Bria API...")
        print("   (This may take 10-30 seconds)")

        headers = {
            "Content-Type": "application/json",
            "api_token": api_token
        }

        payload = {
            "prompt": "anime girl with bright blue hair, gentle smile, cherry blossoms background, soft lighting, portrait shot, high quality",
            "model_version": "FIBO",
            "aspect_ratio": "1:1",
            "sync": True,
            "guidance_scale": 5,
            "steps_num": 50
        }

        response = requests.post(BRIA_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        image_url = result["result"]["image_url"]

        print("✅ Bria FIBO API Connected!")
        print(f"   Image URL: {image_url}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ Bria API HTTP Error: {e}")
        print(f"   Response: {e.response.text if e.response else 'No response'}")
        return False
    except Exception as e:
        print(f"❌ Bria API Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Testing FIBO API Connection (via Bria)")
    print("=" * 50)

    print("\nGenerating test image...")
    test_bria_connection()

    print("\n" + "=" * 50)
