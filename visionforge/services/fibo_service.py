"""FIBO Image Generation Service via Bria API"""
import os
import time
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

BRIA_API_URL = "https://engine.prod.bria-api.com/v2/image/generate"
BRIA_API_TOKEN = os.getenv("BRIA_API_TOKEN", "")

# Style-specific prompt enhancements
STYLE_PROMPTS = {
    "anime": "anime style, detailed linework, vibrant colors, cel shading",
    "realistic": "photorealistic, cinematic lighting, detailed, 8k quality",
    "sci-fi": "science fiction, futuristic, high tech, cinematic, neon lighting",
    "fantasy": "fantasy art, magical, detailed illustration, epic lighting"
}


def generate_image(prompt: str, style: str = "anime", aspect_ratio: str = "1:1") -> dict:
    """Generate an image using FIBO via Bria API

    Args:
        prompt: Text description of the image
        style: Art style (anime, realistic, sci-fi, fantasy)
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, etc.)

    Returns:
        Dict with image_url, seed, and structured_prompt
    """
    style_suffix = STYLE_PROMPTS.get(style.lower(), STYLE_PROMPTS["anime"])
    full_prompt = f"{prompt}, {style_suffix}, high quality, masterpiece"

    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    payload = {
        "prompt": full_prompt,
        "model_version": "FIBO",
        "aspect_ratio": aspect_ratio,
        "sync": True,
        "guidance_scale": 5,
        "steps_num": 50
    }

    response = requests.post(BRIA_API_URL, json=payload, headers=headers)

    if response.status_code == 401:
        raise ValueError(f"Bria API authentication failed. Please check your BRIA_API_TOKEN in .env file. Get a new token at https://platform.bria.ai/")

    if not response.ok:
        error_msg = response.text[:200] if response.text else f"HTTP {response.status_code}"
        raise ValueError(f"Bria API error: {error_msg}")

    result = response.json()
    return {
        "image_url": result["result"]["image_url"],
        "seed": result["result"].get("seed"),
        "structured_prompt": result["result"].get("structured_prompt")
    }


def generate_image_async(prompt: str, style: str = "anime", aspect_ratio: str = "1:1") -> dict:
    """Generate an image asynchronously (for long operations)

    Args:
        prompt: Text description of the image
        style: Art style
        aspect_ratio: Image aspect ratio

    Returns:
        Dict with image_url, seed, and structured_prompt
    """
    style_suffix = STYLE_PROMPTS.get(style.lower(), STYLE_PROMPTS["anime"])
    full_prompt = f"{prompt}, {style_suffix}, high quality, masterpiece"

    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    payload = {
        "prompt": full_prompt,
        "model_version": "FIBO",
        "aspect_ratio": aspect_ratio,
        "sync": False,
        "guidance_scale": 5,
        "steps_num": 50
    }

    # Initial request
    response = requests.post(BRIA_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Poll for completion
    status_url = data.get("status_url")
    if status_url:
        while True:
            status_response = requests.get(status_url, headers=headers)
            status_data = status_response.json()

            if status_data.get("status") == "COMPLETED":
                return {
                    "image_url": status_data["result"]["image_url"],
                    "seed": status_data["result"].get("seed"),
                    "structured_prompt": status_data["result"].get("structured_prompt")
                }
            elif status_data.get("status") == "ERROR":
                raise Exception(f"Generation failed: {status_data.get('error')}")

            time.sleep(1)

    return data


def generate_character_portrait(description: str, style: str = "anime") -> str:
    """Generate a character portrait for DNA extraction

    Args:
        description: Detailed character description
        style: Art style

    Returns:
        URL of the generated portrait
    """
    portrait_prompt = f"{description}, character portrait, detailed face, upper body, centered composition, clean background"
    result = generate_image(portrait_prompt, style)
    return result["image_url"]


def build_character_description(dna: dict) -> str:
    """Convert Character DNA JSON to text description for prompt injection

    Args:
        dna: Character DNA dictionary

    Returns:
        Text description for use in prompts
    """
    parts = []

    # Name
    if 'name' in dna:
        parts.append(dna['name'])

    # Physical features
    if 'physical_features' in dna:
        pf = dna['physical_features']

        if 'hair' in pf:
            hair = pf['hair']
            hair_desc = f"{hair.get('color', '')} {hair.get('style', '')} hair"
            if hair.get('texture'):
                hair_desc += f" with {hair['texture']} texture"
            parts.append(hair_desc)

        if 'eyes' in pf:
            eyes = pf['eyes']
            eye_desc = f"{eyes.get('color', '')} {eyes.get('shape', '')} eyes"
            if eyes.get('features') and eyes['features'] != 'none':
                eye_desc += f" with {eyes['features']}"
            parts.append(eye_desc)

        if 'face' in pf:
            face = pf['face']
            if 'skin_tone' in face:
                parts.append(f"{face['skin_tone']} skin")
            if face.get('distinctive_marks') and face['distinctive_marks'] != 'none':
                parts.append(face['distinctive_marks'])
            if 'structure' in face:
                parts.append(face['structure'])

        if 'body' in pf:
            body = pf['body']
            if 'build' in body:
                parts.append(f"{body['build']} build")

    # Clothing
    if 'clothing' in dna:
        clothing = dna['clothing']
        if 'default_outfit' in clothing:
            parts.append(f"wearing {clothing['default_outfit']}")
        if clothing.get('accessories'):
            acc_list = clothing['accessories']
            if acc_list and acc_list[0]:
                parts.append(f"with {', '.join(acc_list)}")
        if clothing.get('weapons') and clothing['weapons'] != 'none':
            parts.append(clothing['weapons'])

    return ", ".join(filter(None, parts))


def generate_scene_with_characters(
    scene_description: str,
    character_dnas: list,
    style: str = "anime"
) -> str:
    """Generate a scene with consistent characters using their DNA

    Args:
        scene_description: Description of the scene/setting
        character_dnas: List of Character DNA dictionaries for characters in scene
        style: Art style

    Returns:
        URL of the generated image
    """
    # Build character descriptions from DNA
    char_descriptions = []
    for dna in character_dnas:
        char_desc = build_character_description(dna)
        if char_desc:
            char_descriptions.append(char_desc)

    # Combine character + scene + style
    if char_descriptions:
        full_prompt = f"{', '.join(char_descriptions)}, {scene_description}"
    else:
        full_prompt = scene_description

    # Add consistency keywords
    full_prompt += ", consistent character design, same characters throughout"

    result = generate_image(full_prompt, style, aspect_ratio="16:9")
    return result["image_url"]


def download_image(url: str) -> Image.Image:
    """Download an image from URL and return as PIL Image

    Args:
        url: Image URL

    Returns:
        PIL Image object
    """
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


# Test
if __name__ == "__main__":
    print("Testing FIBO service via Bria API...")
    print("Generating test image...")
    try:
        result = generate_image("anime samurai with silver hair, dramatic pose, sunset background")
        print(f"Generated: {result['image_url']}")
    except Exception as e:
        print(f"Error: {e}")
