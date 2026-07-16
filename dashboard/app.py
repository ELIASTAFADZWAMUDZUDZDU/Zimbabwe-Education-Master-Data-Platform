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
    "A centralized platform for Zimbabwe Secondary School Information."
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
    # Dashboard Statistics
    # ==========================

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