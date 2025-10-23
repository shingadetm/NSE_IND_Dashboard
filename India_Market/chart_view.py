import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def chart_view(data,line_chart_flag,crosshair_flag):

    # Your rename map
    rename_map = {
        "TRADE_LOW_PRICE": "Low",
        "TRADE_HIGH_PRICE": "High",
        # "open": "Open",
        "OPENING_PRICE": "Open",
        # "close": "Close",
        "CLOSING_PRICE": "Close",
        "TIMESTAMP": "Date",
    }

    # Build a new mapping based on partial, case-insensitive match
    new_columns = {}
    for col in data.columns:
        for key, new_name in rename_map.items():
            if key.lower() in col.lower():
                new_columns[col] = new_name
                break  # Stop at first match

    # Apply renaming
    data = data.rename(columns=new_columns)

    try:
        print(type( data['Date']))
        data['Date'] = pd.to_datetime(data['Date'])
        data.index = pd.to_datetime(data['Date'])
        data.drop(columns='Date', inplace=True)
        data = data.sort_values(by=['Date'],ascending=True)
        
    except:
        data.index = data['Date']
        data.drop(columns='Date', inplace=True)
        # data.index = data.reset_index(drop=True)

    
    
    
    price_cols = [col for col in data.columns if col.endswith("Price")]
    # Remove commas and convert to float for all price columns
    try:
        data[price_cols] = data[price_cols].apply(lambda col: pd.to_numeric(col.str.replace(",", ""), errors="coerce"))        
    except:
        pass
    # Remove 'Price' from all column names
    data.columns = data.columns.str.replace("Price", "", regex=False)


    data['50sma'] = data['Close'].rolling(window=50).mean()
    data['200sma'] = data['Close'].rolling(window=200).mean()

    
    fig = go.Figure(data=[
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
        ),
    go.Scatter(
            x=data.index,
            y=data['50sma'],
            mode='lines',
            line=dict(color='blue', width=1),
            name='50 SMA'
        ),
    go.Scatter(
            x=data.index,
            y=data['200sma'],
            mode='lines',
            line=dict(color='red', width=1),
            name='200 SMA'
        )

    ])

    if line_chart_flag:
        fig = go.Figure(data=[
            go.Scatter(
                x=data.index,       # or data["Date"] if you have a date column
                y=data["Close"],
                mode='lines',
                name='Close Price'
            )
        ])

    fig.update_xaxes(
        autorange=True,
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(count = 1, label = "1m", step = "month", stepmode = "backward"),
                dict(count = 6, label = "6m", step = "month", stepmode = "backward"),
                dict(count = 1, label = "YTD", step = "year", stepmode = "todate"),
                dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
                dict(step = "all")
            ])
        )
    )

    # Set figure size
    fig.update_layout(
        dragmode='zoom',
        xaxis=dict(fixedrange=False),
        xaxis_rangeslider_visible=False,
        yaxis=dict(fixedrange=False),
        width=1400,   # Width in pixels
        height=700    # Height in pixels
    )
    fig.update_yaxes(
        autorange=True,
        tickformat=',',  # Adds comma separators (e.g., 25000 → 25,000)
    )

    if crosshair_flag:
        fig.update_layout(
            # hovermode='x unified',  # or 'closest' for full XY tracking
            xaxis=dict(
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikedash='dot',
                spikecolor='grey',
                spikethickness=1
            ),
            yaxis=dict(
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikedash='dot',
                spikecolor='grey',
                spikethickness=1
            ),
        #     hoverlabel=dict(
        #     bgcolor="white",
        #     font_size=12,
        #     font_family="Arial"
        # )
        )


    # st.plotly_chart(fig)
    st.plotly_chart(fig, use_container_width=False, config={
        "scrollZoom": True,       # Enables scroll-to-zoom
        "doubleClick": "reset",   # Double-click resets zoom
        "displayModeBar": True    # Shows toolbar for zoom/pan/save
    })
