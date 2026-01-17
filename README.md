## 개발중

# Prediction Markets UI

PySide6-based trading interface for prediction markets.

## Features

- Market browser with search and filters
- Real-time orderbook display
- Order entry form
- Position and portfolio tracking
- Split/Merge operations (Polymarket)

## Installation

```bash
# Development (with local core)
uv sync

# Production (from GitHub)
pip install -r requirements.in
```

## Usage

```bash
python -m prediction_markets_ui.main
```

## Configuration

Environment variables:
- `PM_UI_THEME`: Theme selection (dark/light)
- `PM_UI_FONT_SIZE`: Font size in points (default: 12)
- `PM_UI_WIDTH`: Window width (default: 1400)
- `PM_UI_HEIGHT`: Window height (default: 900)
