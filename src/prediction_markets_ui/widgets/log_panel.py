"""Log panel widget - event log and debug console."""

import sys
from PySide6 import QtWidgets, QtCore

from prediction_markets_ui.theme.colors import CLR_ACCENT, CLR_MUTED, BG_DARKEST, BORDER_DEFAULT


class LogPanel(QtWidgets.QWidget):
    """
    Log panel with two log boxes.

    - Event Log: Main events (orders, trades, connections, etc.)
    - Debug Console: stdout/print output for debugging
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_stdout = sys.stdout
        self._setup_ui()
        self._redirect_stdout()

    def _setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Event Log (left)
        event_group = QtWidgets.QGroupBox("Event Log")
        event_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                color: {CLR_ACCENT};
                border: 1px solid {BORDER_DEFAULT};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                top: 2px;
                padding: 0 5px;
            }}
        """)
        event_layout = QtWidgets.QVBoxLayout(event_group)
        event_layout.setContentsMargins(4, 4, 4, 4)

        self.event_log = QtWidgets.QPlainTextEdit()
        self.event_log.setReadOnly(True)
        self.event_log.setMaximumBlockCount(1000)  # Limit lines for memory
        self.event_log.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {BG_DARKEST};
                border: none;
            }}
        """)
        event_layout.addWidget(self.event_log)

        layout.addWidget(event_group)

        # Debug Console (right)
        debug_group = QtWidgets.QGroupBox("Debug Console")
        debug_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                color: {CLR_MUTED};
                border: 1px solid {BORDER_DEFAULT};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                top: 2px;
                padding: 0 5px;
            }}
        """)
        debug_layout = QtWidgets.QVBoxLayout(debug_group)
        debug_layout.setContentsMargins(4, 4, 4, 4)

        self.debug_log = QtWidgets.QPlainTextEdit()
        self.debug_log.setReadOnly(True)
        self.debug_log.setMaximumBlockCount(1000)  # Limit lines for memory
        self.debug_log.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {BG_DARKEST};
                border: none;
            }}
        """)
        debug_layout.addWidget(self.debug_log)

        layout.addWidget(debug_group)

    def _redirect_stdout(self):
        """Redirect stdout to debug console."""
        self._stdout_redirector = StdoutRedirector(self.debug_log)
        sys.stdout = self._stdout_redirector

    def restore_stdout(self):
        """Restore original stdout."""
        sys.stdout = self._original_stdout

    def log_event(self, message: str):
        """Add a message to the event log."""
        self.event_log.appendPlainText(message)

    def log_debug(self, message: str):
        """Add a message to the debug console."""
        self.debug_log.appendPlainText(message)

    def clear_event_log(self):
        """Clear the event log."""
        self.event_log.clear()

    def clear_debug_log(self):
        """Clear the debug console."""
        self.debug_log.clear()


class StdoutRedirector(QtCore.QObject):
    """Redirects stdout to a QPlainTextEdit widget."""

    text_written = QtCore.Signal(str)

    def __init__(self, text_edit: QtWidgets.QPlainTextEdit):
        super().__init__()
        self._text_edit = text_edit
        self.text_written.connect(self._append_text)

    def write(self, text: str):
        """Write text to the widget (called by print())."""
        if text.strip():  # Ignore empty lines
            self.text_written.emit(text.rstrip())

    def flush(self):
        """Flush (no-op for compatibility)."""
        pass

    def _append_text(self, text: str):
        """Append text to the widget (runs in main thread)."""
        self._text_edit.appendPlainText(text)
