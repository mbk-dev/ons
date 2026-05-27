from importlib.metadata import version

from ons.request_data import get_data as get_data, get_timeseries as get_timeseries
from ons.gdp import get_gdp as get_gdp
from ons.infl import get_cpih as get_cpih, get_inflation_cpih as get_inflation_cpih

__version__ = version("ons")
