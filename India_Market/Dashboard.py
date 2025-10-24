from nselib import capital_market, derivatives
import nselib.capital_market.capital_market_data  as capital_market_data
from nselib.libutil import trading_holiday_calendar,NSEdataNotFound
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
from datetime import datetime,date,timedelta
from chart_view import chart_view
import plotly.graph_objects as go
from nselib.strategy import strategy_data
from nselib.libutil import *






def set_start_end_date():
    select_start_date = st.sidebar.date_input('Start Date',value=date.today()-timedelta(days=30) ,max_value=date.today())
    select_start_date = datetime.strptime(str(select_start_date), "%Y-%m-%d").strftime("%d-%m-%Y")

    select_end_date = st.sidebar.date_input('End Date',value=date.today(),max_value=date.today())
    select_end_date = datetime.strptime(str(select_end_date), "%Y-%m-%d").strftime("%d-%m-%Y")
    return select_start_date, select_end_date

def html_table(data,index = True):
    styled_table = data.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}]
    ) # .hide(axis='index')  # hides the index column 
    if index==False:
        styled_table = styled_table.hide(axis='index')  
    return styled_table

def highlight_return(val):
    val = float(val.strip('%'))/100
    if isinstance(val, (int, float)):
        # Normalize intensity (adjust 0.2 to match your data range)
        intensity = min(abs(val) / 0.2, 1)
        if val > 0:
            # Green gradient: light to dark
            r = int(255 * (1 - intensity))
            g = 255
            b = int(255 * (1 - intensity))
        elif val < 0:
            # Red gradient: light to dark
            r = 255
            g = int(255 * (1 - intensity))
            b = int(255 * (1 - intensity))
        else:
            r, g, b = 255, 255, 255  # neutral
        return f'background-color: rgb({r}, {g}, {b})'
    return ''

# try:
symbol_eq = capital_market.fno_equity_list()
symbol_idx = capital_market.fno_index_list()
# holiday = trading_holiday_calendar()
# holiday['tradingDate'] = pd.to_datetime(holiday['tradingDate'], format="%d-%b-%Y").dt.date

#TODO Implement Holiday check
# st.write(holiday)


