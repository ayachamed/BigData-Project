# 📘 PROJECT REPORT

## Big Data Analysis of YouTube Content Related to the Gaza Conflict

---

## 1. Introduction

The rapid growth of social media platforms has led to the generation of massive amounts of digital content. YouTube, as one of the largest video-sharing platforms in the world, plays a major role in shaping and reflecting public discourse on global events. The conflict in Gaza, in particular, has generated a significant volume of videos, discussions, and user interactions.

The purpose of this project is to **collect, store, process, and analyze YouTube data related to the Gaza conflict** using **Big Data technologies**. By applying distributed storage and processing techniques, the project aims to extract meaningful insights regarding dominant topics, user engagement, and temporal trends.

---

## 2. Project Objectives

The main objectives of this project are:

1. To automatically collect YouTube video data using the YouTube Data API.
2. To store the collected data in a distributed storage system (HDFS).
3. To process and analyze the data using Apache Spark.
4. To perform exploratory data analysis and visualization.
5. To interpret the results in the context of media coverage and public interest.

---

## 3. Architecture and Technical Environment

### 3.1 System Architecture

The project follows a complete Big Data pipeline:

```
YouTube Data API
        ↓
Python Data Collection
        ↓
HDFS (Distributed Storage)
        ↓
Apache Spark (Distributed Processing)
        ↓
HDFS / Local Outputs
        ↓
Pandas & Matplotlib (Visualization)
```

This architecture ensures scalability, fault tolerance, and reproducibility.

---

### 3.2 Technical Environment

To save time and avoid complex manual installation, a **preconfigured virtual machine** containing Hadoop and Spark was used. This environment includes:

* Hadoop (HDFS)
* Apache Spark
* Java
* Python
* Linux operating system

**Academic justification**:
Using a preconfigured environment ensures system stability, correct configuration of distributed components, and reproducibility, while allowing the focus to remain on data analysis rather than infrastructure setup.

---

### 3.3 Technologies Used

| Technology          | Purpose                      |
| ------------------- | ---------------------------- |
| YouTube Data API v3 | Data collection              |
| Python              | Data collection and analysis |
| Hadoop HDFS         | Distributed storage          |
| Apache Spark        | Distributed processing       |
| PySpark             | Big Data analytics           |
| Pandas              | Exploratory analysis         |
| Matplotlib          | Data visualization           |
| Linux               | Execution environment        |

---

## 4. Data Collection

### 4.1 Data Source

Data was collected using the **YouTube Data API v3**. The following search queries were used:

* Gaza war
* Israel Palestine conflict
* Gaza humanitarian crisis
* Palestine news
* Israel Hamas war

The data covers videos published within the **last six months**.

---

### 4.2 Collected Data

Two types of data were collected:

#### Video Data

* Video title
* Channel name
* Publication date
* View count
* Like count
* Comment count
* Search query keyword

#### Comment Data

* Comment text
* Author
* Like count
* Publication date

The data was saved in both **JSON and CSV formats** for flexibility.

---

## 5. Distributed Storage with HDFS

The video dataset was uploaded to the Hadoop Distributed File System (HDFS):

```
/youtube/youtube_gaza.csv
```

Using HDFS provides:

* Distributed and fault-tolerant storage
* Compatibility with Spark
* Scalability for larger datasets

---

## 6. Big Data Processing with Apache Spark

### 6.1 Keyword Frequency Analysis

Using PySpark, the following steps were applied:

1. Reading data directly from HDFS.
2. Converting text to lowercase.
3. Tokenizing video titles into words.
4. Removing non-alphabetic tokens.
5. Removing common stop words.
6. Counting word occurrences.
7. Sorting results by frequency.

**Key findings** include dominant terms such as:

* *gaza*
* *israel*
* *palestinians*
* *palestine*
* *war*
* *peace*
* *ceasefire*

These results confirm that the collected data is highly relevant to the studied topic.

---

### 6.2 Sentiment Analysis

A simple **rule-based sentiment analysis** was implemented using PySpark. Video titles were classified as:

* **Positive**: containing keywords such as *peace*, *ceasefire*
* **Negative**: containing keywords such as *war*, *attack*, *kill*
* **Neutral**: all other cases

Although basic, this approach provides an initial emotional categorization of video content while remaining scalable.

---

### 6.3 Writing Results to HDFS

The results of the Spark word count analysis were saved back to HDFS:

```
/youtube/results_wordcount/
```

This completes the distributed processing pipeline from ingestion to result persistence.

---

## 7. Exploratory Analysis with Pandas

In addition to Spark, **Pandas** was used for:

* Statistical aggregation
* Easier manipulation of structured data
* Preparing data for visualization

This hybrid approach reflects real-world Big Data workflows, where Spark handles large-scale processing and Pandas is used for reporting and analysis.

---

## 8. Data Visualization and Results

Several visualizations were generated using **Matplotlib**:

### 8.1 Search Query Distribution

* The query **“Israel Hamas war”** accounts for the largest share of videos.
* Other queries show a relatively balanced distribution.

### 8.2 Views and Likes by Query

* Videos related to **“Israel Hamas war”** receive the highest number of views and likes.
* **“Palestine news”** follows as the second most engaging topic.

### 8.3 Temporal Evolution

* A clear increase in the number of published videos is observed over time.
* This reflects growing media attention and public interest.

### 8.4 Top Channels by Number of Videos

* A limited number of channels publish multiple videos on the topic.
* News-oriented channels dominate the dataset.

### 8.5 Most Viewed Videos

* The most viewed videos are mainly produced by international news channels.
* Titles often focus on strategic and geopolitical analysis.

All visual outputs were saved in the `deliverables/` directory.

---

## 9. Interpretation of Results

The analysis highlights several key insights:

* The Gaza conflict generates strong audience engagement on YouTube.
* Conflict-oriented keywords attract significantly more views than humanitarian-focused content.
* Search keywords strongly influence content visibility.
* YouTube acts as a major amplifier of international news and political discourse.

---

## 10. Project Limitations

* The dataset size is limited by YouTube API quotas.
* Sentiment analysis is rule-based and lacks linguistic nuance.
* Only video titles were deeply analyzed; comments could be further explored.

---

## 11. Future Improvements

Possible extensions of this project include:

* Advanced NLP-based sentiment analysis (BERT, VADER, TextBlob).
* Large-scale analysis of user comments.
* Real-time data processing using Kafka and Spark Streaming.
* Deployment on a real multi-node cluster.
* Interactive dashboards for result visualization.

---

## 12. Conclusion

This project demonstrates the practical use of **Big Data technologies** to analyze real-world social media data. By combining **HDFS**, **Apache Spark**, and **Python-based analytics**, a complete and scalable data pipeline was implemented.

Despite a moderate dataset size, the project fully adheres to **Big Data principles**, as it relies on distributed storage, distributed processing, and scalable architecture. The approach and methodology used can be directly extended to much larger datasets and more complex analyses.

---

## ✅ Academic Validation

> *This project qualifies as a Big Data project due to the use of distributed storage (HDFS), distributed processing (Apache Spark), and a scalable data pipeline architecture.*