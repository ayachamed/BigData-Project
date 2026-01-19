# 🇵🇸 Big Data Project: YouTube Analytics on Gaza Genocide

**A comprehensive Big Data analytical pipeline for processing and analyzing YouTube data with user-friendly GUI interface, advanced text normalization, and distributed processing.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Usage Guide](#usage-guide)
8. [GUI Features](#gui-features)
9. [Multimedia Enhancements](#multimedia-enhancements)
10. [Advanced Features](#advanced-features)
11. [Troubleshooting](#troubleshooting)
12. [Key Findings](#key-findings)
13. [Future Enhancements](#future-enhancements)
14. [Technical Details](#technical-details)
15. [License](#license)

---

## Overview

This project implements a **production-grade Big Data analytical pipeline** to process and analyze YouTube data related to the ongoing genocide in Gaza. The system combines:

- **YouTube Data API v3** for intelligent data collection with temporal filtering
- **Apache Spark** concepts for distributed data processing
- **Hadoop HDFS** for fault-tolerant distributed storage
- **Python ecosystem** (Pandas, Matplotlib, Seaborn) for advanced analytics
- **Tkinter GUI** with interactive controls for end-user accessibility
- **Porter Stemmer** for advanced text normalization and keyword analysis

The project democratizes access to complex Big Data pipelines through an intuitive graphical interface while maintaining enterprise-grade scalability and reliability.

---

## 🎯 Features

### Core Data Pipeline
✅ **Intelligent Data Collection**: YouTube API integration with split-window temporal strategy  
✅ **Distributed Storage**: Hadoop HDFS for reliable, fault-tolerant data persistence  
✅ **Advanced Analytics**: PySpark-based processing with statistical analysis  
✅ **Comprehensive Visualizations**: 6+ auto-generated charts with publication-quality graphics  

### GUI & User Interface
✅ **Interactive GUI**: Tkinter-based configuration, progress tracking, and results viewer  
✅ **Arrow Key Navigation**: Browse generated charts using keyboard (← →) or buttons  
✅ **Date Range Selection**: Interactive calendar widgets for temporal filtering  
✅ **Real-Time Progress Tracking**: Live status updates during pipeline execution  
✅ **Responsive UI**: Thread-safe execution prevents UI freezing  

### Text Processing & Analytics
✅ **Keyword Normalization**: Porter Stemmer reduces words to root forms (attack, attacks, attacking → attack)  
✅ **Stop Word Filtering**: Removes common words for meaningful analysis  
✅ **Sentiment-Ready**: Architecture prepared for future NLP integration  

### Multimedia Enhancements
✅ **Background Music**: Palestinian anthem plays during processing  
✅ **Background Images**: Professional visual design with 30% brightness darkening  
✅ **Graceful Degradation**: Optional pygame support, GUI works without it  

### Design & Aesthetics
✅ **Palestinian Flag Colors**: Professional green (#00732F), red (#CE1126), black palette  
✅ **Responsive Layout**: Adapts to different screen sizes  
✅ **Accessibility**: Keyboard shortcuts and mouse support  

---

## 📁 Project Structure

```
BigData-Project-main/
├── 📄 README.md                          # Comprehensive documentation (this file)
├── 📄 INSTALL.md                         # Detailed installation manual
├── 📄 GUI_README.md                      # GUI user guide
├── 📄 MULTIMEDIA_README.md               # Multimedia features documentation
├── 📄 run_gui.py                         # Main entry point for GUI
│
├── 📂 src/                               # Source code directory
│   ├── config.py                         # Configuration & API keys
│   ├── data_collector.py                 # YouTube API data collection module
│   ├── data_analyzer.py                  # PySpark-based analysis engine
│   ├── data_visualizer.py                # Chart generation module
│   ├── gui.py                            # Tkinter GUI application
│   ├── utils.py                          # Utilities (stemming, text processing)
│   └── __pycache__/                      # Python cache (auto-generated)
│
├── 📂 data/                              # Data directory
│   ├── youtube_videos.json               # Collected video metadata
│   ├── youtube_videos.csv                # Video data in CSV format
│   ├── youtube_comments.json             # Comment data in JSON format
│   └── youtube_comments.csv              # Comment data in CSV format
│
├── 📂 outputs/                           # Generated outputs
│   ├── analysis_comments_pandas.csv      # Pandas analysis results
│   ├── analysis_comments_pyspark.csv     # PySpark analysis results
│   ├── analysis_videos_pandas.csv        # Video analysis (Pandas)
│   ├── analysis_videos_pyspark.csv       # Video analysis (PySpark)
│   ├── top_channels.png                  # Chart: Top 10 channels
│   ├── top_words.png                     # Chart: Keyword frequency
│   ├── query_distribution.png            # Chart: Query distribution
│   ├── query_performance.png             # Chart: Engagement metrics
│   ├── timeline.png                      # Chart: Upload timeline
│   └── top_videos.png                    # Chart: Top videos by engagement
│
├── 📂 docs/                              # Documentation & images
│   ├── project_proposal.pdf              # Project specification
│   ├── isamm.png                         # ISAMM logo
│   ├── logo.png                          # Project logo
│   ├── photo_2025-12-31_11-31-41.jpg     # Background image
│   └── [additional diagrams/images]      # Architecture diagrams, etc.
│
├── 📂 Report/                            # LaTeX report files
│   ├── Report.tex                        # Main report document
│   ├── Report.md                         # Markdown version of report
│   └── Report.pdf                        # Compiled PDF report (generated)
│
├── 📂 tests/                             # Unit tests
│   └── test_utils.py                     # Tests for utility functions
│
├── 🎵 Abu_Ubayda_Mawtini.mp3             # Background music file
└── .gitignore                            # Git ignore configuration

```

---

## 🔧 Prerequisites

### Hardware Requirements
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: At least 20GB free
- **Network**: Stable internet connection for API calls

### Software Requirements

| Component | Requirement | Version |
|-----------|-------------|---------|
| Python | Required | 3.7+ |
| Java (for Hadoop) | Optional | JDK 8 or 11 |
| Virtual Machine | Recommended | VirtualBox or VMware |
| Git | Optional | Latest |

### Python Dependencies

```bash
# Core dependencies
requests              # HTTP library for API calls
pandas                # Data manipulation
matplotlib            # Visualization
seaborn               # Statistical graphics
pyspark              # Distributed processing (optional)

# GUI dependencies
tkcalendar           # Calendar widgets for date selection
Pillow               # Image processing
pygame               # Audio playback (optional)

# Text processing
nltk                 # Natural Language Toolkit
```

### YouTube API Key
- Get from [Google Cloud Console](https://console.cloud.google.com/)
- Enable YouTube Data API v3
- Create API key in credentials
- Restrict key for security (recommended)

---

## 📦 Installation

### Step 1: Environment Setup

#### Option A: Using Virtual Machine (Recommended) ⭐

As documented in the project report, Docker configuration presented challenges. We **strongly recommend** using a pre-configured VM provided by your lab instructor.

```bash
# 1. Obtain VM from lab instructor
# 2. Import into VirtualBox/VMware
# 3. Start the VM
# 4. Login with provided credentials

# 5. Verify VM environment
java -version        # Should show JDK 8 or 11
hadoop version       # Should show Hadoop 3.x
python3 --version    # Should show Python 3.7+
```

#### Option B: Local Setup (Advanced)

**Note**: Local setup is complex and not recommended without expert assistance.

```bash
# Install JDK
sudo apt update
sudo apt install openjdk-8-jdk

# Install Hadoop (advanced)
# Download from https://hadoop.apache.org/releases.html
# Extract and configure environment variables
# See INSTALL.md for detailed steps
```

### Step 2: Project Setup

```bash
# 1. Clone/download the project
git clone https://github.com/ayachamed/BigData-Project.git
cd BigData-Project-main

# 2. Create required directories
mkdir -p data outputs docs logs

# 3. Verify structure
ls -la
```

### Step 3: Python Environment Setup

```bash
# 1. Create virtual environment (recommended)
python3 -m venv bigdata_env
source bigdata_env/bin/activate

# 2. Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-tk python3-pil.imagetk

# 3. Install Python packages
pip install --upgrade pip
pip install requests pandas matplotlib seaborn pillow tkcalendar nltk
pip install pyspark  # For distributed processing
pip install pygame   # Optional, for background music
```

### Step 4: YouTube API Configuration

```bash
# 1. Navigate to config file
nano src/config.py

# 2. Replace API_KEY placeholder with your actual key
API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

# 3. Test API connectivity
python3 -c "
from src.config import API_KEY
import requests
url = 'https://www.googleapis.com/youtube/v3/search'
params = {'part': 'snippet', 'q': 'test', 'key': API_KEY, 'maxResults': 1}
response = requests.get(url, params=params)
print('✅ API Key Valid' if response.status_code == 200 else '❌ API Key Invalid')
"
```

### Step 5: Hadoop HDFS Setup (Optional)

```bash
# Start Hadoop services (if using HDFS)
# 1. Format HDFS (first time only)
hdfs namenode -format

# 2. Start HDFS and YARN
start-dfs.sh
start-yarn.sh

# 3. Verify services
jps  # Should see: NameNode, DataNode, ResourceManager, NodeManager

# 4. Create project directory
hdfs dfs -mkdir -p /user/project/youtube_data
hdfs dfs -ls /
```

### Step 6: Verify Installation

```bash
# Test all components
python3 << 'EOF'
import sys
print(f"✅ Python {sys.version}")

try:
    import requests; print("✅ requests")
    import pandas; print("✅ pandas")
    import matplotlib; print("✅ matplotlib")
    import PIL; print("✅ Pillow")
    import tkcalendar; print("✅ tkcalendar")
    import nltk; print("✅ nltk")
    print("\n✅ All core packages installed!")
except ImportError as e:
    print(f"❌ Missing: {e}")
EOF
```

---

## 🚀 Quick Start

### Launch the GUI (Easiest)

```bash
# Make sure virtual environment is activated
source bigdata_env/bin/activate

# Run the GUI application
python3 run_gui.py
```

### Command-Line Pipeline

```bash
# 1. Collect data
python3 src/data_collector.py

# 2. Analyze data
python3 src/data_analyzer.py

# 3. Generate visualizations
python3 src/data_visualizer.py

# 4. Results are in outputs/ directory
ls outputs/
```

---

## 📖 Usage Guide

### 🖥️ GUI Application (Recommended for Users)

#### Configuration Screen
1. **Launch**: `python3 run_gui.py`
2. **Input Parameters**:
   - **Search Queries**: Enter 5 comma-separated queries (e.g., "Gaza war, Israel Palestine conflict, Gaza crisis, Palestine news, Israel Hamas war")
   - **Date Range**: Select start date (Oct 2023) and end date (up to Oct 2025) using calendar widgets
   - **Video Count**: Choose 1-100 videos per query
   - **Comment Count**: Set maximum comments to collect per video
3. **Validation**: All inputs are validated before execution
4. **Start**: Click "**Start Processing**" to launch the pipeline

#### Progress Screen
- Real-time pipeline execution tracking:
  - **10-35%**: Data Collection (YouTube API calls)
  - **40-65%**: Analysis (PySpark processing)
  - **70-95%**: Visualization (Chart generation)
- Live status messages
- Cancel option if needed

#### Results Gallery
- Browse generated charts using **Previous** and **Next** buttons
- Alternative: Use **arrow keys** (← →) for keyboard navigation
- View image counter and filename
- Charts available:
  - Top 10 Channels by video count
  - Top 20 Keywords (normalized)
  - Query Distribution
  - Query Performance (Views/Likes)
  - Video Upload Timeline
  - Top Videos by Engagement

#### Color Palette (Palestinian Theme)
| Element | Color | Hex Code |
|---------|-------|----------|
| Primary (Buttons, Accents) | Green | #00732F |
| Secondary | Red | #CE1126 |
| Headers | Black | #2C2C2C |
| Background | White | #FFFFFF |

---

### 💻 Command-Line Usage (Advanced)

#### Data Collection
```bash
cd src
python3 data_collector.py

# Parameters can be modified in config.py
# Default: 100 videos × 5 queries = 500 videos total
# Time: ~5-15 minutes depending on API quota
```

**Output Files**:
- `data/youtube_videos.json` - Video metadata
- `data/youtube_comments.json` - Comment data
- `data/youtube_videos.csv` - Video data (CSV format)
- `data/youtube_comments.csv` - Comment data (CSV format)

#### Data Analysis
```bash
python3 data_analyzer.py

# Performs:
# - Data cleaning and type conversion
# - Statistical calculations (means, counts, aggregations)
# - Keyword extraction and stemming
# - Temporal analysis
```

**Output**:
- Console statistics
- `outputs/analysis_videos_pyspark.csv` - PySpark results
- `outputs/analysis_comments_pyspark.csv` - Comment analysis

#### Visualization
```bash
python3 data_visualizer.py

# Generates publication-quality charts:
# - top_channels.png (bar chart)
# - top_words.png (word frequency)
# - query_distribution.png (pie chart)
# - query_performance.png (dual bar chart)
# - timeline.png (time series)
# - top_videos.png (engagement metrics)
```

**Output Location**: `outputs/` directory

#### HDFS Integration (Optional)
```bash
# Upload to Hadoop HDFS for distributed processing
hdfs dfs -mkdir -p /user/project/youtube_data

hdfs dfs -put data/youtube_videos.json /user/project/youtube_data/
hdfs dfs -put data/youtube_comments.json /user/project/youtube_data/

# Verify
hdfs dfs -ls /user/project/youtube_data/
hdfs dfs -du -sh /user/project/youtube_data/
```

---

## 🎨 GUI Features

### Interactive Controls

| Feature | Interaction | Purpose |
|---------|-------------|---------|
| **Date Picker** | Calendar widget (click to select) | Temporal filtering |
| **Query Input** | Multi-line text area | Custom search queries |
| **Result Limits** | Spin boxes (↑ ↓ or type) | Control data volume |
| **Progress Bar** | Visual + percentage | Track execution |
| **Gallery Navigation** | ← → buttons or arrow keys | Browse charts |
| **Status Messages** | Real-time text updates | Monitor pipeline |

### Keyboard Shortcuts

```
Arrow Keys:  ← Previous image  |  → Next image
Tab:         Navigate between form fields
Enter:       Submit configuration / Start processing
Ctrl+Q:      Exit application (when in focus)
```

### Input Validation

```
Queries:
  ✅ Exactly 5 queries
  ✅ Comma-separated format
  ✅ English language only
  ✅ At least 3 characters each

Date Range:
  ✅ Start date: Oct 2023 - Oct 2025
  ✅ End date: After start date
  ✅ End date: Before Oct 2025

Video Count:
  ✅ Range: 1-100
  ✅ Integer values only
```

---

## 🎵 Multimedia Enhancements

### Background Music

**File**: `Abu_Ubayda_Mawtini.mp3` (Palestinian anthem)

```python
# Automatically plays when pipeline starts
pygame.mixer.music.load('Abu_Ubayda_Mawtini.mp3')
pygame.mixer.music.set_volume(0.5)  # 50% volume
pygame.mixer.music.play(-1)         # Loop indefinitely
```

**Behavior**:
- ✅ Plays during progress screen
- ✅ Continues during gallery browsing
- ✅ Stops when clicking "Back to Start"
- ✅ Gracefully disabled if pygame unavailable

### Background Images

**File**: `photo_2025-12-31_11-31-41.jpg`

```python
# Applied with brightness enhancement for readability
bg_img = Image.open('photo_2025-12-31_11-31-41.jpg')
enhancer = ImageEnhance.Brightness(bg_img.convert('RGB'))
bg_img = enhancer.enhance(0.3)  # 30% brightness (subtle effect)
```

**Locations**:
- ✅ Progress tracking screen
- ✅ Results gallery screen
- ❌ Configuration screen (clean, distraction-free)

### Backward Compatibility

```python
# PIL version compatibility (9.0.1+)
try:
    img.thumbnail((700, 500), Image.Resampling.LANCZOS)  # New PIL
except AttributeError:
    img.thumbnail((700, 500), Image.LANCZOS)            # Old PIL
```

---

## 🧠 Advanced Features

### Keyword Normalization with Porter Stemmer

**Problem**: Word variations complicate frequency analysis
- "attacking", "attacked", "attacks", "war", "wars", "warring" appear as separate keywords

**Solution**: Porter Stemmer algorithm reduces words to root forms

```python
from nltk.stem import PorterStemmer

def normalize_keyword(word):
    """Reduce word to root form."""
    stemmer = PorterStemmer()
    return stemmer.stem(word.lower())

# Examples
normalize_keyword("attacking")  # → "attack"
normalize_keyword("attacked")   # → "attack"
normalize_keyword("wars")       # → "war"
normalize_keyword("humanitarian") # → "human"
```

**Benefits**:
- ✅ More accurate keyword frequency counts
- ✅ Better trend analysis
- ✅ Cleaner visualizations
- ✅ Improved semantic understanding

### Text Processing Pipeline

```
Raw Title Text
    ↓
[1. Lowercase conversion]
    ↓
[2. Tokenization (split into words)]
    ↓
[3. Remove stopwords (the, and, for, with, to, in, of)]
    ↓
[4. Remove short words (< 3 characters)]
    ↓
[5. Apply Porter Stemmer]
    ↓
[6. Aggregated keyword frequency]
    ↓
Normalized Keywords for Analysis
```

### Stop Words Filtering

Common English stop words automatically removed:

```python
stop_words = {
    'the', 'and', 'for', 'with', 'to', 'in', 'of', 'a', 'is',
    'on', 'at', 'that', 'this', 'are', 'be', 'by', 'or', 'as',
    'was', 'from', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might'
}
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. ImportError: cannot import name 'ImageTk'

**Problem**: `PIL.ImageTk` module not found

**Solution**:
```bash
# Install system dependency
sudo apt-get install python3-pil.imagetk

# Reinstall PIL
pip install --upgrade Pillow
```

#### 2. ImportError: No module named 'pyspark'

**Problem**: PySpark not installed

**Solution**:
```bash
pip install pyspark

# For Jupyter/interactive use
export PYSPARK_PYTHON=python3
```

#### 3. YouTube API Quota Exceeded

**Problem**: "quotaExceeded" error after too many requests

**Solution**:
- Wait 24 hours (quota resets daily)
- Create a new API key in Google Cloud Console
- Reduce video count in configuration (1-10 instead of 100)
- Use split-window temporal strategy (automatically applied)

#### 4. Hadoop Services Won't Start

**Problem**: `start-dfs.sh` fails

**Solutions**:
```bash
# Check Java is installed
java -version

# Format namenode (first time only)
hdfs namenode -format

# Check logs
tail -f $HADOOP_HOME/logs/*.log

# Check if ports are in use
netstat -tlnp | grep java
```

#### 5. GUI Doesn't Display (Headless Server)

**Problem**: No display for Tkinter

**Solution**:
```bash
# Enable X11 forwarding (SSH)
ssh -X user@host

# Or use virtual display
xvfb-run python3 run_gui.py

# Or run headless analysis instead
python3 src/data_analyzer.py
```

#### 6. No Images Appear in Gallery

**Problem**: Gallery shows no charts

**Solutions**:
```bash
# Check outputs directory exists
ls -la outputs/

# Run visualizer manually
python3 src/data_visualizer.py

# Check for error messages
python3 src/data_visualizer.py 2>&1 | head -20
```

#### 7. Permission Denied Errors

**Problem**: Access denied to files/directories

**Solution**:
```bash
# Fix permissions
chmod -R 755 BigData-Project-main/
chmod -R 755 BigData-Project-main/data/
chmod -R 755 BigData-Project-main/outputs/

# Or use sudo (not recommended)
sudo python3 run_gui.py
```

### Debug Mode

Enable verbose output for troubleshooting:

```python
# In src/gui.py or run_gui.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run with output
python3 run_gui.py 2>&1 | tee debug.log
```

---

## 📊 Key Findings

The analysis of YouTube data from October 2023 to October 2025 reveals:

### Media Dominance
- **Major news networks** dominate content creation
- Unlike other platforms, YouTube functions as a **news aggregator**
- Corporate media outlets far exceed independent creators

### Temporal Patterns
- **Sharp peaks** in video uploads correlate with real-world events
- Content creation is **highly reactive**, not proactive
- Trending topics drive engagement cycles

### Engagement Metrics
- **High engagement** with conflict-related content ("War", "Attack")
- **Lower engagement** with humanitarian aspects ("Crisis", "Humanitarian")
- Vocabulary dominated by **kinetic terminology**

### Keyword Analysis
- Top keywords: "war", "israel", "palestin*", "gaza", "attack", "conflict"
- After Porter Stemming normalization:
  - "war" (attacks, wars, warfare, warring → "war")
  - "attack" (attacking, attacked, attacks → "attack")
  - "israel" (israeli, israelis → "israel")

### Channel Performance
- Top channels: BBC News, CNN, Al Jazeera, Reuters, NPR
- Average views per video: 50,000 - 500,000
- Average engagement rate: 2-5%

---

## 🔮 Future Enhancements

### Planned Features

**Phase 2 (Sentiment Analysis)**
```
├─ VADER Sentiment Classification
├─ Comment sentiment aggregation
├─ Temporal sentiment trends
└─ Channel sentiment profiles
```

**Phase 3 (Real-Time Processing)**
```
├─ Apache Kafka streaming
├─ Live dashboard updates
├─ Event-driven architecture
└─ Real-time alert system
```

**Phase 4 (Geospatial Analysis)**
```
├─ Comment origin mapping
├─ Regional engagement patterns
├─ Global heatmaps
└─ Cross-border analysis
```

**Phase 5 (Advanced NLP)**
```
├─ Topic modeling (LDA, NMF)
├─ Named Entity Recognition
├─ Dependency parsing
└─ Aspect-based sentiment analysis
```

**Phase 6 (Internationalization)**
```
├─ Multi-language support (Arabic, Hebrew, etc.)
├─ Multilingual GUI
├─ Cross-language analysis
└─ Regional customization
```

**Phase 7 (Advanced Visualization)**
```
├─ Interactive dashboards (Plotly, Dash)
├─ 3D visualization
├─ Custom chart templates
└─ Export to multiple formats (PDF, PNG, SVG, PPT)
```

---

## 🔧 Technical Details

### Architecture

```
┌─────────────────────────────────────────────────┐
│           GUI Layer (Tkinter)                   │
│  ┌──────────┬──────────┬──────────────────┐     │
│  │ Config   │ Progress │ Gallery (Arrow   │     │
│  │ Screen   │ Screen   │ Navigation)      │     │
│  └──────────┴──────────┴──────────────────┘     │
└──────────────┬────────────────────────────────┘
               │
┌──────────────┴────────────────────────────────┐
│      Data Collection & Processing Layer       │
│  ┌──────────┐  ┌──────────┐  ┌─────────────┐ │
│  │ Collector│→ │ Analyzer │→ │ Visualizer  │ │
│  └──────────┘  └──────────┘  └─────────────┘ │
└──────────────┬────────────────────────────────┘
               │
┌──────────────┴────────────────────────────────┐
│         Data Storage Layer                    │
│  ┌──────────────┐      ┌──────────────────┐  │
│  │ Local JSON   │      │ Hadoop HDFS      │  │
│  │ CSV Files    │      │ (Optional)       │  │
│  └──────────────┘      └──────────────────┘  │
└──────────────────────────────────────────────┘
```

### Data Flow

```
YouTube API
    ↓ [Video metadata + comments]
Data Collector (data_collector.py)
    ↓ [JSON + CSV]
Local Storage (data/)
    ↓ [HDFS put]
Hadoop HDFS (Optional)
    ↓
Data Analyzer (data_analyzer.py)
    ├─→ Statistical Analysis
    ├─→ Keyword Normalization (Porter Stemmer)
    └─→ Aggregation
    ↓ [Statistics + processed data]
Data Visualizer (data_visualizer.py)
    ├─→ Chart 1: Top Channels
    ├─→ Chart 2: Keywords
    ├─→ Chart 3: Query Distribution
    ├─→ Chart 4: Query Performance
    ├─→ Chart 5: Timeline
    └─→ Chart 6: Top Videos
    ↓ [PNG images]
Outputs Directory (outputs/)
    ↓
GUI Gallery (Arrow Key Navigation)
    ↓ [User views results]
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API** | YouTube Data API v3 | Data source |
| **Collection** | Python requests | HTTP API calls |
| **Processing** | PySpark, Pandas | Data transformation |
| **Storage** | HDFS, JSON, CSV | Data persistence |
| **Analysis** | NumPy, SciPy | Statistical analysis |
| **Text** | NLTK, Porter Stemmer | NLP & normalization |
| **Visualization** | Matplotlib, Seaborn | Chart generation |
| **GUI** | Tkinter | User interface |
| **Multimedia** | Pygame | Audio playback |
| **Reports** | LaTeX, pandoc | Documentation |

### Performance Metrics

| Operation | Time | Volume |
|-----------|------|--------|
| Data Collection | 5-15 min | 500 videos × 100 comments |
| Analysis | 2-5 min | 50,000+ data points |
| Visualization | 1-3 min | 6 charts generated |
| Total Pipeline | ~15-30 min | ~100,000 data points |

### Scalability

- **Horizontal**: Add more DataNodes to HDFS cluster
- **Vertical**: Increase executor memory in PySpark
- **Data**: Current setup handles ~1GB datasets; scales to TB with HDFS

---

## 📝 Report & Documentation

For comprehensive methodology, detailed results, and technical discussion:

**Main Report**: `Report/Report.tex`
- Problem statement and objectives
- System architecture and design
- Implementation details (7 phases)
- Results and findings
- Future enhancements
- Technical appendix

**Compile to PDF**:
```bash
cd Report/
pdflatex Report.tex  # Run 3x for cross-references
pdflatex Report.tex
pdflatex Report.tex
evince Report.pdf    # View on Linux
open Report.pdf      # View on macOS
```

---

## 🔐 Security Notes

- **Never commit API keys** to version control
- Use environment variables for sensitive data:
  ```bash
  export YOUTUBE_API_KEY="your_actual_key"
  ```
- Restrict API key in Google Cloud Console:
  - HTTP referrer restrictions
  - IP address whitelisting
  - API quota limits
- Regularly rotate API keys
- Use HTTPS for all communications

---

## 📋 Environment Variables

```bash
# Optional environment configuration
export YOUTUBE_API_KEY="your_key_here"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export PYSPARK_PYTHON=python3
export SPARK_HOME=/opt/spark  # If using Spark
export HADOOP_HOME=/opt/hadoop  # If using Hadoop
```

---

## 💡 Tips & Best Practices

### For First-Time Users
1. ✅ Start with GUI (easiest entry point)
2. ✅ Use default parameters first (smaller dataset)
3. ✅ Check outputs/ directory after completion
4. ✅ Review generated charts before modifying queries

### For Performance
- ⚡ Use smaller result counts for quick testing (10-20 videos)
- ⚡ Run during off-peak API hours to avoid quota limits
- ⚡ Cache data locally; don't re-collect unnecessarily
- ⚡ Use HDFS for repeated large-scale processing

### For Analysis
- 📊 Review all 6 charts before drawing conclusions
- 📊 Check temporal patterns for real-world event correlations
- 📊 Compare query performance to identify narrative focus
- 📊 Use keyword normalization insights for semantic analysis

---

## 📞 Support

- **Documentation**: See README.md (this file), INSTALL.md, GUI_README.md
- **Code Comments**: Check source files in `src/` directory
- **Issues**: Review troubleshooting section above
- **Lab Instructor**: Contact for VM-specific issues

---

## 📜 License

This project is for **educational purposes only**.

**Compliance Requirements**:
- ✅ Respect YouTube API Terms of Service
- ✅ Comply with Google Cloud policies
- ✅ Honor data privacy regulations
- ✅ Follow academic integrity guidelines
- ✅ Cite sources appropriately

---

## 🙏 Acknowledgments

- **Lab Instructor**: For providing pre-configured VM environment
- **Google**: For YouTube Data API
- **Apache**: For Hadoop and Spark frameworks
- **Python Community**: For excellent data science libraries
- **Open Source**: For all supporting libraries and tools

---

**Last Updated**: January 19, 2026  
**Project Status**: ✅ Complete with GUI, Keyword Stemming, Arrow Key Navigation  
**Version**: 2.0.0

---

*Dedicated to documenting the digital narrative of the ongoing genocide in Gaza* 🇵🇸