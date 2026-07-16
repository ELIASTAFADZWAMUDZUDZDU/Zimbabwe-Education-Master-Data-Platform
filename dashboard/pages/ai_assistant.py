"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : AI Assistant
Purpose : Natural Language Search
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================================================
# Imports
# ==========================================================

import streamlit as st

from ai_engine import (

    generate_sql,

    validate_sql,

    execute_sql,

    explain_results

)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="AI Assistant",

    page_icon="🤖",

    layout="wide"

)

# ==========================================================
# Title
# ==========================================================

st.title("🤖 Zimbabwe Education AI Assistant")

st.write(

    "Ask questions about Zimbabwe Secondary Schools using natural language."

)

st.divider()

# ==========================================================
# Sidebar Examples
# ==========================================================

st.sidebar.header("💡 Example Questions")

st.sidebar.markdown("""

- Show all schools in Harare

- Top 10 O Level schools

- Top 20 A Level schools

- Schools with websites

- Schools with email addresses

- Schools in Bulawayo

- A Level schools in Midlands

- Schools in Manicaland

- Schools in Masvingo

""")

# ==========================================================
# User Input
# ==========================================================

question = st.text_area(

    "Ask a Question",

    placeholder="""
Example:

Show all A Level schools in Harare
"""

)

# ==========================================================
# Ask AI
# ==========================================================

if st.button("🚀 Ask AI"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("🤖 Thinking..."):

                # ------------------------------------------
                # Generate SQL
                # ------------------------------------------

                sql = generate_sql(question)

                # ------------------------------------------
                # Validate SQL
                # ------------------------------------------

                if not validate_sql(sql):

                    st.error(

                        "Unsafe SQL detected. Query rejected."

                    )

                    st.stop()

                # ------------------------------------------
                # Execute SQL
                # ------------------------------------------

                dataframe = execute_sql(sql)

                # ------------------------------------------
                # AI Summary
                # ------------------------------------------

                summary = explain_results(

                    question,

                    dataframe

                )

            # ==========================================
            # Results
            # ==========================================

            st.success(

                f"{len(dataframe)} record(s) found."

            )

            st.subheader("🤖 AI Response")

            st.info(summary)

            st.subheader("📊 Results")

            st.dataframe(

                dataframe,

                use_container_width=True,

                hide_index=True

            )

            # ==========================================
            # SQL
            # ==========================================

            with st.expander("🛠 View Generated SQL"):

                st.code(

                    sql,

                    language="sql"

                )

        except Exception as error:

            st.error(error)