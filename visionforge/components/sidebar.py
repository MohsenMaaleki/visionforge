"""VisionForge - Sidebar Component with Sakura Theme"""
import reflex as rx

# Sakura Theme Colors
SAKURA = {
    "background": "#FFF8F0",
    "surface": "#FFFFFF",
    "surface_hover": "#FFF0E6",
    "primary": "#E8837B",
    "primary_hover": "#D66B63",
    "text": "#2D2A26",
    "text_muted": "#9A8F8A",
    "border": "#F0E6E0",
    "accent": "#7EB09B",
    "secondary": "#FFB5BA",
}


def project_item(project) -> rx.Component:
    """Single project item in the sidebar"""
    from ..state import State

    return rx.hstack(
        rx.icon("file-text", size=14, color=SAKURA["text"]),
        rx.text(project.name, size="2", color=SAKURA["text"]),
        width="100%",
        padding="0.5em",
        border_radius="8px",
        cursor="pointer",
        _hover={"background": SAKURA["surface_hover"]},
        on_click=lambda: State.load_project(project.id),
    )


def sidebar() -> rx.Component:
    """Left sidebar with projects, settings, and export - Sakura styled"""
    from ..state import State

    return rx.vstack(
        # Projects Section
        rx.vstack(
            rx.hstack(
                rx.icon("folder", size=16, color=SAKURA["primary"]),
                rx.text("PROJECTS", size="1", weight="bold", color=SAKURA["text_muted"]),
                width="100%",
            ),
            rx.vstack(
                rx.foreach(State.projects, project_item),
                width="100%",
            ),
            rx.button(
                rx.icon("plus", size=14),
                "New Project",
                variant="ghost",
                size="1",
                width="100%",
                style={"color": SAKURA["primary"]},
                on_click=State.new_project,
            ),
            width="100%",
            spacing="2",
        ),

        rx.divider(style={"border_color": SAKURA["border"]}),

        # Settings Section
        rx.vstack(
            rx.hstack(
                rx.icon("settings", size=16, color=SAKURA["primary"]),
                rx.text("SETTINGS", size="1", weight="bold", color=SAKURA["text_muted"]),
                width="100%",
            ),
            rx.button(
                rx.icon("palette", size=14),
                "Style Settings",
                variant="ghost",
                size="1",
                width="100%",
                style={"color": SAKURA["text"]},
            ),
            rx.button(
                rx.icon("key", size=14),
                "API Keys",
                variant="ghost",
                size="1",
                width="100%",
                style={"color": SAKURA["text"]},
                on_click=State.toggle_settings,
            ),
            width="100%",
            spacing="1",
        ),

        rx.divider(style={"border_color": SAKURA["border"]}),

        # Quick Export Section
        rx.vstack(
            rx.hstack(
                rx.icon("download", size=16, color=SAKURA["primary"]),
                rx.text("QUICK EXPORT", size="1", weight="bold", color=SAKURA["text_muted"]),
                width="100%",
            ),
            rx.button(
                rx.icon("layout-grid", size=14),
                "Manga",
                variant="outline",
                size="1",
                width="100%",
                style={"border_color": SAKURA["border"], "color": SAKURA["text"]},
                on_click=State.export_manga,
                disabled=State.scenes.length() == 0,
            ),
            rx.button(
                rx.icon("scroll", size=14),
                "Manhwa",
                variant="outline",
                size="1",
                width="100%",
                style={"border_color": SAKURA["border"], "color": SAKURA["text"]},
                on_click=State.export_manhwa,
                disabled=State.scenes.length() == 0,
            ),
            rx.button(
                rx.icon("film", size=14),
                "Slideshow",
                variant="outline",
                size="1",
                width="100%",
                style={"border_color": SAKURA["border"], "color": SAKURA["text"]},
                on_click=State.export_slideshow,
                disabled=State.scenes.length() == 0,
            ),
            rx.button(
                rx.icon("sparkles", size=14),
                "AI Video",
                size="1",
                width="100%",
                style={
                    "background": f"linear-gradient(135deg, {SAKURA['primary']} 0%, {SAKURA['secondary']} 100%)",
                    "color": "white",
                    "border": "none",
                },
                on_click=State.export_luma_video,
                disabled=State.scenes.length() == 0,
            ),
            width="100%",
            spacing="2",
        ),

        # Export status
        rx.cond(
            State.export_loading,
            rx.vstack(
                rx.divider(style={"border_color": SAKURA["border"]}),
                rx.text(State.export_progress, size="1", color=SAKURA["text_muted"]),
                rx.spinner(size="2"),
                width="100%",
                spacing="2",
            ),
        ),

        width="220px",
        min_height="100vh",
        padding="1em",
        background=SAKURA["surface"],
        border_right=f"1px solid {SAKURA['border']}",
        spacing="4",
        box_shadow="2px 0 8px rgba(45, 42, 38, 0.03)",
    )
