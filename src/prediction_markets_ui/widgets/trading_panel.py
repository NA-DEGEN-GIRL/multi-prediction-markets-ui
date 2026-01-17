"""Trading panel widget - orderbook and order entry."""

from PySide6 import QtWidgets, QtCore, QtGui

from prediction_markets_ui.theme.colors import (
    CLR_LONG,
    CLR_SHORT,
    CLR_MUTED,
    CLR_ACCENT,
    BG_HOVER,
    BG_BASE,
    BORDER_DEFAULT,
)
from prediction_markets_ui.theme.styles import BTN_LONG, BTN_SHORT, BTN_TOGGLE


class OrderbookWidget(QtWidgets.QWidget):
    """Orderbook display widget - unified view with asks and bids."""

    # Signal emitted when a price row is clicked (price: float)
    price_clicked = QtCore.Signal(float)
    # Signal emitted when outcome changes
    outcome_changed = QtCore.Signal(str)  # "YES" or "NO"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_outcome = "YES"
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Market title
        self.market_title = QtWidgets.QLabel("Select a market")
        self.market_title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT};")
        self.market_title.setWordWrap(True)
        layout.addWidget(self.market_title)

        # Outcome selector - prominent display
        outcome_frame = QtWidgets.QFrame()
        outcome_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_HOVER};
                border: 1px solid {BORDER_DEFAULT};
                border-radius: 4px;
            }}
        """)
        outcome_layout = QtWidgets.QHBoxLayout(outcome_frame)
        outcome_layout.setContentsMargins(8, 6, 8, 6)

        outcome_label = QtWidgets.QLabel("Outcome:")
        outcome_layout.addWidget(outcome_label)

        self.yes_btn = QtWidgets.QPushButton("YES")
        self.yes_btn.setCheckable(True)
        self.yes_btn.setChecked(True)
        self.yes_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {CLR_LONG};
                border: 2px solid {CLR_LONG};
                border-radius: 4px;
                padding: 4px 16px;
                font-weight: bold;
            }}
            QPushButton:checked {{
                background-color: {CLR_LONG};
                color: black;
            }}
        """)
        outcome_layout.addWidget(self.yes_btn)

        self.no_btn = QtWidgets.QPushButton("NO")
        self.no_btn.setCheckable(True)
        self.no_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {CLR_SHORT};
                border: 2px solid {CLR_SHORT};
                border-radius: 4px;
                padding: 4px 16px;
                font-weight: bold;
            }}
            QPushButton:checked {{
                background-color: {CLR_SHORT};
                color: white;
            }}
        """)
        outcome_layout.addWidget(self.no_btn)

        # Make YES/NO mutually exclusive
        self.outcome_group = QtWidgets.QButtonGroup(self)
        self.outcome_group.addButton(self.yes_btn)
        self.outcome_group.addButton(self.no_btn)
        self.outcome_group.buttonClicked.connect(self._on_outcome_changed)

        outcome_layout.addStretch()

        # Spread display
        spread_label = QtWidgets.QLabel("Spread:")
        spread_label.setStyleSheet(f"color: {CLR_MUTED};")
        outcome_layout.addWidget(spread_label)

        self.spread_value = QtWidgets.QLabel("$0.02 (3.1%)")
        self.spread_value.setStyleSheet(f"color: {CLR_ACCENT}; font-weight: bold;")
        outcome_layout.addWidget(self.spread_value)

        layout.addWidget(outcome_frame)

        # Unified orderbook table
        self.orderbook_table = QtWidgets.QTableWidget()
        self.orderbook_table.setColumnCount(3)
        self.orderbook_table.setHorizontalHeaderLabels(["Price", "Size", "Total ($)"])
        self.orderbook_table.verticalHeader().setVisible(False)
        self.orderbook_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.orderbook_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Column resize modes
        header = self.orderbook_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Populate with placeholder data
        self._populate_orderbook()

        # Connect click signal
        self.orderbook_table.cellClicked.connect(self._on_cell_clicked)

        layout.addWidget(self.orderbook_table, 1)

        # Position display for this market
        self._setup_position_display(layout)

    def _setup_position_display(self, layout: QtWidgets.QVBoxLayout):
        """Setup the position and orders display section below orderbook."""
        # Container frame
        info_frame = QtWidgets.QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_HOVER};
                border: 1px solid {BORDER_DEFAULT};
                border-radius: 4px;
            }}
        """)
        info_layout = QtWidgets.QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 8, 8, 8)
        info_layout.setSpacing(6)

        # === Position Section ===
        pos_title = QtWidgets.QLabel("My Position")
        pos_title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT};")
        info_layout.addWidget(pos_title)

        # Position info grid
        pos_grid = QtWidgets.QGridLayout()
        pos_grid.setSpacing(8)

        # YES position
        yes_label = QtWidgets.QLabel("YES:")
        yes_label.setStyleSheet(f"color: {CLR_LONG}; font-weight: bold;")
        pos_grid.addWidget(yes_label, 0, 0)

        self.yes_size_label = QtWidgets.QLabel("150 shares")
        pos_grid.addWidget(self.yes_size_label, 0, 1)

        self.yes_avg_label = QtWidgets.QLabel("@ $0.58")
        self.yes_avg_label.setStyleSheet(f"color: {CLR_MUTED};")
        pos_grid.addWidget(self.yes_avg_label, 0, 2)

        self.yes_pnl_label = QtWidgets.QLabel("+$7.50")
        self.yes_pnl_label.setStyleSheet(f"color: {CLR_LONG};")
        pos_grid.addWidget(self.yes_pnl_label, 0, 3)

        # NO position
        no_label = QtWidgets.QLabel("NO:")
        no_label.setStyleSheet(f"color: {CLR_SHORT}; font-weight: bold;")
        pos_grid.addWidget(no_label, 1, 0)

        self.no_size_label = QtWidgets.QLabel("0 shares")
        pos_grid.addWidget(self.no_size_label, 1, 1)

        self.no_avg_label = QtWidgets.QLabel("@ --")
        self.no_avg_label.setStyleSheet(f"color: {CLR_MUTED};")
        pos_grid.addWidget(self.no_avg_label, 1, 2)

        self.no_pnl_label = QtWidgets.QLabel("$0.00")
        self.no_pnl_label.setStyleSheet(f"color: {CLR_MUTED};")
        pos_grid.addWidget(self.no_pnl_label, 1, 3)

        info_layout.addLayout(pos_grid)

        # Separator
        sep1 = QtWidgets.QFrame()
        sep1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sep1.setStyleSheet(f"background-color: {BORDER_DEFAULT};")
        info_layout.addWidget(sep1)

        # === Open Orders Section ===
        orders_title = QtWidgets.QLabel("Open Orders")
        orders_title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT};")
        info_layout.addWidget(orders_title)

        # Orders table (compact)
        self.market_orders_table = QtWidgets.QTableWidget(0, 5)
        self.market_orders_table.setHorizontalHeaderLabels(["Side", "Outcome", "Price", "Size", ""])
        self.market_orders_table.verticalHeader().setVisible(False)
        self.market_orders_table.setMaximumHeight(80)
        self.market_orders_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Column resize
        header = self.market_orders_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.market_orders_table.setColumnWidth(4, 50)

        # Placeholder orders
        orders_data = [
            ("BUY", "YES", "0.62", "100"),
        ]
        self.market_orders_table.setRowCount(len(orders_data))
        for row, (side, outcome, price, size) in enumerate(orders_data):
            side_item = QtWidgets.QTableWidgetItem(side)
            side_item.setForeground(QtGui.QColor(CLR_LONG if side == "BUY" else CLR_SHORT))
            self.market_orders_table.setItem(row, 0, side_item)

            outcome_item = QtWidgets.QTableWidgetItem(outcome)
            outcome_item.setForeground(QtGui.QColor(CLR_LONG if outcome == "YES" else CLR_SHORT))
            self.market_orders_table.setItem(row, 1, outcome_item)

            self.market_orders_table.setItem(row, 2, QtWidgets.QTableWidgetItem(price))
            self.market_orders_table.setItem(row, 3, QtWidgets.QTableWidgetItem(size))

            # Cancel button
            cancel_btn = QtWidgets.QPushButton("X")
            cancel_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {CLR_SHORT};
                    border: none;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    color: white;
                }}
            """)
            cancel_btn.setFixedWidth(30)
            self.market_orders_table.setCellWidget(row, 4, cancel_btn)

        info_layout.addWidget(self.market_orders_table)

        layout.addWidget(info_frame)

    def _on_outcome_changed(self, button: QtWidgets.QPushButton):
        """Handle outcome button click."""
        self._current_outcome = "YES" if button == self.yes_btn else "NO"
        self.outcome_changed.emit(self._current_outcome)
        # TODO: Reload orderbook for new outcome

    def set_market_title(self, title: str):
        """Set the market title."""
        self.market_title.setText(title)
        self.market_title.setToolTip(title)

    def set_outcome(self, outcome: str):
        """Set outcome from order entry selection."""
        # Block signals to prevent infinite loop
        self.outcome_group.blockSignals(True)
        if outcome == "YES":
            self.yes_btn.setChecked(True)
        else:
            self.no_btn.setChecked(True)
        self._current_outcome = outcome
        self.outcome_group.blockSignals(False)
        # TODO: Reload orderbook for new outcome

    def _on_cell_clicked(self, row: int, column: int):
        """Handle cell click - emit price if valid row."""
        item = self.orderbook_table.item(row, 0)  # Price column
        if item and item.text():
            try:
                price = float(item.text())
                self.price_clicked.emit(price)
            except ValueError:
                pass  # Separator row or invalid

    def _populate_orderbook(self):
        """Populate orderbook with placeholder data."""
        # Asks data (sells) - sorted by price descending (highest at top)
        asks_data = [
            (0.68, 120),
            (0.67, 85),
            (0.66, 200),
            (0.65, 150),
            (0.64, 300),
        ]

        # Bids data (buys) - sorted by price descending (highest at top)
        bids_data = [
            (0.62, 250),
            (0.61, 180),
            (0.60, 320),
            (0.59, 100),
            (0.58, 450),
        ]

        # Total rows: asks + separator + bids
        total_rows = len(asks_data) + 1 + len(bids_data)
        self.orderbook_table.setRowCount(total_rows)

        row = 0

        # Add asks (cumulative sum from bottom to top, displayed top to bottom)
        # Calculate cumulative totals from best ask (lowest) to worst (highest)
        asks_reversed = list(reversed(asks_data))  # lowest price first
        cumulative = 0
        ask_rows = []
        for price, size in asks_reversed:
            cumulative += price * size
            ask_rows.append((price, size, cumulative))
        # Display in reverse (highest price at top, lowest near spread)
        for price, size, total in reversed(ask_rows):
            self._set_row(row, price, size, total, CLR_SHORT)
            row += 1

        # Separator row
        separator_row = row
        for col in range(3):
            item = QtWidgets.QTableWidgetItem()
            item.setBackground(QtGui.QColor(BORDER_DEFAULT))
            item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            self.orderbook_table.setItem(separator_row, col, item)
        self.orderbook_table.setRowHeight(separator_row, 3)
        row += 1

        # Add bids (cumulative sum from top to bottom)
        cumulative = 0
        for price, size in bids_data:
            cumulative += price * size
            self._set_row(row, price, size, cumulative, CLR_LONG)
            row += 1

    def _set_row(self, row: int, price: float, size: int, total: float, color: str):
        """Set a row in the orderbook table."""
        price_item = QtWidgets.QTableWidgetItem(f"{price:.2f}")
        price_item.setForeground(QtGui.QColor(color))
        price_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        size_item = QtWidgets.QTableWidgetItem(f"{size:,}")
        size_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        total_item = QtWidgets.QTableWidgetItem(f"${total:,.2f}")
        total_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.orderbook_table.setItem(row, 0, price_item)
        self.orderbook_table.setItem(row, 1, size_item)
        self.orderbook_table.setItem(row, 2, total_item)


class OrderEntryWidget(QtWidgets.QWidget):
    """Order entry form widget with operations."""

    # Signal emitted when outcome changes
    outcome_changed = QtCore.Signal(str)  # "YES" or "NO"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Title
        title = QtWidgets.QLabel("Place Order")
        title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT};")
        layout.addWidget(title)

        # Side selection (BUY / SELL)
        side_layout = QtWidgets.QHBoxLayout()
        side_label = QtWidgets.QLabel("Side:")
        side_layout.addWidget(side_label)

        self.buy_btn = QtWidgets.QPushButton("BUY")
        self.buy_btn.setCheckable(True)
        self.buy_btn.setChecked(True)
        self.buy_btn.setStyleSheet(BTN_LONG)
        side_layout.addWidget(self.buy_btn)

        self.sell_btn = QtWidgets.QPushButton("SELL")
        self.sell_btn.setCheckable(True)
        self.sell_btn.setStyleSheet(BTN_SHORT)
        side_layout.addWidget(self.sell_btn)

        # Make BUY/SELL mutually exclusive
        self.side_group = QtWidgets.QButtonGroup(self)
        self.side_group.addButton(self.buy_btn)
        self.side_group.addButton(self.sell_btn)

        layout.addLayout(side_layout)

        # Outcome selection (YES / NO)
        outcome_layout = QtWidgets.QHBoxLayout()
        outcome_label = QtWidgets.QLabel("Outcome:")
        outcome_layout.addWidget(outcome_label)

        self.yes_btn = QtWidgets.QPushButton("YES")
        self.yes_btn.setCheckable(True)
        self.yes_btn.setChecked(True)
        self.yes_btn.setStyleSheet(BTN_TOGGLE)
        outcome_layout.addWidget(self.yes_btn)

        self.no_btn = QtWidgets.QPushButton("NO")
        self.no_btn.setCheckable(True)
        self.no_btn.setStyleSheet(BTN_TOGGLE)
        outcome_layout.addWidget(self.no_btn)

        # Make YES/NO mutually exclusive
        self.outcome_group = QtWidgets.QButtonGroup(self)
        self.outcome_group.addButton(self.yes_btn)
        self.outcome_group.addButton(self.no_btn)

        layout.addLayout(outcome_layout)

        # Order type (LIMIT / MARKET)
        type_layout = QtWidgets.QHBoxLayout()
        type_label = QtWidgets.QLabel("Type:")
        type_layout.addWidget(type_label)

        self.limit_btn = QtWidgets.QPushButton("LIMIT")
        self.limit_btn.setCheckable(True)
        self.limit_btn.setChecked(True)
        self.limit_btn.setStyleSheet(BTN_TOGGLE)
        type_layout.addWidget(self.limit_btn)

        self.market_btn = QtWidgets.QPushButton("MARKET")
        self.market_btn.setCheckable(True)
        self.market_btn.setStyleSheet(BTN_TOGGLE)
        type_layout.addWidget(self.market_btn)

        # Make LIMIT/MARKET mutually exclusive
        self.type_group = QtWidgets.QButtonGroup(self)
        self.type_group.addButton(self.limit_btn)
        self.type_group.addButton(self.market_btn)

        layout.addLayout(type_layout)

        # Size input
        size_layout = QtWidgets.QHBoxLayout()
        size_label = QtWidgets.QLabel("Size:")
        size_layout.addWidget(size_label)

        self.size_input = QtWidgets.QLineEdit()
        self.size_input.setPlaceholderText("0.00")
        size_layout.addWidget(self.size_input)

        self.size_type_combo = QtWidgets.QComboBox()
        self.size_type_combo.addItems(["Shares", "USD"])
        size_layout.addWidget(self.size_type_combo)

        layout.addLayout(size_layout)

        # Price input
        price_layout = QtWidgets.QHBoxLayout()
        self.price_label = QtWidgets.QLabel("Price:")
        price_layout.addWidget(self.price_label)

        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("0.00")
        price_layout.addWidget(self.price_input)

        layout.addLayout(price_layout)

        # Estimated cost
        estimate_frame = QtWidgets.QFrame()
        estimate_frame.setStyleSheet(f"background-color: {BG_HOVER}; border-radius: 4px;")
        estimate_layout = QtWidgets.QVBoxLayout(estimate_frame)
        estimate_layout.setContentsMargins(8, 8, 8, 8)

        self.est_cost = QtWidgets.QLabel("Est. Cost: $0.00")
        estimate_layout.addWidget(self.est_cost)

        self.est_fee = QtWidgets.QLabel("Est. Fee: $0.00")
        self.est_fee.setStyleSheet(f"color: {CLR_MUTED};")
        estimate_layout.addWidget(self.est_fee)

        layout.addWidget(estimate_frame)

        # Place order button
        self.place_btn = QtWidgets.QPushButton("Place Order")
        self.place_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CLR_LONG};
                color: black;
                font-weight: bold;
                padding: 12px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #9ccc9c;
            }}
            QPushButton:disabled {{
                background-color: #555;
                color: #888;
            }}
        """)
        layout.addWidget(self.place_btn)

        # Separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {BORDER_DEFAULT};")
        layout.addWidget(separator)

        # Operations section (Split/Merge/Redeem)
        ops_title = QtWidgets.QLabel("Operations")
        ops_title.setStyleSheet(f"font-weight: bold; color: {CLR_ACCENT}; margin-top: 8px;")
        layout.addWidget(ops_title)

        # Split section
        split_layout = QtWidgets.QHBoxLayout()
        self.split_amount = QtWidgets.QLineEdit()
        self.split_amount.setPlaceholderText("Amount (USDC)")
        split_layout.addWidget(self.split_amount)

        self.split_btn = QtWidgets.QPushButton("Split")
        self.split_btn.setStyleSheet(BTN_TOGGLE)
        self.split_btn.setToolTip("USDC → YES + NO")
        split_layout.addWidget(self.split_btn)
        layout.addLayout(split_layout)

        # Merge section
        merge_layout = QtWidgets.QHBoxLayout()
        self.merge_amount = QtWidgets.QLineEdit()
        self.merge_amount.setPlaceholderText("Amount (pairs)")
        merge_layout.addWidget(self.merge_amount)

        self.merge_btn = QtWidgets.QPushButton("Merge")
        self.merge_btn.setStyleSheet(BTN_TOGGLE)
        self.merge_btn.setToolTip("YES + NO → USDC")
        merge_layout.addWidget(self.merge_btn)
        layout.addLayout(merge_layout)

        # Redeem section
        redeem_layout = QtWidgets.QHBoxLayout()
        self.redeem_amount = QtWidgets.QLineEdit()
        self.redeem_amount.setPlaceholderText("Amount")
        redeem_layout.addWidget(self.redeem_amount)

        self.redeem_btn = QtWidgets.QPushButton("Redeem")
        self.redeem_btn.setStyleSheet(BTN_TOGGLE)
        self.redeem_btn.setToolTip("Redeem winning tokens")
        redeem_layout.addWidget(self.redeem_btn)
        layout.addLayout(redeem_layout)

        layout.addStretch()

    def _connect_signals(self):
        """Connect internal signals."""
        self.limit_btn.toggled.connect(self._on_order_type_changed)
        self.market_btn.toggled.connect(self._on_order_type_changed)
        self.outcome_group.buttonClicked.connect(self._on_outcome_clicked)

    def _on_order_type_changed(self):
        """Enable/disable price input based on order type."""
        is_limit = self.limit_btn.isChecked()
        self.price_input.setEnabled(is_limit)
        if not is_limit:
            self.price_input.clear()
            self.price_input.setPlaceholderText("N/A (Market)")
        else:
            self.price_input.setPlaceholderText("0.00")

    def _on_outcome_clicked(self, button: QtWidgets.QPushButton):
        """Handle outcome button click and emit signal."""
        outcome = "YES" if button == self.yes_btn else "NO"
        self.outcome_changed.emit(outcome)

    def set_price(self, price: float):
        """Set price from orderbook click and switch to LIMIT."""
        self.limit_btn.setChecked(True)
        self.price_input.setText(f"{price:.2f}")

    def set_outcome(self, outcome: str, emit_signal: bool = True):
        """Set outcome from orderbook selection."""
        # Block signals to prevent infinite loop
        self.outcome_group.blockSignals(True)
        if outcome == "YES":
            self.yes_btn.setChecked(True)
        else:
            self.no_btn.setChecked(True)
        self.outcome_group.blockSignals(False)


