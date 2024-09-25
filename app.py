
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

import analysis
import analysis2
import budget_analysis

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title='Mental health', )


st.title("Mental health Analysis")


with st.sidebar:
    selected = option_menu(
    menu_title = "",
    options=["Home", "Analysis1","Analysis2",],
    icons=["house", "info-circle", "info-circle"],
    menu_icon="cast",
    default_index = 0,
)


if selected == "Home":
    # st.title(f"You have selected {selected}")
    st.image("constants/MentalHealthImage.jpg", caption="")
    analysis.show_analysis_page()

elif selected == "Analysis1":
    analysis2.show_analysis2_page()

elif selected == "Analysis2":
    budget_analysis.analysis3()

