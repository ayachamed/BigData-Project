# Installation Manual for Big Data YouTube Analytics Project

## Overview

This manual provides a comprehensive, step-by-step guide to set up and run the Big Data YouTube Analytics project. The project analyzes YouTube content related to the Gaza genocide using Python, YouTube Data API v3, and Hadoop HDFS for distributed storage.

## Prerequisites

Before starting the installation, ensure you have the following:

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- At least 20GB free disk space
- Stable internet connection for API calls and data download

### Software Requirements
- **Operating System**: Windows 10/11 (for host), Ubuntu/CentOS (for VM)
- **Python**: Version 3.7 or higher
- **Java Development Kit (JDK)**: Version 8 or 11 (for Hadoop)
- **Virtual Machine Software**: VirtualBox or VMware (if using VM approach)
- **Git**: For cloning repositories (optional)

## Installation Steps

### Step 1: Environment Setup

#### Option A: Using Virtual Machine (Recommended)
As documented in the project report, Docker configuration presented challenges. We recommend using the pre-configured VM provided by your lab instructor.

1. **Obtain the VM**:
   - Contact your lab instructor to get access to the pre-configured Big Data VM
   - The VM should have Hadoop, Spark, and Java pre-installed

2. **Import the VM**:
   - Open VirtualBox (or your VM software)
   - File → Import Appliance
   - Select the provided .ova or .ovf file
   - Click Import and wait for completion

3. **Start the VM**:
   - Select the imported VM
   - Click Start
   - Login with provided credentials (usually: username `student`, password `student` or as instructed)

4. **Verify VM Environment**:
   ```bash
   # Check Java version
   java -version

   # Check Hadoop version
   hadoop version

   # Check Python version
   python3 --version
   ```

#### Option B: Local Setup (Advanced)
If you prefer local setup despite the documented challenges:

