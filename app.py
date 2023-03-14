import streamlit as st

import numpy as np
import pandas as pd
import datetime as dt
import requests
import json

st.set_page_config(page_title='AIS Project', page_icon='💰', layout='centered', initial_sidebar_state="collapsed" )


def prediction_url(date, number, risk,industries=None):
    params = dict(
                year = date.isocalendar()[0],
                week = date.isocalendar()[1],
                # day = date.isocalendar()[2],
                investment = number,
                #risk = risk,
                #industries = ind
            )
    
    url = f"http://127.0.0.1:8000/predict?year={params['year']}&week={params['week']}&investment={number}&risk={risk}&industries={industries}"
    return url

def fetch_prediction(url):
    try:
        result = requests.get(url)
        return result.json()
    except Exception:
        return {}

def main(): 
    prediction =''
    html_temp = """
    <div>
    <h1 style="color:BLACK;text-align:left;">Welcome to AIS PROJECT APP 💰</h1>
    <h3 style="color:BLACK;text-align:left;">The commit of this project is to help you Building an Strategy for your Economy wellness<h3>
    <p style="color:GRAY;text-align:left;"> 
        This front queries the AIS API:\n
        http://127.0.0.1:8000/predict?year=2023&week=11&investment=1000&risk=low&industries=[%27Financials%27]
    </p>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2,2])
    
    with col1:
        
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
            
            submitted = st.form_submit_button("Make prediction")
            if submitted:
                print(ind)
                pred_url = prediction_url(date, number, risk, ind)
                print(pred_url)
                prediction = fetch_prediction(pred_url)
                
            else:
                st.write('Have you some questions?')
            # st.header(response.url)
            # st.header(prediction)
            

    with col2:
        with st.expander("ℹ️ How does it works?", expanded=False):
            st.write("""
                    1. Choose the amount of money you want to invest
                    2. Specify the period of time you want to invest
                    3. risky? conservative? or balanced? Choose the level of risk you want to take
                    4. Feeling kind with an industry of your choice? Select it!
                        """)
        
        if prediction != '':
            df = json.loads(prediction['data'])
            pred = pd.DataFrame(columns=df['columns'], data=df['data'])
            ear = prediction['total_earnings']
            roi = prediction['roi']

            st.dataframe(pred)
            st.header(f'Total earnings: ${round(ear, 2)}')
            st.header(f'ROI: {round(roi, 1)}')
        else:
            st.error('Ups...')

        # st.write('The current number is ', number)

        # t = st.time_input('Set a period of time for your investment', dt.datetime.now())

        # st.write('', t)
        




# @st.cache
# def get_slider_data():

#     return pd.DataFrame({
#           'ticker': list(range(1, 11)),
#           'name': np.arange(10, 101, 10),
#           'industry': np.arange(100, 1001, 100),
#           'stock price': np.arange(1000, 10001, 1000),
#           'predicted class': np.arange(10000, 100001, 10000),
#         })

# df = get_slider_data()

# option = st.slider('Play with the output size', 1, 10, 3)

# filtered_df = df[df['ticker'] % option == 0]

# st.write(filtered_df)




# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# and used to select the displayed lines
# head_df = df.head(line_count)

# head_df



if __name__ == '__main__':
	main()