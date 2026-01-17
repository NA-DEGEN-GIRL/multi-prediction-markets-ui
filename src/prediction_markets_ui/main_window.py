"""Main window for the trading UI."""

from PySide6 import QtWidgets, QtCore, QtGui

from prediction_markets_ui.theme.colors import CLR_LONG, CLR_SHORT, CLR_MUTED, CLR_ACCENT, BG_HOVER
from prediction_markets_ui.widgets.market_browser import MarketBrowser
from prediction_markets_ui.widgets.trading_panel import TradingPanel
from prediction_markets_ui.widgets.bottom_tabs import BottomTabs
from prediction_markets_ui.widgets.log_panel import LogPanel


class ConnectionIndicator(QtWidgets.QWidget):
    """Connection status indicator widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self.setFixedSize(16, 16)

    def set_connected(self, connected: bool):
        self._connected = connected
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        color = QtGui.QColor(CLR_LONG if self._connected else CLR_SHORT)
        painter.setBrush(color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 12, 12)


class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window.

    Layout:
    - Top toolbar: Exchange selector, connection status, settings, help
    - Left panel: Market browser
    - Right top: Trading panel (orderbook + order entry)
    - Right bottom: Orders/Positions/Portfolio/Operations tabs
    - Status bar: Status messages, latency, WS status
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prediction Markets Trading")
        self.setMinimumSize(1200, 800)
        self._setup_ui()

    def _setup_ui(self):
        # Central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top toolbar
        toolbar = self._create_toolbar()
        main_layout.addWidget(toolbar)

        # Main content (horizontal splitter)
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Left panel: Market browser
        self.market_browser = MarketBrowser()
        self.market_browser.setMinimumWidth(250)
        self.market_browser.setMaximumWidth(400)
        main_splitter.addWidget(self.market_browser)

        # Right panel (vertical splitter)
        right_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)

        # Right top: Trading panel
        self.trading_panel = TradingPanel()
        right_splitter.addWidget(self.trading_panel)

        # Right middle: Bottom tabs
        self.bottom_tabs = BottomTabs()
        self.bottom_tabs.setMinimumHeight(150)
        right_splitter.addWidget(self.bottom_tabs)

        # Right bottom: Log panel
        self.log_panel = LogPanel()
        self.log_panel.setMinimumHeight(100)
        right_splitter.addWidget(self.log_panel)

        # Set initial sizes (50% trading, 30% tabs, 20% logs)
        right_splitter.setSizes([350, 200, 150])

        main_splitter.addWidget(right_splitter)

        # Set initial sizes (left panel: 280px)
        main_splitter.setSizes([280, 920])

        main_layout.addWidget(main_splitter, 1)

        # Status bar
        self._create_statusbar()

        # Connect signals
        self.market_browser.market_selected.connect(self._on_market_selected)

    def _create_toolbar(self) -> QtWidgets.QWidget:
        """Create the top toolbar."""
        toolbar = QtWidgets.QWidget()
        toolbar.setStyleSheet(f"background-color: {BG_HOVER}; border-bottom: 1px solid #555;")
        toolbar.setFixedHeight(44)

        layout = QtWidgets.QHBoxLayout(toolbar)
        layout.setContentsMargins(12, 6, 12, 6)

        # Exchange selector
        exchange_label = QtWidgets.QLabel("Exchange:")
        layout.addWidget(exchange_label)

        self.exchange_combo = QtWidgets.QComboBox()
        self.exchange_combo.addItems(["Polymarket", "Kalshi (soon)"])
        self.exchange_combo.setMinimumWidth(150)
        layout.addWidget(self.exchange_combo)

        # Connection indicator
        layout.addSpacing(16)
        conn_label = QtWidgets.QLabel("Status:")
        layout.addWidget(conn_label)

        self.conn_indicator = ConnectionIndicator()
        self.conn_indicator.set_connected(True)  # Placeholder: connected
        layout.addWidget(self.conn_indicator)

        self.conn_text = QtWidgets.QLabel("Connected")
        self.conn_text.setStyleSheet(f"color: {CLR_LONG};")
        layout.addWidget(self.conn_text)

        layout.addStretch()

        # Settings button
        self.settings_btn = QtWidgets.QPushButton("Settings")
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: #4a4a4a;
            }}
        """)
        layout.addWidget(self.settings_btn)

        # Help button
        self.help_btn = QtWidgets.QPushButton("Help")
        self.help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: #4a4a4a;
            }}
        """)
        layout.addWidget(self.help_btn)

        return toolbar

    def _create_statusbar(self):
        """Create the status bar."""
        statusbar = self.statusBar()

        # Status message
        self.status_label = QtWidgets.QLabel("Ready")
        statusbar.addWidget(self.status_label, 1)

        # REST latency
        self.rest_label = QtWidgets.QLabel("REST: --ms")
        self.rest_label.setStyleSheet(f"color: {CLR_MUTED};")
        statusbar.addPermanentWidget(self.rest_label)

        # WebSocket status
        self.ws_label = QtWidgets.QLabel("WS: Disconnected")
        self.ws_label.setStyleSheet(f"color: {CLR_MUTED};")
        statusbar.addPermanentWidget(self.ws_label)

    def _on_market_selected(self, event_id: str, market_id: str):
        """Handle market selection from browser."""
        self.trading_panel.open_market(market_id)
        self.status_label.setText(f"Loaded: {market_id}")
        self.log_panel.log_event(f"Market opened: {market_id} (Event: {event_id})")
