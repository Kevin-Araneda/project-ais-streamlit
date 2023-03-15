import streamlit as st

import numpy as np
import pandas as pd
import datetime as dt
import requests
import json
import plotly.express as px

st.set_page_config(page_title='AIS Project', page_icon='💰', layout='wide', initial_sidebar_state="collapsed" )

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

def historic_url(date, number, risk,industries=None):
    params = dict(
                year = date.isocalendar()[0],
                week = date.isocalendar()[1],
                # day = date.isocalendar()[2],
                investment = number,
                #risk = risk,
                #industries = ind
            )
    
    url = f"http://127.0.0.1:8000/historic?year={params['year']}&week={params['week']}&investment={number}&risk={risk}&industries={industries}"
    return url

def fetch_prediction(url):
    try:
        result = requests.get(url)
        return result.json()
    except Exception:
        return {}

def main():
    row0_spacer1, row0_1, row_spacer2 = st.columns((.1, 2.3,.1))
    prediction = {'type': 'strategy',
                 'data': '{"columns":["ticker","name","industry","last_price","pred_pct","earnings"],"data":[["BAC","Bank of America","Financials",34.1599998474,1.43,2.8629329],["V","Visa Inc.","Information Technology",223.7700042725,1.28,2.553722],["IT","Gartner","Information Technology",333.8099975586,1.1,2.2082244],["MU","Micron Technology","Information Technology",56.7799987793,0.69,1.3840979],["AAPL","Apple Inc.","Information Technology",151.0299987793,0.23,0.46433852]]}',
                 'total_earnings': 9, 'roi': 0.95}
    historic = {'type': 'strategy',
                'data': '{"columns":["pred_year","pred_week","pred_earnings","real_earnings","pred_earnings_pct","real_earnings_pct"],"data":[[2023,9,32.3211654,4.8471957354,3.23,0.48],[2023,8,32.72969176,-27.2666216483,3.27,-2.73],[2023,7,12.638196,-1.4921986424,1.26,-0.15],[2023,6,0.0,0.0,0.0,0.0]]}',
                'pred_total_earnings': 77,
                'real_total_earnings': -23,
                'pred_roi': 7.77,
                'real_roi': -2.39}
    industries_options = ['Financials', 'Health Care', 'Information Technology', 'Consumer Discretionary', 'Industrials', 'Consumer Staples', 'Energy', 'Materials', 'Real Estate', 'Utilities', 'Telecommunication Services']
    industries_default = ['Financials','Information Technology','Industrials']
    html_temp = """
    <div>
    <p style="color:GRAY;text-align:left;"> 
        This front queries the AIS API:\n
        http://127.0.0.1:8000/predict?year=2023&week=11&investment=1000&risk=low&industries=[%27Financials%27]
    </p>
    </div>
    """
    with row0_1:
        st.title('Welcome to AIS PROJECT APP 💰')
        st.subheader('The commit of this project is to help you Building an Strategy for your Economy wellness')
        
    row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
    with row3_1:
        with st.expander("ℹ️ How does it works?", expanded=False):
            st.write("""
                    1. Choose the amount of money you want to invest
                    2. Specify the period of time you want to invest
                    3. risky? conservative? or balanced? Choose the level of risk you want to take
                    4. Feeling kind with an industry of your choice? Select it!
                        """)
        
        with st.form(key='params_for_api'):
            number = st.number_input('Insert the amount to invest', min_value=0, max_value=1000000, value=1000, step=1000)
            risk = st.select_slider('Select a level of risk', ['low', 'moderate', 'high'])
            date = st.date_input('Set a period of time for your investment: year/month/day', value=dt.datetime(2023, 3, 11))
            ind = st.multiselect('Select an industry',options=industries_options, default=industries_default)
            # week = st.date_input('week', value=dt.datetime(2023, 3, 11))
            # day = st.date_input('day', value=dt.datetime(2023, 3, 11))
            # investment = investment,
            # risk = risk,
            # industries = industries)
            
            submitted = st.form_submit_button("Make prediction")
            if submitted:
                pred_url = prediction_url(date, number, risk, ind)
                hist_url = historic_url(date,number,risk,ind)
                print(hist_url)
                prediction = fetch_prediction(pred_url)
                historic = fetch_prediction(hist_url)
                
            else:
                st.write('Have you some questions?')
            # st.header(response.url)
            # st.header(prediction)
        
    if prediction != '':
        col1_s,col1, col2, col2_s = st.columns((.1,1,1,.1))
        with col1:
            df = json.loads(prediction['data'])
            pred = pd.DataFrame(columns=df['columns'], data=df['data'])
            ear = prediction['total_earnings']
            roi = prediction['roi']
            st.dataframe(pred)
        with col2:
            st.metric(label='Total earnings', value=str(int(ear))+"$", delta=str(float(roi))+' ROI')
    else:
        st.error('Ups...')

    # @st.cache_data
    # def get_slider_data():

    #     return pd.DataFrame({
    #         'ticker': list(range(1, 11)),
    #         'name': np.arange(10, 101, 10),
    #         'industry': np.arange(100, 1001, 100),
    #         'stock price': np.arange(1000, 10001, 1000),
    #         'predicted class': np.arange(10000, 100001, 10000),
    #         })

    # df = get_slider_data()

    # option = st.slider('Play with the output size', 1, 10, 3)

    # filtered_df = df[df['ticker'] % option == 0]

    # st.write(filtered_df)
    row0_spacer1, row0_1, row_spacer2 = st.columns((.1, 2.3,.1))
    with row0_1:
        st.subheader('Recommendations')

        space, g1,spacef = st.columns((.1,1,.1))
        
        earnings_df = json.loads(historic['data'])
        
        real_earn_df = pd.DataFrame(columns=earnings_df['columns'], data=earnings_df['data'])
        real_earn_df['Year-Week'] = real_earn_df['pred_year'].astype(str) + '--' + real_earn_df['pred_week'].astype(str)
        real_earn_df.drop(columns=['pred_year','pred_week','pred_earnings','pred_earnings_pct','real_earnings_pct'], inplace=True)
        
        
        pred_earn_df = pd.DataFrame(columns=earnings_df['columns'], data=earnings_df['data'])
        pred_earn_df['Year-Week'] = pred_earn_df['pred_year'].astype(str) + '--' + pred_earn_df['pred_week'].astype(str)
        pred_earn_df.drop(columns=['pred_year','pred_week','real_earnings','pred_earnings_pct','real_earnings_pct'], inplace=True)
        
        pred_total_earnings = historic['pred_total_earnings']
        real_total_earnings = historic['real_total_earnings']
        pred_roi = historic['pred_roi']
        real_roi = historic['real_roi']
        
        fig_real = px.bar(
            real_earn_df,
            x='Year-Week',
            y='real_earnings',
            title='Real Earnings',
            color_discrete_sequence=["#9EE6CF"]
        )
        
        fig_pred = px.bar(
            pred_earn_df,
            x='Year-Week',
            y='pred_earnings',
            title='Prediction Earnings',
            color_discrete_sequence=["#9EE6CF"]
        )
        
        col1_s,col1, col2, col2_s = st.columns((.1,1,1,.1))
        with col1:
            st.metric(label='Total prediction earnings', value=str(int(pred_total_earnings))+"$", delta=str(float(pred_roi))+' ROI')
            st.plotly_chart(fig_pred, theme="streamlit", use_container_width=True)
        with col2:
            st.metric(label='Total real earnings', value=str(int(real_total_earnings))+"$", delta=str(float(real_roi))+' ROI')
            st.plotly_chart(fig_real, theme="streamlit", use_container_width=True)
        
    
    # fgdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'Graph')
    
    # fgdf = fgdf[fgdf['Hospital Attended']==hosp] 
    
    # fig = px.bar(fgdf, x = 'Earnings', y='Earnings', template = 'seaborn')
    
    # fig.update_traces(marker_color='#264653')
    
    # fig.update_layout(title_text="Number of Completed Handovers by Hour",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    # g1.plotly_chart(fig, use_container_width=True) 

if __name__ == '__main__':
	main()