"""Gemini LLM Service for story parsing and DNA extraction"""
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

STORY_PARSER_PROMPT = '''You are a story analyst for visual media production (anime, film, games).
Analyze the following story and extract:

1. CHARACTERS: List each character with detailed visual descriptions
2. SCENES: Break the story into 4-6 visual scenes

Return ONLY valid JSON in this exact format:
{
  "characters": [
    {
      "id": "char_01",
      "name": "Character Name",
      "description": "Detailed visual description including: hair color/style, eye color/shape, face structure, skin tone, body type, clothing, accessories, any distinctive features"
    }
  ],
  "scenes": [
    {
      "id": "scene_01",
      "title": "Scene Title",
      "description": "What happens in this scene",
      "visual_direction": "Detailed visual description including: setting, time of day, lighting, mood, camera angle, character poses/expressions",
      "characters_present": ["char_01"]
    }
  ]
}

IMPORTANT:
- Be extremely detailed about character visual features
- Include specific colors, styles, and distinguishing marks
- Each scene should have clear visual direction for image generation
'''


def parse_story(story_text: str, style: str = "anime") -> dict:
    """Parse a story into characters and scenes using Gemini

    Args:
        story_text: The story/concept to parse
        style: Visual style (anime, realistic, sci-fi, fantasy)

    Returns:
        Dictionary with characters and scenes
    """
    model = genai.GenerativeModel('gemini-2.0-flash')

    style_context = f"\nTarget visual style: {style}\n"

    full_prompt = STORY_PARSER_PROMPT + style_context + "\n\nSTORY TO ANALYZE:\n" + story_text

    response = model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        text = response.text
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
        raise ValueError("Could not parse Gemini response as JSON")


STORY_NAME_PROMPT = '''Generate a short, creative title for this story (2-4 words max).
The title should capture the essence of the story in a memorable way.

Story:
{story}

Return ONLY the title, nothing else. No quotes, no explanation.
Examples of good titles: "Samurai's Spirit", "Neo Tokyo Dreams", "Crystal Mage", "Starship Alliance"
'''


def generate_story_name(story_text: str) -> str:
    """Generate a short creative name for a story using Gemini

    Args:
        story_text: The story content

    Returns:
        A short creative title (2-4 words)
    """
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Truncate story if too long
    truncated = story_text[:500] if len(story_text) > 500 else story_text
    prompt = STORY_NAME_PROMPT.replace("{story}", truncated)

    try:
        response = model.generate_content(prompt)
        name = response.text.strip().strip('"\'')
        # Ensure it's not too long
        if len(name) > 30:
            name = name[:30]
        return name if name else "Untitled Story"
    except Exception:
        return "Untitled Story"


DNA_EXTRACTION_PROMPT = '''Analyze this character image and extract detailed visual features for consistent reproduction.

Return ONLY valid JSON in this exact format:
{
  "name": "{name}",
  "physical_features": {
    "hair": {
      "color": "specific color with any highlights or gradients",
      "style": "length, cut, texture, distinctive features",
      "texture": "sleek, wavy, curly, etc."
    },
    "eyes": {
      "color": "specific color including any special features like glow",
      "shape": "shape and size description",
      "features": "any special features like cybernetic elements"
    },
    "face": {
      "structure": "face shape and key features",
      "skin_tone": "skin color description with undertones",
      "distinctive_marks": "scars, marks, tattoos, or 'none'"
    },
    "body": {
      "build": "body type description",
      "height_impression": "tall/average/short",
      "posture": "characteristic posture or stance"
    }
  },
  "clothing": {
    "default_outfit": "detailed description of outfit",
    "accessories": ["list", "of", "accessories"],
    "weapons": "any weapons or tools, or 'none'"
  },
  "style_attributes": {
    "art_style": "anime/realistic/stylized/etc",
    "shading": "type of shading used",
    "color_palette": ["#hex1", "#hex2", "#hex3", "#hex4"]
  },
  "personality_visual_cues": {
    "default_expression": "typical expression",
    "stance": "characteristic body language"
  }
}

Be VERY specific and detailed - this will be used to recreate the character consistently across multiple scenes.
Character name: {name}
'''


def extract_character_dna(image_data, character_name: str) -> dict:
    """Extract Character DNA from an image using Gemini Vision

    Args:
        image_data: PIL Image object or image bytes
        character_name: Name of the character

    Returns:
        Character DNA dictionary
    """
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = DNA_EXTRACTION_PROMPT.replace("{name}", character_name)

    response = model.generate_content(
        [prompt, image_data],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        text = response.text
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
        raise ValueError("Could not parse DNA extraction response as JSON")


DIALOG_GENERATION_PROMPT = '''You are a manga/manhwa dialog writer. Based on the scene description and characters, generate appropriate dialog and narration.

Scene: {scene_description}
Characters in scene: {characters}
Format: {format}

Generate dialog that fits the scene. Return ONLY valid JSON in this format:
{{
  "dialogs": [
    {{
      "speaker": "Character Name or NARRATOR",
      "text": "The dialog or narration text",
      "type": "speech" or "thought" or "narration"
    }}
  ]
}}

Guidelines:
- For manga: Short, punchy dialog with dramatic pauses
- For manhwa: More flowing, emotional dialog
- Include 2-4 dialog entries per scene
- Keep each text under 50 words
- Match the tone of the scene (action, emotional, comedic, etc.)
'''


def generate_scene_dialog(scene_description: str, characters: list, format_type: str = "manga") -> list:
    """Generate dialog for a scene using Gemini

    Args:
        scene_description: Description of what happens in the scene
        characters: List of character names present in the scene
        format_type: "manga" or "manhwa"

    Returns:
        List of dialog dictionaries with speaker, text, and type
    """
    model = genai.GenerativeModel('gemini-2.0-flash')

    characters_str = ", ".join(characters) if characters else "Unknown characters"
    prompt = DIALOG_GENERATION_PROMPT.format(
        scene_description=scene_description,
        characters=characters_str,
        format=format_type
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)
        return result.get("dialogs", [])
    except Exception as e:
        print(f"Error generating dialog: {e}")
        # Return default dialog
        return [{"speaker": "NARRATOR", "text": scene_description[:100], "type": "narration"}]


# Test
if __name__ == "__main__":
    test_story = """
    A cyberpunk samurai named Kaito with silver hair and glowing red eyes
    wanders through Neo Tokyo. He encounters a mysterious girl named Yuki
    with purple hair who claims to know his forgotten past.
    """

    print("Testing story parser...")
    result = parse_story(test_story)
    print(json.dumps(result, indent=2))
