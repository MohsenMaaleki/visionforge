"""VisionForge - Electric Violet Theme with Sidebar"""
import reflex as rx
from .state import State, Character, Scene

# Electric Violet Theme Colors
THEME = {
    # Backgrounds
    "background": "#F8F9FF",
    "surface": "#FFFFFF",
    "surface_hover": "#F0F1FF",

    # Primary Colors (Violet)
    "primary": "#7C3AED",
    "primary_hover": "#6D28D9",
    "primary_light": "#EDE9FE",

    # Secondary Colors (Cyan)
    "secondary": "#06B6D4",
    "secondary_hover": "#0891B2",
    "secondary_light": "#CFFAFE",

    # Accent Colors
    "accent": "#EC4899",
    "accent_light": "#FCE7F3",
    "success": "#10B981",
    "success_light": "#D1FAE5",

    # Text Colors
    "text": "#1E1B4B",
    "text_muted": "#6B7280",
    "text_light": "#9CA3AF",

    # Borders
    "border": "#E5E7EB",

    # Gradients
    "gradient_header": "linear-gradient(135deg, #7C3AED 0%, #2563EB 50%, #06B6D4 100%)",
    "gradient_button": "linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)",
}


# ============== SIDEBAR COMPONENTS ==============

# Gold colors for "Coming Soon" features
GOLD = "#F59E0B"
GOLD_LIGHT = "#FEF3C7"


def story_sub_item(icon: str, label: str, on_click=None, coming_soon: bool = False) -> rx.Component:
    """Sub-item under expanded story"""
    if coming_soon:
        return rx.box(
            rx.hstack(
                rx.icon(icon, size=12, color=GOLD),
                rx.text(label, size="1", color=GOLD),
                rx.badge("Soon", size="1", style={"background": GOLD_LIGHT, "color": GOLD, "font_size": "9px"}),
                spacing="2",
                width="100%",
                align="center",
            ),
            padding="0.3em 0.5em 0.3em 1.5em",
            width="100%",
        )
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=12, color=THEME["text_muted"]),
            rx.text(label, size="1", color=THEME["text"]),
            spacing="2",
            width="100%",
            align="center",
        ),
        padding="0.3em 0.5em 0.3em 1.5em",
        border_radius="6px",
        cursor="pointer",
        width="100%",
        _hover={"background": THEME["surface_hover"]},
        on_click=on_click if on_click else None,
    )


# Style options for dropdown
STYLE_OPTIONS = ["Anime", "Realistic", "Sci-Fi", "Fantasy"]


