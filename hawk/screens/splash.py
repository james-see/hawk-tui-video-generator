"""Splash screen with fade-in effect."""

from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult
from textual import on
from textual.containers import Center, Middle
import asyncio

HAWK_ASCII = r"""
[#4a5f4a]
                                    ▄▄▄
                                  ▄█████▄
                                 ▐███████▌
                                  ▀█████▀
                                    ███
                                   ▄███▄
                                  ██▀ ▀██
                                 ▐█▌   ▐█▌
                                 ██     ██
                                ▐█▌     ▐█▌
                               ▄██       ██▄
                              ▐██▌       ▐██▌
                             ▄███         ███▄
                            ▐███▌         ▐███▌
                           ▄█████         █████▄
                          ███████▄       ▄███████
                         ▐████████▄   ▄████████▌
                        ▄██████████▀ ▀██████████▄
                       ▐████████▀       ▀████████▌
                      ▄███████▀           ▀███████▄
                     ▐██████▀               ▀██████▌
                    ▄█████▀                   ▀█████▄
                   ▐████▀                       ▀████▌
                  ▄███▀                           ▀███▄
                 ▐██▀                               ▀██▌
[/]
"""

HAWK_2E_LOGO = """
[bold #c9a227]
    ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗    ██████╗ ███████╗
    ██║  ██║██╔══██╗██║    ██║██║ ██╔╝    ╚════██╗██╔════╝
    ███████║███████║██║ █╗ ██║█████╔╝      █████╔╝█████╗
    ██╔══██║██╔══██║██║███╗██║██╔═██╗     ██╔═══╝ ██╔══╝
    ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗    ███████╗███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝╚══════╝
[/]
[#4a5f4a]
              ╔═══════════════════════════════════╗
              ║     TikTok Video Creator TUI      ║
              ╚═══════════════════════════════════╝
[/]
[dim]
        // Powered by Claude Code Agent SDK + Replicate
[/]
"""


class SplashContent(Static):
    """The splash screen content."""

    def __init__(self):
        super().__init__()
        self._phase = 0

    def render(self) -> str:
        if self._phase == 0:
            return ""
        elif self._phase == 1:
            return HAWK_2E_LOGO
        elif self._phase == 2:
            return HAWK_2E_LOGO + HAWK_ASCII
        else:
            return HAWK_2E_LOGO + HAWK_ASCII

    def advance(self) -> bool:
        """Advance to next phase. Returns True if more phases remain."""
        self._phase += 1
        self.refresh()
        return self._phase < 3


class SplashScreen(Screen):
    """Splash screen with fade-in animation."""

    CSS = """
    SplashScreen {
        background: #1a1d23;
        align: center middle;
    }

    SplashContent {
        width: auto;
        height: auto;
        text-align: center;
    }
    """

    BINDINGS = [
        ("escape", "skip", "Skip"),
        ("enter", "skip", "Skip"),
        ("space", "skip", "Skip"),
    ]

    def compose(self) -> ComposeResult:
        yield Middle(
            Center(
                SplashContent(id="splash-content")
            )
        )

    async def on_mount(self) -> None:
        """Start the animation sequence."""
        self.run_animation()

    async def run_animation(self) -> None:
        """Run the fade-in animation."""
        content = self.query_one("#splash-content", SplashContent)

        # Phase 1: Show logo
        await asyncio.sleep(0.3)
        content.advance()

        # Phase 2: Show hawk
        await asyncio.sleep(0.5)
        content.advance()

        # Wait then dismiss
        await asyncio.sleep(1.5)
        self.app.pop_screen()

    def action_skip(self) -> None:
        """Skip the splash screen."""
        self.app.pop_screen()