class TradingPanel(QtWidgets.QWidget):
    """
    Right top panel for trading.

    Contains:
    - Market tabs (for multi-market support)
    - Orderbook
    - Order entry form
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Market tabs
        self.market_tabs = QtWidgets.QTabWidget()
        self.market_tabs.setTabsClosable(True)
        self.market_tabs.setMovable(True)
        self.market_tabs.tabCloseRequested.connect(self._on_tab_close)

        # Limit tab size
        self.market_tabs.tabBar().setElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.market_tabs.tabBar().setExpanding(False)
        self.market_tabs.setStyleSheet("QTabBar::tab { max-width: 150px; }")

        # Add placeholder tab
        self._add_market_tab("BTC > $100k?")

        layout.addWidget(self.market_tabs)

    def _on_tab_close(self, index: int):
        """Handle tab close request."""
        self.market_tabs.removeTab(index)

    def _add_market_tab(self, market_name: str):
        """Add a new market tab."""
        tab_widget = QtWidgets.QWidget()
        tab_layout = QtWidgets.QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        # Orderbook (left)
        orderbook = OrderbookWidget()
        orderbook.set_market_title(market_name)
        tab_layout.addWidget(orderbook, 1)

        # Order entry (right)
        order_entry = OrderEntryWidget()
        order_entry.setMaximumWidth(300)
        tab_layout.addWidget(order_entry)

        # Connect orderbook signals to order entry (bidirectional)
        orderbook.price_clicked.connect(order_entry.set_price)
        orderbook.outcome_changed.connect(order_entry.set_outcome)
        order_entry.outcome_changed.connect(orderbook.set_outcome)

        # Add tab with tooltip for long titles
        tab_index = self.market_tabs.addTab(tab_widget, market_name)
        self.market_tabs.setTabToolTip(tab_index, market_name)

    def open_market(self, market_name: str):
        """Open a market in a new tab or switch to existing."""
        # Check if already open
        for i in range(self.market_tabs.count()):
            if self.market_tabs.tabText(i) == market_name:
                self.market_tabs.setCurrentIndex(i)
                return

        # Add new tab
        self._add_market_tab(market_name)
        self.market_tabs.setCurrentIndex(self.market_tabs.count() - 1)