def story_item_expandable(project) -> rx.Component:
    """Expandable story item in sidebar with sub-sections"""
    return rx.box(
        # Story header row
        rx.hstack(
            # Chevron for expand/collapse
            rx.box(
                rx.cond(
                    State.expanded_story_id == project.id,
                    rx.icon("chevron-down", size=14, color=THEME["primary"]),
                    rx.icon("chevron-right", size=14, color=THEME["text_muted"]),
                ),
                cursor="pointer",
                on_click=lambda: State.toggle_story_expand(project.id),
            ),
            # Story name - clickable to go to main view
            rx.hstack(
                rx.icon("book-open", size=14, color=THEME["primary"]),
                rx.text(project.name, size="2", color=THEME["text"], style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"}),
                spacing="1",
                flex="1",
                cursor="pointer",
                _hover={"opacity": "0.8"},
                on_click=lambda: State.load_project_and_go_main(project.id),
            ),
            rx.icon_button(
                rx.icon("trash-2", size=12),
                size="1",
                variant="ghost",
                color_scheme="red",
                on_click=lambda: State.open_delete_dialog(project.id, project.name),
            ),
            spacing="1",
            width="100%",
            align="center",
        ),
        # Expanded sub-items
        rx.cond(
            State.expanded_story_id == project.id,
            rx.vstack(
                story_sub_item("users", "Characters", State.go_to_characters_view),
                story_sub_item("film", "Scenes", State.go_to_scenes_view),
                story_sub_item("layout-grid", "Manga", State.go_to_manga_view),
                story_sub_item("scroll", "Manhwa", State.go_to_manhwa_view),
                story_sub_item("video", "Video", coming_soon=True),
                spacing="0",
                width="100%",
                padding_top="0.25em",
            ),
        ),
        padding="0.4em 0.6em",
        border_radius="8px",
        width="100%",
        background=rx.cond(State.expanded_story_id == project.id, THEME["primary_light"], "transparent"),
        _hover={"background": THEME["surface_hover"]},
    )


def style_option(name: str) -> rx.Component:
    """Style option in sidebar"""
    return rx.box(
        rx.hstack(
            rx.cond(
                State.selected_style == name,
                rx.box(width="8px", height="8px", border_radius="50%", background=THEME["primary"]),
                rx.box(width="8px", height="8px", border_radius="50%", background=THEME["border"]),
            ),
            rx.text(name, size="2", color=THEME["text"]),
            spacing="2",
            width="100%",
        ),
        padding="0.4em 0.75em",
        border_radius="6px",
        cursor="pointer",
        width="100%",
        on_click=lambda: State.set_selected_style(name),
    )


def export_option(icon: str, name: str, on_click, coming_soon: bool = False, premium: bool = False) -> rx.Component:
    """Export option in sidebar"""
    # Gold/Amber colors for premium AI Video
    gold = "#F59E0B"
    gold_light = "#FEF3C7"

    if premium:
        return rx.box(
            rx.hstack(
                rx.icon(icon, size=14, color=gold),
                rx.text(name, size="2", weight="medium", color=gold),
                rx.spacer(),
                rx.badge(
                    "✨ Soon",
                    size="1",
                    style={"background": gold_light, "color": gold, "font_weight": "600"}
                ),
                spacing="2",
                width="100%",
            ),
            padding="0.5em 0.75em",
            border_radius="6px",
            width="100%",
            background=f"linear-gradient(135deg, {gold_light} 0%, #FFFBEB 100%)",
            border=f"1px solid {gold}",
        )

    return rx.box(
        rx.hstack(
            rx.icon(icon, size=14, color=THEME["secondary"] if not coming_soon else THEME["text_light"]),
            rx.text(name, size="2", color=THEME["text"] if not coming_soon else THEME["text_light"]),
            rx.spacer(),
            spacing="2",
            width="100%",
        ),
        padding="0.5em 0.75em",
        border_radius="6px",
        cursor="pointer",
        width="100%",
        on_click=on_click,
    )


def sidebar() -> rx.Component:
    """Clean sidebar with Electric Violet styling"""
    return rx.box(
        rx.vstack(
            # Logo/Brand in sidebar
            rx.hstack(
                rx.text("⚡", font_size="1.5em"),
                rx.text("VISIONFORGE", size="3", weight="bold", color=THEME["primary"]),
                spacing="2",
                align="center",
                padding="0.5em 0",
            ),

            rx.divider(style={"border_color": THEME["border"], "margin": "0.5em 0"}),

            # MY STORIES Section
            rx.vstack(
                rx.hstack(
                    rx.text("📖", font_size="1em"),
                    rx.text("MY STORIES", size="1", weight="bold", color=THEME["text_muted"]),
                    spacing="2",
                    width="100%",
                ),
                # Show stories or empty state
                rx.cond(
                    State.projects.length() > 0,
                    rx.vstack(
                        rx.foreach(State.projects, story_item_expandable),
                        spacing="1",
                        width="100%",
                    ),
                    rx.text("No stories yet", size="2", color=THEME["text_light"], padding="0.5em"),
                ),
                # Create New button
                rx.box(
                    rx.hstack(
                        rx.icon("plus", size=14, color=THEME["primary"]),
                        rx.text("Create New", size="2", color=THEME["primary"], weight="medium"),
                        spacing="2",
                        width="100%",
                    ),
                    padding="0.5em 0.75em",
                    border_radius="6px",
                    cursor="pointer",
                    width="100%",
                    border=f"1px dashed {THEME['primary']}",
                    _hover={"background": THEME["primary_light"]},
                    on_click=State.open_new_story_dialog,
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            rx.divider(style={"border_color": THEME["border"], "margin": "0.5em 0"}),

            # Style Section with Custom Menu
            rx.vstack(
                rx.hstack(
                    rx.text("🎨", font_size="1em"),
                    rx.text("STYLE", size="1", weight="bold", color=THEME["text_muted"]),
                    spacing="2",
                    width="100%",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.hstack(
                                rx.match(
                                    State.selected_style,
                                    ("Anime", rx.icon("sparkles", size=14, color=THEME["accent"])),
                                    ("Realistic", rx.icon("camera", size=14, color=THEME["secondary"])),
                                    ("Sci-Fi", rx.icon("rocket", size=14, color=THEME["primary"])),
                                    ("Fantasy", rx.icon("wand", size=14, color=THEME["success"])),
                                    rx.icon("palette", size=14, color=THEME["primary"]),  # default
                                ),
                                rx.text(State.selected_style, size="2", color=THEME["text"]),
                                rx.icon("chevron-down", size=14, color=THEME["primary"]),
                                spacing="2",
                                width="100%",
                                justify="between",
                                align="center",
                            ),
                            variant="outline",
                            width="100%",
                            style={
                                "border_color": THEME["primary_light"],
                                "background": THEME["surface"],
                                "justify_content": "space-between",
                                "&:hover": {
                                    "border_color": THEME["primary"],
                                    "background": THEME["primary_light"],
                                },
                            },
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            rx.hstack(
                                rx.icon("sparkles", size=14, color=THEME["accent"]),
                                rx.text("Anime", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=lambda: State.set_selected_style("Anime"),
                            style={"color": THEME["text"], "&:hover": {"background": THEME["primary_light"], "color": THEME["primary"]}},
                        ),
                        rx.menu.item(
                            rx.hstack(
                                rx.icon("camera", size=14, color=THEME["secondary"]),
                                rx.text("Realistic", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=lambda: State.set_selected_style("Realistic"),
                            style={"color": THEME["text"], "&:hover": {"background": THEME["primary_light"], "color": THEME["primary"]}},
                        ),
                        rx.menu.item(
                            rx.hstack(
                                rx.icon("rocket", size=14, color=THEME["primary"]),
                                rx.text("Sci-Fi", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=lambda: State.set_selected_style("Sci-Fi"),
                            style={"color": THEME["text"], "&:hover": {"background": THEME["primary_light"], "color": THEME["primary"]}},
                        ),
                        rx.menu.item(
                            rx.hstack(
                                rx.icon("wand", size=14, color=THEME["success"]),
                                rx.text("Fantasy", size="2"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=lambda: State.set_selected_style("Fantasy"),
                            style={"color": THEME["text"], "&:hover": {"background": THEME["primary_light"], "color": THEME["primary"]}},
                        ),
                        style={
                            "background": THEME["surface"],
                            "border": f"2px solid {THEME['primary_light']}",
                            "border_radius": "10px",
                            "padding": "0.5em",
                            "box_shadow": "0 4px 20px rgba(124, 58, 237, 0.15)",
                        },
                    ),
                ),
                spacing="2",
                width="100%",
                align="start",
            ),

            rx.spacer(),

            # Back to main button when in a view
            rx.cond(
                State.active_view != "main",
                rx.box(
                    rx.hstack(
                        rx.icon("arrow-left", size=14, color=THEME["text"]),
                        rx.text("Back to Create", size="2", color=THEME["text"]),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    padding="0.5em 0.75em",
                    border_radius="6px",
                    cursor="pointer",
                    width="100%",
                    background=THEME["surface_hover"],
                    _hover={"background": THEME["primary_light"]},
                    on_click=State.go_to_main_view,
                ),
            ),

            spacing="2",
            width="100%",
            height="100%",
        ),
        width="280px",
        min_width="220px",
        max_width="320px",
        height="100vh",
        padding="1.25em",
        background=THEME["surface"],
        border_right=f"1px solid {THEME['border']}",
        position="fixed",
        left="0",
        top="0",
        overflow="hidden",
        z_index="100",
    )


# ============== DIALOGS ==============

def new_story_dialog() -> rx.Component:
    """Dialog for creating a new story with a name"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon("book-open", size=24, color=THEME["primary"]),
                    "Create New Story",
                    spacing="2",
                    align="center",
                ),
            ),
            rx.dialog.description(
                "Give your story a name, or let AI generate one based on your story content.",
                size="2",
                color=THEME["text_muted"],
            ),
            rx.vstack(
                rx.input(
                    placeholder="Enter story name...",
                    value=State.new_story_name,
                    on_change=State.set_new_story_name,
                    width="100%",
                    size="3",
                    style={
                        "border": f"2px solid {THEME['primary_light']}",
                        "border_radius": "8px",
                        "&:focus": {
                            "border_color": THEME["primary"],
                        },
                    },
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color="gray",
                            on_click=State.close_new_story_dialog,
                        ),
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("sparkles", size=16),
                            "AI Name Later",
                            variant="outline",
                            style={
                                "border_color": THEME["secondary"],
                                "color": THEME["secondary"],
                            },
                            on_click=State.create_story_ai_name_later,
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("check", size=16),
                            "Create",
                            style={
                                "background": THEME["gradient_button"],
                                "color": "white",
                            },
                            on_click=State.create_named_story,
                        ),
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                padding_top="1em",
            ),
            style={
                "max_width": "450px",
                "padding": "1.5em",
            },
        ),
        open=State.show_new_story_dialog,
    )


def delete_confirm_dialog() -> rx.Component:
    """Confirmation dialog for deleting a story"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon("triangle-alert", size=20, color="#EF4444"),
                    "Delete Story",
                    spacing="2",
                    align="center",
                ),
            ),
            rx.dialog.description(
                rx.text(
                    "Are you sure you want to delete ",
                    rx.text(State.delete_target_name, weight="bold", as_="span"),
                    "? This action cannot be undone.",
                ),
                size="2",
                color=THEME["text_muted"],
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color="gray",
                        on_click=State.close_delete_dialog,
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Delete",
                        color_scheme="red",
                        on_click=State.confirm_delete_story,
                    ),
                ),
                spacing="3",
                justify="end",
                width="100%",
                padding_top="1em",
            ),
            style={
                "max_width": "400px",
                "padding": "1.5em",
            },
        ),
        open=State.show_delete_dialog,
    )


def scene_preview_modal() -> rx.Component:
    """Modal for viewing scene in full size"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header with title and close
                rx.hstack(
                    rx.heading(
                        rx.cond(
                            State.scenes.length() > 0,
                            State.scenes[State.preview_scene_index].title,
                            "Scene Preview"
                        ),
                        size="5",
                        color=THEME["text"],
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            on_click=State.close_scene_preview,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                # Image
                rx.cond(
                    State.scenes.length() > 0,
                    rx.image(
                        src=State.scenes[State.preview_scene_index].image_url,
                        width="100%",
                        max_height="60vh",
                        object_fit="contain",
                        border_radius="12px",
                    ),
                ),
                # Navigation
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", size=20),
                        "Previous",
                        variant="soft",
                        disabled=State.preview_scene_index == 0,
                        on_click=State.prev_scene,
                    ),
                    rx.spacer(),
                    rx.text(
                        f"Scene {State.preview_scene_index + 1} of {State.scenes.length()}",
                        size="2",
                        color=THEME["text_muted"],
                    ),
                    rx.spacer(),
                    rx.button(
                        "Next",
                        rx.icon("chevron-right", size=20),
                        variant="soft",
                        disabled=State.preview_scene_index >= State.scenes.length() - 1,
                        on_click=State.next_scene,
                    ),
                    width="100%",
                    align="center",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "800px",
                "width": "90vw",
                "padding": "1.5em",
            },
        ),
        open=State.show_scene_preview,
    )


def manga_preview_modal() -> rx.Component:
    """Preview modal for manga export"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("layout-grid", size=24, color=THEME["primary"]),
                    rx.heading("Manga Preview", size="5", color=THEME["text"]),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            on_click=State.close_manga_preview,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    "Your scenes will be exported as black & white manga panels.",
                    color=THEME["text_muted"],
                    size="2",
                ),
                # Preview grid of scenes
                rx.box(
                    rx.hstack(
                        rx.foreach(
                            State.scenes[:4],
                            lambda scene: rx.image(
                                src=scene.image_url,
                                width="120px",
                                height="80px",
                                object_fit="cover",
                                border_radius="8px",
                                style={"filter": "grayscale(100%)"},
                            ),
                        ),
                        spacing="2",
                        flex_wrap="wrap",
                        justify="center",
                    ),
                    padding="1em",
                    background=THEME["surface_hover"],
                    border_radius="12px",
                    width="100%",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color="gray",
                            on_click=State.close_manga_preview,
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("download", size=16),
                            "Export Manga",
                            style={
                                "background": THEME["gradient_button"],
                                "color": "white",
                            },
                            on_click=State.export_manga,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "600px",
                "padding": "1.5em",
            },
        ),
        open=State.show_manga_preview,
    )


def manhwa_preview_modal() -> rx.Component:
    """Preview modal for manhwa export"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("scroll", size=24, color=THEME["secondary"]),
                    rx.heading("Manhwa Preview", size="5", color=THEME["text"]),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            on_click=State.close_manhwa_preview,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    "Your scenes will be exported as a colorful vertical scroll.",
                    color=THEME["text_muted"],
                    size="2",
                ),
                # Preview vertical stack of scenes
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.scenes[:3],
                            lambda scene: rx.image(
                                src=scene.image_url,
                                width="100%",
                                height="60px",
                                object_fit="cover",
                                border_radius="4px",
                            ),
                        ),
                        spacing="1",
                        width="150px",
                    ),
                    padding="1em",
                    background=THEME["surface_hover"],
                    border_radius="12px",
                    width="100%",
                    display="flex",
                    justify_content="center",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color="gray",
                            on_click=State.close_manhwa_preview,
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("download", size=16),
                            "Export Manhwa",
                            style={
                                "background": f"linear-gradient(135deg, {THEME['secondary']} 0%, {THEME['secondary_hover']} 100%)",
                                "color": "white",
                            },
                            on_click=State.export_manhwa,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "500px",
                "padding": "1.5em",
            },
        ),
        open=State.show_manhwa_preview,
    )


def dna_field_editable(label: str, value, icon: str, on_change) -> rx.Component:
    """An editable DNA field with full text visibility"""
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=14, color=THEME["primary"]),
            rx.text(label, size="2", weight="medium", color=THEME["text"]),
            spacing="2",
            align="center",
        ),
        rx.text_area(
            value=value,
            size="1",
            resize="vertical",
            style={
                "width": "100%",
                "min_height": "50px",
                "background": THEME["surface"],
                "border": f"1px solid {THEME['border']}",
                "border_radius": "6px",
                "color": THEME["text"],
                "font_size": "12px",
                "padding": "8px",
                "&:focus": {
                    "border_color": THEME["primary"],
                    "box_shadow": f"0 0 0 2px {THEME['primary_light']}",
                },
            },
            on_change=on_change,
        ),
        spacing="1",
        width="100%",
        padding="0.3em 0",
        align="start",
    )


def dna_section(title: str, icon: str, children: list) -> rx.Component:
    """A section of DNA fields"""
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=16, color=THEME["secondary"]),
            rx.text(title, size="2", weight="bold", color=THEME["text"]),
            spacing="2",
            padding_bottom="0.5em",
            border_bottom=f"1px solid {THEME['border']}",
            margin_bottom="0.5em",
        ),
        rx.vstack(
            *children,
            spacing="0",
            width="100%",
        ),
        width="100%",
        padding="0.75em",
        background=THEME["surface_hover"],
        border_radius="10px",
    )


def character_editor_modal() -> rx.Component:
    """Modal for viewing/editing character DNA"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("dna", size=28, color=THEME["secondary"]),
                    rx.vstack(
                        rx.heading(State.selected_dna_name, size="5", color=THEME["text"]),
                        rx.text("Character DNA Profile", size="1", color=THEME["text_muted"]),
                        spacing="0",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            color_scheme="gray",
                            on_click=State.close_character_editor,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),

                # DNA Content - Editable Fields
                rx.box(
                    rx.vstack(
                        # Hair Section
                        dna_section("Hair", "sparkles", [
                            dna_field_editable("Color", State.selected_dna_hair_color, "palette", State.set_dna_hair_color),
                            dna_field_editable("Style", State.selected_dna_hair_style, "scissors", State.set_dna_hair_style),
                        ]),

                        # Eyes Section
                        dna_section("Eyes", "eye", [
                            dna_field_editable("Color", State.selected_dna_eye_color, "palette", State.set_dna_eye_color),
                            dna_field_editable("Shape", State.selected_dna_eye_shape, "scan", State.set_dna_eye_shape),
                        ]),

                        # Face Section
                        dna_section("Face", "user", [
                            dna_field_editable("Skin Tone", State.selected_dna_skin_tone, "palette", State.set_dna_skin_tone),
                            dna_field_editable("Structure", State.selected_dna_face_structure, "scan", State.set_dna_face_structure),
                        ]),

                        # Body Section
                        dna_section("Body", "person-standing", [
                            dna_field_editable("Build", State.selected_dna_body_build, "ruler", State.set_dna_body_build),
                        ]),

                        # Clothing Section
                        dna_section("Clothing", "shirt", [
                            dna_field_editable("Outfit", State.selected_dna_outfit, "shirt", State.set_dna_outfit),
                            dna_field_editable("Accessories", State.selected_dna_accessories, "gem", State.set_dna_accessories),
                        ]),

                        # Style Section
                        dna_section("Art Style", "brush", [
                            dna_field_editable("Style", State.selected_dna_art_style, "palette", State.set_dna_art_style),
                        ]),

                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                    max_height="500px",
                    overflow_y="auto",
                    padding_right="0.5em",
                ),

                # Info text
                rx.text(
                    "Edit any field above, then click 'Regenerate All Scenes' to update images with new DNA.",
                    size="1",
                    color=THEME["text_muted"],
                    text_align="center",
                    style={"font_style": "italic"},
                ),

                # Action buttons
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Close",
                            variant="soft",
                            style={"background": THEME["surface_hover"], "color": THEME["text"]},
                            on_click=State.close_character_editor,
                        ),
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("refresh-cw", size=16),
                            "Regenerate All Scenes",
                            loading=State.regenerating_all_scenes,
                            style={
                                "background": THEME["gradient_button"],
                                "color": "white",
                            },
                            on_click=State.regenerate_all_scenes_with_dna,
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                # Progress indicator
                rx.cond(
                    State.regenerating_all_scenes,
                    rx.vstack(
                        rx.text(State.current_step, size="1", color=THEME["text_muted"]),
                        rx.progress(value=State.generation_progress, width="100%"),
                        spacing="2",
                        width="100%",
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "650px",
                "padding": "1.5em",
                "background": THEME["surface"],
                "border_radius": "16px",
            },
        ),
        open=State.show_character_editor,
    )


