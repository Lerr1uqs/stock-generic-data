import os
import sys
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)

from .sdmngr import StocksManager
from .sdmngr import trading_dates
StocksManager.load_from_storage()
