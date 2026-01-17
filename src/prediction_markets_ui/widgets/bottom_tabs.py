"""Bottom tabs widget - Orders, Positions, Portfolio, Operations."""

from PySide6 import QtWidgets, QtCore, QtGui

from prediction_markets_ui.theme.colors import (
    CLR_LONG,
    CLR_SHORT,
    CLR_MUTED,
    CLR_ACCENT,
    CLR_COLLATERAL,
    BG_HOVER,
    BORDER_DEFAULT,
)
from prediction_markets_ui.theme.styles import BTN_TABLE


class OrdersTab(QtWidgets.QWidget):
    """Open orders tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Orders table
        self.orders_table = QtWidgets.QTableWidget(0, 9)
        self.orders_table.setHorizontalHeaderLabels([
            "Market", "Side", "Outcome", "Type", "Price",
            "Size", "Filled", "Status", "Actions"
        ])
        self.orders_table.verticalHeader().setVisible(False)

        # Set column resize modes
        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Market
        for col in range(1, 8):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeMode.Fixed)  # Actions
        self.orders_table.setColumnWidth(8, 80)  # Fixed width for action buttons

        # Add placeholder orders
        orders_data = [
            ("BTC > $100k?", "BUY", "YES", "LIMIT", "0.62", "100", "0", "OPEN"),
            ("ETH > $5k?", "SELL", "NO", "LIMIT", "0.45", "50", "25", "PARTIAL"),
        ]
        self.orders_table.setRowCount(len(orders_data))

        for row, data in enumerate(orders_data):
            for col, value in enumerate(data):
                item = QtWidgets.QTableWidgetItem(value)
                # Color code side
                if col == 1:  # Side
                    item.setForeground(QtGui.QColor(CLR_LONG if value == "BUY" else CLR_SHORT))
                self.orders_table.setItem(row, col, item)

            # Add cancel button
            cancel_btn = QtWidgets.QPushButton("Cancel")
            cancel_btn.setStyleSheet(BTN_TABLE)
            self.orders_table.setCellWidget(row, 8, cancel_btn)

        layout.addWidget(self.orders_table)


class PositionsTab(QtWidgets.QWidget):
    """Positions tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Positions table
        self.positions_table = QtWidgets.QTableWidget(0, 7)
        self.positions_table.setHorizontalHeaderLabels([
            "Market", "Outcome", "Size", "Avg Price", "Current", "PnL", "Actions"
        ])
        self.positions_table.verticalHeader().setVisible(False)

        # Set column resize modes
        header = self.positions_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Market
        for col in range(1, 6):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)  # Actions
        self.positions_table.setColumnWidth(6, 80)  # Fixed width for action buttons

        # Add placeholder positions
        positions_data = [
            ("BTC > $100k?", "YES", "150", "0.58", "0.63", "+$7.50"),
            ("Super Bowl Winner", "NO", "80", "0.70", "0.65", "-$4.00"),
        ]
        self.positions_table.setRowCount(len(positions_data))

        for row, data in enumerate(positions_data):
            for col, value in enumerate(data):
                item = QtWidgets.QTableWidgetItem(value)
                # Color code PnL
                if col == 5:  # PnL
                    color = CLR_LONG if value.startswith("+") else CLR_SHORT
                    item.setForeground(QtGui.QColor(color))
                self.positions_table.setItem(row, col, item)

            # Add close button
            close_btn = QtWidgets.QPushButton("Close")
            close_btn.setStyleSheet(BTN_TABLE)
            self.positions_table.setCellWidget(row, 6, close_btn)

        layout.addWidget(self.positions_table)


class PortfolioTab(QtWidgets.QWidget):
    """Portfolio summary tab - simple and clear."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Row 1: Total Value / Cash / Positions Value
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(32)

        row1.addWidget(QtWidgets.QLabel("Total Value:"))
        self.total_value = QtWidgets.QLabel("$1,234.56")
        self.total_value.setStyleSheet("font-weight: bold;")
        row1.addWidget(self.total_value)

        row1.addWidget(QtWidgets.QLabel("Cash (USDC):"))
        self.cash_balance = QtWidgets.QLabel("$500.00")
        row1.addWidget(self.cash_balance)

        row1.addWidget(QtWidgets.QLabel("Positions Value:"))
        self.positions_value = QtWidgets.QLabel("$734.56")
        row1.addWidget(self.positions_value)

        row1.addStretch()
        layout.addLayout(row1)

        # Row 2: Unrealized PnL / Open Positions / Open Orders
        row2 = QtWidgets.QHBoxLayout()
        row2.setSpacing(32)

        row2.addWidget(QtWidgets.QLabel("Unrealized PnL:"))
        self.unrealized_pnl = QtWidgets.QLabel("+$45.20")
        self.unrealized_pnl.setStyleSheet(f"color: {CLR_LONG};")
        row2.addWidget(self.unrealized_pnl)

        row2.addWidget(QtWidgets.QLabel("Open Positions:"))
        self.positions_count = QtWidgets.QLabel("2")
        row2.addWidget(self.positions_count)

        row2.addWidget(QtWidgets.QLabel("Open Orders:"))
        self.orders_count = QtWidgets.QLabel("3")
        row2.addWidget(self.orders_count)

        row2.addStretch()
        layout.addLayout(row2)

        layout.addStretch()


class BottomTabs(QtWidgets.QTabWidget):
    """
    Bottom panel with tabs for Portfolio, Orders, Positions.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        # Portfolio tab (default)
        self.portfolio_tab = PortfolioTab()
        self.addTab(self.portfolio_tab, "Portfolio")

        # Orders tab
        self.orders_tab = OrdersTab()
        self.addTab(self.orders_tab, "Orders")

        # Positions tab
        self.positions_tab = PositionsTab()
        self.addTab(self.positions_tab, "Positions")
