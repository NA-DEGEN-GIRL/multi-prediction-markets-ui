"""Global stylesheet for the dark theme."""

from prediction_markets_ui.theme.colors import (
    CLR_LONG,
    CLR_SHORT,
    CLR_ACCENT,
    BG_BASE,
    BG_DARKEST,
    BG_HOVER,
    BG_ACTIVE,
    BG_PRESSED,
    BORDER_DEFAULT,
    BORDER_HOVER,
    GROUP_COLORS,
)


def get_global_stylesheet(font_size: int = 12, font_family: str = "") -> str:
    """Generate global stylesheet."""

    # Font fallback chain (Korean + emoji support)
    font_families = []
    if font_family:
        font_families.append(font_family)
    font_families += [
        "Noto Sans CJK KR",      # Korean (Linux)
        "Malgun Gothic",          # Korean (Windows)
        "Segoe UI",               # English (Windows)
        "Noto Color Emoji",       # Emoji (Linux)
        "Segoe UI Emoji",         # Emoji (Windows)
        "Apple Color Emoji",      # Emoji (macOS)
        "Sans"                    # Fallback
    ]
    css_fonts = ", ".join(f'"{f}"' for f in font_families)

    return f"""
    /* Global defaults */
    QWidget {{
        font-size: {font_size}pt;
        font-family: {css_fonts};
    }}

    /* Tooltip */
    QToolTip {{
        background-color: {BG_DARKEST};
        color: white;
        border: 1px solid {BORDER_DEFAULT};
        padding: 4px 8px;
    }}

    /* Group box */
    QGroupBox {{
        font-weight: bold;
        border: 1px solid #777;
        border-radius: 6px;
        margin-top: 6px;
        padding-top: 10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }}

    /* Button */
    QPushButton {{
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 4px;
        padding: 5px;
        background-color: #444;
    }}
    QPushButton:hover {{
        background-color: #555;
    }}
    QPushButton:disabled {{
        background-color: #333;
        color: #777;
        border: 1px solid #333;
    }}

    /* Input field */
    QLineEdit {{
        padding: 4px;
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        background-color: {BG_BASE};
        color: white;
    }}

    /* ComboBox */
    QComboBox {{
        padding: 4px;
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        background-color: {BG_BASE};
        color: white;
    }}
    QComboBox::drop-down {{
        width: 20px;
    }}
    QComboBox QAbstractItemView {{
        border: 1px solid {BORDER_DEFAULT};
        background-color: {BG_BASE};
        color: white;
        selection-background-color: #1976d2;
        outline: none;
        padding: 4px;
    }}

    /* Text editor */
    QPlainTextEdit {{
        font-family: {css_fonts};
        font-size: {font_size}pt;
        background-color: {BG_DARKEST};
        border: 1px solid {BORDER_DEFAULT};
    }}

    /* Scrollbar */
    QScrollBar:vertical {{
        width: 12px;
        background: {BG_BASE};
    }}
    QScrollBar::handle:vertical {{
        background: {BORDER_DEFAULT};
        border-radius: 4px;
    }}

    /* TabWidget */
    QTabWidget::pane {{
        border: 1px solid {BORDER_DEFAULT};
        background-color: {BG_BASE};
    }}
    QTabBar::tab {{
        background-color: {BG_HOVER};
        border: 1px solid {BORDER_DEFAULT};
        padding: 6px 12px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background-color: {BG_BASE};
        border-bottom-color: {BG_BASE};
    }}
    QTabBar::tab:hover {{
        background-color: {BG_ACTIVE};
    }}

    /* Table */
    QTableWidget {{
        background-color: {BG_BASE};
        border: 1px solid {BORDER_DEFAULT};
        gridline-color: #444;
        color: white;
    }}
    QTableWidget::item {{
        padding: 4px;
    }}
    QTableWidget::item:selected {{
        background-color: #1976d2;
    }}
    QHeaderView::section {{
        background-color: {BG_HOVER};
        color: #e0e0e0;
        padding: 4px;
        border: 1px solid {BORDER_DEFAULT};
    }}

    /* Splitter */
    QSplitter::handle {{
        background-color: {BORDER_DEFAULT};
    }}
    QSplitter::handle:horizontal {{
        width: 3px;
    }}
    QSplitter::handle:vertical {{
        height: 3px;
    }}
    """


# Button style templates
BTN_BASE = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: #e0e0e0;
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        padding: 6px 12px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        border-color: {BORDER_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {BG_PRESSED};
    }}
    QPushButton:disabled {{
        background-color: {BG_PRESSED};
        color: {BORDER_DEFAULT};
        border-color: #333;
    }}
"""

# Small button for table cells
BTN_TABLE = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: #e0e0e0;
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        padding: 2px 4px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        border-color: {BORDER_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {BG_PRESSED};
    }}
"""

BTN_LONG = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: {CLR_LONG};
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        padding: 8px 16px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        border-color: {CLR_LONG};
    }}
    QPushButton:pressed {{
        background-color: {BG_PRESSED};
    }}
    QPushButton:checked {{
        border: 2px solid {CLR_LONG};
        background-color: #2e3d2e;
    }}
    QPushButton:disabled {{
        background-color: {BG_PRESSED};
        color: {BORDER_DEFAULT};
        border-color: #333;
    }}
"""

BTN_SHORT = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: {CLR_SHORT};
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        padding: 8px 16px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        border-color: {CLR_SHORT};
    }}
    QPushButton:pressed {{
        background-color: {BG_PRESSED};
    }}
    QPushButton:checked {{
        border: 2px solid {CLR_SHORT};
        background-color: #3d2e2e;
    }}
    QPushButton:disabled {{
        background-color: {BG_PRESSED};
        color: {BORDER_DEFAULT};
        border-color: #333;
    }}
"""

BTN_TOGGLE = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: #e0e0e0;
        border: 1px solid {BORDER_DEFAULT};
        border-radius: 3px;
        padding: 4px 12px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        border-color: {BORDER_HOVER};
    }}
    QPushButton:checked {{
        background-color: #1b3146;
        border: 2px solid #64b5f6;
        color: #64b5f6;
    }}
    QPushButton:disabled {{
        background-color: {BG_PRESSED};
        color: {BORDER_DEFAULT};
        border-color: #333;
    }}
"""
