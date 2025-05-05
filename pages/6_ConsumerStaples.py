import fitz
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from bert import generate_gradients, analyze_document_sentiment
from datetime import datetime

# Define stocks to track
STOCKS = ['PG', 'KO', 'PEP', 'WMT', 'COST', 'PM', 'CL', 'MDLZ']
NAMES =  ['Procter & Gamble Co.', 'Coca-Cola Co.', 'PepsiCo, Inc.', 'Walmart Inc.', 'Costco Wholesale Corp.', 'Philip Morris International Inc.', 'Colgate-Palmolive Co.', 'Mondelez International, Inc.']

# Set up Streamlit page
st.set_page_config(page_title='Consumer Staples Stocks', layout='wide')
st.header('Energy Stocks Dashboard')
st.subheader('Live Stock Data for Energy Stocks')
st.markdown('---')

# Display data
row1col1, row1col2 = st.columns([2, 1])

with row1col1:
    st.markdown("### Current Stock Prices")
    
    # Prepare data for display
    display_data = []
    for stock, name in zip(STOCKS, NAMES):
        data = st.session_state.get(stock, {})
        rows = {'Name': name, 'Stocks': stock}
        
        # Add data if available
        if 'price' in data:
            rows['Price'] = f'${data['price']}'
        else:
            rows['Price'] = '-'
        if 'volume' in data:
            rows['Volume'] = f'{data['volume']}'
        else:
            rows['Volume'] = '-'
            
        # Status indicator
        if data:
            rows['status'] = '✅ Live'
        else:
            rows['status'] = '⏳ Waiting'
        display_data.append(rows)
        
    # Display as a dataframe
    if display_data:
        stocks_df = pd.DataFrame(display_data)
        stocks_df.index = np.arange(1, len(stocks_df)+1)
        st.dataframe(stocks_df, use_container_width=True)
    else:
        st.info('Waiting for data')

with row1col2:
    st.markdown("#### Market Details")
    selected_stock = st.selectbox("Select Stock for Details", STOCKS)
    data = st.session_state.get(selected_stock, {})
    st.markdown('---')
    if True:
        st.markdown('#### Stock Details')
        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            st.markdown('###### Current Price')
            if 'price' in data:
                st.write(data['price'])
            else:
                st.write('--')
        with cols2:
            st.markdown('###### High')
            if 'high' in data:
                st.write(data['high'])
            else:
                st.write('--')
        with cols3:
            st.markdown('###### Open')
            if 'open' in data:
                st.write(data['open'])
            else:
                st.write('--')
            
        cols4, cols5, cols6 = st.columns(3)
        with cols4:
            st.markdown('###### Volume')
            if 'volume' in data:
                st.write(data['volume'])
            else:
                st.write('--')
        with cols5:
            st.markdown('###### Day Low')
            if 'low' in data:
                st.write(data['low'])
            else:
                st.write('--')
        with cols6:
            st.markdown('###### Previous Close')
            st.write('--')
    else:
        st.info(f"Waiting for data for {selected_stock}...")

st.markdown('---')

# Second row
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('#### BERT Financial Sentiment Score')

    # Build the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=100,
        title={'text': 'BERT Score'},
        gauge={
            'axis': {'range': [-100, 100]},
            'steps': generate_gradients()
        }
    ))
    
    st.plotly_chart(fig)
   
with row2_col2:
    st.markdown('#### Analyze the sentiment of Financial Document')
    file = st.file_uploader('Upload Text of PDF File', type=['txt', 'pdf'])
    contents = ''
    if file is not None:
        if file.name.endswith('txt'):
            contents = file.read().decode('utf-8')
        elif file.name.endswith('pdf'):
            bytes = file.read()
            doc = fitz.open(stream=bytes, filetype='pdf')
            contents = ''
            for page in doc:
                text = page.get_text()
                contents += text
            doc.close()
    result = analyze_document_sentiment(contents)
    label = result[0]['label']
    score = result[0]['score']
    st.markdown('#### Sentiment of the Document')
    st.write('Tone: ', str.capitalize(label))
    st.write(f'Confidence:  {round(score, 2)*100}%')

st.markdown('---')
st.caption('Data provided by Alpaca Markets API. Dashboard refreshes every second.')
st.caption(f"Page last refreshed: {datetime.now().strftime('%H:%M:%S')}")