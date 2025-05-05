import os
import json
import websocket
import threading
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
API_SECRET = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = "wss://stream.data.alpaca.markets/v2/iex"

TECHS = ['AAPL', 'MSFT', 'GOOG', 'META', 'NVIDIA', 'TSM', 'AVGO', 'CRM']
HEALTH = ['LLY', 'UNH', 'JNJ', 'ABBV', 'NVO', 'MRK', 'ABT']
UTILITIES = ['NEE', 'DUK', 'SO', 'XEL', 'AEP', 'CEG', 'SRE']
FINANCE = ['JPM', 'GS', 'BRK.B', 'BAC', 'MS', 'WFC', 'C']
ENERGY = ['XOM', 'CVX', 'COP', 'NEE', 'EOG', 'SLB', 'KMI']
STAPLES = ['PG', 'KO', 'PEP', 'WMT', 'COST', 'PM', 'CL', 'MDLZ']

STOCKS = [TECHS ,HEALTH, UTILITIES, FINANCE, ENERGY, STAPLES]
FLAT_STOCKS = sum(STOCKS, [])
# STOCKS = ['AAPL', 'MSFT', 'GOOG', 'META', 'NVIDIA', 'TSM', 'AVGO', 'CRM',
#             'LLY', 'UNH', 'JNJ', 'ABBV', 'NVO', 'MRK', 'ABT',
#             'NEE', 'DUK', 'SO', 'XEL', 'AEP', 'CEG', 'SRE',
#             'JPM', 'GS', 'BRK.B', 'BAC', 'MS', 'WFC', 'C',
#             'XOM', 'CVX', 'COP', 'NEE', 'EOG', 'SLB', 'KMI',
#             'PG', 'KO', 'PEP', 'WMT', 'COST', 'PM', 'CL', 'MDLZ']

st.set_page_config(page_title='Financial Sentiment Analysis', layout='wide')


st.header('Main Dashboard for Financial Sentiment')
st.subheader('Discuss & Analyze the sentiment of different Stock sectors')
st.write("""
Welcome to the Stock Insights Dashboard!  
Explore real-time charts, sentiment analysis, and key metrics for various stock sectors.  
Use the sidebar to dive into specific categories.
""")

st.markdown('---')
col1, col2, col3 = st.columns(3)
col1.metric(" Total Sectors", 6)
col2.metric(" Tracked Stocks", 44)
col3.metric(" Top Gainer", f"Tesla 20 %")


st.subheader("Market Sentiment Overview")
st.progress(77)

news = [
    {
        "title": "Apple shares surge after earnings beat expectations",
        "url": "https://example.com/apple-earnings"
    },
    {
        "title": "Tesla stock dips as production slows in China",
        "url": "https://example.com/tesla-production"
    },
    {
        "title": "Microsoft invests in AI chipmaker, fueling market optimism",
        "url": "https://example.com/microsoft-ai"
    },
]

st.markdown("---")


# Sentiment Indicator Gauge
st.subheader(" Market Sentiment Gauge")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=90,
    gauge={"axis": {"range": [0, 100]},
           "bar": {"color": "green" if 90 > 0.5 else "red"},
           "steps": [
               {"range": [0, 50], "color": "lightcoral"},
               {"range": [50, 100], "color": "lightgreen"}]},
    domain={"x": [0, 1], "y": [0, 1]},
    title={"text": "Bullish Sentiment (%)"}))
st.plotly_chart(fig_gauge, use_container_width=True)


# Search Bar and Redirect to the page of stocks
st.markdown("###  Quick Stock Search")
search_query = st.text_input("Enter a stock ticker or name", placeholder="e.g., AAPL, MSFT").strip().upper()

if search_query in TECHS:
    st.switch_page('pages/1_Technology.py')
elif search_query in HEALTH:
    st.switch_page('pages/2_Healthcare.py')
elif search_query in UTILITIES:
    st.switch_page('pages/3_Utilities.py')
elif search_query in FINANCE:
    st.switch_page('pages/4_Finance.py')
elif search_query in ENERGY:
    st.switch_page('pages/5_Energy.py')
elif search_query in STAPLES:
    st.switch_page('pages/6_ConsumerStaples.py')
else:
    st.error('Given Stock is not tracked under current Dashboard')

    
    
st.subheader(" Latest Market News")
for article in news[:5]:
    st.markdown(f"- [{article['title']}]({article['url']})")


st.info("""
 **How to use the Dashboard:**
- Use the sidebar to pick a sector.
- Select a stock to view its performance.
- Charts and sentiment analysis are available for each stock.
""")


def on_open(ws):
    auth = {
        'action': 'auth',
        'key': API_KEY, 
        'secret': API_SECRET
    }
    ws.send(json.dumps(auth))
    print('Auth sent')
    
    sub_message = {
        'action': 'subscribe',
        'trades': FLAT_STOCKS[:3],
        'bars': FLAT_STOCKS[:3]
    }
    ws.send(json.dumps(sub_message))
    print('Sent Subscription for: ', FLAT_STOCKS[:3])
    return on_open
    
def on_message(ws, msg):
    data = json.loads(msg)
    for entry in data:
        print(entry)
        event_type = entry.get('T')
        
        if event_type == 't':
            ticker = entry.get('S')
            price = entry.get('p')
            if ticker and price is not None:
                st.session_state[ticker] = {'price': f'${price}'}
                print('Price in st.session_state')
        elif event_type == 'o':
            ticker = entry.get('S')
            open_price = entry.get('o')
            if ticker and open_price is not None:
                if ticker not in st.session_state:
                    st.session_state[ticker] = {}
                st.session_state[ticker]['open'] = f'${open_price}'
                print('Open Price logged in')
                
        elif event_type == 'h':
            ticker = entry.get('S')
            high_price = entry.get('h')
            if ticker and high_price is not None:
                if ticker not in st.session_state:
                    st.session_state[ticker] = {}
                st.session_state[ticker]['high'] = f'${high_price}'
                
        elif event_type == 'l':
            ticker = entry.get('S')
            low_price = entry.get('l')
            if ticker and low_price is not None:
                if ticker not in st.session_state:
                    st.session_state[ticker] = {}    
                st.session_state[ticker]['low'] = f'${low_price}'
                print('Low Price logged in')
                
        elif event_type == 'c':
            ticker = entry.get('S')
            close_price = entry.get('c')
            if ticker and close_price is not None:
                if ticker not in st.session_state:
                    st.session_state[ticker] = {}
                st.session_state[ticker]['close'] = f'${close_price}'
                
        elif event_type == 'v': # Volume event
            ticker = entry.get('S')
            volume = entry.get('v')
            if ticker and volume is not None:
                if ticker not in st.session_state:
                    st.session_state[ticker]  = {}
                st.session_state[ticker]['volume'] = f'{volume}'
                 
def on_error(ws, error):
    print('Websocket Error', error)

def on_close(ws, clost_status_code, close_msg):
    print('Websocket connection: ', clost_status_code, close_msg)
    
def websocket_thread():
    ws = websocket.WebSocket(
        BASE_URL,
        on_open = on_open,
        on_message=on_message,
        on_error=on_error, 
        on_close = on_close
    )
    ws.run_forever()

if 'ws_started' not in st.session_state:
    #for stocks_list in STOCKS:
    threading.Thread(target=websocket_thread, daemon=True).start()
    #time.sleep(1)   # Slight delay to avoid rate limit
    st.session_state.ws_started = True