1. **Install JDK**:
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install openjdk-8-jdk

   # On CentOS/RHEL
   sudo yum install java-1.8.0-openjdk
   ```

2. **Install Hadoop**:
   - Download Hadoop 3.3.x from https://hadoop.apache.org/releases.html
   - Extract to `/opt/hadoop`
   - Configure environment variables in `~/.bashrc`:
     ```bash
     export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
     export HADOOP_HOME=/opt/hadoop
     export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
     ```

3. **Configure Hadoop** (Single Node Cluster):
   - Edit `$HADOOP_HOME/etc/hadoop/hadoop-env.sh`:
     ```bash
     export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
     ```
   - Configure core-site.xml, hdfs-site.xml, mapred-site.xml, yarn-site.xml as per Hadoop documentation

### Step 2: Project Setup

1. **Download the Project**:
   - Download the project zip file from the provided source
   - Extract to a directory (e.g., `~/bigdata-project`)

2. **Navigate to Project Directory**:
   ```bash
   cd ~/bigdata-project
   ```

3. **Create Required Directories**:
   ```bash
   mkdir -p data outputs docs
   ```

### Step 3: Python Environment Setup

1. **Install Python (if not already installed)**:
   ```bash
   # On Ubuntu/Debian
   sudo apt install python3 python3-pip

   # On CentOS/RHEL
   sudo yum install python3 python3-pip
   ```

2. **Create Virtual Environment (Recommended)**:
   ```bash
   python3 -m venv bigdata_env
   source bigdata_env/bin/activate
   ```

3. **Install Required Python Packages**:
   ```bash
   pip install requests pandas matplotlib seaborn
   ```

4. **Verify Installation**:
   ```bash
   python3 -c "import requests, pandas, matplotlib; print('All packages installed successfully')"
   ```

### Step 4: YouTube API Configuration

1. **Obtain YouTube Data API v3 Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API Key)
   - Restrict the API key for security (optional but recommended)

2. **Configure API Key in Project**:
   - Open `src/config.py`
   - Replace the existing API_KEY with your key:
     ```python
     API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
     ```

3. **Test API Key**:
   ```bash
   python3 -c "
   import requests
   from src.config import API_KEY
   url = 'https://www.googleapis.com/youtube/v3/search'
   params = {'part': 'snippet', 'q': 'test', 'key': API_KEY, 'maxResults': 1}
   response = requests.get(url, params=params)
   print('API Key valid' if response.status_code == 200 else 'API Key invalid')
   "
   ```

### Step 5: Hadoop HDFS Setup

1. **Start Hadoop Services** (in VM or local setup):
   ```bash
   # Format HDFS (first time only)
   hdfs namenode -format

   # Start HDFS
   start-dfs.sh

   # Start YARN
   start-yarn.sh
   ```

2. **Verify Hadoop Services**:
   ```bash
   # Check running processes
   jps

   # You should see: NameNode, DataNode, ResourceManager, NodeManager

   # Check HDFS health
   hdfs dfsadmin -report
   ```

3. **Create Project Directory in HDFS**:
   ```bash
   hdfs dfs -mkdir -p /user/project/youtube_data
   hdfs dfs -ls /
   ```

### Step 6: Data Collection Setup

1. **Configure Data Collection Parameters**:
   - Review `src/data_collector.py` for search queries and parameters
   - Adjust `max_results` and date ranges as needed

2. **Test Data Collection** (Optional small test):
   ```bash
   cd src
   python3 data_collector.py
   # This will run with default parameters and create sample data
   ```

### Step 7: Run the Complete Pipeline

1. **Execute Data Collection**:
   ```bash
   cd src
   python3 data_collector.py
   ```
   - This will collect YouTube video data and save to `../data/youtube_videos.json`
   - May take several minutes depending on API quotas

2. **Transfer Data to HDFS**:
   ```bash
   hdfs dfs -put ../data/youtube_videos.json /user/project/youtube_data/
   hdfs dfs -put ../data/youtube_comments.json /user/project/youtube_data/
   hdfs dfs -ls /user/project/youtube_data/
   ```

3. **Run Data Analysis**:
   ```bash
   python3 data_analyzer.py
   ```
   - This processes the data and displays statistics

4. **Generate Visualizations**:
   ```bash
   python3 data_visualizer.py
   ```
   - Output charts will be saved in `../outputs/`

### Step 8: Generate Report

1. **Compile LaTeX Report** (if LaTeX is installed):
   ```bash
   cd Report
   pdflatex Report.tex
   # Run multiple times for cross-references
   pdflatex Report.tex
   pdflatex Report.tex
   ```

2. **View Results**:
   - Check `outputs/` directory for generated charts
   - Open `Report/Report.pdf` for the complete report

## Troubleshooting

### Common Issues

1. **Hadoop Services Won't Start**:
   - Check Java installation: `java -version`
   - Verify environment variables: `echo $JAVA_HOME`
   - Check logs in `$HADOOP_HOME/logs/`

2. **API Quota Exceeded**:
   - YouTube API has daily limits
   - Wait 24 hours or create a new API key
   - Reduce `max_results` in data collection

3. **Python Import Errors**:
   - Ensure virtual environment is activated
   - Reinstall packages: `pip install -r requirements.txt` (if file exists)
   - Check Python path: `which python3`

4. **VM Network Issues**:
   - Ensure VM network is set to "Bridged" or "NAT"
   - Check internet connectivity from VM

5. **Permission Errors**:
   - Use `sudo` for system installations
   - Check file permissions: `ls -la`

### Getting Help

- Check the project README.md for additional information
- Review the LaTeX report for detailed methodology
- Consult lab instructor for VM-specific issues
- Check YouTube API documentation for quota and usage details

## Performance Optimization

- **Memory**: Increase VM RAM if processing large datasets
- **Storage**: Ensure sufficient HDFS space for data replication
- **Network**: Use wired connection for stable API calls
- **API Limits**: Implement rate limiting in data collection scripts

## Security Notes

- Never commit API keys to version control
- Restrict API key usage in Google Cloud Console
- Use HTTPS for all API communications
- Regularly rotate API keys

## Maintenance

- **Update Dependencies**: `pip install --upgrade requests pandas matplotlib`
- **Hadoop Maintenance**: Monitor disk usage and clean temporary files
- **Backup Data**: Regularly backup HDFS data and project files
- **Log Rotation**: Clean Hadoop logs periodically

---

**Note**: This installation manual assumes the use of the lab-provided VM as documented in the project report. Local Docker setup encountered multiple technical challenges and is not recommended without expert assistance.