def dialog_editor_modal() -> rx.Component:
    """Modal for editing scene dialog text - Light theme"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("message-circle", size=24, color=THEME["primary"]),
                    rx.heading("Add Dialog", size="5", color=THEME["text"]),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            style={"color": THEME["text_muted"]},
                            on_click=State.close_dialog_editor,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    "Add speech bubbles or narration text to this scene.",
                    color=THEME["text_muted"],
                    size="2",
                ),
                rx.text_area(
                    placeholder="Enter dialog or narration...\n\nExample:\nCharacter: Hello there!\nNarration: The sun set behind the mountains...",
                    value=State.dialog_text_input,
                    on_change=State.set_dialog_text_input,
                    width="100%",
                    min_height="150px",
                    style={
                        "background": THEME["surface"],
                        "border": f"1px solid {THEME['border']}",
                        "color": THEME["text"],
                    },
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            style={"background": THEME["surface_hover"], "color": THEME["text"]},
                            on_click=State.close_dialog_editor,
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("check", size=16),
                            "Save Dialog",
                            style={
                                "background": THEME["gradient_button"],
                                "color": "white",
                            },
                            on_click=State.save_dialog,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "500px",
                "padding": "1.5em",
                "background": THEME["surface"],
                "border_radius": "16px",
            },
        ),
        open=State.editing_dialog_scene_id != "",
    )


# ============== VIEW SECTIONS ==============

def view_header(icon: str, title: str, subtitle: str = "") -> rx.Component:
    """Header for view sections"""
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=28, color=THEME["primary"]),
            rx.heading(title, size="6", color=THEME["text"]),
            spacing="3",
            align="center",
        ),
        rx.cond(
            subtitle != "",
            rx.text(subtitle, color=THEME["text_muted"], size="2"),
        ),
        width="100%",
        spacing="1",
        padding_bottom="1em",
        border_bottom=f"2px solid {THEME['primary_light']}",
        margin_bottom="1.5em",
    )


def characters_view() -> rx.Component:
    """Full view for characters with DNA editing"""
    return rx.box(
        rx.vstack(
            view_header("users", "Characters", "Click on a character to view and edit their DNA"),
            rx.cond(
                State.characters.length() > 0,
                rx.hstack(
                    rx.foreach(
                        State.characters,
                        lambda char: rx.box(
                            rx.vstack(
                                rx.image(
                                    src=char.image_url,
                                    width="100%",
                                    height="250px",
                                    object_fit="cover",
                                    border_radius="12px",
                                ),
                                rx.text(char.name, weight="bold", size="4", color=THEME["text"]),
                                rx.text(char.description[:100] + "...", size="2", color=THEME["text_muted"]),
                                rx.button(
                                    rx.icon("dna", size=16),
                                    "View DNA",
                                    size="2",
                                    width="100%",
                                    style={
                                        "background": f"linear-gradient(135deg, {THEME['secondary']} 0%, {THEME['secondary_hover']} 100%)",
                                        "color": "white",
                                        "font_weight": "600",
                                    },
                                    on_click=lambda: State.open_character_editor(char.id),
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            padding="1em",
                            background=THEME["surface"],
                            border_radius="16px",
                            border=f"1px solid {THEME['border']}",
                            width="280px",
                            cursor="pointer",
                            _hover={"box_shadow": "0 4px 20px rgba(124, 58, 237, 0.15)"},
                        ),
                    ),
                    spacing="4",
                    flex_wrap="wrap",
                    justify="center",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("users", size=48, color=THEME["text_light"]),
                        rx.text("No characters yet", size="3", color=THEME["text_muted"]),
                        rx.text("Generate a story to create characters", size="2", color=THEME["text_light"]),
                        spacing="2",
                        align="center",
                    ),
                    padding="4em",
                ),
            ),
            width="100%",
            spacing="4",
        ),
        padding="2em",
        background=THEME["background"],
        min_height="calc(100vh - 120px)",
    )


def scenes_view() -> rx.Component:
    """Full view for scenes with regeneration"""
    return rx.box(
        rx.vstack(
            view_header("film", "Scenes", "Click regenerate to create a new version of any scene"),
            rx.cond(
                State.scenes.length() > 0,
                rx.vstack(
                    rx.foreach(
                        State.scenes,
                        lambda scene: rx.box(
                            rx.hstack(
                                rx.image(
                                    src=scene.image_url,
                                    width="300px",
                                    height="200px",
                                    object_fit="cover",
                                    border_radius="12px",
                                ),
                                rx.vstack(
                                    rx.text(scene.title, weight="bold", size="4", color=THEME["text"]),
                                    rx.text(scene.description, size="2", color=THEME["text_muted"]),
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("refresh-cw", size=16),
                                            "Regenerate",
                                            variant="outline",
                                            size="2",
                                            style={"border_color": THEME["primary"], "color": THEME["primary"]},
                                            loading=State.regenerating_scene_id == scene.id,
                                            on_click=lambda: State.regenerate_scene(scene.id),
                                        ),
                                        rx.button(
                                            rx.icon("expand", size=16),
                                            "Full View",
                                            variant="soft",
                                            size="2",
                                            on_click=lambda: State.open_scene_preview(0),
                                        ),
                                        spacing="2",
                                    ),
                                    spacing="3",
                                    flex="1",
                                    align="start",
                                ),
                                spacing="4",
                                width="100%",
                                align="start",
                            ),
                            padding="1.5em",
                            background=THEME["surface"],
                            border_radius="16px",
                            border=f"1px solid {THEME['border']}",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("film", size=48, color=THEME["text_light"]),
                        rx.text("No scenes yet", size="3", color=THEME["text_muted"]),
                        rx.text("Generate a story to create scenes", size="2", color=THEME["text_light"]),
                        spacing="2",
                        align="center",
                    ),
                    padding="4em",
                ),
            ),
            width="100%",
            max_width="900px",
            margin="0 auto",
            spacing="4",
        ),
        padding="2em",
        background=THEME["background"],
        min_height="calc(100vh - 120px)",
    )


def manga_panel_with_dialog(scene, dialog: str) -> rx.Component:
    """Manga panel with dialog text below image"""
    return rx.vstack(
        # Image container with grayscale filter
        rx.box(
            rx.image(
                src=scene.image_url,
                width="100%",
                height="280px",
                object_fit="cover",
                style={"filter": "grayscale(100%) contrast(1.1)"},
            ),
            # Edit dialog button
            rx.box(
                rx.icon_button(
                    rx.icon("message-circle", size=16),
                    size="1",
                    variant="solid",
                    style={"background": THEME["primary"]},
                    on_click=lambda: State.open_dialog_editor(scene.id),
                ),
                position="absolute",
                bottom="10px",
                right="10px",
            ),
            position="relative",
            width="100%",
        ),
        # Dialog text below image
        rx.cond(
            dialog != "",
            rx.box(
                rx.text(
                    dialog,
                    size="1",
                    color="black",
                    weight="medium",
                    style={
                        "font_size": "11px",
                        "line_height": "1.4",
                        "white_space": "pre-wrap",
                    },
                ),
                background="white",
                padding="0.6em 0.8em",
                width="100%",
                border_top="2px solid black",
            ),
        ),
        spacing="0",
        border="3px solid black",
        border_radius="4px",
        overflow="hidden",
        background="white",
    )


def manga_view() -> rx.Component:
    """Full manga view with dialog overlays"""
    return rx.box(
        rx.vstack(
            view_header("layout-grid", "Manga View", "Add speech bubbles and export as black & white manga"),
            rx.cond(
                State.scenes.length() > 0,
                rx.vstack(
                    # AI Generate Dialogs button
                    rx.button(
                        rx.icon("sparkles", size=18),
                        "AI Generate Dialogs",
                        size="2",
                        variant="outline",
                        loading=State.generating_dialogs,
                        style={
                            "border_color": THEME["accent"],
                            "color": THEME["accent"],
                            "margin_bottom": "1em",
                        },
                        on_click=State.generate_manga_dialogs,
                    ),
                    # Progress indicator
                    rx.cond(
                        State.generating_dialogs,
                        rx.text(State.current_step, size="1", color=THEME["text_muted"]),
                    ),
                    # Manga grid layout
                    rx.box(
                        rx.foreach(
                            State.scenes,
                            lambda scene: manga_panel_with_dialog(scene, State.scene_dialogs.get(scene.id, "")),
                        ),
                        display="grid",
                        grid_template_columns="repeat(2, 1fr)",
                        gap="8px",
                        padding="1em",
                        background="white",
                        border="4px solid black",
                        border_radius="8px",
                        max_width="700px",
                    ),
                    # Export button
                    rx.button(
                        rx.icon("download", size=18),
                        "Export Manga",
                        size="3",
                        style={
                            "background": THEME["gradient_button"],
                            "color": "white",
                            "margin_top": "1.5em",
                        },
                        on_click=State.export_manga,
                    ),
                    align="center",
                    spacing="3",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("layout-grid", size=48, color=THEME["text_light"]),
                        rx.text("No scenes for manga", size="3", color=THEME["text_muted"]),
                        rx.text("Generate a story first", size="2", color=THEME["text_light"]),
                        spacing="2",
                        align="center",
                    ),
                    padding="4em",
                ),
            ),
            width="100%",
            spacing="4",
            align="center",
        ),
        padding="2em",
        background=THEME["background"],
        min_height="calc(100vh - 120px)",
    )


def manhwa_panel_with_dialog(scene, dialog: str) -> rx.Component:
    """Manhwa panel with speech bubble overlay"""
    return rx.box(
        # Full color image
        rx.image(
            src=scene.image_url,
            width="100%",
            height="400px",
            object_fit="cover",
        ),
        # Dialog bubble overlay
        rx.cond(
            dialog != "",
            rx.box(
                rx.text(dialog, size="2", color="white", weight="medium"),
                position="absolute",
                bottom="20px",
                left="20px",
                background="rgba(0,0,0,0.75)",
                padding="0.75em 1.25em",
                border_radius="16px",
                max_width="80%",
            ),
        ),
        # Scene title
        rx.box(
            rx.text(scene.title, size="1", color="white", weight="bold"),
            position="absolute",
            top="10px",
            left="10px",
            background="rgba(124, 58, 237, 0.9)",
            padding="0.25em 0.75em",
            border_radius="8px",
        ),
        # Edit dialog button
        rx.box(
            rx.icon_button(
                rx.icon("message-circle", size=16),
                size="1",
                variant="solid",
                style={"background": THEME["secondary"]},
                on_click=lambda: State.open_dialog_editor(scene.id),
            ),
            position="absolute",
            top="10px",
            right="10px",
        ),
        position="relative",
        border_radius="8px",
        overflow="hidden",
        box_shadow="0 4px 20px rgba(0,0,0,0.2)",
    )


def manhwa_view() -> rx.Component:
    """Full manhwa view with dialog overlays - vertical scroll"""
    return rx.box(
        rx.vstack(
            view_header("scroll", "Manhwa View", "Add dialog text and export as colorful vertical scroll"),
            rx.cond(
                State.scenes.length() > 0,
                rx.vstack(
                    # AI Generate Dialogs button
                    rx.button(
                        rx.icon("sparkles", size=18),
                        "AI Generate Dialogs",
                        size="2",
                        variant="outline",
                        loading=State.generating_dialogs,
                        style={
                            "border_color": THEME["secondary"],
                            "color": THEME["secondary"],
                            "margin_bottom": "1em",
                        },
                        on_click=State.generate_manhwa_dialogs,
                    ),
                    # Progress indicator
                    rx.cond(
                        State.generating_dialogs,
                        rx.text(State.current_step, size="1", color=THEME["text_muted"]),
                    ),
                    # Manhwa vertical scroll layout
                    rx.vstack(
                        rx.foreach(
                            State.scenes,
                            lambda scene: manhwa_panel_with_dialog(scene, State.scene_dialogs.get(scene.id, "")),
                        ),
                        spacing="1",
                        width="100%",
                        max_width="500px",
                        padding="0.5em",
                        background=THEME["surface"],
                        border_radius="12px",
                        border=f"1px solid {THEME['border']}",
                    ),
                    # Export button
                    rx.button(
                        rx.icon("download", size=18),
                        "Export Manhwa",
                        size="3",
                        style={
                            "background": f"linear-gradient(135deg, {THEME['secondary']} 0%, {THEME['secondary_hover']} 100%)",
                            "color": "white",
                            "margin_top": "1.5em",
                        },
                        on_click=State.export_manhwa,
                    ),
                    align="center",
                    spacing="3",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("scroll", size=48, color=THEME["text_light"]),
                        rx.text("No scenes for manhwa", size="3", color=THEME["text_muted"]),
                        rx.text("Generate a story first", size="2", color=THEME["text_light"]),
                        spacing="2",
                        align="center",
                    ),
                    padding="4em",
                ),
            ),
            width="100%",
            spacing="4",
            align="center",
        ),
        padding="2em",
        background=THEME["background"],
        min_height="calc(100vh - 120px)",
    )


# ============== HEADER ==============

def header() -> rx.Component:
    """Centered logo header with Electric Violet gradient"""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.text("🔥", font_size="3em"),
                    rx.heading(
                        "VisionForge",
                        size="8",
                        weight="bold",
                        style={"color": "white", "letter_spacing": "-0.02em"},
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.text(
                    "One character. Infinite scenes.",
                    size="3",
                    style={
                        "color": "rgba(255,255,255,0.85)",
                        "font_style": "italic",
                        "letter_spacing": "0.05em",
                    },
                ),
                spacing="1",
                align="center",
            ),
            width="100%",
            padding="2em",
        ),
        background=THEME["gradient_header"],
        box_shadow="0 4px 20px rgba(124, 58, 237, 0.3)",
    )


# ============== MAIN COMPONENTS ==============

def progress_indicator() -> rx.Component:
    """Show generation progress"""
    return rx.cond(
        State.is_loading,
        rx.vstack(
            rx.text(State.current_step, size="2", color=THEME["text_muted"]),
            rx.progress(value=State.generation_progress, width="100%"),
            width="100%",
            spacing="2",
            padding_top="1em",
        ),
    )


def story_input() -> rx.Component:
    """Story input with Electric Violet styling"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("pencil", size=22, color=THEME["primary"]),
                rx.heading("Tell Your Story", size="5", color=THEME["text"]),
                spacing="2",
                align="center",
                justify="center",
                width="100%",
            ),
            rx.text(
                "Describe your characters and scenes with visual details like hair color, eye color, clothing, and settings.",
                color=THEME["text_muted"],
                size="2",
                text_align="center",
            ),
            rx.text_area(
                placeholder="A wandering samurai named Kaito with silver hair and piercing red eyes travels through feudal Japan. He wears a tattered black haori with red lining...\n\nIn an abandoned temple, he discovers a mysterious girl named Yuki with long white hair and violet eyes...",
                value=State.story_text,
                on_change=State.set_story_text,
                width="100%",
                min_height="200px",
                size="3",
                style={
                    "background": THEME["surface"],
                    "border": f"2px solid {THEME['primary_light']}",
                    "border_radius": "12px",
                    "color": THEME["text"],
                    "font_size": "15px",
                    "line_height": "1.6",
                    "&:focus": {
                        "border_color": THEME["primary"],
                        "box_shadow": f"0 0 0 3px {THEME['primary_light']}",
                    },
                    "&::placeholder": {
                        "color": "#374151 !important",
                        "opacity": "1 !important",
                    },
                    "::placeholder": {
                        "color": "#374151 !important",
                        "opacity": "1 !important",
                    },
                },
            ),
            rx.hstack(
                rx.badge(
                    rx.hstack(
                        rx.text("🎨", font_size="0.9em"),
                        rx.text(State.selected_style, size="2"),
                        spacing="1",
                    ),
                    size="2",
                    style={
                        "background": THEME["primary_light"],
                        "color": THEME["primary"],
                        "padding": "0.5em 1em",
                        "border_radius": "8px",
                    },
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("file-text", size=18),
                    "Load Example",
                    variant="outline",
                    size="3",
                    style={
                        "border": f"2px solid {THEME['primary']}",
                        "color": THEME["primary"],
                        "border_radius": "10px",
                        "font_weight": "500",
                    },
                    on_click=State.load_example,
                    disabled=State.is_loading,
                ),
                rx.button(
                    rx.icon("zap", size=18),
                    "Forge Vision",
                    size="3",
                    loading=State.is_loading,
                    style={
                        "background": THEME["gradient_button"],
                        "color": "white",
                        "border_radius": "10px",
                        "padding": "0 2em",
                        "font_weight": "600",
                        "box_shadow": "0 4px 15px rgba(124, 58, 237, 0.4)",
                    },
                    on_click=State.generate_story,
                ),
                width="100%",
                spacing="3",
                flex_wrap="wrap",
                justify="center",
                align="center",
            ),
            progress_indicator(),
            width="100%",
            spacing="4",
            align="center",
        ),
        padding="2em",
        background=THEME["surface"],
        border_radius="20px",
        border=f"1px solid {THEME['primary_light']}",
        box_shadow="0 4px 20px rgba(124, 58, 237, 0.08)",
        id="story-input",
    )


