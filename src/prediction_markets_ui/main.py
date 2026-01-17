"""Main entry point for the trading UI."""

import os
import sys
from PySide6 import QtWidgets

from prediction_markets_ui.app import apply_app_style, position_window
from prediction_markets_ui.main_window import MainWindow


def _setup_wsl_platform():
    """Set Qt platform for WSL to avoid rendering artifacts."""
    try:
        release = os.uname().release
        if "WSL" in release or "microsoft" in release.lower():
            os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
    except Exception:
        pass


def main():
    """Run the trading UI application."""
    _setup_wsl_platform()
    app = QtWidgets.QApplication(sys.argv)

    # Apply styling
    apply_app_style(app)

    # Create and show main window
    window = MainWindow()
    position_window(app, window)
    window.show()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
