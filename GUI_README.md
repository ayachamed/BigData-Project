# Complete GUI Application - User Guide

## Overview

**All-in-one GUI** for YouTube Gaza data collection with automatic pipeline execution and integrated results viewer.

## Features

🎨 **Palestinian Flag Colors**: Professional design with green, red, black, white palette  
⚙️ **Automatic Pipeline**: Runs collector → analyzer → visualizer automatically  
📊 **Progress Tracking**: Real-time progress bar with status updates  
🖼️ **Image Gallery**: Browse generated charts with prev/next navigation  
✅ **Complete Validation**: All inputs validated before execution  

## Installation

```bash
# Install dependencies
sudo apt-get install python3-tk
pip3 install tkcalendar Pillow
```

## Quick Start

```bash
# Launch GUI
python3 src/gui.py
```

## Workflow

### 1. Configuration Screen
- **Queries**: Enter exactly 5 English queries, comma-separated
- **Date Range**: Select start and end dates (Oct 2023 - Oct 2025)
- **Video Count**: Choose 1-100 videos per query
- Click **"Start Processing"**

### 2. Progress Screen
- Shows pipeline stages:
  - Collecting videos (10-35%)
  - Analyzing with PySpark (40-65%)
  - Creating visualizations (70-95%)
- Real-time status updates
- Progress bar and percentage

### 3. Results Gallery
- Automatically displays generated charts
- Navigate with **Previous** and **Next** buttons
- Shows image counter and filename
- Charts include:
  - Top channels
  - Top keywords
  - Performance by keyword
  - Top videos
  - Timeline evolution
  - Keyword distribution

## Validation Rules

| Field | Rule |
|-------|------|
| Queries | Exactly 5, comma-separated, English only |
| Start Date | Oct 2023 - Oct 2025 |
| End Date | After start date, before Oct 2025 |
| Videos | 1-100 per query |

## Technical Details

### Architecture
- **Threading**: Pipeline runs in separate thread (non-blocking UI)
- **Progress Callbacks**: Thread-safe progress updates
- **Image Loading**: PIL/Pillow for image display
- **Gallery**: Automatic image resizing and navigation

### Pipeline Stages
1. **Data Collection**: YouTube API calls with split-window strategy
2. **PySpark Analysis**: Distributed processing of videos and comments
3. **Matplotlib Visualization**: Generate 6 PNG charts

### Error Handling
- Input validation before execution
- Pipeline errors displayed in dialogs
- Graceful fallback to configuration screen

## Color Palette

Inspired by the Palestinian flag:

| Color | Code | Usage |
|-------|------|-------|
| Green | `#00732F` | Primary buttons, accents |
| Red | `#CE1126` | Secondary accents (future) |
| Black | `#2C2C2C` | Headers, text |
| White | `#FFFFFF` | Background |

## Screenshots

### Configuration View
- Clean input forms
- Date pickers with calendar widgets
- Validation messages

### Progress View
- Centered progress display
- Styled Palestinian green progress bar
- Real-time status text

### Gallery View
- Large image display area
- Navigation buttons (◀ Previous | Next ▶)
- Image counter with filename

## Tips

💡 **First Run**: May take 5-15 minutes depending on API quota and video count  
💡 **API Key**: Ensure `config.py` has valid YouTube API key  
💡 **Gallery**: Use keyboard arrow keys for navigation (future enhancement)  
💡 **Restart**: Click "Back to Start" to run with new parameters  

## Troubleshooting

**"Collection failed"**: Check API key in `config.py` and quota limits  
**"Analysis failed"**: Ensure PySpark is installed (`pyspark` package)  
**"Visualization failed"**: Check `matplotlib` installation  
**No images in gallery**: Verify `outputs/` directory has PNG files  

## Next Steps

After viewing results in gallery:
- Export charts for presentations
- Review CSVs in `outputs/` directory
- Modify queries and re-run analysis
- Share visualizations

---

**Enjoy exploring your data! 🇵🇸**
