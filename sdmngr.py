# stock data manager
from utils import *
from stocktoken import StockToken
from functools import wraps

import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))


name2code = {}
code2name = {}
codes: List[str] = [] # 所有要入库的股票代码 e.g. 000001.SZ
traderdate_isopen: Dict[Datetime, bool] = {}
trading_dates: List[str] = [] # e.g. 20241231
DT_STDFMT = r"%Y%m%d" # datetime standard format 

def load():
    '''
    生成所有所需要的全局变量
    '''
    NAME2CODE: pd.DataFrame = pd.read_csv(ROOT + "/storage/name2code.csv")
    CALANDER : pd.DataFrame = pd.read_csv(ROOT + "/storage/calander.csv")

    for (idx, line) in NAME2CODE.iterrows():
        name2code[line["name"]] = line["ts_code"]
        code2name[line["ts_code"]] = line["name"]
        codes.append(str(line["ts_code"]))

    for (idx, line) in CALANDER.iterrows():
        if line["is_open"] == 1:
            trading_dates.append(str(line["cal_date"]))

    trading_dates.reverse() # 因为 CALANDER中是倒序
    
def check_data_loaded(f: Callable) -> Callable:

    @wraps(f)
    def wrapper(cls, *args, **kwargs):
        t = cls
        if t.loaded is False:
            raise RuntimeError
        ret = f(cls, *args, **kwargs)
        return ret

    return wrapper

class StocksManager:
    '''
    管理List[StockToken] 并转换成所需要的形式
    '''
    loaded = False
    stock_tokens: List[StockToken] = []

    @classmethod
    def load_from_storage(cls) -> None:
        '''
        从本地的预存文件中加载数据 比如股票代码 名字 日历
        '''
        load()
        cls.loaded = True

        for code in codes:
            name = code2name[code]
            cls.stock_tokens.append(StockToken(code, name))

    @check_data_loaded
    @classmethod
    def gen_code_list(cls, exchg_as_suffix=True, exchg_as_upper=True) -> List[str]:
        '''
        产生代码字符串表示列表
        '''
        return [st.repr(exchg_as_suffix, exchg_as_upper) for st in cls.stock_tokens]
    
    @check_data_loaded
    @classmethod
    def code_to_name(cls, code: str) -> str:
        '''
        sh000001
        000001.SH
        '''

        st = StockToken(code)

        return code2name[st.repr()]

    @check_data_loaded
    @classmethod
    def name_to_code(cls, name: str) -> Optional[str]:

        return name2code[name]

    @check_data_loaded
    @classmethod
    def name_to_token(cls, name: str) -> Optional[str]:

        return StockToken(name2code[name], name)