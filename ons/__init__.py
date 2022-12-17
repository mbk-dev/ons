from importlib.metadata import version

from ons.request_data import get_data_frame
from ons.gdp import get_gdp
from ons.infl import (get_cp, get_inflation)

__version__ = version("ons")
