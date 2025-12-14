"""Hawk TUI entry point."""

import sys
from hawk.app import HawkApp


def main():
    """Main entry point."""
    app = HawkApp()
    app.run()


if __name__ == "__main__":
    main()
