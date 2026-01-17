"""Application setup and configuration."""

import os
from PySide6 import QtWidgets, QtGui

from prediction_markets_ui.theme.palette import apply_dark_palette
from prediction_markets_ui.theme.styles import get_global_stylesheet


# Environment configuration
UI_THEME = os.getenv("PM_UI_THEME", "dark").lower()
UI_FONT_FAMILY = os.getenv("PM_UI_FONT_FAMILY", "")
UI_FONT_SIZE = int(os.getenv("PM_UI_FONT_SIZE", "12"))
UI_WINDOW_WIDTH = int(os.getenv("PM_UI_WIDTH", "1400"))
UI_WINDOW_HEIGHT = int(os.getenv("PM_UI_HEIGHT", "900"))
UI_MONITOR = os.getenv("PM_UI_MONITOR", "cursor").lower()


def apply_app_style(app: QtWidgets.QApplication) -> None:
    """Apply application styling."""
    # 1. Use Fusion style (cross-platform consistency)
    app.setStyle("Fusion")

    # 2. Font settings
    font = app.font()
    if UI_FONT_FAMILY:
        font.setFamily(UI_FONT_FAMILY)
    if UI_FONT_SIZE > 0:
        font.setPointSize(UI_FONT_SIZE)
    app.setFont(font)

    # 3. Apply dark palette
    if UI_THEME == "dark":
        apply_dark_palette(app)

    # 4. Apply stylesheet
    app.setStyleSheet(get_global_stylesheet(UI_FONT_SIZE, UI_FONT_FAMILY))


def position_window(app: QtWidgets.QApplication, window: QtWidgets.QMainWindow) -> None:
    """Position the window on the appropriate monitor."""
    window.resize(UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT)

    if UI_MONITOR == "primary":
        screen = app.primaryScreen()
    else:
        # Find screen under cursor
        cursor_pos = QtGui.QCursor.pos()
        screen = None
        for s in app.screens():
            if s.geometry().contains(cursor_pos):
                screen = s
                break
        if screen is None:
            screen = app.primaryScreen()

    if screen:
        geo = screen.availableGeometry()
        x = geo.x() + (geo.width() - window.width()) // 2
        y = geo.y() + (geo.height() - window.height()) // 2
        window.move(x, y)
