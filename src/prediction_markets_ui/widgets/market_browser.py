"""Market browser widget - search and list markets."""

from PySide6 import QtWidgets, QtCore, QtGui

from prediction_markets_ui.theme.colors import CLR_MUTED, CLR_ACCENT, CLR_LONG, BORDER_DEFAULT


class MarketBrowser(QtWidgets.QWidget):
    """
    Left panel for searching and browsing markets.

    Contains:
    - Search input
    - Category filter
    - Event/Market tree (Events contain Markets)
    """

    # Signal emitted when a market is selected
    market_selected = QtCore.Signal(str, str)  # (event_id, market_id)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Title
        title = QtWidgets.QLabel("Markets")
        title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT};")
        layout.addWidget(title)

        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search events/markets...")
        layout.addWidget(self.search_input)

        # Category filter
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItems([
            "All Categories",
            "Crypto",
            "Sports",
            "Politics",
            "Entertainment",
            "Science",
        ])
        layout.addWidget(self.category_combo)

        # Event/Market tree
        self.market_tree = QtWidgets.QTreeWidget()
        self.market_tree.setHeaderHidden(True)
        self.market_tree.setStyleSheet(f"""
            QTreeWidget::item {{
                padding: 4px;
                border-bottom: 1px solid #333;
            }}
            QTreeWidget::item:hover {{
                background-color: #3a3a3a;
            }}
            QTreeWidget::item:selected {{
                background-color: #1976d2;
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                image: none;
                border-image: none;
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                image: none;
                border-image: none;
            }}
        """)

        # Add placeholder events and markets
        self._populate_placeholder_data()

        layout.addWidget(self.market_tree, 1)  # stretch=1

        # Hint label
        hint = QtWidgets.QLabel("Double-click market to open")
        hint.setStyleSheet(f"color: {CLR_MUTED}; font-style: italic;")
        hint.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        # Connect signals (double-click to open market)
        self.market_tree.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _populate_placeholder_data(self):
        """Add placeholder events and markets."""
        # Event data: (event_title, [market_titles])
        events_data = [
            ("Bitcoin Price Predictions", [
                "BTC > $100k by Jan 31?",
                "BTC > $150k by March?",
                "BTC > $200k by EOY?",
            ]),
            ("Ethereum Milestones", [
                "ETH > $5k by March?",
                "ETH flips BTC market cap?",
            ]),
            ("Super Bowl 2025", [
                "Kansas City Chiefs win?",
                "Philadelphia Eagles win?",
                "Total points over 50?",
            ]),
            ("US Politics", [
                "Next Fed Rate Decision - Cut?",
                "Government shutdown in Q1?",
            ]),
            ("Tech & Science", [
                "SpaceX Starship Success by Feb?",
                "Will AI achieve AGI before 2030? This is a very long title for testing",
            ]),
        ]

        for event_title, markets in events_data:
            event_item = QtWidgets.QTreeWidgetItem([f"📁 {event_title}"])
            event_item.setToolTip(0, event_title)
            event_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {"type": "event", "id": event_title})
            # Make event items bold
            font = event_item.font(0)
            font.setBold(True)
            event_item.setFont(0, font)

            for market_title in markets:
                market_item = QtWidgets.QTreeWidgetItem([f"  {market_title}"])
                market_item.setToolTip(0, market_title)
                market_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, {
                    "type": "market",
                    "id": market_title,
                    "event_id": event_title
                })
                event_item.addChild(market_item)

            self.market_tree.addTopLevelItem(event_item)

        # Expand first event by default
        if self.market_tree.topLevelItemCount() > 0:
            self.market_tree.topLevelItem(0).setExpanded(True)

    def _on_item_double_clicked(self, item: QtWidgets.QTreeWidgetItem, column: int):
        """Handle item double-click."""
        data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "market":
            # Emit market selection with event context
            self.market_selected.emit(data["event_id"], data["id"])
