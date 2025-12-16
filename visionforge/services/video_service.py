"""VisionForge - Video Service for Slideshow Export"""
import requests
from io import BytesIO
from PIL import Image
import os
import tempfile


def download_image_for_video(url: str, output_path: str) -> str:
    """Download image and save locally for video processing"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    img.save(output_path)
    return output_path


def create_slideshow_video(
    scenes: list,
    output_path: str,
    duration_per_scene: float = 4.0,
    transition_duration: float = 1.0,
    resolution: tuple = (1920, 1080),
    fps: int = 24,
    add_ken_burns: bool = True,
    music_path: str = None
) -> str:
    """Create slideshow video with transitions using moviepy

    Args:
        scenes: List of scene dicts with image_url and title
        output_path: Output video path
        duration_per_scene: How long each scene shows
        transition_duration: Fade transition duration
        resolution: Video resolution
        fps: Frames per second
        add_ken_burns: Add subtle zoom/pan effect
        music_path: Optional background music

    Returns:
        Path to video file
    """
    try:
        from moviepy.editor import (
            ImageClip, concatenate_videoclips, CompositeVideoClip,
            AudioFileClip, TextClip
        )
    except ImportError:
        raise ImportError(
            "moviepy is required for video export. "
            "Install it with: pip install moviepy"
        )

    clips = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, scene in enumerate(scenes):
            # Download image
            img_path = os.path.join(tmpdir, f"scene_{i}.png")
            download_image_for_video(scene.image_url, img_path)

            # Create clip
            clip = ImageClip(img_path).set_duration(duration_per_scene)

            # Resize to fit resolution
            clip = clip.resize(height=resolution[1])
            if clip.w < resolution[0]:
                clip = clip.resize(width=resolution[0])

            # Center crop to exact resolution
            clip = clip.crop(
                x_center=clip.w/2, y_center=clip.h/2,
                width=resolution[0], height=resolution[1]
            )

            # Add fade in/out
            clip = clip.fadein(transition_duration).fadeout(transition_duration)

            # Add title overlay
            title = scene.title if hasattr(scene, 'title') else f"Scene {i+1}"
            try:
                txt_clip = TextClip(
                    title,
                    fontsize=48,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2
                ).set_position(('center', 'bottom')).set_duration(duration_per_scene)
                txt_clip = txt_clip.margin(bottom=50, opacity=0)

                # Composite with title
                final_clip = CompositeVideoClip([clip, txt_clip])
            except Exception:
                # If text fails, just use the image clip
                final_clip = clip

            clips.append(final_clip)

        # Concatenate all clips
        video = concatenate_videoclips(clips, method="compose")

        # Add background music if provided
        if music_path and os.path.exists(music_path):
            try:
                audio = AudioFileClip(music_path)
                # Loop or trim audio to match video duration
                if audio.duration < video.duration:
                    audio = audio.loop(duration=video.duration)
                else:
                    audio = audio.subclip(0, video.duration)
                audio = audio.volumex(0.3)  # Lower volume
                video = video.set_audio(audio)
            except Exception:
                pass  # Skip audio if it fails

        # Write video file
        video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='medium'
        )

    return output_path


def create_slideshow_gif(
    scenes: list,
    output_path: str,
    duration_per_scene: int = 3000,
    resolution: tuple = (800, 450)
) -> str:
    """Create slideshow GIF (fallback when moviepy not available)

    Args:
        scenes: List of scene objects with image_url
        output_path: Output GIF path
        duration_per_scene: Duration per frame in milliseconds
        resolution: GIF resolution

    Returns:
        Path to GIF file
    """
    frames = []

    for scene in scenes:
        # Download image
        response = requests.get(scene.image_url)
        img = Image.open(BytesIO(response.content)).convert('RGB')

        # Resize to fit resolution while maintaining aspect ratio
        img.thumbnail(resolution, Image.Resampling.LANCZOS)

        # Create canvas and center the image
        canvas = Image.new('RGB', resolution, (26, 26, 46))  # Dark background
        x = (resolution[0] - img.width) // 2
        y = (resolution[1] - img.height) // 2
        canvas.paste(img, (x, y))

        frames.append(canvas)

    # Save as GIF
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_per_scene,
            loop=0
        )

    return output_path


def export_slideshow(scenes: list, output_dir: str, music_path: str = None) -> str:
    """Export scenes as slideshow video or GIF

    Args:
        scenes: List of scene objects
        output_dir: Output directory
        music_path: Optional music file path

    Returns:
        Path to video/gif file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Try video first, fall back to GIF
    try:
        output_path = os.path.join(output_dir, "visionforge_slideshow.mp4")
        return create_slideshow_video(scenes, output_path, music_path=music_path)
    except ImportError:
        # Fall back to GIF if moviepy not available
        output_path = os.path.join(output_dir, "visionforge_slideshow.gif")
        return create_slideshow_gif(scenes, output_path)
