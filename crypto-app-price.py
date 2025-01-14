import streamlit as st
from PIL import Image
import pandas as pd
import base64
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# CoinMarketCap API URL
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Title
image = Image.open('logo.jpg')
st.image(image, width=500)
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrencies from **CoinMarketCap**!
""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")

#---------------------------------#
# Page layout (continued)
## Divide page into 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

#---------------------------------# 

# Sidebar - API Key input
col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

## Sidebar - User API Key
user_api_key = col1.text_input("Enter your CoinMarketCap API Key", type="password")

# Web API call to CoinMarketCap
def load_data(api_key):
    if not api_key:
        st.error("Please provide your CoinMarketCap API key.")
        return pd.DataFrame()

    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accept': 'application/json',
    }
    params = {
        'start': '1',
        'limit': '100',  # Top 100 cryptocurrencies
        'convert': currency_price_unit,
    }
    response = requests.get(API_URL, headers=headers, params=params)

    # Check if the response is successful
    if response.status_code != 200:
        st.error("Failed to fetch data. Please check your API key and try again.")
        return pd.DataFrame()

    data = response.json()

    # Extract relevant data
    coins = []
    for coin in data['data']:
        coins.append({
            'coin_name': coin['name'],
            'coin_symbol': coin['symbol'],
            'price': coin['quote'][currency_price_unit]['price'],
            'percent_change_1h': coin['quote'][currency_price_unit]['percent_change_1h'],
            'percent_change_24h': coin['quote'][currency_price_unit]['percent_change_24h'],
            'percent_change_7d': coin['quote'][currency_price_unit]['percent_change_7d'],
            'market_cap': coin['quote'][currency_price_unit]['market_cap'],
            'volume_24h': coin['quote'][currency_price_unit]['volume_24h'],
            'circulating_supply': coin['circulating_supply'],
            'total_supply': coin['total_supply'],
            'max_supply': coin.get('max_supply', 'N/A'),  # Some coins don't have max_supply
            'last_updated': coin['last_updated']
        })

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(coins)
    return df

# Function to get historical data for the 7 days change (Simulated data)
def get_historical_data(symbol):
    # Here we simulate historical data for 7 days as CoinMarketCap doesn't provide historical price directly
    # In real-world use, you would fetch data from an endpoint that provides historical data for that coin
    historical_prices = np.random.randn(7)  # Simulated random data for the example
    return historical_prices

# Function to get historical 24h volume data for the selected coin
def get_historical_24h_volume(symbol, api_key):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical?symbol={symbol}&time_start=2024-01-07&time_end=2024-01-14'
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Extract the 24-hour volume data from the response
    if 'data' in data and symbol in data['data']:
        volumes = [item['quote'][currency_price_unit]['volume_24h'] for item in data['data'][symbol]['quotes']]
        return volumes
    else:
        return None

# Only load data if the user provides a valid API key
if user_api_key:
    API_KEY = user_api_key
    df = load_data(API_KEY)

    # Sidebar - Cryptocurrency selections
    sorted_coin = sorted(df['coin_symbol'])
    selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

    df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]  # Filtering data

    ## Sidebar - Number of coins to display
    num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
    df_coins = df_selected_coin[:num_coin]

    ## Sidebar - Percent change timeframe
    percent_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
    percent_dict = {"7d": 'percent_change_7d', "24h": 'percent_change_24h', "1h": 'percent_change_1h'}
    selected_percent_timeframe = percent_dict[percent_timeframe]

    ## Sidebar - Sorting values
    sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

    col2.subheader('Price Data of Selected Cryptocurrency')
    col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

    col2.dataframe(df_coins)

    # Download CSV data
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
        return href

    col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

    #---------------------------------#
    # Preparing data for Bar plot of % Price change
    col2.subheader('Table of % Price Change')
    df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
    df_change = df_change.set_index('coin_symbol')
    df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
    df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
    df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
    col2.dataframe(df_change)

    # Conditional creation of Bar plot (time frame)
    col3.subheader('Bar plot of % Price Change')

    if percent_timeframe == '7d':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_7d'])
        col3.write('*7 days period*')
        plt.figure(figsize=(5, 25))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    elif percent_timeframe == '24h':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_24h'])
        col3.write('*24 hour period*')
        plt.figure(figsize=(5, 25))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_1h'])
        col3.write('*1 hour period*')
        plt.figure(figsize=(5, 25))
        plt.subplots_adjust(top=1, bottom=0)
        df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)

    #---------------------------------#
    # Display Detailed Info of a Specific Coin
    def get_coin_details(symbol, api_key):
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={symbol}'
        headers = {
            'X-CMC_PRO_API_KEY': api_key,
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data

    # Sidebar to select a coin for detailed info (only after API key is provided)
    if user_api_key:
        selected_coin_for_details = col1.selectbox('Select a coin for detailed info', df['coin_symbol'])

        # Only proceed if a coin is selected
        if selected_coin_for_details:
            # Fetch and display details if a coin is selected
            coin_details = get_coin_details(selected_coin_for_details, API_KEY)
            coin_data = coin_details.get('data', {}).get(selected_coin_for_details, {})

            st.write(f"**{coin_data.get('name', 'No name available')}**")

            # Display description if available
            description = coin_data.get('description', 'No description available')
            st.write(f"Description: {description}")

            # Display logo if available
            logo_url = coin_data.get('logo', None)
            if logo_url:
                st.image(logo_url, width=100)
            else:
                st.write("No logo available.")

            # Display website URL if available
            website = coin_data.get('urls', {}).get('website', [])
            if website:
                st.markdown(f"Website: [Visit Website]({website[0]})")
            else:
                st.write("No website available.")

            # Fetch and display 7-day data (historical data)
            historical_data = get_historical_data(selected_coin_for_details)

            if historical_data is not None:
                # Create a line graph for 7-day price change using Plotly
                x = np.arange(1, 8)  # 7 days range
                fig = go.Figure(data=go.Scatter(x=x, y=historical_data, mode='lines+markers', name=selected_coin_for_details))
                fig.update_layout(title=f'{selected_coin_for_details} - 7-Day Percentage Change',
                                  xaxis_title='Days',
                                  yaxis_title='Price Change (%)')
                st.plotly_chart(fig)
            else:
                st.write("No data available for the selected coin.")

            # Fetch and display 24h volume data
            historical_volume = get_historical_24h_volume(selected_coin_for_details, API_KEY)

            if historical_volume is not None:
                # Create a line graph for 24h volume using Plotly
                x = np.arange(1, 8)  # 7 days range for the volume plot
                fig_volume = go.Figure(data=go.Scatter(x=x, y=historical_volume, mode='lines+markers', name=f'{selected_coin_for_details} - Volume (24h)'))
                fig_volume.update_layout(title=f'{selected_coin_for_details} - 24h Volume',
                                         xaxis_title='Days',
                                         yaxis_title='Volume')
                st.plotly_chart(fig_volume)
            else:
                st.write("No data available for the selected coin.")