st.set_page_config(page_title="StockView360", layout="wide")
# Custom CSS to freeze header
st.markdown("""
    <style>
        .sticky-header {
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            background-color: white;
            padding: 10px 0;
            z-index: 999;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Apply sticky class to your header
st.markdown("<div class='sticky-header'><h1 style='margin:0;'>🔍 StockView360 🌐</h1></div>", unsafe_allow_html=True)



pg_title = 'StockView360 Financial Dashboard'
# st.write('-- Financial Dashboard by Tushar Shingade, Sr. Quant Research Analyst ')
st.markdown("<p style='text-align: right;'>-- by Tushar Shingade, Sr.Quant Researcher  </p>", unsafe_allow_html=True)
# st.markdown(
#     f"<h2 style='text-align: left; color: #001EA1; font-size:28px;'>{pg_title}</h2>",
#     unsafe_allow_html=True)

# st.header('#Indian Stock Financial Dashboard')
instrument = st.sidebar.selectbox('Instrument Type', options=('NSE Equity Market','NSE Derivative Market','Intra-Day Alert'))


if instrument == 'NSE Equity Market':
    data_info = st.sidebar.selectbox('Data to extract', 
    options= (
'bhav_copy_equities', 
# 'bhav_copy_sme', 
'bhav_copy_with_delivery', 
'block_deals_data', 
'bulk_deal_data', 
# 'corporate_actions_for_equity', 
# 'corporate_bond_trade_report', 
# 'deliverable_position_data', 
'equity_list', 
# 'event_calendar_for_equity', 
'fii_dii_trading_activity', 
'financial_results_for_equity', 
'fno_equity_list', 
'fno_index_list', 
# 'index_data', 
# 'india_vix_data', 
'market_watch_all_indices', 
'nifty50_equity_list', 
'pe_ratio', 
'price_volume_and_deliverable_position_data', 
'price_volume_data', 
'short_selling_data', 
'sme_band_complete', 
'sme_bhav_copy', 
'var_1st_intra_day', 
'var_2nd_intra_day', 
'var_3rd_intra_day', 
'var_4th_intra_day', 
'var_begin_day', 
'var_end_of_day', 
'week_52_high_low_report'
    ) )

    if data_info in ['equity_list',
                    'fno_equity_list',
                    'fno_index_list',
                    'market_watch_all_indices',
                    'nifty50_equity_list',
                    'fii_dii_trading_activity',                     
                    ]:
        
        data = getattr(capital_market_data,data_info)()


    if data_info in ['bhav_copy_with_delivery', 
                    'bhav_copy_equities',
                    'bhav_copy_sme',
                    'pe_ratio',
                    'corporate_bond_trade_report',
                    'sme_band_complete',
                    'sme_bhav_copy',
                    'var_1st_intra_day',
                    'var_2nd_intra_day', 
                    'var_3rd_intra_day', 
                    'var_4th_intra_day',
                    'var_begin_day',
                    'var_end_of_day',
                    'week_52_high_low_report'
                        ]:
        # date = st.sidebar.text_input('Date','21-10-2025')
        select_date = st.sidebar.date_input('Date',value=date.today(),max_value=date.today())
        select_date = datetime.strptime(str(select_date), "%Y-%m-%d").strftime("%d-%m-%Y")        
        data = getattr(capital_market_data,data_info)(select_date)

    if data_info in ['bulk_deal_data', 
                    'block_deals_data',
                    'india_vix_data',
                    'short_selling_data',
                    'financial_results_for_equity',
                    
                    ]:
        period_ = st.sidebar.text_input('Period','1M') #TODO  Add select box 1m,3m,6m,1y
        data = getattr(capital_market_data,data_info)(period = period_)
    
    if data_info in [
                    'price_volume_data'
                    ]:
        
        symbol = st.sidebar.selectbox('Index',symbol_eq['symbol'])
        select_start_date,select_end_date = set_start_end_date()
        data = getattr(capital_market_data,data_info)(symbol = symbol,
                                                    from_date = select_start_date,
                                                    to_date = select_end_date)
        # period_ = st.sidebar.text_input('Period','1M') #TODO  Add select box 1m,3m,6m,1y
        # data = getattr(capital_market_data,data_info)(symbol = symbol,period = period_)              

    if data_info in [
                    'price_volume_and_deliverable_position_data'
                    ]:
        
        symbol = st.sidebar.selectbox('Stock',symbol_eq['symbol'])
        select_start_date,select_end_date = set_start_end_date()
        data = getattr(capital_market_data,data_info)(symbol = symbol,
                                                    from_date = select_start_date,
                                                    to_date = select_end_date)







if instrument == 'NSE Derivative Market':
    expiry_dt_fut = derivatives.expiry_dates_future()
    expiry_dt_opt_idx = derivatives.expiry_dates_option_index()
    # st.write(expiry_dt_opt_idx)
    


    data_info = st.sidebar.selectbox('Data to extract', 
    options= (
        'expiry_dates_future', 
        'expiry_dates_option_index', 
        'fii_derivatives_statistics', 
        'fno_bhav_copy', 
        'fno_security_in_ban_period', 
        'future_price_volume_data', 
        'nse_live_option_chain', 
        'option_price_volume_data', 
        'participant_wise_open_interest', 
        'participant_wise_trading_volume'))
    
    if data_info in ['expiry_dates_future',
                    'expiry_dates_option_index']:
        data = getattr(derivatives,data_info)() #TODO add the index/put it in nice way

    if data_info in['fno_bhav_copy',
                    'fii_derivatives_statistics', 
                    'participant_wise_trading_volume', 
                    'participant_wise_open_interest',
                    'fno_security_in_ban_period']:
        

        select_date = st.sidebar.date_input('Date',value=date.today(),max_value=date.today())
        select_date = datetime.strptime(str(select_date), "%Y-%m-%d").strftime("%d-%m-%Y")
        
        data = getattr(derivatives,data_info)(select_date)
    
    if data_info in ['future_price_volume_data' ]: #TODO as per the instument, give expiry date
        
        choice = st.sidebar.radio('Instrument Type', ['Stock', 'Index'])
        type_ = 'FUTSTK' if choice == 'Stock' else  'FUTIDX'
        if choice=='Stock':
            symbol = st.sidebar.selectbox('Ticker',symbol_eq['symbol'])
        else:
            symbol = st.sidebar.selectbox('Ticker',symbol_idx['symbol'])

        select_start_date,select_end_date = set_start_end_date()
        # period_ = st.sidebar.text_input('Period','1M') #TODO Add select box 1m,3m,6m,1y
        data = getattr(derivatives,data_info)(symbol, type_,
                                            from_date = select_start_date,
                                            to_date = select_end_date,
                                            )
    
    if data_info in ['option_price_volume_data']: #TODO as per the instument, give expiry date
        choice = st.sidebar.radio('Instrument Type', ['Stock', 'Index'])
        type_ = 'OPTSTK' if choice == 'Stock' else  'OPTIDX'
        if choice=='Stock':
            symbol = st.sidebar.selectbox('Ticker',symbol_eq['symbol'])
        else:
            symbol = st.sidebar.selectbox('Ticker',symbol_idx['symbol'])
        
        
        select_start_date,select_end_date = set_start_end_date()
        ce_pe = st.sidebar.selectbox('Option Type (CE/PE)', ('CE','PE'))
        
        # period_ = st.sidebar.selectbox('Period',['1W','1M']) #TODO Add select box 1m,3m,6m,1y
        # data = getattr(derivatives,data_info)(symbol, type_,period = period_)
        data = getattr(derivatives,data_info)(symbol, type_,from_date = select_start_date,
                                            to_date = select_end_date,
                                            option_type = ce_pe)


    if data_info in ['nse_live_option_chain']: #TODO Give option to select active expiry dates
        combined_df = pd.concat([symbol_idx[['symbol']],symbol_eq[['symbol']]], ignore_index=True)
        symbol = st.sidebar.selectbox('Ticker',combined_df['symbol'])
        try:
            expiry_date = expiry_dt_opt_idx[symbol]
        except:
            expiry_date = expiry_dt_fut
        
        expiry_date = [datetime.strptime(d, "%d-%b-%Y").strftime("%d-%m-%Y") for d in expiry_date]
    
        expiry_date = st.sidebar.selectbox('Expiry date',expiry_date)
        data = getattr(derivatives,data_info)(symbol, expiry_date = expiry_date)
        



if instrument == 'Intra-Day Alert':
    data_info = 'Stock_Filtering'
    formatted_title = data_info.replace("_", " ").upper()
    st.markdown(f"<h2 style='text-align: left; color: #ff4040; font-size:20px;'>{formatted_title}</h2>",unsafe_allow_html=True)

    data_derivative_fno, no_of_stock_count, nifty50 = strategy_data.derivative_fno()
    st.write(no_of_stock_count)
    # st.markdown("---")  # Creates a horizontal line
    st.write(nifty50)

    st.markdown("---")  # Creates a horizontal line
    data_oi_spurts = strategy_data.oi_spurts()
    
    stock_selection = pd.merge(data_oi_spurts, data_derivative_fno, on='symbol', how='left')
    stock_selection.rename(columns={'pChange': '%PriceChange',
                                        'open':'dayOpen',
                                        'avgInOI':'avgOIChange',
                                        'lastPrice':'dayLastPrice'}, inplace=True)
    
    cols = ['Date','symbol', 'avgOIChange', '%PriceChange', 'previousClose', 'dayOpen', 'dayHigh', 'dayLow', 'dayLastPrice']
    data = stock_selection[cols]
    data['abs_avgOIChange'] = abs(data['avgOIChange'])
    data['abs_Price_change'] = abs(data['%PriceChange'])

    signal = st.toggle('Filter Most Active Stocks')
    show_shart= 0
    if signal:
        col1,col2,_ = st.columns([1,1,2])
        with col1:
            price_change = st.number_input('% Price Change', 0)
        with col2:
            oi_change = st.number_input('OI Spurts Change', 0)
        data = data.loc[((data['abs_avgOIChange'] >= oi_change) & (data['abs_Price_change'] >= price_change)),:]
    
    data_style = html_table(data.round(3).astype(str),index = True)
    data_style = data_style.applymap(highlight_return, subset=['%PriceChange','avgOIChange'])
    try:       
        st.write(data_style)
    except:
        st.write(data)
    
else:    
    formatted_title = data_info.replace("_", " ").upper()
    st.markdown(f"<h2 style='text-align: left; color: #ff4040; font-size:20px;'>{formatted_title}</h2>",unsafe_allow_html=True)
    show_shart = st.toggle('Show Chart')
    data_org = data



    try:
        data = dataframe_explorer(data)
        st.dataframe(data)
    except:
        st.write(data)





try:    
    st.write(f'Total Rows: {data.shape[0]} ;   Columns: {data.shape[1]}')
    st.download_button("Download CSV", data.to_csv(index=False), file_name=f"{data_info}_"+ str(datetime.today())+".csv")    
    price_cols = [col for col in data.columns if col.endswith("Price")]

    if show_shart or data_info in ['price_volume_data',
                     'price_volume_and_deliverable_position_data']:

        col1,col2 = st.columns([1,1])
        with col1:
            line_chart_flag = st.toggle("Show Line chart") # Horizontal layout for toggle + download
        with col2:
            crosshair_flag = st.toggle("Crosshair") # Horizontal layout for toggle + download
        chart_view(data,line_chart_flag,crosshair_flag)

except Exception as e:
    st.write(e)


# except:
#     st.write('⚠️ No data available for the selected period or dates. Try modifying the period or date range to continue. Some features are still under active development!')


