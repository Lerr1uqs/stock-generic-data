from utils import *

class StockToken:

    def __init__(self, code: str, name: str="", industry: str="") -> None:

        self._name    = name
        self.industry = industry
        # NOTE: exchange 用小写存储
        
        # 000001.SH
        if "." in code:

            a, b = code.split(".")
            if a.lower() in ["sh", "sz"]:
                self.exchange = a.lower()
                self.code = b
                
            elif b.lower() in ["sh", "sz"]:
                self.exchange = b.lower()
                self.code = a
                
        elif code.lower().startswith("sh") or code.lower().startswith("sz"):
            
            self.exchange = code.lower()[:2]
            self.code = code[2:]
            
        else:
            raise RuntimeError("illegal stock code") # TODO:
    
    def __repr__(self) -> str:
        return self.repr()
    
    def repr(self, exchg_as_suffix=True, exchg_as_upper=True) -> str:
        '''
        变成代码+交易所后缀的形式 e.g: 000001.SH
        '''

        exchg = self.exchange.upper() \
                    if exchg_as_upper \
                    else self.exchange.lower()

        if exchg_as_suffix:
            return self.code + "." + exchg
        else:
            return exchg + "." + self.code
    
    @property
    def name(self) -> str:
        return self._name
    

