import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def budget_analysis(df_budget):
    df=df_budget

    st.markdown("""
    The dataset is from https://www.data.gov.in/resource/year-wise-details-budget-allocation-mental-health-2019-20-2022-23 which contains information about the mental health budget allocation across years, with the following columns:

    **YEAR:** The financial year (e.g., 2019-20).
    **TOTALHEALTHBUDGET:** The total health budget for the respective year.
    **TOTALALLOCATION_MENTALHEALTH:** The allocation specifically for mental health within the total health budget.

    The below donut chart shows the percentage allocation of the mental health budget over the years by the government.

    """)
    # --------------

    fig, ax = plt.subplots(figsize=(5,2))
    ax.pie(df['TOTALALLOCATION_MENTALHEALTH'], labels=df['YEAR'], autopct='%1.1f%%', startangle=90,textprops={'fontsize':4}, wedgeprops={'width': 0.3})

    center_circle = plt.Circle((0, 0), 0.40, fc='white')
    fig.gca().add_artist(center_circle)

    ax.axis('equal')
    plt.title('Total Mental Health Budget ALlocation (2019-2023)',fontsize=5)
    st.pyplot(fig)





# -----------------


    # fig, ax = plt.subplots(figsize=(5,4))

    # ax.plot(df['YEAR'], df['TOTALHEALTHBUDGET'], label='Total Health Budget', marker='o')
    # ax.plot(df['YEAR'], df['TOTALALLOCATION_MENTALHEALTH'], label='Total Mental Health Allocation', marker='o')

    # ax.set_xlabel('Year', fontsize=6)
    # ax.set_ylabel('Budget (in crores)', fontsize=6)
    # ax.set_title('Total Health Budget vs Mental Health Allocation (2019-2023)', fontsize=10)

    # ax.legend()
    # st.pyplot(fig)




def analysis3():

    # Create a Snowflake connection function with caching
    # @st.cache_resource  # Use this to cache the Snowflake connection
    df = pd.read_csv("data/districtWiseMentalHealth_18to20.csv")
    df.head()

    def get_snowflake_connection():
        conn = snowflake.connector.connect( 
            user=st.secrets["user"],
            password=st.secrets["password"],
            account=st.secrets["account"],
            database=st.secrets["database"],
            warehouse='COMPUTE_WH',
            schema='ACCOUNTADMIN'
        )
        return conn

    conn = get_snowflake_connection()
    st.write("Fetching data from Snowflake...")
    # query = "SELECT CURRENT_VERSION()"
    query1= "SELECT * from BUDGET_TABLE"
    cursor = conn.cursor()
    try:
        cursor.execute(query1)
        # version = cursor.fetchone()
        budget_data =cursor.fetchall()
        df_budget=pd.DataFrame(budget_data)
        df_budget.columns = ['SLNO', 'YEAR', 'TOTALHEALTHBUDGET', 'TOTALALLOCATION_MENTALHEALTH']
        st.write(df_budget)

        # st.write(f"Snowflake version: {budget_data[0]}")

        budget_analysis(df_budget)
    finally:
        cursor.close()
        conn.close()