def section_header(icon: str, title: str, count_text) -> rx.Component:
    """Section header with Electric Violet styling"""
    return rx.hstack(
        rx.icon(icon, size=22, color=THEME["primary"]),
        rx.heading(title, size="5", color=THEME["text"]),
        rx.spacer(),
        rx.badge(
            count_text,
            size="2",
            style={"background": THEME["secondary_light"], "color": THEME["secondary"]},
        ),
        width="100%",
        align="center",
        padding_bottom="0.5em",
        border_bottom=f"2px solid {THEME['primary_light']}",
        margin_bottom="1em",
    )


def character_card(character: Character) -> rx.Component:
    """Character card with Electric Violet styling"""
    return rx.box(
        rx.vstack(
            rx.cond(
                character.image_url != "",
                rx.image(
                    src=character.image_url,
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    border_radius="12px",
                ),
                rx.center(
                    rx.spinner(size="3"),
                    width="100%",
                    height="200px",
                    background=THEME["surface_hover"],
                    border_radius="12px",
                ),
            ),
            rx.hstack(
                rx.text(character.name, weight="bold", size="3", color=THEME["text"]),
                rx.spacer(),
                rx.badge(
                    "🧬 DNA",
                    size="1",
                    style={"background": THEME["secondary_light"], "color": THEME["secondary"]},
                ),
                width="100%",
                align="center",
            ),
            spacing="3",
            width="100%",
        ),
        padding="0.75em",
        background=THEME["surface"],
        border_radius="16px",
        border=f"1px solid {THEME['border']}",
        box_shadow="0 2px 12px rgba(124, 58, 237, 0.06)",
        width="220px",
    )


