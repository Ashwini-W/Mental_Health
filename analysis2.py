import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

import plotly.express as px


from constants.constants import district_list,year

@st.cache
def load_data():
    df = pd.read_csv("data/districtWiseMentalHealth_18to20.csv")
    return df



def show_analysis2_page():
    
    df = load_data()
    # st.dataframe(df) 

    # Sidebar multiselect for district and year
    selected_cities = st.multiselect("Select District",district_list )
    selected_years = st.multiselect("Select years", df['Year'].unique())
    value_column = st.selectbox("Select the metric to plot", ['SEVERE_MENTAL_DISORDER_(SMD)',
       'COMMON_MENTAL _DISORDER(CMD)', 'ALCOHOL_&_SUBSTANCE_ABUSE',
       'CASES_REFERRED_TO_HIGHER_CENTRES', 'SUICIDE_ATTEMPT_CASES', 'Others',
       'Total'])

    filtered_data = df[(df['DISTRICT'].isin(selected_cities)) & (df['Year'].isin(selected_years))]
    filtered_data['Year'] = filtered_data['Year'].astype(str)

    # Plot the graph if data is selected
    if len(selected_years) == 1:
        st.warning("Please select more than one year to generate a plot.")

    elif not filtered_data.empty:

        fig = px.bar(
        filtered_data, 
        x="Year", 
        y=value_column, 
        color="DISTRICT", 
        # markers=True,
        barmode="group",
        text=value_column,  # Show values above the bars
        title=f"District Data Over Year for {value_column} cases",
        labels={'Year': 'Year', value_column: value_column}
        )

        fig.update_traces(textposition='outside',textfont=dict(size=18))
        fig.update_layout(hovermode="x unified",xaxis_type='category')
        
        fig.update_layout(
            width=1600, height=800,
            xaxis_title_font=dict(size=21), 
            yaxis_title_font=dict(size=21),
            xaxis=dict(titlefont=dict(size=16), tickfont=dict(size=18)), 
            yaxis=dict(titlefont=dict(size=16), tickfont=dict(size=18)) 
    
        )
        st.plotly_chart(fig)
    else:
        st.warning("Please select at least one district and one year to plot the graph.")
