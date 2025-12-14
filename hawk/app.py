"""Hawk TUI - Main Textual application."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, Button, Label, ListItem, ListView
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual import work
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

from hawk.config import PROJECTS, COLORS, Project
from hawk import replicate_client, video


class ProjectSelector(Static):
    """Sidebar showing available projects."""

    selected = reactive("wedding-vision")

    def render(self) -> Panel:
        lines = []
        for i, (slug, proj) in enumerate(PROJECTS.items(), 1):
            if slug == self.selected:
                line = f"[bold {COLORS['accent']}]>[{i}] {proj.name}[/]"
            else:
                line = f" [{COLORS['dim']}][{i}][/] {proj.name}"
            lines.append(line)
            lines.append(f"    [dim]{proj.description}[/]")
            lines.append("")

        return Panel(
            "\n".join(lines),
            title="[bold]PROJECTS[/]",
            border_style=COLORS["border"],
        )


class ImageList(Static):
    """Display list of images in current project."""

    images: reactive[list[Path]] = reactive(list)
    selected_indices: reactive[set[int]] = reactive(set)

    def render(self) -> Panel:
        if not self.images:
            content = "[dim]No images yet. Press [g] to generate.[/]"
        else:
            lines = []
            for i, img in enumerate(self.images[:20]):  # Show last 20
                marker = "[green]✓[/]" if i in self.selected_indices else " "
                name = img.name[:40] + "..." if len(img.name) > 40 else img.name
                lines.append(f"{marker} [{i+1:2}] {name}")
            content = "\n".join(lines)
            if len(self.images) > 20:
                content += f"\n[dim]... and {len(self.images) - 20} more[/]"

        return Panel(
            content,
            title=f"[bold]IMAGES ({len(self.images)})[/]",
            border_style=COLORS["border"],
        )


class StatusBar(Static):
    """Bottom status bar."""

    message: reactive[str] = reactive("Ready")
    is_working: reactive[bool] = reactive(False)

    def render(self) -> Text:
        if self.is_working:
            return Text(f"⏳ {self.message}", style=f"bold {COLORS['accent']}")
        return Text(f"✓ {self.message}", style=f"bold {COLORS['success']}")


class MenuPanel(Static):
    """Right panel showing available actions."""

    def render(self) -> Panel:
        lines = [
            f"[{COLORS['accent']}][g][/] Generate images",
            f"[{COLORS['accent']}][b][/] Browse gallery",
            f"[{COLORS['accent']}][s][/] Select/deselect",
            f"[{COLORS['accent']}][a][/] Select all",
            "",
            f"[{COLORS['accent']}][v][/] Create video",
            f"[{COLORS['accent']}][o][/] Add audio",
            "",
            f"[{COLORS['accent']}][1][/] Wedding Vision",
            f"[{COLORS['accent']}][2][/] Latin Bible",
            f"[{COLORS['accent']}][3][/] DXP Albums",
            "",
            f"[{COLORS['accent']}][d][/] Delete selected",
            f"[{COLORS['accent']}][q][/] Quit",
        ]

        return Panel(
            "\n".join(lines),
            title="[bold]ACTIONS[/]",
            border_style=COLORS["border"],
        )


class PromptInput(Static):
    """Prompt input area."""

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Enter prompt for image generation...",
            id="prompt-input"
        )


class HawkApp(App):
    """Hawk TUI main application."""

    CSS = """
    Screen {
        background: #1a1d23;
    }

    #main-container {
        layout: horizontal;
        height: 100%;
    }

    #left-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #center-panel {
        width: 2fr;
        height: 100%;
        padding: 1;
    }

    #right-panel {
        width: 1fr;
        height: 100%;
        padding: 1;
    }

    #prompt-container {
        height: 5;
        dock: bottom;
        padding: 1;
    }

    #prompt-input {
        width: 100%;
        background: #2d3748;
        color: #e0e0e0;
        border: solid #4a5f4a;
    }

    #status-bar {
        height: 1;
        dock: bottom;
        padding: 0 1;
        background: #2d3748;
    }

    ProjectSelector {
        height: auto;
    }

    ImageList {
        height: 1fr;
    }

    MenuPanel {
        height: auto;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("g", "generate", "Generate"),
        Binding("b", "browse", "Browse"),
        Binding("v", "create_video", "Video"),
        Binding("o", "add_audio", "Audio"),
        Binding("s", "toggle_select", "Select"),
        Binding("a", "select_all", "Select All"),
        Binding("d", "delete_selected", "Delete"),
        Binding("1", "select_project_1", "Wedding"),
        Binding("2", "select_project_2", "Latin"),
        Binding("3", "select_project_3", "DXP"),
        Binding("escape", "clear_selection", "Clear"),
    ]

    current_project: reactive[str] = reactive("wedding-vision")
    selected_images: reactive[set[int]] = reactive(set)

    def __init__(self):
        super().__init__()
        self.images: list[Path] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Container(
                ProjectSelector(id="project-selector"),
                id="left-panel",
            ),
            Container(
                ImageList(id="image-list"),
                id="center-panel",
            ),
            Container(
                MenuPanel(id="menu-panel"),
                id="right-panel",
            ),
            id="main-container",
        )
        yield Container(
            Input(
                placeholder="Enter prompt for image generation... (press Enter)",
                id="prompt-input"
            ),
            id="prompt-container",
        )
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app."""
        self.refresh_images()
        self.query_one("#prompt-input", Input).focus()

    @property
    def project(self) -> Project:
        """Get the current project."""
        return PROJECTS[self.current_project]

    def refresh_images(self) -> None:
        """Refresh the image list."""
        self.images = replicate_client.get_project_images(self.project)
        image_list = self.query_one("#image-list", ImageList)
        image_list.images = self.images
        image_list.selected_indices = self.selected_images

    def watch_current_project(self, project_slug: str) -> None:
        """Called when project changes."""
        self.selected_images = set()
        selector = self.query_one("#project-selector", ProjectSelector)
        selector.selected = project_slug
        self.refresh_images()
        self.set_status(f"Switched to {self.project.name}")

    def set_status(self, message: str, working: bool = False) -> None:
        """Update the status bar."""
        status = self.query_one("#status-bar", StatusBar)
        status.message = message
        status.is_working = working

    def action_select_project_1(self) -> None:
        self.current_project = "wedding-vision"

    def action_select_project_2(self) -> None:
        self.current_project = "latin-bible"

    def action_select_project_3(self) -> None:
        self.current_project = "dxp-albs"

    def action_toggle_select(self) -> None:
        """Toggle selection of current image."""
        if not self.images:
            return
        # For now, just toggle first unselected or last selected
        if 0 in self.selected_images:
            self.selected_images.discard(0)
        else:
            self.selected_images.add(0)
        image_list = self.query_one("#image-list", ImageList)
        image_list.selected_indices = self.selected_images

    def action_select_all(self) -> None:
        """Select all images."""
        self.selected_images = set(range(len(self.images)))
        image_list = self.query_one("#image-list", ImageList)
        image_list.selected_indices = self.selected_images
        self.set_status(f"Selected {len(self.images)} images")

    def action_clear_selection(self) -> None:
        """Clear all selections."""
        self.selected_images = set()
        image_list = self.query_one("#image-list", ImageList)
        image_list.selected_indices = self.selected_images
        self.set_status("Selection cleared")

    def action_delete_selected(self) -> None:
        """Delete selected images."""
        if not self.selected_images:
            self.set_status("No images selected")
            return
        count = 0
        for idx in sorted(self.selected_images, reverse=True):
            if idx < len(self.images):
                if replicate_client.delete_image(self.images[idx]):
                    count += 1
        self.selected_images = set()
        self.refresh_images()
        self.set_status(f"Deleted {count} images")

    @work(exclusive=True, thread=True)
    def action_generate(self) -> None:
        """Generate images from prompt."""
        prompt_input = self.query_one("#prompt-input", Input)
        prompt = prompt_input.value.strip()

        if not prompt:
            self.call_from_thread(self.set_status, "Enter a prompt first")
            return

        self.call_from_thread(self.set_status, f"Generating with {self.project.name}...", True)

        try:
            paths = replicate_client.generate_image(self.project, prompt)
            self.call_from_thread(self.refresh_images)
            self.call_from_thread(self.set_status, f"Generated {len(paths)} image(s)")
            self.call_from_thread(lambda: setattr(prompt_input, "value", ""))
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error: {str(e)[:50]}")

    @work(exclusive=True, thread=True)
    def action_create_video(self) -> None:
        """Create video from selected images."""
        if not self.selected_images:
            self.call_from_thread(self.set_status, "Select images first (press 'a' for all)")
            return

        self.call_from_thread(self.set_status, "Creating video...", True)

        try:
            selected_paths = [self.images[i] for i in sorted(self.selected_images)]
            output = video.create_slideshow(self.project, selected_paths)
            self.call_from_thread(self.set_status, f"Video saved: {output.name}")
        except Exception as e:
            self.call_from_thread(self.set_status, f"Error: {str(e)[:50]}")

    def action_browse(self) -> None:
        """Open the exports folder."""
        import subprocess
        subprocess.run(["open", str(self.project.exports_dir)])
        self.set_status(f"Opened {self.project.exports_dir}")

    def action_add_audio(self) -> None:
        """Show audio files available."""
        audio_files = video.get_project_audio(self.project)
        if audio_files:
            self.set_status(f"Found {len(audio_files)} audio files in {self.project.audio_dir}")
        else:
            self.set_status(f"Add audio files to: {self.project.audio_dir}")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in prompt input."""
        if event.input.id == "prompt-input":
            self.action_generate()


def main():
    """Entry point."""
    app = HawkApp()
    app.run()


if __name__ == "__main__":
    main()
