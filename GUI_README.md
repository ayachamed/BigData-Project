# GUI Data Collector

## Overview

Modern Python GUI for YouTube Gaza data collection with **Palestinian flag colors** (black, white, green, red).

## Features

✅ **Query Input**: Exactly 5 English queries, comma-separated  
✅ **Date Range**: Oct 2023 - Oct 2025 (default: Oct 6, 2023 → Oct 11, 2025)  
✅ **Video Count**: 1-100 videos per query (default: 100)  
✅ **Real-time Validation**: All inputs validated before execution  
✅ **Professional Design**: Palestinian flag color palette

## Installation

```bash
# Install tkinter (if not already installed)
sudo apt-get install python3-tk

#install tkcalendar
pip3 install tkcalendar
```

## Usage

### Launch GUI
```bash
python3 run_gui.py
```

### Workflow
1. **Enter 5 queries** (comma-separated, English only)
2. **Select date range** (Oct 2023 - Oct 2025)
3. **Choose video count** (max 100 per query)
4. **Click "Start Collection"**
5. Data collection begins automatically

### Example Queries
```
Gaza war, Israel Palestine conflict, Gaza humanitarian crisis, Palestine news, Israel Hamas war
```

## Validation Rules

| Field | Rule |
|-------|------|
| Queries | Exactly 5, comma-separated, English only |
| Start Date | Oct 2023 - Oct 2025 |
| End Date | After start date, before Oct 2025 |
| Videos | 1-100 per query |

## Color Palette

Inspired by the Palestinian flag:

- **Primary (Green)**: `#00732F` - Main buttons
- **Secondary (Red)**: `#CE1126` - Accents
- **Accent (Black)**: `#2C2C2C` - Headers
- **Background (White)**: `#FFFFFF` - Clean canvas

## Screenshots

The GUI features:
- Clean, uncluttered layout
- Clear section headers
- Helpful validation messages
- Professional color scheme
- Date picker with calendar widget
- Real-time input feedback

## Output

After successful collection:
- Data saved to `data/` directory
- Run analyzer: `python3 src/data_analyzer.py`
- Run visualizer: `python3 src/data_visualizer.py`
