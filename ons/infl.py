import pandas as pd
from io import StringIO
import  ons

cp_add_str = "cpih01/editions/time-series/versions/29.csv"
base_link = "https://api.beta.ons.gov.uk/v1/datasets/cpih01"
key_cp = "cpih01"

def get_cp():
    jresp = ons.request_data.get_data_frame(key=key_cp)
    df = pd.read_csv(StringIO(jresp), engine='python', encoding='utf-8')
    df = df[df['Aggregate'] == 'Overall Index']
    df = df.iloc[:, [0, 1]]
    df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format='%b-%y')
    df.iloc[:, 0] = df.iloc[:, 0].astype('float', copy=False)
    df.set_index(list(df.columns[[1]]), inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df

def get_inflation():
    df = get_cp()
    df = df.iloc[:, 0].pct_change().round(4)
    df.dropna(inplace=True)
    return df

