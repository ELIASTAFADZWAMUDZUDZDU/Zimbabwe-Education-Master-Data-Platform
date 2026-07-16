# 🏫 Zimbabwe Education Master Data Platform (ZEMDP)

*A centralized education data platform built using modern Data Engineering practices, enhanced with an integrated AI assistant for natural language database exploration.*

---

## 📖 Overview

The **Zimbabwe Education Master Data Platform (ZEMDP)** is an end-to-end Data Engineering project designed to collect, transform, integrate, store, and visualize Zimbabwe secondary school information from multiple public data sources.

The platform automates the complete ETL (Extract, Transform, Load) process, consolidating fragmented educational data into a centralized PostgreSQL database. Users can explore the data through an interactive Streamlit dashboard featuring real-time statistics, search, filtering, and an integrated AI assistant capable of answering natural language questions about the database.

---

# 🎯 Project Objectives

The project was developed to demonstrate modern Data Engineering principles by:

- Designing a complete ETL pipeline
- Integrating data from multiple public sources
- Cleaning and standardizing inconsistent datasets
- Building a normalized PostgreSQL database
- Developing an interactive analytics dashboard
- Integrating an AI assistant for natural language database exploration
- Applying software engineering best practices for modular and maintainable code

---

# ✨ Features

## 🔹 Data Engineering

- Automated ETL Pipeline
- Multi-source Data Integration
- Data Cleaning
- Data Standardization
- Duplicate Detection
- Missing Value Handling
- Data Validation
- Master Dataset Generation

---

## 🔹 Database

- PostgreSQL Relational Database
- Normalized Database Design
- Database Views
- ETL Execution Logging
- Data Quality Monitoring

---

## 🔹 Dashboard

Interactive Streamlit dashboard providing:

- Dashboard Statistics
- School Directory
- Search Functionality
- Province Filter
- Education Level Filter
- Responsive Data Tables

---

## 🔹 AI Assistant

The platform includes an integrated AI assistant powered by **Google Gemini**.

Instead of writing SQL queries manually, users can ask questions in natural language.

Example questions include:

- Show all schools in Harare
- Top 10 O Level schools
- Schools with websites
- Schools offering A Level education
- Schools in Bulawayo
- Schools in Midlands Province

The AI assistant:

- Converts natural language into SQL
- Validates generated SQL
- Executes safe read-only queries
- Retrieves results from PostgreSQL
- Generates human-readable summaries

---

# 🏗 System Architecture

```text
                      Zimbabwe Education Master Data Platform

                           Public Data Sources
        ┌────────────────────┬────────────────────┬────────────────────┐
        │                    │                    │
    Wikipedia          ZimbabweYP          IBZIM Rankings
        │                    │                    │
        └────────────────────┴────────────────────┴────────────────────┘
                                 │
                                 ▼
                        Data Extraction Layer
                                 │
                                 ▼
                      Data Transformation Layer

                • Cleaning
                • Standardization
                • Validation
                • Merge
                • Missing Value Handling

                                 │
                                 ▼
                       Master JSON Dataset
                                 │
                                 ▼
                     PostgreSQL Relational Database
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
        Streamlit Dashboard             Integrated AI Assistant
        • Dashboard Statistics          • Natural Language Queries
        • Search                        • SQL Generation
        • Filters                       • SQL Validation
        • School Directory              • AI Response Generation
```

---

# 🔄 ETL Pipeline

The platform follows a complete ETL workflow.

## 1️⃣ Extract

Data is automatically collected from:

- Wikipedia
- Zimbabwe Yellow Pages
- IBZIM O-Level Rankings
- IBZIM A-Level Rankings

---

## 2️⃣ Transform

The extracted datasets are processed through:

- Raw Data Loading
- School Name Cleaning
- Data Standardization
- Source Merging
- Missing Value Completion
- Validation
- Master Dataset Generation

---

## 3️⃣ Load

The processed dataset is loaded into a normalized PostgreSQL database.

Each ETL execution is recorded in the **etl_runs** table, enabling monitoring and auditing of pipeline executions.

---

# 🗄 Database Design

The PostgreSQL database consists of the following tables:

| Table | Description |
|--------|-------------|
| provinces | Stores province information |
| schools | Master school records |
| school_phones | School telephone numbers |
| school_sources | Links schools to their data sources |
| sources | Stores metadata about data sources |
| staging_schools | Temporary staging area |
| quality_issues | Data quality monitoring |
| etl_runs | ETL execution history |

Database views are used to simplify dashboard queries and reporting.

---

# 📊 Dashboard

The Streamlit dashboard provides an interactive interface for exploring educational data.

### Dashboard Statistics

- Total Schools
- Provinces
- Phone Numbers
- Websites
- Email Addresses
- Ranked Schools

### School Directory

Users can:

- Search schools by name
- Filter by province
- Filter by education level
- Browse complete school information

---

# 🤖 AI Assistant Workflow

The integrated AI assistant enables users to interact with the database using natural language.

```text
User Question
      │
      ▼
Google Gemini
(Natural Language → SQL)
      │
      ▼
SQL Validation
      │
      ▼
PostgreSQL Database
      │
      ▼
Query Results
      │
      ▼
AI Response Generation
      │
      ▼
Displayed in Streamlit
```

Only safe **SELECT** statements are allowed to protect database integrity.

---

# 💻 Technology Stack

### Programming Language

- Python

### Database

- PostgreSQL

### Dashboard

- Streamlit

### Data Processing

- Pandas

### Web Scraping

- Requests
- BeautifulSoup

### Artificial Intelligence

- Google Gemini API

### Environment Management

- python-dotenv

# 📂 Project Structure

```text
ZEMDP/
│
├── dashboard/                      # Streamlit application
│   ├── pages/                      # Additional dashboard pages
│   ├── assets/                     # Images and static assets
│   ├── ai_engine.py                # Gemini AI engine
│   ├── analytics.py                # Dashboard analytics
│   ├── app.py                      # Main Streamlit application
│   ├── database.py                 # PostgreSQL connection
│   ├── export.py                   # Data export functionality
│   └── test_models.py              # AI model testing
│
├── data/
│   ├── raw/                        # Extracted raw datasets
│   ├── staging/                    # Intermediate processing files
│   └── processed/                  # Master datasets
│
├── database/
│   ├── schema/                     # Table creation scripts
│   ├── seeds/                      # Initial database seed data
│   └── views/                      # PostgreSQL views
│
├── scripts/
│   ├── extract/                    # Data extraction modules
│   ├── transform/                  # Data transformation modules
│   ├── load/                       # PostgreSQL loading modules
│   └── main.py                     # Complete ETL pipeline
│
├── .env                            # Environment variables
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/ZEMDP.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=zemdp
DB_USER=postgres
DB_PASSWORD=your_password

GEMINI_API_KEY=your_api_key
```

---

# ▶ Running the Project

### Execute the ETL Pipeline

```bash
python scripts/main.py
```

The ETL pipeline will:

- Extract data
- Transform data
- Validate records
- Generate the master dataset
- Load PostgreSQL
- Record ETL execution logs

---

### Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📈 Future Improvements

- Interactive Charts
- Geographic School Mapping
- School Comparison Tool
- REST API
- Automated ETL Scheduling
- Docker Deployment
- Cloud Deployment
- User Authentication
- Advanced AI Analytics

---

# 👨‍💻 Author

**Elias Tafadzwa Mudzudzu**

Computer Engineering Student

### Areas of Interest

- Data Engineering
- Artificial Intelligence
- Machine Learning
- Data Analytics
- Data Infrastructure

---

# 📄 License

This project is intended for educational, research, and portfolio purposes.