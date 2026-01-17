"""Color constants for the dark theme."""

# Text colors
CLR_TEXT = "#e0e0e0"           # Default text (light gray)
CLR_MUTED = "#888888"          # Secondary/inactive text (medium gray)
CLR_ACCENT = "#4fc3f7"         # Accent color (sky blue)

# Status colors
CLR_LONG = "#81c784"           # Long/up (green)
CLR_SHORT = "#ef9a9a"          # Short/down (red)
CLR_NEUTRAL = "#e0e0e0"        # Neutral (same as default text)

# Special colors
CLR_COLLATERAL = "rgba(139, 125, 77, 1)"  # Balance/collateral (gold)
CLR_DANGER = "#ef5350"         # Danger/delete (red)
CLR_INFO = "#90caf9"           # Info (blue)
CLR_DETAIL = "#ce93d8"         # Detail/secondary (purple)

# Group colors (6 groups)
GROUP_COLORS = {
    0: {"bg": "#1b5e20", "border": "#81c784", "text": "#81c784"},  # Green
    1: {"bg": "#0d47a1", "border": "#64b5f6", "text": "#64b5f6"},  # Blue
    2: {"bg": "#e65100", "border": "#ffb74d", "text": "#ffb74d"},  # Orange
    3: {"bg": "#6a1b9a", "border": "#ce93d8", "text": "#ce93d8"},  # Purple
    4: {"bg": "#00838f", "border": "#4dd0e1", "text": "#4dd0e1"},  # Cyan
    5: {"bg": "#c62828", "border": "#ef9a9a", "text": "#ef9a9a"},  # Red
}

# Background color layers (darkest to lightest)
BG_DARKEST = "#1e1e1e"     # Darkest (editor, input field interior)
BG_DARKER = "#232323"      # Slightly lighter (input field background)
BG_BASE = "#2b2b2b"        # Base background (input elements)
BG_WINDOW = "#353535"      # Window background (RGB: 53, 53, 53)
BG_HOVER = "#3a3a3a"       # Button default / pre-hover
BG_ACTIVE = "#4a4a4a"      # Hover state
BG_PRESSED = "#2a2a2a"     # Pressed state
BG_DISABLED = "#2a2a2a"    # Disabled state

# Border colors
BORDER_DEFAULT = "#555555"
BORDER_HOVER = "#666666"
BORDER_DISABLED = "#333333"