def characters_section() -> rx.Component:
    """Characters section"""
    return rx.cond(
        State.characters.length() > 0,
        rx.vstack(
            section_header("users", "Characters", rx.text(State.characters.length(), " DNA Locked")),
            rx.hstack(
                rx.foreach(State.characters, character_card),
                spacing="4",
                flex_wrap="wrap",
                justify="center",
            ),
            width="100%",
            spacing="3",
        ),
    )


def scene_card(scene: Scene, index: int) -> rx.Component:
    """Scene card with Electric Violet styling - clickable"""
    return rx.box(
        rx.vstack(
            rx.cond(
                scene.image_url != "",
                rx.image(
                    src=scene.image_url,
                    width="100%",
                    height="160px",
                    object_fit="cover",
                    border_radius="10px",
                ),
                rx.center(
                    rx.spinner(size="3"),
                    width="100%",
                    height="160px",
                    background=THEME["surface_hover"],
                    border_radius="10px",
                ),
            ),
            rx.hstack(
                rx.text(scene.title, weight="medium", size="2", color=THEME["text"]),
                rx.spacer(),
                rx.icon("expand", size=14, color=THEME["text_muted"]),
                width="100%",
                align="center",
            ),
            spacing="2",
            width="100%",
        ),
        padding="0.5em",
        background=THEME["surface"],
        border_radius="14px",
        border=f"1px solid {THEME['border']}",
        box_shadow="0 2px 10px rgba(124, 58, 237, 0.05)",
        width="200px",
        cursor="pointer",
        _hover={"box_shadow": "0 4px 20px rgba(124, 58, 237, 0.15)", "transform": "translateY(-2px)"},
        transition="all 0.2s ease",
        on_click=lambda: State.open_scene_preview(index),
    )


