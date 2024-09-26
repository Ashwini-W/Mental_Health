import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

from constants.constants import district_list,year

@st.cache
def load_data():

    df = pd.read_csv("data/districtWiseMentalHealth_18to20.csv")
    print(df.head())    
    return df



def show_analysis_page():

    st.title("Analysing trend")

    df = load_data()
    st.dataframe(df) 

    # ----------------
    st.markdown("""
    The dataset contains information on mental health patients for various districts, with the following columns:

    **DISTRICT:** Name of the district.
    **SEVERE_MENTAL_DISORDER_(SMD): Number of patients with severe mental disorders.
    **COMMON_MENTAL_DISORDER(CMD):** Number of patients with common mental disorders.
    **ALCOHOL_&_SUBSTANCE_ABUSE:** Number of patients with alcohol and substance abuse issues.
    **CASES_REFERRED_TO_HIGHER_CENTRES:** Cases referred to higher medical centers.
    **SUICIDE_ATTEMPT_CASES:** Number of suicide attempt cases.
    **Others:** Other types of cases.
    **Total:** Total number of cases per district.

    The Dataset is -> https://www.data.gov.in/resource/district-wise-mental-health-patients-2018-19

    The dataset has been successfully aggregated by year, summing the total number of mental health-related cases across all districts. 
    2018: 1,010,467 cases
    2019: 1,065,175 cases
    2020: 457,652 cases
    """)
    # ---------------------
    print(df.columns)
    st.markdown("""select **districts** and **Year** and visualize it against various mental disorders.
    """)

    year_selected = st.radio("Select a year:",year )
    district_selected=st.multiselect("Select district",df['DISTRICT'].unique(),default='BELLARY')


    if(district_selected):
        
        District_all3years = df[df['DISTRICT'].isin(district_selected)]
        st.write("District Data for all 3 years")
        st.write(District_all3years)


        filtered_df = df[(df['DISTRICT'].isin(district_selected)) & (df['Year'] == year_selected)]
        
        fig = go.Figure()

        for district in district_selected :
            district_data = filtered_df[filtered_df['DISTRICT'] == district]

            x_values = ['SEVERE_MENTAL_DISORDER_(SMD)','COMMON_MENTAL _DISORDER(CMD)', 'ALCOHOL_&_SUBSTANCE_ABUSE',
        'CASES_REFERRED_TO_HIGHER_CENTRES', 'SUICIDE_ATTEMPT_CASES']
            y_values = [
                        district_data['SEVERE_MENTAL_DISORDER_(SMD)'].values[0],
                        district_data['COMMON_MENTAL _DISORDER(CMD)'].values[0], 
                        district_data['ALCOHOL_&_SUBSTANCE_ABUSE'].values[0],
                        district_data['CASES_REFERRED_TO_HIGHER_CENTRES'].values[0],
                        district_data['SUICIDE_ATTEMPT_CASES'].values[0]
                        ]

            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers',
                name=district,
                text=[f'Cases: {y}' for y in y_values],
                hoverinfo='text+name'
            ))

        # Add labels and title
        fig.update_layout(
            title=f"Mental Health by Category for District {district_selected} and year - ({year_selected})",
            xaxis_title="Category",
            yaxis_title="Number of Cases",
            hovermode="x unified",
            xaxis_title_font=dict(size=21),
            yaxis_title_font=dict(size=21),
            font=dict(size=14),
            xaxis=dict(gridcolor='lightgray'),
            yaxis=dict(gridcolor='lightgray')
        )

        st.plotly_chart(fig,use_container_width=True)
            
    else:
        st.write("Please select at least one column to plot.")


