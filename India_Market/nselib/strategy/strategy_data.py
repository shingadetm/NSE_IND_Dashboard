from nselib.libutil import NSEdataNotFound,nse_urlfetch
import pandas as pd
from datetime import datetime as dt



def oi_spurts():
    origin_url = 'https://www.nseindia.com/market-data/oi-spurts'
    url = 'https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings'
    data_obj = nse_urlfetch(url,origin_url= origin_url)
    if data_obj.status_code != 200:
        print(data_obj.status_code)
        raise NSEdataNotFound(f" {data_obj.status_code} Resource not available for oi_spurts")
    data_dict = data_obj.json()
    data_df = pd.DataFrame(data_dict['data'])
    return data_df

def derivative_fno():
    origin_url = 'https://www.nseindia.com/market-data/equity-derivatives-watch'
    url = 'https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O'
    data_obj = nse_urlfetch(url,origin_url=origin_url)
    if data_obj.status_code != 200:
        print(data_obj.status_code)
        raise NSEdataNotFound(f" {data_obj.status_code} Resource not available for derivative_fno")
    data_dict = data_obj.json()
    data_df = pd.DataFrame(data_dict['data'])[['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice', 
                                                 'previousClose', 'change', 'pChange']]
    data_df['Date'] = dt.strptime(data_dict['timestamp'],'%d-%b-%Y %H:%M:%S').strftime('%a %d-%b-%Y %I:%M:%S %p')
    dict = data_dict['advance']
    df_dict = {key: pd.Series(value) for key, value in dict.items()}
    no_of_stock_count = pd.DataFrame(df_dict)

    dict = data_dict['marketStatus']
    df_dict = {key: pd.Series(value) for key, value in dict.items()}
    nifty50 = pd.DataFrame(df_dict)
    nifty50 = nifty50[[ 'tradeDate', 'index', 'last', 'variation', 'percentChange', 'marketStatusMessage']]


    # marketStatus_df = pd.DataFrame(data_dict['marketStatus'])
    return data_df, no_of_stock_count, nifty50
