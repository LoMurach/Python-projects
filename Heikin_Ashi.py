import pandas as pd
import pandas.io as web
import numpy as np

def HA(df):
    df["HA_Close"] = (df["Open"] + df["High"] + df["Low"] + df["Close"])/4
    ha_o = df["Open"] + df["Close"]
    df["HA_Open"] = 0.0
    HA_O = df["HA_Open"].shift(1) + df["HA_Close"].shift(1)
    df["HA_Open"] = np.where(df["HA_Open"] == np.nan, ha_o/2, HA_O/2)
    df["HA_High"] = df[["HA_Open", "HA_Close", "High"]].max(axis=1)
    df["HA_Low"] = df[["HA_Open", "HA_Close", "Low"]].min(axis=1)
    return df


start = "2016-1-1"
end = "2016-10-30"
DAX = web.datareader("^GDAXI", "Yahoo", start, end)
del DAX["Volume"]
del DAX["Adj Close"]

print(HA(DAX).head(10).round(2))


def HA(df):
    df['HA_Close'] = (df['Open']+ df['High']+ df['Low']+df['Close'])/4

    idx = df.index.name
    df.reset_index(inplace=True)

    for i in range(0, len(df)):
        if i == 0:
            df.set_value(i, 'HA_Open', ((df.get_value(i, 'Open') + df.get_value(i, 'Close')) / 2))
        else:
            df.set_value(i, 'HA_Open', ((df.get_value(i - 1, 'HA_Open') + df.get_value(i - 1, 'HA_Close')) / 2))

    if idx:
        df.set_index(idx, inplace=True)

    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df


def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])

    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)

    return heikin_ashi_df