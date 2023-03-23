import pandas as pd
from io import StringIO
import  ons

cp_add_str = "cpih01/editions/time-series/versions/29.csv"
base_link = "https://api.beta.ons.gov.uk/v1/datasets/cpih01"

def get_cpih() -> pd.Series:
    """
    Get UK Consumer Prices Index including owner occupiers' housing costs (CPIH).

    CPIH is the most comprehensive measure of inflation. It extends CPI to include a measure of the costs
    associated with owning, maintaining and living in one's own home, known as owner occupiers' housing costs (OOH),
    along with council tax.
    """
    key_cpih = "cpih01"
    jresp = ons.request_data.get_data(key=key_cpih)
    df = pd.read_csv(StringIO(jresp),
                     engine='python',
                     encoding='utf-8')
    df = df[df['Aggregate'] == 'Overall Index']
    df = df.iloc[:, [0, 1]]
    df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format='%b-%y')
    df.iloc[:, 0] = df.iloc[:, 0].astype('float', copy=False)
    df.set_index(list(df.columns[[1]]), inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df.squeeze(axis=1)

def get_inflation_cpih() -> pd.Series:
    """
    Calculate inflation based on UK CPIH.
    """
    s = get_cpih()
    s = s.pct_change().round(4)
    s.dropna(inplace=True)
    return s

