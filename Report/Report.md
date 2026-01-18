# Big Data Analysis: YouTube Content Related to the Gaza Genocide

**Ministry of Higher Education and Scientific Research**
**University of Manouba**
**Higher Institute of Multimedia Arts (ISAMM)**

**Prepared by:** Mohamed Ayacha (3IM1)
**Academic Year:** 2025/2026

---

## Abstract
This report details the design and implementation of a comprehensive Big Data analytical pipeline tailored to process and analyze YouTube data concerning the ongoing genocide in Gaza. Leveraging the **YouTube Data API v3**, the project systematically aggregates video metadata and user comments from **October 6, 2023 to October 10, 2025**. The infrastructure employs a distributed architecture featuring **Hadoop HDFS** for resilient data storage and **Apache Spark** concepts for processing. The analysis, executed via Python, uncovers critical insights into global public engagement, the dominance of major media outlets, and the temporal evolution of digital discourse. This work demonstrates the efficacy of Big Data technologies in interpreting complex, high-volume social media trends.

---

## 1. Introduction & Problem Statement

The digital age has fundamentally altered the landscape of geopolitical discourse. Social media platforms, particularly YouTube, serve not only as repositories of user-generated content but as primary sources of news and information for millions globally. The genocide in Gaza has generated an unprecedented volume of digital interaction, providing a unique opportunity to apply data science techniques to understand global feeling.

### 1.1 Problem Identification
Analyzing this vast ocean of data presents significant challenges:
*   **Volume & Velocity:** The rate of video uploads and comment generation exceeds the capacity of traditional manual analysis.
*   **Variety:** The data is highly heterogeneous, comprising unstructured text, metadata, and numerical metrics.
*   **Veracity:** The politicized nature of the topic requires rigorous data collection methods.

### 1.2 Project Goals
The primary objective is to build a scalable pipeline that can:
1.  Ingest data reliably from external APIs.
2.  Store large datasets in a fault-tolerant manner.
3.  Process and transform raw data into analytical insights.
4.  Visualize trends to make complex data accessible.

---

## 2. Proposed Solution: The Big Data Pipeline
To address these challenges, we designed a pipeline grounded in the **Lambda Architecture** principles. The solution automates the end-to-end flow from data acquisition to insight generation.

### 2.1 Analytical Approach
We employ a mixed-methods approach:
*   **Descriptive Analytics:** To understand "what happened" (e.g., total views, upload frequency).
*   **Diagnostic Analytics:** To understand "why it happened" (e.g., correlating spikes in views with real-world events).
*   **Text Mining:** To extract key themes and dominant narratives from video titles.

---

## 3. System Architecture & Technology Stack

The architecture is designed for modularity and scalability. Each component plays a specific role in the data lifecycle.

### 3.1 Technology Stack
*   **YouTube Data API v3:** The extraction layer. It allows granular search capabilities.
*   **Hadoop HDFS:** The storage layer. HDFS provides high throughput access and data replication.
*   **Apache Spark:** The processing layer. Spark's in-memory computation capabilities allow for rapid iteration.
*   **Python (Pandas, Matplotlib, Seaborn):** The analysis and presentation layer for generating visualizations.

---

## 4. Implementation Details (Step-by-Step)

### Phase 1: Environment Configuration
Before coding, a robust Big Data environment was established utilizing a pre-configured Virtual Machine mimicking a single-node cluster (HDFS Setup, Service Verification).

### Phase 2: Data Ingestion (The Collector)
We developed a custom Python module, `src/data_collector.py`, to interface with the Google Cloud Platform. The search queries were carefully selected to cover various aspects of the conflict, and we configured the collector to retrieve up to **50 videos for each query** to ensure a sufficient dataset size:
*"Gaza war", "Israel Palestine conflict", "Gaza humanitarian crisis", "Palestine news", "Israel Hamas war"*.

We utilize **relevance-based sorting** to ensure the dataset captures the most significant content from the entire 2023-2025 period, rather than just the most recent uploads.

### Phase 3: Distributed Storage (HDFS Integration)
Once collected, data is migrated from the local file system to the Hadoop Distributed File System.
```bash
hdfs dfs -put data/youtube_videos.json /user/project/youtube_data/
```

### Phase 4: Data Processing & Analysis
The `src/data_analyzer.py` script serves as the engine for extracting insights (Data Cleaning, Type Casting, Normalization).

### Phase 5: Visualization
Finally, `src/data_visualizer.py` converts the processed data into visual narratives.

---

## 5. Results and Discussion

The analysis of the dataset collected between **Oct 6, 2023 and Oct 10, 2025** yielded significant findings regarding the digital coverage of the conflict.

### 5.1 Media Dominance
The analysis of the "Top Channels" clearly indicates that legacy media and established international news outlets dominate the conversation on YouTube.

### 5.2 Temporal Evolution
The timeline of video uploads is not linear. It exhibits peaks that correlate strongly with real-world escalation events.

### 5.3 Keyword Analysis
The textual analysis of video titles reveals a focus on high-impact, emotive keywords. Terms like "War", "Attack", and "Crisis" are prevalent.

---

## 6. Conclusion & Future Work

### Conclusion
This project has successfully demonstrated the implementation of a Big Data pipeline for social media analysis.
1.  **Scalability:** The architecture is decoupled.
2.  **Insight:** The analysis confirmed that digital discourse is news-driven and reactive.
3.  **Reliability:** The use of distributed systems ensures data integrity.

### Future Enhancements
*   feeling Analysis on comments.
*   Real-Time Streaming with Kafka.
*   Geospatial Analysis.