def scenes_section() -> rx.Component:
    """Scenes section"""
    return rx.cond(
        State.scenes.length() > 0,
        rx.vstack(
            section_header("film", "Story Scenes", rx.text(State.scenes.length(), " scenes")),
            rx.text("Click any scene to view full size", size="1", color=THEME["text_muted"], style={"margin_top": "-0.5em", "margin_bottom": "0.5em"}),
            rx.hstack(
                rx.foreach(
                    State.scenes,
                    lambda scene, idx: scene_card(scene, idx),
                ),
                spacing="3",
                flex_wrap="wrap",
                justify="center",
            ),
            width="100%",
            spacing="3",
        ),
    )


def error_banner() -> rx.Component:
    """Error message display"""
    return rx.cond(
        State.error_message != "",
        rx.callout(
            State.error_message,
            icon="circle-alert",
            color="red",
            width="100%",
        ),
    )


def export_status() -> rx.Component:
    """Export progress status"""
    return rx.cond(
        State.export_progress != "",
        rx.callout(
            State.export_progress,
            icon="download",
            color="green",
            width="100%",
        ),
    )


def footer() -> rx.Component:
    """Footer"""
    return rx.center(
        rx.hstack(
            rx.text("Built with", size="2", color=THEME["text_muted"]),
            rx.link(
                "FIBO by Bria AI",
                href="https://bria.ai/fibo",
                style={"color": THEME["primary"], "font_weight": "500"},
            ),
            rx.text("for the FIBO Hackathon 2025", size="2", color=THEME["text_muted"]),
            spacing="1",
            justify="center",
            align="center",
        ),
        width="100%",
        padding="3em",
    )


