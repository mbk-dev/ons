import pandas as pd
from io import StringIO

import ons

def get_gdp() -> pd.Series:
    jresp = ons.request_data.get_data_frame()
    df = pd.read_csv(StringIO(jresp), engine='python', encoding='utf-8',
                     usecols=["V4_1", "Time", "nuts", "sic-unofficial", "GrowthRate"],
                     dtype={"V4_1": float},
                     parse_dates=["Time"],
                     )
    df = df[df['nuts'] == 'UK0']
    df = df[df['sic-unofficial'] == 'A--T']
    df = df[df['GrowthRate'] == 'Quarterly index']
    df = df.iloc[:, [0, 1]]
    df.rename(columns={df.columns[1]: "date"}, inplace=True)
    df.rename(columns={df.columns[0]: "GDP"}, inplace=True)
    df.set_index("date", inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df.squeeze()

def get_infl_from_gdp( data: pd.Series) ->pd.Series:
    s = data.pct_change().round(4)
    s = s.dropna()
    s.name = "Inflation"
    return s
