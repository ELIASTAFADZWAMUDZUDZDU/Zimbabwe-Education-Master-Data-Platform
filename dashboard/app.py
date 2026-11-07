"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Dashboard
Purpose : Main Dashboard Application
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import streamlit as st
import plotly.express as px

from database import get_connection

from analytics import (
    get_dashboard_statistics,
    get_school_directory,
    get_schools_by_province,
    get_education_distribution,
    get_website_coverage,
    get_email_coverage,
    get_ranking_coverage
)

# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="Zimbabwe Education Master Data Platform",
    page_icon="🏫",
    layout="wide"
)

# ==========================
# Title
# ==========================

st.title("🏫 Zimbabwe Education Master Data Platform")

st.markdown(
    "A centralized education data platform built using modern Data Engineering practices, enhanced with an integrated AI assistant for natural language database exploration."
)

st.divider()

# ==========================
# Database Connection
# ==========================

try:

    connection = get_connection()
    connection.close()

    st.success("Connected to PostgreSQL")

    # ==========================
    # System Overview
    # ==========================

    st.header("📖 System Overview")

    st.info(
        """
The Zimbabwe Education Master Data Platform (ZEMDP) is an end-to-end Data Engineering system that automates the collection, transformation, storage and analysis of Zimbabwe secondary school information.

The platform integrates multiple public data sources into a centralized PostgreSQL database and provides interactive analytics, data export capabilities and AI-assisted querying through a Streamlit dashboard.
"""
    )

    # ==========================
    # System Architecture
    # ==========================

    st.header("🏗 System Architecture")

    st.code(
        """
        Multiple Data Sources
                 │
                 ▼
          Data Extraction
                 │
                 ▼
       Data Cleaning & Standardization
                 │
                 ▼
        Master Dataset Generation
                 │
                 ▼
          PostgreSQL Database
                 │
                 ▼
      Streamlit Analytics Dashboard
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 Analytics     Export      AI Assistant
"""
    )

    st.divider()

    # ==========================
    # Platform Features
    # ==========================

    st.header("✨ Platform Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            """
### ⚙️ ETL Pipeline

✓ Multi-source extraction

✓ Data cleaning

✓ Standardization

✓ Data integration

✓ Automated loading
"""
        )

    with col2:
        st.success(
            """
### 📊 Analytics

✓ Dashboard statistics

✓ Province insights

✓ Education distribution

✓ Coverage analysis

✓ Interactive charts
"""
        )

    with col3:
        st.success(
            """
### 🤖 AI Assistant

✓ Natural language queries

✓ SQL generation

✓ PostgreSQL querying

✓ AI summaries

✓ Intelligent exploration
"""
        )

    st.divider()

    # ==========================
    # Project Statistics
    # ==========================

    st.header("📈 Project Statistics")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric("Data Sources", "6")
    p2.metric("Dashboard Pages", "4")
    p3.metric("Database Tables", "7")
    p4.metric("SQL Views", "5")

    st.divider()

    # ==========================
    # Dashboard Statistics
    # ==========================

    st.header("📊 Dashboard Statistics")

    stats = get_dashboard_statistics()

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric(
        "🏫 Schools",
        stats["schools"]
    )

    col2.metric(
        "🌍 Provinces",
        stats["provinces"]
    )

    col3.metric(
        "📞 Phone Numbers",
        stats["phones"]
    )

    col4.metric(
        "🌐 Websites",
        stats["websites"]
    )

    col5.metric(
        "📧 Emails",
        stats["emails"]
    )

    col6.metric(
        "⭐ Ranked Schools",
        stats["ranked"]
    )

    st.divider()

    # ==========================
    # School Directory
    # ==========================

    st.header("🏫 School Directory")

    schools = get_school_directory()

    # --------------------------
    # Search
    # --------------------------

    search = st.text_input(
        "🔍 Search School",
        placeholder="Type a school name..."
    )

    if search:
        schools = schools[
            schools["school_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # --------------------------
    # Filters
    # --------------------------

    col1, col2 = st.columns(2)

    province = col1.selectbox(
        "Province",
        ["All"] +
        sorted(
            schools["province"]
            .dropna()
            .unique()
        )
    )

    education = col2.selectbox(
        "Education Level",
        ["All"] +
        sorted(
            schools["education_level"]
            .dropna()
            .unique()
        )
    )

    if province != "All":
        schools = schools[
            schools["province"] == province
        ]

    if education != "All":
        schools = schools[
            schools["education_level"] == education
        ]

    st.write(f"### Schools Found: {len(schools)}")

    st.dataframe(
        schools,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================
    # Analytics
    # ==========================

    st.header("📊 Analytics")

    # --------------------------
    # Schools by Province
    # --------------------------

    province_data = get_schools_by_province()

    fig = px.bar(
        province_data,
        x="province",
        y="total_schools",
        title="Schools by Province",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------
    # Education Levels
    # --------------------------

    education_data = get_education_distribution()

    fig = px.bar(
        education_data,
        x="education_level",
        y="total_schools",
        title="Education Level Distribution",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------
    # Coverage Charts
    # --------------------------

    col1, col2, col3 = st.columns(3)

    website = get_website_coverage()

    fig = px.pie(
        website,
        names="website_status",
        values="total",
        title="Website Coverage",
        hole=0.5
    )

    col1.plotly_chart(
        fig,
        use_container_width=True
    )

    email = get_email_coverage()

    fig = px.pie(
        email,
        names="email_status",
        values="total",
        title="Email Coverage",
        hole=0.5
    )

    col2.plotly_chart(
        fig,
        use_container_width=True
    )

    ranking = get_ranking_coverage()

    fig = px.pie(
        ranking,
        names="ranking_status",
        values="total",
        title="Ranking Coverage",
        hole=0.5
    )

    col3.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as error:

    st.error(
        f"Database Connection Failed\n\n{error}"
    )