def main_content() -> rx.Component:
    """Main content area for story creation"""
    return rx.box(
        rx.vstack(
            # Error banner
            error_banner(),

            # Export status
            export_status(),

            # Story Input
            story_input(),

            # Characters Section
            characters_section(),

            # Scenes Section
            scenes_section(),

            # Footer
            footer(),

            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding="2em",
            spacing="6",
        ),
        background=THEME["background"],
        min_height="calc(100vh - 120px)",
    )


def index() -> rx.Component:
    """Main page with sidebar and conditional views"""
    return rx.box(
        # Sidebar (fixed left)
        sidebar(),

        # Dialogs
        new_story_dialog(),
        delete_confirm_dialog(),
        scene_preview_modal(),
        manga_preview_modal(),
        manhwa_preview_modal(),
        character_editor_modal(),
        dialog_editor_modal(),

        # Main content area
        rx.box(
            # Centered Header (show on main view)
            rx.cond(
                State.active_view == "main",
                header(),
            ),

            # Conditional content based on active view
            rx.match(
                State.active_view,
                ("characters", characters_view()),
                ("scenes", scenes_view()),
                ("manga", manga_view()),
                ("manhwa", manhwa_view()),
                main_content(),  # Default: main view
            ),

            # Push content right to account for sidebar
            margin_left="280px",
            style={
                "@media (max-width: 768px)": {
                    "margin_left": "220px",
                },
                "@media (min-width: 1400px)": {
                    "margin_left": "300px",
                },
            },
        ),

        background=THEME["background"],
    )


# App config with Electric Violet theme
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="violet",
        radius="large",
    ),
    style={
        "background_color": THEME["background"],
        "font_family": "'Inter', -apple-system, sans-serif",
        "textarea::placeholder": {
            "color": "#374151 !important",
            "opacity": "1 !important",
        },
        ".rt-TextAreaInput::placeholder": {
            "color": "#374151 !important",
            "opacity": "1 !important",
        },
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "/custom.css",
    ],
)
app.add_page(index, title="VisionForge - AI Visual Story Creation")
