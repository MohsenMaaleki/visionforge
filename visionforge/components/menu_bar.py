"""VisionForge - Menu Bar Component with Sakura Theme"""
import reflex as rx

# Sakura Theme Colors
SAKURA = {
    "background": "#FFF8F0",
    "surface": "#FFFFFF",
    "primary": "#E8837B",
    "text": "#2D2A26",
    "text_muted": "#9A8F8A",
    "border": "#F0E6E0",
    "secondary": "#FFB5BA",
}


def menu_bar() -> rx.Component:
    """Top menu bar with File, Edit, Export, Help - Sakura styled"""
    from ..state import State

    return rx.hstack(
        # File Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("folder", size=16),
                    "File",
                    variant="ghost",
                    size="2",
                    style={"color": SAKURA["text"]},
                ),
            ),
            rx.menu.content(
                rx.menu.item("New Project", shortcut="Ctrl+N", on_click=State.new_project),
                rx.menu.item("Save Project", shortcut="Ctrl+S"),
                rx.menu.separator(),
                rx.menu.item("Load Example", on_click=State.load_example),
            ),
        ),

        # Edit Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("pencil", size=16),
                    "Edit",
                    variant="ghost",
                    size="2",
                    style={"color": SAKURA["text"]},
                ),
            ),
            rx.menu.content(
                rx.menu.item("Clear All", on_click=State.clear_results),
                rx.menu.separator(),
                rx.menu.item("Settings", on_click=State.toggle_settings),
            ),
        ),

        # Export Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("download", size=16),
                    "Export",
                    variant="ghost",
                    size="2",
                    style={"color": SAKURA["text"]},
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.hstack(
                        rx.icon("layout-grid", size=14),
                        rx.text("Manga (B&W)"),
                        spacing="2",
                    ),
                    on_click=State.export_manga,
                ),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("scroll", size=14),
                        rx.text("Manhwa (Color)"),
                        spacing="2",
                    ),
                    on_click=State.export_manhwa,
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("film", size=14),
                        rx.text("Slideshow Video"),
                        spacing="2",
                    ),
                    on_click=State.export_slideshow,
                ),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("sparkles", size=14),
                        rx.text("AI Video (Luma)"),
                        spacing="2",
                    ),
                    on_click=State.export_luma_video,
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.hstack(
                        rx.icon("archive", size=14),
                        rx.text("All Images (ZIP)"),
                        spacing="2",
                    ),
                    on_click=State.export_all_images,
                ),
            ),
        ),

        # Help Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("circle-help", size=16),
                    "Help",
                    variant="ghost",
                    size="2",
                    style={"color": SAKURA["text"]},
                ),
            ),
            rx.menu.content(
                rx.menu.item("Documentation"),
                rx.menu.item("Keyboard Shortcuts"),
                rx.menu.separator(),
                rx.menu.item("About VisionForge"),
            ),
        ),

        rx.spacer(),

        # Theme badge
        rx.badge("🌸 Sakura", color_scheme="pink", variant="soft"),

        width="100%",
        padding="0.5em 1em",
        background=SAKURA["surface"],
        border_bottom=f"1px solid {SAKURA['border']}",
        align="center",
    )
