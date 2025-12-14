"""Splash screen with typewriter fade-in effect."""

from textual.screen import Screen
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.reactive import reactive

HAWK_LOGO_LINES = [
    "[bold #c9a227]    ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗    ██████╗ ███████╗[/]",
    "[bold #c9a227]    ██║  ██║██╔══██╗██║    ██║██║ ██╔╝    ╚════██╗██╔════╝[/]",
    "[bold #c9a227]    ███████║███████║██║ █╗ ██║█████╔╝      █████╔╝█████╗[/]",
    "[bold #c9a227]    ██╔══██║██╔══██║██║███╗██║██╔═██╗     ██╔═══╝ ██╔══╝[/]",
    "[bold #c9a227]    ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗    ███████╗███████╗[/]",
    "[bold #c9a227]    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝╚══════╝[/]",
]

HAWK_ASCII_LINES = [
    "[#4a5f4a]                                 ▄▄▄[/]",
    "[#4a5f4a]                               ▄█████▄[/]",
    "[#4a5f4a]                              ▐███████▌[/]",
    "[#4a5f4a]                               ▀█████▀[/]",
    "[#4a5f4a]                                 ███[/]",
    "[#4a5f4a]                                ▄███▄[/]",
    "[#4a5f4a]                               ██▀ ▀██[/]",
    "[#4a5f4a]                              ▐█▌   ▐█▌[/]",
    "[#4a5f4a]                              ██     ██[/]",
    "[#4a5f4a]                             ▐█▌     ▐█▌[/]",
    "[#4a5f4a]                            ▄██       ██▄[/]",
    "[#4a5f4a]                           ▐██▌       ▐██▌[/]",
    "[#4a5f4a]                          ▄███         ███▄[/]",
    "[#4a5f4a]                         ▐███▌         ▐███▌[/]",
    "[#4a5f4a]                        ▄█████         █████▄[/]",
    "[#4a5f4a]                       ███████▄       ▄███████[/]",
    "[#4a5f4a]                      ▐████████▄   ▄████████▌[/]",
    "[#4a5f4a]                     ▄██████████▀ ▀██████████▄[/]",
    "[#4a5f4a]                    ▐████████▀       ▀████████▌[/]",
    "[#4a5f4a]                   ▄███████▀           ▀███████▄[/]",
]

TAGLINE = "[#4a5f4a]         ╔═══════════════════════════════════╗[/]"
TAGLINE2 = "[#4a5f4a]         ║     TikTok Video Creator TUI      ║[/]"
TAGLINE3 = "[#4a5f4a]         ╚═══════════════════════════════════╝[/]"
POWERED = "[dim]      // Powered by Claude Code Agent SDK + Replicate[/]"
ENTER_PROMPT = "\n\n[bold #c9a227]              ▶ Press ENTER to continue ◀[/]"


class SplashText(Static):
    """Animated splash text."""

    phase = reactive(0)

    def render(self) -> str:
        lines = []

        # Phase 0: empty
        if self.phase == 0:
            return ""

        # Phase 1-6: HAWK 2E logo line by line
        if self.phase >= 1:
            for i, line in enumerate(HAWK_LOGO_LINES):
                if self.phase > i:
                    lines.append(line)

        # Phase 7: blank line + tagline box
        if self.phase >= 7:
            lines.append("")
            lines.append(TAGLINE)

        if self.phase >= 8:
            lines.append(TAGLINE2)

        if self.phase >= 9:
            lines.append(TAGLINE3)

        # Phase 10: powered by
        if self.phase >= 10:
            lines.append("")
            lines.append(POWERED)

        # Phase 11+: hawk ASCII art
        if self.phase >= 11:
            lines.append("")
            hawk_lines_to_show = min(self.phase - 10, len(HAWK_ASCII_LINES))
            for i in range(hawk_lines_to_show):
                lines.append(HAWK_ASCII_LINES[i])

        # Phase 31+: show enter prompt
        if self.phase >= 31:
            lines.append(ENTER_PROMPT)

        return "\n".join(lines)


class SplashScreen(Screen):
    """Splash screen with typewriter animation."""

    CSS = """
    SplashScreen {
        background: #1a1d23;
        align: center middle;
    }

    #splash-text {
        width: auto;
        height: auto;
        text-align: center;
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("enter", "continue", "Continue"),
        ("space", "continue", "Continue"),
        ("escape", "continue", "Continue"),
    ]

    def __init__(self):
        super().__init__()
        self._timer = None
        self._ready = False

    def compose(self) -> ComposeResult:
        yield Middle(
            Center(
                SplashText(id="splash-text")
            )
        )

    def on_mount(self) -> None:
        """Start the animation."""
        self._animate()

    def _animate(self) -> None:
        """Run typewriter animation."""
        text = self.query_one("#splash-text", SplashText)
        text.phase += 1

        # Total phases: 6 (logo) + 4 (taglines) + 20 (hawk) + 1 (prompt) = 31
        if text.phase < 32:
            # Faster for logo, slower for hawk
            delay = 0.05 if text.phase <= 10 else 0.03
            self._timer = self.set_timer(delay, self._animate)
        else:
            self._ready = True

    def action_continue(self) -> None:
        """Continue to main app."""
        if self._timer:
            self._timer.stop()
        self.app.pop_screen()
