import tushare as ts
import pandas as pd
from typing import List

class BrokenTokenException(Exception): pass#许可证全部无法使用异常
class SPDBankruptException(Exception): pass#浦发银行退市/倒闭异常
class DelistException(Exception):pass#股票退市
    
class Tushare_DB_Processer:
    tokens = {} # 许可证储存
    tokens['LJY'] = '4b60806f0b7517f2dd53a4324264a40571e8bf215e7dfb631f7e8535'
    tokens['GCH'] = '36d89a5fd4687a7b734fad998d72c08bcfa672f015e0eb617506e68d'
    tokens['DJY'] = '8f3a3b63b5e5ad7ad7633d802c897b93c5d6758e6cc6f6898a4dd193'
    tokens['YY']  = '7415319eef4fca4d4cc4be1b6cffe0c3be2648c72570e1baaae44ddd'
    tokens['MTY'] = '589d3d72a3542967d941c5e8c51c27e89011c98160c8e76abf619088'
    tokens['MR']  = '291567dc757e6a49fab0978befdd22da86a366f068a42ab0f314e9ed'
    tokens['HK']  = '019d021ca2880c5e20f873e12448831527ead2a890b6ca45016f55ce'
    def __init__(self) -> None:
        self.pro=self.test_and_get_token()
    def test_and_get_token(self):#测试许可证是否可用
        try:
            for value in self.tokens.values():
                try:
                    pro_test = ts.pro_api(value)
                    data = pro_test.daily(
                        ts_code = '600000.SH',#以浦发银行为基准，不容易退市/倒闭
                        start_date = '20211229',
                        end_date   = '20211230',
                        fields = ['trade_date','close'])
                except:
                    raise SPDBankruptException("警告：浦发银行（600000.SH）可能出现了问题！")
                if not data.empty:
                    return pro_test
                else:
                    continue
        except:
            raise BrokenTokenException("警告：所有TOKEN全部无法使用！")
    def get_stock_data(self,
                       ts_code:str,
                       date_start:str,
                       date_end:str,
                       fields:List[str]=["ts_code",#股票代码
                                         "open",#开盘价
                                         "high",#最高价
                                         "low",#最低价
                                         "close",#收盘价
                                         "pre_close",#昨收价(前复权)
                                         "change",#涨跌额
                                         "pct_chg",#涨跌幅(未复权)
                                         "vol",#成交量(手)
                                         "amount"#成交量(千元)
                                         ],
                       date_as_index:bool=True):
        """
        单一股票数据
        ts_code例："000001.SZ" 
        date_start&date_end例："20120506"
        fields例：["trade_date","close"]
        """
        try:
            data = self.pro.daily(
                ts_code=ts_code,
                start_date=date_start,
                end_date=date_end,
                fields=["trade_date"]+fields)
            data['trade_date'] = pd.to_datetime(data['trade_date'],format="%Y%m%d")
            
            if date_as_index: return data.set_index(keys='trade_date').sort_index()
            else: return data.sort_values(by='trade_date')
        except:
            raise DelistException("所选股票不存在或者已退市！！！")
    def get_stocks_data(self,
                        ts_codes:List[str],
                        date_start:str,
                        date_end:str,
                        field:str):
        """
        单一股票数据
        ts_codes例：["000001.SZ","600000,SH"] 
        date_start&date_end例："20120506"
        field例："close"
        """
        return pd.concat(objs=[self.get_stock_data(ts_code=ts_code,
                                                   date_start=date_start,
                                                   date_end=date_end,
                                                   fields=[field]).rename(columns={field:ts_code}) for ts_code in ts_codes],
                         axis=1,
                         join="inner",
                         ignore_index=False)
        
        
if __name__ == "__main__":
    DB = Tushare_DB_Processer()
    print(DB.get_stocks_data(ts_codes=["600000.SH","000001.SZ"],date_start="20211130",date_end="20211130",field='close'))
