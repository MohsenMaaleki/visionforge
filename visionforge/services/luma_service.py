"""VisionForge - Luma AI Video Service"""
import requests
import time
import os
from typing import Optional

# Luma AI Dream Machine API
LUMA_API_URL = "https://api.lumalabs.ai/dream-machine/v1"


class LumaVideoService:
    """Luma AI Dream Machine service for image-to-video generation"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_video_from_image(
        self,
        image_url: str,
        prompt: str = "",
        aspect_ratio: str = "16:9"
    ) -> dict:
        """Generate video from an image using Luma AI

        Args:
            image_url: URL of the source image
            prompt: Optional motion/action prompt
            aspect_ratio: Video aspect ratio

        Returns:
            Dict with video URL and metadata
        """
        payload = {
            "prompt": prompt or "subtle gentle motion, cinematic",
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": image_url
                }
            },
            "aspect_ratio": aspect_ratio,
            "loop": False
        }

        # Create generation request
        response = requests.post(
            f"{LUMA_API_URL}/generations",
            headers=self.headers,
            json=payload
        )

        if response.status_code != 201:
            raise Exception(f"Luma API error: {response.text}")

        generation = response.json()
        generation_id = generation["id"]

        # Poll for completion
        return self._wait_for_completion(generation_id)

    def _wait_for_completion(
        self,
        generation_id: str,
        max_wait: int = 300,
        poll_interval: int = 5
    ) -> dict:
        """Wait for video generation to complete

        Args:
            generation_id: The generation ID to poll
            max_wait: Maximum seconds to wait
            poll_interval: Seconds between polls

        Returns:
            Completed generation dict with video URL
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            response = requests.get(
                f"{LUMA_API_URL}/generations/{generation_id}",
                headers=self.headers
            )

            if response.status_code != 200:
                raise Exception(f"Luma API error: {response.text}")

            generation = response.json()
            state = generation.get("state")

            if state == "completed":
                return {
                    "video_url": generation["assets"]["video"],
                    "thumbnail_url": generation["assets"].get("thumbnail"),
                    "generation_id": generation_id,
                    "state": "completed"
                }
            elif state == "failed":
                raise Exception(f"Video generation failed: {generation.get('failure_reason')}")

            # Still processing
            time.sleep(poll_interval)

        raise Exception("Video generation timed out")

    def download_video(self, video_url: str, output_path: str) -> str:
        """Download generated video to local file

        Args:
            video_url: URL of the video
            output_path: Local path to save

        Returns:
            Path to saved video
        """
        response = requests.get(video_url, stream=True)

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return output_path


def generate_story_video(
    scenes: list,
    api_key: str,
    output_dir: str,
    motion_prompts: Optional[list] = None,
    progress_callback=None
) -> list:
    """Generate AI videos for each scene

    Args:
        scenes: List of scene objects with image_url
        api_key: Luma API key
        output_dir: Where to save videos
        motion_prompts: Optional list of motion descriptions
        progress_callback: Optional callback for progress updates

    Returns:
        List of video file paths
    """
    os.makedirs(output_dir, exist_ok=True)

    luma = LumaVideoService(api_key)
    video_paths = []

    # Default motion prompts if not provided
    if not motion_prompts:
        motion_prompts = [
            "gentle camera movement, subtle animation",
            "soft wind blowing, slight movement",
            "cinematic slow motion, atmospheric",
            "gentle zoom, particles floating",
            "serene movement, peaceful animation"
        ]

    for i, scene in enumerate(scenes):
        if progress_callback:
            progress_callback(f"Generating AI video {i+1}/{len(scenes)}...")

        prompt = motion_prompts[i % len(motion_prompts)]
        if hasattr(scene, 'title') and scene.title:
            prompt = f"{scene.title}, {prompt}"

        try:
            result = luma.generate_video_from_image(
                image_url=scene.image_url,
                prompt=prompt
            )

            # Download video
            output_path = os.path.join(output_dir, f"scene_{i+1}_video.mp4")
            luma.download_video(result["video_url"], output_path)
            video_paths.append(output_path)

        except Exception as e:
            print(f"Error on scene {i+1}: {e}")
            video_paths.append(None)

    return video_paths


def combine_scene_videos(
    video_paths: list,
    output_path: str,
    transition_duration: float = 0.5
) -> str:
    """Combine individual scene videos into one story video

    Args:
        video_paths: List of video file paths
        output_path: Output combined video path
        transition_duration: Crossfade duration

    Returns:
        Path to combined video
    """
    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips
    except ImportError:
        raise ImportError("moviepy is required to combine videos")

    clips = []
    for path in video_paths:
        if path and os.path.exists(path):
            clip = VideoFileClip(path)
            clip = clip.fadein(transition_duration).fadeout(transition_duration)
            clips.append(clip)

    if not clips:
        raise Exception("No valid video clips to combine")

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )

    return output_path


def export_luma_video(
    scenes: list,
    api_key: str,
    output_dir: str,
    progress_callback=None
) -> str:
    """Full Luma AI video export pipeline

    Args:
        scenes: List of scene objects
        api_key: Luma API key
        output_dir: Output directory
        progress_callback: Optional callback for progress updates

    Returns:
        Path to final video
    """
    # Generate individual videos
    video_paths = generate_story_video(
        scenes, api_key, output_dir,
        progress_callback=progress_callback
    )

    # Filter out failed generations
    valid_paths = [p for p in video_paths if p]

    if not valid_paths:
        raise Exception("All video generations failed")

    # If only one video, return it
    if len(valid_paths) == 1:
        return valid_paths[0]

    # Combine into one video
    try:
        final_path = os.path.join(output_dir, "visionforge_ai_video.mp4")
        return combine_scene_videos(valid_paths, final_path)
    except ImportError:
        # If moviepy not available, return first video
        return valid_paths[0]
