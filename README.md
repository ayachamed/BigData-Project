# Big Data Project: YouTube Analytics on Gaza Genocide

## Overview

This project implements a comprehensive Big Data analytical pipeline to process and analyze YouTube data related to the ongoing genocide in Gaza. It leverages the YouTube Data API v3 for data collection, Hadoop HDFS for distributed storage, and Python with Pandas for data processing and analysis. The project includes visualization components to present insights on video engagement, channel dominance, temporal trends, and keyword analysis.

## Project Structure

- `data/`: Directory containing raw and processed data files (JSON format)
- `docs/`: Documentation files and images used in the report
- `outputs/`: Generated visualizations and output files (PNG images)
- `Report/`: LaTeX source files for the project report
- `src/`: Source code directory
  - `config.py`: Configuration file containing API keys and settings
  - `data_collector.py`: Python script for collecting data from YouTube API
  - `data_analyzer.py`: Script for data analysis and processing
  - `data_visualizer.py`: Script for generating visualizations

## Prerequisites

- Python 3.7+
- YouTube Data API v3 key (obtain from Google Cloud Console)
- Hadoop HDFS environment (configured in VM as described in the report)
- Required Python packages: `requests`, `pandas`, `matplotlib`

## Installation

1. Clone or download the project repository to your local machine.

2. Install the required Python dependencies:
   ```
   pip install requests pandas matplotlib
   ```

3. Configure the YouTube API key:
   - Open `src/config.py`
   - Replace the placeholder with your actual YouTube Data API v3 key

4. Ensure Hadoop HDFS is properly configured in your VM environment (see report for details).

## Usage

### Data Collection
Run the data collector script to fetch YouTube data:
```
python src/data_collector.py
```
This will collect video metadata and comments based on predefined search queries.

### Data Analysis
Process and analyze the collected data:
```
python src/data_analyzer.py
```
This script performs data cleaning, statistical analysis, and generates insights.

### Visualization
Generate charts and visualizations:
```
python src/data_visualizer.py
```
Output images will be saved in the `outputs/` directory.

### HDFS Integration
Use HDFS commands to store data in the distributed file system:
```
hdfs dfs -mkdir -p /user/project/youtube_data
hdfs dfs -put data/youtube_videos.json /user/project/youtube_data/
hdfs dfs -put data/youtube_comments.json /user/project/youtube_data/
```

## Key Findings

The analysis reveals:
- Dominance of major media outlets in content creation
- Temporal patterns correlating with real-world events
- High engagement with conflict-related content
- Keyword analysis showing focus on kinetic aspects of the conflict

## Report

For detailed methodology, results, and discussion, refer to `Report/Report.tex`. Compile the LaTeX file to generate the PDF report.

## Environment Setup Notes

Due to technical challenges with Docker configuration on local machines, this project was developed using a pre-configured Virtual Machine provided by the lab instructor, following the setups from Labs 1 and 2.

## License

This project is for educational purposes. Please ensure compliance with YouTube API terms of service and data usage policies.