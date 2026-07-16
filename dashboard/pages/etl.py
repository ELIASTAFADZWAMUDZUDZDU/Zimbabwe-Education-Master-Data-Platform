"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : ETL Monitor
Purpose : Execute and Monitor ETL Pipeline
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import streamlit as st
import subprocess
import sys

# ==========================
# Page Configuration
# ==========================

st.set_page_config(

    page_title="ETL Pipeline",

    page_icon="⚙️",

    layout="wide"

)

# ==========================
# Title
# ==========================

st.title("⚙️ ETL Pipeline Monitor")

st.write(
    "Run the complete Zimbabwe Education Master Data Platform pipeline."
)

st.divider()

# ==========================
# Progress Display
# ==========================

progress = st.progress(0)

status_box = st.empty()

log_box = st.empty()

# ==========================
# Stage Status
# ==========================

stages = {

    "EXTRACT": False,
    "LOAD_RAW": False,
    "CLEAN": False,
    "STANDARDIZE": False,
    "MERGE": False,
    "FILL": False,
    "VALIDATE": False,
    "SAVE": False,
    "POSTGRES": False

}

progress_values = {

    "EXTRACT": 10,
    "LOAD_RAW": 20,
    "CLEAN": 35,
    "STANDARDIZE": 50,
    "MERGE": 65,
    "FILL": 75,
    "VALIDATE": 85,
    "SAVE": 95,
    "POSTGRES": 100

}


def display_status():

    text = ""

    for stage, complete in stages.items():

        icon = "🟢" if complete else "⚪"

        text += f"{icon} {stage.replace('_',' ')}\n"

    status_box.markdown(text)


display_status()

st.divider()

# ==========================
# Run Pipeline
# ==========================

if st.button(

    "▶ Run Complete ETL Pipeline",

    use_container_width=True

):

    output = ""

    process = subprocess.Popen(

        [

            sys.executable,

            "scripts/main.py"

        ],

        stdout=subprocess.PIPE,

        stderr=subprocess.STDOUT,

        text=True,

        bufsize=1

    )

    for line in process.stdout:

        output += line

        log_box.code(output)

        if "STEP:" in line:

            step = line.replace("STEP:", "").strip()

            if step in stages:

                stages[step] = True

                display_status()

                progress.progress(

                    progress_values[step]

                )

    process.wait()

    if process.returncode == 0:

        st.success("Pipeline Completed Successfully!")

        st.balloons()

    else:

        st.error("Pipeline Failed.")