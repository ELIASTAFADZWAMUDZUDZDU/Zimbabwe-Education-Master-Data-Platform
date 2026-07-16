"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Export
Purpose : Export School Directory
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

import streamlit as st
import pandas as pd

from analytics import get_school_directory

# ==========================
# Page Configuration
# ==========================

st.set_page_config(

    page_title="Export Data",

    page_icon="📤",

    layout="wide"

)

st.title("📤 Export School Directory")

st.write(
    "Export the Zimbabwe School Directory."
)

st.divider()

# ==========================
# Load Data
# ==========================

schools = get_school_directory()

st.dataframe(

    schools,

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================
# CSV Export
# ==========================

csv = schools.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download CSV",

    data=csv,

    file_name="zimbabwe_school_directory.csv",

    mime="text/csv"

)

# ==========================
# Excel Export
# ==========================

from io import BytesIO

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

    schools.to_excel(

        writer,

        index=False,

        sheet_name="Schools"

    )

st.download_button(

    label="⬇ Download Excel",

    data=buffer,

    file_name="zimbabwe_school_directory.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)