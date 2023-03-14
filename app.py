import streamlit as st

import numpy as np
import pandas as pd
import datetime as dt
import requests
import json

'''
# AIS front

This front queries the AIS API]('http://127.0.0.1:8000/predict?year=2023&week=11&investment=1000&risk=low&industries=[%27Financials%27]')
'''


st.write('Page In Construction')

st.markdown(
    """
    # Welcome to AIS project app
    ## The commit of this project is to help you Building an Strategy for your Economy wellness
    """)

txt = st.text_area('How does it works?', '''
    1. Choose the amount of money you want to invest
    2. Specify the period of time you want to invest
    3. risky? conservative? or balanced? Choose the level of risk you want to take
    4. Feeling kind with an industry of your choice? Select it!
    ''')

# st.write('The current number is ', number)

# t = st.time_input('Set a period of time for your investment', dt.datetime.now())

# st.write('', t)

with st.form(key='params_for_api'):
     number = st.number_input('Insert the amount to invest', min_value=0, max_value=1000000, value=1000, step=1000)
     risk = st.select_slider('Select a level of risk', ['low', 'moderate', 'high'])
     date = st.date_input('Set a period of time for your investment: year/month/day', value=dt.datetime(2023, 3, 11))
     ind = st.multiselect('Select an industry', ['Financials', 'Health Care', 'Information Technology', 'Consumer Discretionary', 'Industrials', 'Consumer Staples', 'Energy', 'Materials', 'Real Estate', 'Utilities', 'Telecommunication Services'])
     # week = st.date_input('week', value=dt.datetime(2023, 3, 11))
     # day = st.date_input('day', value=dt.datetime(2023, 3, 11))
     # investment = investment,
     # risk = risk,
     # industries = industries)

     if st.form_submit_button('Make prediction'):
         st.write('Loading strategy...')
     else:
         st.write('Have you some questions?')

params = dict(
    year = date.isocalendar()[0],
    week = date.isocalendar()[1],
    # day = date.isocalendar()[2],
    investment = number,
    #risk = risk,
    #industries = ind
    )

api_url = 'http://127.0.0.1:8000/predict'

response = requests.get(api_url, params=params)
prediction = response.json()

# st.header(response.url)
# st.header(prediction)
df = json.loads(prediction['data'])
pred = pd.DataFrame(columns=df['columns'], data=df['data'])
ear = prediction['total_earnings']
roi = prediction['roi']

st.dataframe(pred)
st.header(f'Total earnings: ${round(ear, 2)}')
st.header(f'ROI: {round(roi, 1)}')


@st.cache
def get_slider_data():

    return pd.DataFrame({
          'ticker': list(range(1, 11)),
          'name': np.arange(10, 101, 10),
          'industry': np.arange(100, 1001, 100),
          'stock price': np.arange(1000, 10001, 1000),
          'predicted class': np.arange(10000, 100001, 10000),
        })

df = get_slider_data()

option = st.slider('Play with the output size', 1, 10, 3)

filtered_df = df[df['ticker'] % option == 0]

st.write(filtered_df)

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# and used to select the displayed lines
# head_df = df.head(line_count)

# head_df
