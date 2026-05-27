import pandas as pd
import ons


def get_cpih() -> pd.Series:
    """
    Get UK Consumer Prices Index including owner occupiers' housing costs (CPIH).

    CPIH is the most comprehensive measure of inflation. It extends CPI
    to include a measure of the costs associated with owning, maintaining
    and living in one's own home, known as owner occupiers' housing costs
    (OOH), along with council tax.
    """
    data = ons.request_data.get_timeseries("l522")
    months = data["months"]
    dates = pd.to_datetime(
        [m["date"] for m in months], format="%Y %b"
    )
    values = [float(m["value"]) for m in months]
    s = pd.Series(values, index=dates, name="CPIH")
    s.index.name = "date"
    s.sort_index(ascending=True, inplace=True)
    return s

def get_inflation_cpih() -> pd.Series:
    """
    Calculate inflation based on UK CPIH.
    """
    s = get_cpih()
    s = s.pct_change().round(4)
    s.dropna(inplace=True)
    return s

