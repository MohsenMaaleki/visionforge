"""VisionForge - Export Service for Manga and Manhwa"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import requests
from io import BytesIO
import os
import zipfile


def download_image(url: str) -> Image.Image:
    """Download image from URL"""
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert('RGB')


def convert_to_manga_style(image: Image.Image) -> Image.Image:
    """Convert color image to manga-style black & white"""
    # Convert to grayscale
    gray = image.convert('L')

    # Increase contrast for manga look
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(1.5)

    # Apply slight posterize effect for cel-shaded look
    posterized = ImageOps.posterize(high_contrast, 4)

    return posterized.convert('RGB')


def create_manga_panel(
    images: list,
    titles: list,
    output_path: str,
    panel_size: tuple = (800, 600),
    gap: int = 10,
    border: int = 3
) -> str:
    """Create manga-style panel layout from scene images

    Args:
        images: List of image URLs
        titles: List of scene titles
        output_path: Where to save the manga page
        panel_size: Size of each panel
        gap: Gap between panels
        border: Border thickness

    Returns:
        Path to saved manga image
    """
    num_images = len(images)

    # Calculate layout (2 columns for manga)
    cols = 2
    rows = (num_images + 1) // 2

    # Calculate total size
    total_width = cols * panel_size[0] + (cols + 1) * gap
    total_height = rows * panel_size[1] + (rows + 1) * gap

    # Create white canvas
    manga_page = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(manga_page)

    # Try to load a font for titles
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for i, (img_url, title) in enumerate(zip(images, titles)):
        row = i // cols
        col = i % cols

        x = gap + col * (panel_size[0] + gap)
        y = gap + row * (panel_size[1] + gap)

        # Download and process image
        img = download_image(img_url)
        img = convert_to_manga_style(img)
        img = img.resize(panel_size, Image.Resampling.LANCZOS)

        # Draw border
        draw.rectangle(
            [x - border, y - border, x + panel_size[0] + border, y + panel_size[1] + border],
            outline='black',
            width=border
        )

        # Paste image
        manga_page.paste(img, (x, y))

        # Add title at bottom of panel
        text_y = y + panel_size[1] - 30
        draw.rectangle(
            [x, text_y, x + panel_size[0], y + panel_size[1]],
            fill='white'
        )
        draw.text((x + 10, text_y + 5), title[:40], fill='black', font=font)

    # Save
    manga_page.save(output_path, quality=95)
    return output_path


def export_manga(scenes: list, output_dir: str) -> str:
    """Export scenes as manga page(s)

    Args:
        scenes: List of scene dicts with image_url and title
        output_dir: Directory to save output

    Returns:
        Path to manga file
    """
    os.makedirs(output_dir, exist_ok=True)

    images = [s.image_url for s in scenes]
    titles = [s.title for s in scenes]

    output_path = os.path.join(output_dir, "visionforge_manga.png")

    return create_manga_panel(images, titles, output_path)


def create_manhwa_scroll(
    images: list,
    titles: list,
    descriptions: list,
    output_path: str,
    panel_width: int = 800,
    gap: int = 20
) -> str:
    """Create manhwa-style vertical scroll layout (full color)

    Args:
        images: List of image URLs
        titles: List of scene titles
        descriptions: List of scene descriptions
        output_path: Where to save
        panel_width: Width of each panel
        gap: Gap between panels

    Returns:
        Path to saved manhwa image
    """
    # Download all images first to calculate heights
    downloaded = []
    for url in images:
        img = download_image(url)
        # Resize to fixed width, maintain aspect ratio
        ratio = panel_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((panel_width, new_height), Image.Resampling.LANCZOS)
        downloaded.append(img)

    # Calculate total height (images + titles + gaps)
    title_height = 60
    desc_height = 40
    total_height = sum(img.height + title_height + desc_height + gap for img in downloaded) + gap

    # Create long vertical canvas with dark background
    manhwa = Image.new('RGB', (panel_width + gap * 2, total_height), '#1a1a2e')
    draw = ImageDraw.Draw(manhwa)

    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        desc_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()

    y = gap

    for i, (img, title, desc) in enumerate(zip(downloaded, titles, descriptions)):
        x = gap

        # Draw title
        draw.text((x, y), title, fill='white', font=title_font)
        y += title_height

        # Add subtle shadow around panel
        shadow_offset = 5
        draw.rectangle(
            [x + shadow_offset, y + shadow_offset,
             x + panel_width + shadow_offset, y + img.height + shadow_offset],
            fill='#0a0a15'
        )

        # Paste image
        manhwa.paste(img, (x, y))
        y += img.height + 10

        # Draw description (truncate if too long)
        if len(desc) > 80:
            desc = desc[:77] + "..."
        draw.text((x, y), desc, fill='#888888', font=desc_font)
        y += desc_height + gap

    # Save as high-quality image
    manhwa.save(output_path, quality=95)
    return output_path


def export_manhwa(scenes: list, output_dir: str) -> str:
    """Export scenes as manhwa vertical scroll

    Args:
        scenes: List of scene dicts with image_url, title, description
        output_dir: Directory to save output

    Returns:
        Path to manhwa file
    """
    os.makedirs(output_dir, exist_ok=True)

    images = [s.image_url for s in scenes]
    titles = [s.title for s in scenes]
    descriptions = [s.description[:100] if s.description else "" for s in scenes]

    output_path = os.path.join(output_dir, "visionforge_manhwa.png")

    return create_manhwa_scroll(images, titles, descriptions, output_path)


def export_all_images(scenes: list, characters: list, output_dir: str) -> str:
    """Export all images as a ZIP file

    Args:
        scenes: List of scene objects
        characters: List of character objects
        output_dir: Directory to save output

    Returns:
        Path to ZIP file
    """
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, "visionforge_images.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Download and add character images
        for i, char in enumerate(characters):
            if char.image_url:
                img_data = requests.get(char.image_url).content
                zipf.writestr(f"characters/{char.name}_{i+1}.png", img_data)

        # Download and add scene images
        for i, scene in enumerate(scenes):
            if scene.image_url:
                img_data = requests.get(scene.image_url).content
                safe_title = "".join(c for c in scene.title if c.isalnum() or c in (' ', '_')).strip()
                zipf.writestr(f"scenes/scene_{i+1}_{safe_title[:30]}.png", img_data)

    return zip_path
