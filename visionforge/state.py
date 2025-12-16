"""VisionForge - Application State"""
import reflex as rx
from pydantic import BaseModel
from typing import List, Dict
import os


class Character(BaseModel):
    """Character model for type safety"""
    id: str = ""
    name: str = ""
    description: str = ""
    image_url: str = ""


class Scene(BaseModel):
    """Scene model for type safety"""
    id: str = ""
    title: str = ""
    description: str = ""
    image_url: str = ""


class Project(BaseModel):
    """Project model for saved projects"""
    id: str = ""
    name: str = ""
    story: str = ""


class State(rx.State):
    """Application state for VisionForge"""

    # Input
    story_text: str = ""
    selected_style: str = "Anime"

    # Generated data - using typed models
    characters: List[Character] = []
    scenes: List[Scene] = []
    character_dnas: Dict[str, dict] = {}

    # UI state
    is_loading: bool = False
    error_message: str = ""
    current_step: str = ""
    generation_progress: int = 0

    # Export state
    export_loading: bool = False
    export_progress: str = ""
    luma_api_key: str = ""

    # Settings modal
    show_settings: bool = False

    # Projects
    projects: List[Project] = []
    current_project_id: str = ""

    # New story dialog
    show_new_story_dialog: bool = False
    new_story_name: str = ""

    # Delete confirmation dialog
    show_delete_dialog: bool = False
    delete_target_id: str = ""
    delete_target_name: str = ""

    # Scene preview modal
    show_scene_preview: bool = False
    preview_scene_index: int = 0

    # Export preview modals
    show_manga_preview: bool = False
    show_manhwa_preview: bool = False

    # Sidebar expanded story
    expanded_story_id: str = ""

    # Active view section: "main", "characters", "scenes", "manga", "manhwa"
    active_view: str = "main"

    # Character editing
    selected_character_id: str = ""
    show_character_editor: bool = False
    editing_character_field: str = ""  # Which field is being edited

    # Scene regeneration
    regenerating_scene_id: str = ""

    # Manga/Manhwa dialog overlays
    scene_dialogs: Dict[str, str] = {}  # scene_id -> dialog text
    editing_dialog_scene_id: str = ""
    dialog_text_input: str = ""

    # Explicit setters (required in newer Reflex)
    def set_story_text(self, value: str):
        self.story_text = value

    def set_selected_style(self, value: str):
        self.selected_style = value

    def set_luma_api_key(self, value: str):
        self.luma_api_key = value

    def set_new_story_name(self, value: str):
        self.new_story_name = value

    def set_dialog_text_input(self, value: str):
        self.dialog_text_input = value

    # View navigation methods
    def go_to_characters_view(self):
        """Navigate to characters view"""
        self.active_view = "characters"

    def go_to_scenes_view(self):
        """Navigate to scenes view"""
        self.active_view = "scenes"

    def go_to_manga_view(self):
        """Navigate to manga view"""
        self.active_view = "manga"

    def go_to_manhwa_view(self):
        """Navigate to manhwa view"""
        self.active_view = "manhwa"

    def go_to_main_view(self):
        """Navigate back to main view"""
        self.active_view = "main"

    # Character editing methods
    def open_character_editor(self, char_id: str):
        """Open character DNA editor"""
        self.selected_character_id = char_id
        self.show_character_editor = True

    def close_character_editor(self):
        """Close character DNA editor"""
        self.show_character_editor = False
        self.selected_character_id = ""
        self.editing_character_field = ""

    def get_selected_character_dna(self) -> dict:
        """Get DNA for selected character"""
        if self.selected_character_id and self.selected_character_id in self.character_dnas:
            return self.character_dnas[self.selected_character_id]
        return {}

    @rx.var
    def selected_dna_name(self) -> str:
        """Get selected character DNA name"""
        dna = self.get_selected_character_dna()
        return dna.get("name", "Unknown")

    @rx.var
    def selected_dna_hair_color(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("hair", {}).get("color", "N/A")

    @rx.var
    def selected_dna_hair_style(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("hair", {}).get("style", "N/A")

    @rx.var
    def selected_dna_eye_color(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("eyes", {}).get("color", "N/A")

    @rx.var
    def selected_dna_eye_shape(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("eyes", {}).get("shape", "N/A")

    @rx.var
    def selected_dna_skin_tone(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("face", {}).get("skin_tone", "N/A")

    @rx.var
    def selected_dna_face_structure(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("face", {}).get("structure", "N/A")

    @rx.var
    def selected_dna_body_build(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("physical_features", {}).get("body", {}).get("build", "N/A")

    @rx.var
    def selected_dna_outfit(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("clothing", {}).get("default_outfit", "N/A")

    @rx.var
    def selected_dna_accessories(self) -> str:
        dna = self.get_selected_character_dna()
        accessories = dna.get("clothing", {}).get("accessories", [])
        if isinstance(accessories, list):
            return ", ".join(accessories) if accessories else "None"
        return str(accessories)

    @rx.var
    def selected_dna_art_style(self) -> str:
        dna = self.get_selected_character_dna()
        return dna.get("style_attributes", {}).get("art_style", "N/A")

    # DNA field setters for editable inputs
    def set_dna_hair_color(self, value: str):
        self._set_dna_nested("physical_features", "hair", "color", value)

    def set_dna_hair_style(self, value: str):
        self._set_dna_nested("physical_features", "hair", "style", value)

    def set_dna_eye_color(self, value: str):
        self._set_dna_nested("physical_features", "eyes", "color", value)

    def set_dna_eye_shape(self, value: str):
        self._set_dna_nested("physical_features", "eyes", "shape", value)

    def set_dna_skin_tone(self, value: str):
        self._set_dna_nested("physical_features", "face", "skin_tone", value)

    def set_dna_face_structure(self, value: str):
        self._set_dna_nested("physical_features", "face", "structure", value)

    def set_dna_body_build(self, value: str):
        self._set_dna_nested("physical_features", "body", "build", value)

    def set_dna_outfit(self, value: str):
        self._set_dna_nested("clothing", "default_outfit", None, value)

    def set_dna_accessories(self, value: str):
        # Convert comma-separated string to list
        accessories_list = [a.strip() for a in value.split(",") if a.strip()]
        self._set_dna_nested("clothing", "accessories", None, accessories_list)

    def set_dna_art_style(self, value: str):
        self._set_dna_nested("style_attributes", "art_style", None, value)

    def _set_dna_nested(self, level1: str, level2: str, level3: str = None, value=None):
        """Helper to set nested DNA values"""
        if not self.selected_character_id or self.selected_character_id not in self.character_dnas:
            return

        # Get a mutable copy of the DNA
        dna = dict(self.character_dnas[self.selected_character_id])

        # Ensure nested structure exists
        if level1 not in dna:
            dna[level1] = {}
        if isinstance(dna[level1], dict):
            dna[level1] = dict(dna[level1])

        if level3:
            # Three levels deep: physical_features.hair.color
            if level2 not in dna[level1]:
                dna[level1][level2] = {}
            if isinstance(dna[level1][level2], dict):
                dna[level1][level2] = dict(dna[level1][level2])
            dna[level1][level2][level3] = value
        else:
            # Two levels deep: clothing.default_outfit
            dna[level1][level2] = value

        # Update the character_dnas dict
        updated_dnas = dict(self.character_dnas)
        updated_dnas[self.selected_character_id] = dna
        self.character_dnas = updated_dnas

    def update_character_dna_field(self, field_path: str, value: str):
        """Update a specific field in character DNA"""
        if self.selected_character_id in self.character_dnas:
            dna = self.character_dnas[self.selected_character_id]
            # Parse field path like "physical_features.hair.color"
            parts = field_path.split(".")
            current = dna
            for part in parts[:-1]:
                if part in current:
                    current = current[part]
            if parts[-1] in current:
                current[parts[-1]] = value
            self.character_dnas[self.selected_character_id] = dna

    # Scene regeneration
    async def regenerate_scene(self, scene_id: str):
        """Regenerate a specific scene"""
        self.regenerating_scene_id = scene_id
        yield

        try:
            from .services.fibo_service import generate_scene_with_characters

            # Find the scene
            scene_data = None
            scene_index = -1
            for i, scene in enumerate(self.scenes):
                if scene.id == scene_id:
                    scene_data = scene
                    scene_index = i
                    break

            if not scene_data:
                return

            # Get character DNAs for this scene
            scene_char_dnas = list(self.character_dnas.values())

            # Regenerate with same description
            new_image_url = generate_scene_with_characters(
                scene_data.description or scene_data.title,
                scene_char_dnas,
                self.selected_style.lower()
            )

            # Update the scene
            updated_scene = Scene(
                id=scene_data.id,
                title=scene_data.title,
                description=scene_data.description,
                image_url=new_image_url
            )
            scenes_list = list(self.scenes)
            scenes_list[scene_index] = updated_scene
            self.scenes = scenes_list

        except Exception as e:
            self.error_message = f"Failed to regenerate scene: {str(e)}"
        finally:
            self.regenerating_scene_id = ""

    regenerating_all_scenes: bool = False

    async def regenerate_all_scenes_with_dna(self):
        """Regenerate all scenes with updated DNA"""
        if not self.scenes:
            self.error_message = "No scenes to regenerate!"
            return

        self.regenerating_all_scenes = True
        self.current_step = "Regenerating scenes with updated DNA..."
        yield

        try:
            from .services.fibo_service import generate_scene_with_characters

            scene_char_dnas = list(self.character_dnas.values())
            total = len(self.scenes)

            for i, scene in enumerate(self.scenes):
                self.current_step = f"Regenerating scene {i+1}/{total}: {scene.title}..."
                self.generation_progress = int((i / total) * 100)
                yield

                # Regenerate with DNA
                new_image_url = generate_scene_with_characters(
                    scene.description or scene.title,
                    scene_char_dnas,
                    self.selected_style.lower()
                )

                # Update the scene
                updated_scene = Scene(
                    id=scene.id,
                    title=scene.title,
                    description=scene.description,
                    image_url=new_image_url
                )
                scenes_list = list(self.scenes)
                scenes_list[i] = updated_scene
                self.scenes = scenes_list
                yield

            self.current_step = "All scenes regenerated!"
            self.generation_progress = 100
            yield

        except Exception as e:
            self.error_message = f"Failed to regenerate scenes: {str(e)}"
        finally:
            self.regenerating_all_scenes = False
            self.current_step = ""
            self.generation_progress = 0

    # Dialog overlay methods
    def set_scene_dialog(self, scene_id: str, dialog: str):
        """Set dialog text for a scene"""
        dialogs = dict(self.scene_dialogs)
        dialogs[scene_id] = dialog
        self.scene_dialogs = dialogs

    def open_dialog_editor(self, scene_id: str):
        """Open dialog editor for a scene"""
        self.editing_dialog_scene_id = scene_id
        self.dialog_text_input = self.scene_dialogs.get(scene_id, "")

    def close_dialog_editor(self):
        """Close dialog editor"""
        self.editing_dialog_scene_id = ""
        self.dialog_text_input = ""

    def save_dialog(self):
        """Save the current dialog"""
        if self.editing_dialog_scene_id:
            self.set_scene_dialog(self.editing_dialog_scene_id, self.dialog_text_input)
        self.close_dialog_editor()

    # AI Dialog generation
    generating_dialogs: bool = False

    async def generate_ai_dialogs(self, format_type: str = "manga"):
        """Generate AI dialogs for all scenes"""
        if not self.scenes:
            self.error_message = "No scenes to generate dialogs for!"
            return

        self.generating_dialogs = True
        self.current_step = f"Generating {format_type} dialogs..."
        yield

        try:
            from .services.gemini_service import generate_scene_dialog

            # Get character names for context
            character_names = [c.name for c in self.characters]

            for scene in self.scenes:
                self.current_step = f"Generating dialog for: {scene.title}..."
                yield

                # Generate dialog for this scene
                dialogs = generate_scene_dialog(
                    scene.description or scene.title,
                    character_names,
                    format_type
                )

                # Format dialogs as text
                dialog_text = ""
                for d in dialogs:
                    if d.get("type") == "narration":
                        dialog_text += f"[{d.get('text', '')}]\n\n"
                    elif d.get("type") == "thought":
                        dialog_text += f"{d.get('speaker', '')}: ({d.get('text', '')})\n\n"
                    else:
                        dialog_text += f"{d.get('speaker', '')}: \"{d.get('text', '')}\"\n\n"

                # Save to scene_dialogs
                self.set_scene_dialog(scene.id, dialog_text.strip())

            self.current_step = "Dialogs generated!"
            yield

        except Exception as e:
            self.error_message = f"Failed to generate dialogs: {str(e)}"
        finally:
            self.generating_dialogs = False
            self.current_step = ""

    async def generate_manga_dialogs(self):
        """Generate manga-style dialogs"""
        async for _ in self.generate_ai_dialogs("manga"):
            yield

    async def generate_manhwa_dialogs(self):
        """Generate manhwa-style dialogs"""
        async for _ in self.generate_ai_dialogs("manhwa"):
            yield

    def toggle_settings(self):
        """Toggle settings modal"""
        self.show_settings = not self.show_settings

    # Scene preview methods
    def open_scene_preview(self, index: int):
        """Open scene preview modal"""
        self.preview_scene_index = index
        self.show_scene_preview = True

    def close_scene_preview(self):
        """Close scene preview modal"""
        self.show_scene_preview = False

    def next_scene(self):
        """Go to next scene in preview"""
        if self.preview_scene_index < len(self.scenes) - 1:
            self.preview_scene_index += 1

    def prev_scene(self):
        """Go to previous scene in preview"""
        if self.preview_scene_index > 0:
            self.preview_scene_index -= 1

    # Export preview methods
    def open_manga_preview(self):
        """Open manga export preview"""
        self.show_manga_preview = True

    def close_manga_preview(self):
        """Close manga export preview"""
        self.show_manga_preview = False

    def open_manhwa_preview(self):
        """Open manhwa export preview"""
        self.show_manhwa_preview = True

    def close_manhwa_preview(self):
        """Close manhwa export preview"""
        self.show_manhwa_preview = False

    # Sidebar story expand/collapse
    def toggle_story_expand(self, story_id: str):
        """Toggle story expansion in sidebar"""
        if self.expanded_story_id == story_id:
            self.expanded_story_id = ""
        else:
            self.expanded_story_id = story_id
            self.current_project_id = story_id

    def open_new_story_dialog(self):
        """Open new story dialog"""
        self.new_story_name = ""
        self.show_new_story_dialog = True

    def close_new_story_dialog(self):
        """Close new story dialog"""
        self.show_new_story_dialog = False
        self.new_story_name = ""

    def create_named_story(self):
        """Create a new story with the given name"""
        name = self.new_story_name.strip() if self.new_story_name.strip() else f"Story {len(self.projects) + 1}"
        new_id = f"project_{len(self.projects) + 1}_{name.replace(' ', '_')}"
        new_project = Project(
            id=new_id,
            name=name,
            story=""
        )
        self.projects = self.projects + [new_project]
        self.current_project_id = new_id
        self.expanded_story_id = new_id
        self.story_text = ""
        self.characters = []
        self.scenes = []
        self.character_dnas = {}
        self.show_new_story_dialog = False
        self.new_story_name = ""
        self.active_view = "main"

    def create_story_ai_name_later(self):
        """Create a new story with a placeholder name - AI will name it when generating"""
        name = f"Untitled Story {len(self.projects) + 1}"
        new_id = f"project_{len(self.projects) + 1}_untitled"
        new_project = Project(
            id=new_id,
            name=name,
            story=""
        )
        self.projects = self.projects + [new_project]
        self.current_project_id = new_id
        self.expanded_story_id = new_id
        self.story_text = ""
        self.characters = []
        self.scenes = []
        self.character_dnas = {}
        self.show_new_story_dialog = False
        self.new_story_name = ""
        self.active_view = "main"

    def open_delete_dialog(self, project_id: str, project_name: str):
        """Open delete confirmation dialog"""
        self.delete_target_id = project_id
        self.delete_target_name = project_name
        self.show_delete_dialog = True

    def close_delete_dialog(self):
        """Close delete confirmation dialog"""
        self.show_delete_dialog = False
        self.delete_target_id = ""
        self.delete_target_name = ""

    def confirm_delete_story(self):
        """Confirm and delete the story"""
        project_id = self.delete_target_id
        self.projects = [p for p in self.projects if p.id != project_id]
        if self.current_project_id == project_id:
            self.current_project_id = ""
            self.story_text = ""
            self.characters = []
            self.scenes = []
            self.character_dnas = {}
        self.show_delete_dialog = False
        self.delete_target_id = ""
        self.delete_target_name = ""

    def delete_story(self, project_id: str):
        """Delete a story by ID (legacy - now uses confirmation)"""
        self.projects = [p for p in self.projects if p.id != project_id]
        if self.current_project_id == project_id:
            self.current_project_id = ""
            self.story_text = ""
            self.characters = []
            self.scenes = []
            self.character_dnas = {}

    # Example stories
    EXAMPLE_STORIES: Dict[str, str] = {
        "Anime": """A wandering samurai named Kaito with silver hair, piercing red eyes, and a diagonal scar across his left cheek travels through feudal Japan. He wears a tattered black haori with red lining and carries a katana with a worn hilt.

In an abandoned mountain temple, he discovers a mysterious young girl named Yuki with long white hair that seems to glow faintly and large violet eyes. She wears a simple white kimono with blue wave patterns.

Together they journey through cherry blossom fields at sunset, face bandits in a rain-soaked village at night, find shelter in a cave during a thunderstorm, and finally reach a majestic waterfall at dawn where Yuki reveals her true nature as a spirit.""",

        "Realistic": """Detective Maya Chen, a woman in her mid-30s with short black hair, a cybernetic left eye glowing blue, and a worn leather jacket, investigates a murder in Neo Shanghai 2087.

Her lead suspect is ARIA, an android with porcelain-white synthetic skin, silver geometric patterns tracing her cheekbones, and eerily human green eyes. She wears a sleek white coat with holographic trim.

The investigation takes them through neon-lit alleyways crowded with vendors, a pristine corporate tower with floor-to-ceiling windows, a grimy underground market lit by flickering signs, and finally a confrontation on a rain-swept rooftop overlooking the holographic cityscape at night.""",

        "Sci-Fi": """Commander Elena Vance, a battle-hardened soldier with short auburn hair, green eyes, and a prominent scar running from her temple to jaw, leads humanity's last defense. She wears battered power armor with the insignia of the United Earth Fleet.

Her unlikely ally is Krix, an alien warrior with iridescent blue-purple skin, four eyes arranged in a diamond pattern, and bioluminescent markings that pulse with emotion. He wears organic armor that seems to grow from his body.

Together they fight through the burning corridors of a space station, make a desperate stand in an alien jungle with bioluminescent plants, negotiate in a massive alien council chamber, and face the final battle on the bridge of a massive warship.""",

        "Fantasy": """A young mage named Lyra with flowing copper hair, heterochromatic eyes (one gold, one silver), and constellation-like freckles across her pale skin embarks on a quest. She wears flowing blue robes with silver embroidery and carries an ancient wooden staff.

She is joined by Grimjaw, a grizzled dwarf warrior with a magnificent braided gray beard, deep brown eyes, and intricate tattoos covering his muscular arms. He wears battered plate armor and carries a massive war hammer.

Their journey takes them through an enchanted forest where trees whisper secrets, across a treacherous mountain pass during a blizzard, into the depths of an ancient dwarven mine filled with glowing crystals, and finally to a confrontation in a wizard's tower floating among the clouds."""
    }

    def load_example(self):
        """Load example story based on selected style"""
        style = self.selected_style
        self.story_text = self.EXAMPLE_STORIES.get(style, self.EXAMPLE_STORIES["Anime"])

    def clear_results(self):
        """Clear all generated results"""
        self.characters = []
        self.scenes = []
        self.character_dnas = {}
        self.error_message = ""
        self.current_step = ""
        self.generation_progress = 0

    # Project management
    def new_project(self):
        """Create a new project"""
        new_id = f"project_{len(self.projects) + 1}"
        new_project = Project(
            id=new_id,
            name=f"New Project {len(self.projects) + 1}",
            story=""
        )
        self.projects = self.projects + [new_project]
        self.current_project_id = new_id
        self.story_text = ""
        self.characters = []
        self.scenes = []
        self.character_dnas = {}

    def load_project(self, project_id: str):
        """Load a saved project"""
        for p in self.projects:
            if p.id == project_id:
                self.current_project_id = project_id
                self.story_text = p.story
                break

    def load_project_and_go_main(self, project_id: str):
        """Load a project and navigate to main view"""
        self.load_project(project_id)
        self.expanded_story_id = project_id
        self.active_view = "main"

    # Export methods
    async def export_manga(self):
        """Export scenes as manga (B&W panels)"""
        if not self.scenes:
            self.error_message = "No scenes to export! Generate a story first."
            return

        self.export_loading = True
        self.export_progress = "Creating manga layout..."
        yield

        try:
            from .services.export_service import export_manga
            output_dir = os.path.expanduser("~/Downloads")
            path = export_manga(self.scenes, output_dir)
            self.export_progress = f"Saved to: {path}"
        except Exception as e:
            self.error_message = f"Export failed: {e}"
            import traceback
            traceback.print_exc()
        finally:
            self.export_loading = False

    async def export_manhwa(self):
        """Export scenes as manhwa (color vertical scroll)"""
        if not self.scenes:
            self.error_message = "No scenes to export! Generate a story first."
            return

        self.export_loading = True
        self.export_progress = "Creating manhwa scroll..."
        yield

        try:
            from .services.export_service import export_manhwa
            output_dir = os.path.expanduser("~/Downloads")
            path = export_manhwa(self.scenes, output_dir)
            self.export_progress = f"Saved to: {path}"
        except Exception as e:
            self.error_message = f"Export failed: {e}"
            import traceback
            traceback.print_exc()
        finally:
            self.export_loading = False

    async def export_slideshow(self):
        """Export scenes as slideshow video"""
        if not self.scenes:
            self.error_message = "No scenes to export! Generate a story first."
            return

        self.export_loading = True
        self.export_progress = "Creating slideshow..."
        yield

        try:
            from .services.video_service import export_slideshow
            output_dir = os.path.expanduser("~/Downloads")
            path = export_slideshow(self.scenes, output_dir)
            self.export_progress = f"Saved to: {path}"
        except ImportError:
            self.error_message = "moviepy not installed. Install with: pip install moviepy"
        except Exception as e:
            self.error_message = f"Export failed: {e}"
            import traceback
            traceback.print_exc()
        finally:
            self.export_loading = False

    async def export_luma_video(self):
        """Export scenes as AI animated video using Luma"""
        if not self.scenes:
            self.error_message = "No scenes to export! Generate a story first."
            return

        # Check for API key in env or state
        api_key = self.luma_api_key or os.getenv("LUMA_API_KEY", "")
        if not api_key:
            self.error_message = "Please enter your Luma AI API key in settings!"
            self.show_settings = True
            return

        self.export_loading = True
        self.export_progress = "Generating AI video..."
        yield

        try:
            from .services.luma_service import export_luma_video

            output_dir = os.path.expanduser("~/Downloads")

            def progress_callback(msg):
                self.export_progress = msg

            path = export_luma_video(
                self.scenes, api_key, output_dir,
                progress_callback=progress_callback
            )
            self.export_progress = f"Saved to: {path}"
        except Exception as e:
            self.error_message = f"Export failed: {e}"
            import traceback
            traceback.print_exc()
        finally:
            self.export_loading = False

    async def export_all_images(self):
        """Export all images as ZIP"""
        if not self.scenes and not self.characters:
            self.error_message = "No images to export! Generate a story first."
            return

        self.export_loading = True
        self.export_progress = "Creating ZIP file..."
        yield

        try:
            from .services.export_service import export_all_images
            output_dir = os.path.expanduser("~/Downloads")
            path = export_all_images(self.scenes, self.characters, output_dir)
            self.export_progress = f"Saved to: {path}"
        except Exception as e:
            self.error_message = f"Export failed: {e}"
            import traceback
            traceback.print_exc()
        finally:
            self.export_loading = False

    async def generate_story(self):
        """Main generation pipeline"""
        if not self.story_text.strip():
            self.error_message = "Please enter a story first!"
            return

        self.is_loading = True
        self.clear_results()
        self.current_step = "Naming your story..."
        yield

        try:
            # Import services
            from .services.gemini_service import parse_story, extract_character_dna, generate_story_name
            from .services.fibo_service import (
                generate_character_portrait,
                generate_scene_with_characters,
                download_image,
                build_character_description
            )

            # Step 0: Generate story name and update/create project
            story_name = generate_story_name(self.story_text)

            # Check if we have a current project to update
            if self.current_project_id:
                # Update existing project with AI-generated name
                updated_projects = []
                for p in self.projects:
                    if p.id == self.current_project_id:
                        updated_projects.append(Project(
                            id=p.id,
                            name=story_name,
                            story=self.story_text
                        ))
                    else:
                        updated_projects.append(p)
                self.projects = updated_projects
                self.expanded_story_id = self.current_project_id
            else:
                # Create new project
                new_id = f"project_{len(self.projects) + 1}_{story_name.replace(' ', '_')}"
                new_project = Project(
                    id=new_id,
                    name=story_name,
                    story=self.story_text
                )
                self.projects = self.projects + [new_project]
                self.current_project_id = new_id
                self.expanded_story_id = new_id
            yield

            # Step 1: Parse story with Gemini
            self.current_step = "Analyzing story with AI..."
            self.generation_progress = 10
            yield

            parsed = parse_story(self.story_text, self.selected_style.lower())
            total_chars = len(parsed.get("characters", []))
            total_scenes = len(parsed.get("scenes", []))

            # Step 2: Generate characters and extract DNA
            self.current_step = "Creating characters..."
            self.generation_progress = 20
            yield

            for i, char_data in enumerate(parsed.get("characters", [])):
                self.current_step = f"Forging {char_data['name']}... ({i+1}/{total_chars})"
                self.generation_progress = 20 + int((i / max(total_chars, 1)) * 30)
                yield

                # Generate initial character portrait
                image_url = generate_character_portrait(
                    char_data['description'],
                    self.selected_style.lower()
                )

                # Extract Character DNA from the generated image
                image = download_image(image_url)
                dna = extract_character_dna(image, char_data['name'])
                self.character_dnas[char_data['id']] = dna

                # Add to state using typed model
                new_char = Character(
                    id=char_data['id'],
                    name=char_data['name'],
                    description=char_data['description'],
                    image_url=image_url
                )
                self.characters = self.characters + [new_char]
                yield

            # Step 3: Generate scenes with consistent characters
            self.current_step = "Generating scenes..."
            self.generation_progress = 50
            yield

            for i, scene_data in enumerate(parsed.get("scenes", [])):
                self.current_step = f"Scene {i+1}: {scene_data['title']}..."
                self.generation_progress = 50 + int((i / max(total_scenes, 1)) * 45)
                yield

                # Get Character DNAs for characters in this scene
                scene_char_dnas = []
                for char_id in scene_data.get("characters_present", []):
                    if char_id in self.character_dnas:
                        scene_char_dnas.append(self.character_dnas[char_id])

                # Generate scene with locked character features
                image_url = generate_scene_with_characters(
                    scene_data['visual_direction'],
                    scene_char_dnas,
                    self.selected_style.lower()
                )

                # Add to state using typed model
                new_scene = Scene(
                    id=scene_data['id'],
                    title=scene_data['title'],
                    description=scene_data.get('description', ''),
                    image_url=image_url
                )
                self.scenes = self.scenes + [new_scene]
                yield

            self.current_step = "Complete!"
            self.generation_progress = 100

        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            import traceback
            traceback.print_exc()

        finally:
            self.is_loading = False
