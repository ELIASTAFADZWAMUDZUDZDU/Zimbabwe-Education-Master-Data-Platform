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
- Validates the generated SQL (see *Safety of AI-generated SQL* below)
- Runs it in a read-only transaction with a row limit and a time limit
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

## Safety of AI-generated SQL

The SQL written by the model is treated as untrusted text. Several layers protect the database:

1. **Validation (`dashboard/sql_guard.py`).** A query is accepted only if it is a single `SELECT` that reads from `vw_school_directory`. It rejects comments, quoted identifiers, `UNION`, `INTO`, `COPY`, other tables, and server functions such as `pg_sleep` or `pg_read_file`. Words inside text values (for example `ILIKE '%create%'`) are allowed.
2. **Row limit.** Results are capped at 500 rows.
3. **Read-only session.** The query runs in a read-only transaction with a 10-second timeout.
4. **Recommended: a restricted database role.** Create a role that can only `SELECT` from `vw_school_directory` and use it for the dashboard. This is the strongest protection and does not depend on the checks above:

```sql
CREATE ROLE zemdp_reader LOGIN PASSWORD 'choose-a-password';
GRANT CONNECT ON DATABASE zemdp TO zemdp_reader;
GRANT SELECT ON vw_school_directory TO zemdp_reader;
```

Put that role's details in `.env` as `DB_USER` and `DB_PASSWORD` when running the dashboard.

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
Zimbabwe-Education-Master-Data-Platform/
│
├── dashboard/                      # Streamlit application
│   ├── pages/                      # Additional dashboard pages
│   ├── assets/                     # Images and static assets
│   ├── ai_engine.py                # Gemini AI engine
│   ├── sql_guard.py                # Safety checks for AI-generated SQL
│   ├── analytics.py                # Dashboard analytics
│   ├── app.py                      # Main Streamlit application
│   └── database.py                 # PostgreSQL connection
│
├── data/
│   ├── raw/                        # Extracted raw datasets
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
│   ├── main.py                     # Complete ETL pipeline
│   └── list_gemini_models.py       # Lists the Gemini models your key can use
│
├── tests/                          # Offline tests for the SQL safety checks
├── .env.example                    # Template for your .env file
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/ELIASTAFADZWAMUDZUDZDU/Zimbabwe-Education-Master-Data-Platform.git
cd Zimbabwe-Education-Master-Data-Platform
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Copy `.env.example` to `.env` and fill in your own values. Never commit `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=zemdp
DB_USER=postgres
DB_PASSWORD=your_password

GEMINI_API_KEY=your_api_key

# Optional: change the Gemini models used
# GEMINI_SQL_MODEL=gemini-3.5-flash
# GEMINI_EXPLAIN_MODEL=gemini-flash-latest
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

# 🧪 Tests

The tests run offline (no database or API key needed):

```bash
python -m unittest discover -s tests -v
```

They check that normal questions' SQL is accepted and that dangerous SQL is rejected, including a second statement, other tables, hidden comments, `UNION`, `SELECT ... INTO`, and server functions.

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