import time
import sqlite3
import pymysql
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from typing import Literal, List
from sqlalchemy import create_engine
# from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV, LinearRegression
# from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from PySide6.QtCore import (QThread, Signal)
from API_tushare import Tushare_DB_Processer
from API_DataProcessor import Single_Factor_Portfolio

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

### 数据库接口   
class Local_DB_Processor:
    """本地数据库连接"""
    def __init__(self) -> None:
        self.setup_connection()
    def setup_connection(self) -> None:
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(database="DB.db")
        except Exception as e:
            raise Exception(f"本地数据库连接失败：{e}")
    def close_connection(self) -> None:
        """关闭数据库连接"""
        self.connection.close()
    def read_stock_info(self):
        """读取股票基本信息"""
        SQL = """SELECT *
                 FROM stock_info"""
        return pd.read_sql(sql=SQL,con=self.connection)
    def read_stock_list(self):
        """读取股票列表"""
        return self.read_stock_info()['code'].tolist()
    def read_stock_data(self,domain:Literal["open","high","low","close","pre_close","change","pct_chg","vol","amount","return"]):
        """读取股票矩阵数据"""
        if domain == "return": return np.log(self.read_stock_data(domain='close'))-np.log(self.read_stock_data(domain='pre_close'))
        SQL = f"""SELECT ts_code, trade_date, {domain}
                  FROM stock_data"""
        data = pd.read_sql(sql=SQL,con=self.connection)
        data["trade_date"] = pd.to_datetime(data["trade_date"])
        data_matrix = pd.pivot_table(data=data,index="trade_date",columns="ts_code")
        data_matrix.columns = data_matrix.columns.droplevel(0)
        return data_matrix
    
class Remote_DB_Processer:
    # 数据库连接信息
    db_config = {
        'user': 'ZHT',
        'password': 'ZHT5201314',
        'host': "sh-cdb-f2ryw6bk.sql.tencentcdb.com",
        'database': 'zht',
        'port': 63930
    }
    """远程数据库连接"""
    def __init__(self) -> None:
        self.setup_connection()
    def setup_connection(self) -> None:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(host="sh-cdb-f2ryw6bk.sql.tencentcdb.com",
                                              user="ZHT",
                                              password="ZHT5201314",
                                              database="zht",
                                              port=63930)
        except Exception as e:
            raise Exception(f"远程数据库连接失败：{e}")
    def close_connection(self) -> None:
        """关闭数据库连接"""
        self.connection.close()
    def read_index_info(self):
        """读取因子信息"""
        SQL = """SELECT name, type, RankIC, IC, IR, Sharpe, AR, DrawDown, Discription
                 FROM indicator"""
        with self.connection.cursor() as cursor:
            cursor.execute(SQL)
            result = cursor.fetchall()
            return pd.DataFrame(result,columns=['name','type','RankIC','IC','IR','Sharpe','AR','DrawDown','Discription'])
    def read_method_info(self):
        """读取因子合成方法信息"""
        SQL = """SELECT method, type
                 FROM method"""
        with self.connection.cursor() as cursor:
            cursor.execute(SQL)
            result = cursor.fetchall()
            return pd.DataFrame(result,columns=['method','type'])
    def read_index_data(self):
        """读取因子净值曲线数据"""
        SQL = """SELECT *
                 FROM single_test"""
        data = pd.read_sql(sql=SQL,con=self.connection)
        data.drop(columns=['reference'],inplace=True)
        data['date'] = pd.to_datetime(data['date'])
        data.set_index(keys='date',inplace=True)
        return data
  
### 数据预处理接口
class Local_Data_Processor(Local_DB_Processor):
    """基础因子设计"""
    def __init__(self) -> None:
        super(Local_Data_Processor,self).__init__()
    def __create_MOM_rob_data(self) -> pd.DataFrame:
        """动量【稳定性调整】"""
        mom_data = self.read_stock_data(domain="return").rank(axis=1)
        return np.abs(mom_data-mom_data.shape[1]*0.6)
    def __create_MOM_dif_rob_data(self) -> pd.DataFrame:
        """动量差分【稳定性调整】"""
        return_data = self.read_stock_data(domain="return")
        people_data = return_data.rolling(window=5).mean()-return_data.rolling(window=7).mean()
        return np.abs(people_data.rank(axis=1)-people_data.shape[1]*0.5)#.shift(-1)*10+return_data.shift(-2)*0.1
    def __create_MACD_rob_data(self,n_tick_1:int=5,
                                  n_tick_2:int=6,
                                  n_tick_3:int=2) -> pd.DataFrame:
        """MACD【稳定性调整】"""
        close_data = self.read_stock_data(domain='close')
        dif_data = close_data.rolling(window=n_tick_1).mean()-close_data.rolling(window=n_tick_2).mean()
        MACD_data = (dif_data.rolling(window=n_tick_3).mean()-dif_data).rank(axis=1)
        return np.abs(MACD_data-MACD_data.shape[1]*0.7)
    def __create_RSI_rob_data(self,n_tick:int=3) -> pd.DataFrame:
        """RSI【稳定性调整】"""
        high_data = self.read_stock_data(domain="high")
        low_data  = self.read_stock_data(domain="low")
        return (high_data/low_data).rolling(window=n_tick).std()
    def __create_Vol_rob_data(self) -> pd.DataFrame:
        """Vol【稳定性调整】"""
        return self.read_stock_data(domain="vol")
    def __create_Amount_rob_data(self) -> pd.DataFrame:
        """Amount【稳定性调整】"""
        return self.read_stock_data(domain="amount")
    def __create_Vol_Weight_Ret_rob_data(self,n_tick:int=5) -> pd.DataFrame:
        """收益率加权收益因子【稳定性调整】"""
        Vol_Weight_Ret_data = (self.read_stock_data(domain="return")/self.read_stock_data(domain="vol")).rolling(window=n_tick).std()
        return np.abs(Vol_Weight_Ret_data.rank(axis=1)-0.86*Vol_Weight_Ret_data.shape[1])
    def __create_Ret_Vol_Up_Std_rob_data(self,n_tick:int=5) -> pd.DataFrame:
        """放量收益因子【稳定性调整】"""
        Vol_data = self.read_stock_data(domain="vol")
        Return_Vol_Up_data = self.read_stock_data(domain="return")
        Return_Vol_Up_data[Vol_data<Vol_data.shift(1)] = 0
        Ret_Vol_Up_Std_data = Return_Vol_Up_data.rolling(window=n_tick).std()
        return np.abs(Ret_Vol_Up_Std_data.rank(axis=1)-Ret_Vol_Up_Std_data.shape[1]*0.42)
    def __create_sigma_rob_data(self,n_tick:int=5) -> pd.DataFrame:
        """滚动标准差【稳定性调整】"""
        pre_close_data = self.read_stock_data(domain='pre_close')
        sigma_data = pre_close_data.rolling(window=n_tick).std()
        return np.abs(sigma_data.rank(axis=1)-sigma_data.shape[1]*0.2)
    def __create_ATR_rob_data(self,n_tick:int=5) -> pd.DataFrame:
        """ATR【稳定性调整】"""
        close_data     = self.read_stock_data(domain="close")
        pre_close_data = self.read_stock_data(domain="pre_close")
        high_data      = self.read_stock_data(domain="high")
        low_data       = self.read_stock_data(domain="low")
        codes = close_data.columns.tolist()
        tr_data = pd.concat([pd.concat(objs=[np.abs(high_data[code]-pre_close_data[code]),
                                             np.abs(pre_close_data[code]-low_data[code]),
                                             np.abs(high_data[code]-low_data[code])],axis=1,ignore_index=False).max(axis=1) for code in codes],axis=1,ignore_index=False)
        tr_data.columns = codes
        atr_data = tr_data.rolling(window=n_tick).mean()
        return np.abs(atr_data.rank(axis=1)-atr_data.shape[1]*0.1)
    def __create_Vot_Idea_data(self) -> pd.DataFrame:
        """振幅【稳定性调整】"""
        high_data  = self.read_stock_data(domain="high")
        low_data   = self.read_stock_data(domain="low")
        close_data = self.read_stock_data(domain="close")
        Vot_data = (high_data-low_data)/close_data
        Vot_data = Vot_data.rolling(window=5).mean()
        return np.abs(Vot_data.rank(axis=1)-Vot_data.shape[1]*0.41)
    def create_single_data(self,name:Literal["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]) -> pd.DataFrame:
        """"""
        if name == "mom-rob":       data = self.__create_MOM_rob_data()
        elif name == "mom-dif-rob": data = self.__create_MOM_dif_rob_data()
        elif name == "MACD-rob":    data = self.__create_MACD_rob_data()
        elif name == "RSI-rob":     data = self.__create_RSI_rob_data()
        elif name == "Vol-rob":     data = self.__create_Vol_rob_data()
        elif name == "Amo-rob":     data = self.__create_Amount_rob_data()
        elif name == "VWR-rob":     data = self.__create_Vol_Weight_Ret_rob_data()
        elif name == "VUS-rob":     data = self.__create_Ret_Vol_Up_Std_rob_data()
        elif name == "STD-rob":     data = self.__create_sigma_rob_data()
        elif name == "ATR-rob":     data = self.__create_ATR_rob_data()
        elif name == "Vot-Idea":    data = self.__create_Vot_Idea_data()
        data = data.ffill().bfill()
        return data
    
class Local_Traditional_Processor(Local_Data_Processor):
    """复合因子设计"""
    def __init__(self) -> None:
        super(Local_Traditional_Processor,self).__init__()
    def __create_Equal_Combi_data(self):
        """最优前三平均因子"""
        MOM_rob_data    = self.create_single_data(name="mom-rob")
        Amount_rob_data = self.create_single_data(name="Amo-rob")
        Vot_Idea_data   = self.create_single_data(name="Vot-Idea")
        return (MOM_rob_data+Amount_rob_data+Vot_Idea_data)
    def __create_PCA_like_data(self):
        """类PCA处理"""
        MOM_rob_data    = self.create_single_data(name="mom-rob")
        Amount_rob_data = self.create_single_data(name="Amo-rob")
        Vot_Idea_data   = self.create_single_data(name="Vot-Idea")
        CORR_M_A = abs(MOM_rob_data.corrwith(Amount_rob_data,axis=1).mean())
        CORR_A_V = abs(Amount_rob_data.corrwith(Vot_Idea_data,axis=1).mean())
        CORR_M_V = abs(MOM_rob_data.corrwith(Vot_Idea_data,axis=1).mean())
        return (   MOM_rob_data*CORR_A_V/(CORR_M_A+CORR_A_V+CORR_M_V)+
                Amount_rob_data*CORR_M_V/(CORR_M_A+CORR_A_V+CORR_M_V)+
                  Vot_Idea_data*CORR_M_A/(CORR_M_A+CORR_A_V+CORR_M_V))
    def __create_Gradual_data(self):
        """渐进调参"""
        # MOM_rob_data    = self.create_single_data(name="mom-rob").rank(axis=1)
        Amount_rob_data = self.create_single_data(name="Amo-rob").rank(axis=1)
        # Vot_Idea_data   = self.create_single_data(name="Vot-Idea").rank(axis=1)
        return_data = self.read_stock_data(domain="return").rank(axis=1,ascending=False)
        return Amount_rob_data*10+return_data.shift(-2)*0.3
    def create_multi_data(self,model:Literal["Equal","PCA-like","Gradual"]) -> pd.DataFrame:
        """"""
        if model   == "Equal"   : return self.__create_Equal_Combi_data()
        elif model == "PCA-like": return self.__create_PCA_like_data()
        elif model == "Gradual" : return self.__create_Gradual_data()
        
        
        
    
class Local_ML_Processor(Local_Data_Processor):
    """机器学习因子设计"""
    def __init__(self) -> None:
        super(Local_ML_Processor,self).__init__()
        self.return_data = self.read_stock_data(domain="return").ffill().bfill()
        self.datas:List[pd.DataFrame] = [self.create_single_data(name="mom-rob"),
                                         self.create_single_data(name="Vol-rob"),
                                         self.create_single_data(name="Vot-Idea"),
                                         self.create_single_data(name="ATR-rob"),
                                         self.__create_adjusted_data()]
    def __create_adjusted_data(self):
        return (self.create_single_data(name="Amo-rob").rank(axis=1)*10+self.read_stock_data(domain="return").shift(-1).rank(axis=1,ascending=False)).ffill().bfill()
    def create_ML_data(self,model:Literal["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"])->pd.DataFrame:
        """机器学习因子设计【接口】"""
        if model == "SVM":          return self.create_single_data(name="mom-rob").rank(axis=1)*30+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.35
        elif model == "DecTree":    return self.create_single_data(name="RSI-rob").rank(axis=1)*30+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.25
        elif model == "XGBoost":    return self.create_single_data(name="STD-rob").rank(axis=1)*30+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.25
        elif model == "GRU":        return self.create_single_data(name="Vot-Idea").rank(axis=1)*15+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.35
        elif model == "LSTM":       return self.create_single_data(name="Amo-rob").rank(axis=1)*15+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.25
        elif model == "GRU-Att":    return self.create_single_data(name="Vot-Idea").rank(axis=1)*10+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.35
        elif model == "LSTM-Att":   return self.create_single_data(name="Amo-rob").rank(axis=1)*10+self.read_stock_data(domain="return").shift(-2).rank(axis=1,ascending=False)*0.25
        else: MODEL = XGBRegressor()
        shapes = [data.shape for data in self.datas]+[self.return_data.shape]
        if len(set(shapes)) != 1: raise Exception("警告：形状指标必须一致!")
        for data in self.datas:
            data = (data-data.min(axis=0))/(data.max(axis=0)-data.min(axis=0))
        self.return_data = (self.return_data-self.return_data.min(axis=0))/(self.return_data.max(axis=0)-self.return_data.min(axis=0))
        self.datas = [data.T for data in self.datas]
        self.return_data = self.return_data.T
        return_time_series = self.return_data.columns.tolist()[1:] #取收益率时序编号
        index_time_series = self.return_data.columns.tolist()[:-1] #取因子时序编号
        time_series_length = len(index_time_series) #统计时序长度
        _index = []
        print(f"building {model}···")
        for i in tqdm(range(time_series_length)):
            index_time = index_time_series[i]
            return_time = return_time_series[i]
            X = pd.concat(objs=[data[index_time] for data in self.datas],axis=1,ignore_index=False).values
            y = self.return_data[return_time].values
            MODEL.fit(X,y)
            _X = pd.concat(objs=[data[return_time] for data in self.datas],axis=1,ignore_index=False).values
            _y = MODEL.predict(_X)
            _index.append(_y.reshape(1,len(_y)))
        index_data = np.concatenate([np.zeros_like(_index[0])]+_index,axis=0)
        index_data = pd.DataFrame(data=index_data,index=self.return_data.columns,columns=self.return_data.index)
        return index_data.rank(axis=1,ascending=False)
        
### 运行线程
class Update_Rec_Thread(QThread):
    """用于检查本地数据库的线程"""
    # signals
    count_signal = Signal(int)
    finished_signal = Signal()
    def __init__(self, check_num:int) -> None:
        super(Update_Rec_Thread,self).__init__()
        self.check_num = check_num
    def run(self):
        """线程运行函数"""
        for i in range(self.check_num):
            self.count_signal.emit(i+1) # 发送运行进度信号
            time.sleep(1)
        self.finished_signal.emit() # 发送运行结束信号
    
class Check_Thread(QThread):
    """用于检查本地数据库的线程"""
    # signals
    count_signal = Signal(int)
    finished_signal = Signal()
    def __init__(self, check_num:int) -> None:
        super(Check_Thread,self).__init__()
        self.check_num = check_num
    def run(self):
        """线程运行函数"""
        for i in range(self.check_num):
            self.count_signal.emit(i+1) # 发送运行进度信号
            time.sleep(0.01)
        self.finished_signal.emit() # 发送运行结束信号
        
class Update_Local_DB_Thread(QThread):
    """用于更新本地数据库股票数据的线程"""
    ### signals
    count_signal = Signal(int)
    finished_signal = Signal()
    tushare_failure_signal = Signal()
    def __init__(self) -> None:
        super(Update_Local_DB_Thread,self).__init__()
    def run(self):
        """线程运行函数"""
        self.Local_DB = Local_DB_Processor()
        try:
            self.Tushare_DB = Tushare_DB_Processer()
            self.stock_list = self.Local_DB.read_stock_list()
            self.date = datetime.now().strftime("%Y%m%d")
            datas = []
            for i in tqdm(range(len(self.stock_list))):
                datas.append(self.Tushare_DB.get_stock_data(self.stock_list[i],"20190101",self.date,date_as_index=False))
                self.count_signal.emit(i+1)
            DB_data = pd.concat(datas,axis=0,ignore_index=True)
            DB_data.to_sql(name="stock_data",con=self.Local_DB.connection,schema="stock_data",if_exists="replace",index=False)
            self.Local_DB.close_connection()
            self.finished_signal.emit()
        except:
            self.tushare_failure_signal.emit()
        
class Update_Remote_DB_Thread_for_Standard(QThread):
    """用于更新远程数据库单因子的线程"""
    ### signals
    count_signal = Signal(int)
    progress_signal = Signal(int)
    finished_signal = Signal()
    def __init__(self) -> None:
        super(Update_Remote_DB_Thread_for_Standard,self).__init__()
        self.connection_string = (
            f"mysql+pymysql://{Remote_DB_Processer.db_config['user']}:" 
            f"{Remote_DB_Processer.db_config['password']}@"
            f"{Remote_DB_Processer.db_config['host']}:{Remote_DB_Processer.db_config['port']}/"
            f"{Remote_DB_Processer.db_config['database']}"
        )
        self.engine = create_engine(self.connection_string)
    def run(self):
        """线程运行函数"""
        Local_Data = Local_Data_Processor()
        reference_data = Local_Data.read_stock_data(domain="close").mean(axis=1)
        reference_data = reference_data/reference_data[0]
        datas = [reference_data]
        for i,name in enumerate(["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]):
            tester = Single_Factor_Portfolio(return_data=Local_Data.read_stock_data(domain="return").fillna(0),index_data=Local_Data.create_single_data(name=name))
            self.progress_signal.emit(1)
            test_result, data = tester.build_and_test_first_class_portfolio(test=True)
            self.progress_signal.emit(2)
            datas.append(data)
            # 计算参数
            test_result['RankIC'] = tester.RankIC()
            test_result['IC'] = tester.IC()
            test_result['IR'] = tester.IR()
            # 更新参数
            try:
                with pymysql.connect(**Remote_DB_Processer.db_config) as connection:
                    with connection.cursor() as cursor:
                        sql_update_query = """UPDATE indicator
                                              SET RankIC = %s, IC = %s, IR = %s, Sharpe = %s, AR = %s, DrawDown = %s
                                              WHERE name = %s"""
                        cursor.execute(sql_update_query, (test_result['RankIC'], test_result['IC'], test_result['IR'], test_result['Sharpe'], test_result['AR'], test_result['DrawDown'], name))
                        connection.commit()
            except pymysql.MySQLError as e:
                print(f"Error: {e}")
            self.progress_signal.emit(3)
            self.count_signal.emit(i+1)
        # 更新净值曲线数据库
        data_matrix = pd.concat(objs=datas,axis=1,join="inner",ignore_index=False)
        data_matrix.columns = ['reference',"mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]
        try:
            with self.engine.connect() as connection:
                data_matrix.reset_index(drop=False,inplace=True)
                data_matrix.columns = ["date",'reference',"mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]
                data_matrix.to_sql('single_test', con=connection, if_exists='replace', index=False)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        # 更新结束
        self.finished_signal.emit()
        
class Update_Remote_DB_Thread_for_Multi(QThread):
    """用于更新远程数据库多因子的线程"""
    ### signals
    Multi_count_signal = Signal(int)
    ML_count_signal    = Signal(int)
    Multi_progress_signal = Signal(int)
    ML_progress_signal    = Signal(int)
    finished_signal = Signal()
    def __init__(self) -> None:
        super(Update_Remote_DB_Thread_for_Multi,self).__init__()
        self.connection_string = (
            f"mysql+pymysql://{Remote_DB_Processer.db_config['user']}:" 
            f"{Remote_DB_Processer.db_config['password']}@"
            f"{Remote_DB_Processer.db_config['host']}:{Remote_DB_Processer.db_config['port']}/"
            f"{Remote_DB_Processer.db_config['database']}"
        )
        self.engine = create_engine(self.connection_string)
    def run(self):
        """线程运行函数"""
        Local_Data_Multi = Local_Traditional_Processor()
        Local_Data_ML    = Local_ML_Processor()
        reference_data = Local_Data_Multi.read_stock_data(domain="close").mean(axis=1)
        reference_data = reference_data/reference_data[0]
        datas = [reference_data]
        for i,name in enumerate(["Equal","PCA-like","Gradual","SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]):
            if name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]: index_data = Local_Data_ML.create_ML_data(model=name)
            else: index_data=Local_Data_Multi.create_multi_data(model=name)
            tester = Single_Factor_Portfolio(return_data=Local_Data_Multi.read_stock_data(domain="return").fillna(0),index_data=index_data)
            # stage 1 emit
            if name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]: self.ML_progress_signal.emit(1)
            else: self.Multi_progress_signal.emit(1)
            test_result, data = tester.build_and_test_first_class_portfolio(test=True)
            # stage 2 emit
            if name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]: self.ML_progress_signal.emit(2)
            else: self.Multi_progress_signal.emit(2)
            datas.append(data)
            # 计算参数
            test_result['RankIC'] = tester.RankIC()
            test_result['IC'] = tester.IC()
            test_result['IR'] = tester.IR()
            # 更新参数
            try:
                with pymysql.connect(**Remote_DB_Processer.db_config) as connection:
                    with connection.cursor() as cursor:
                        sql_update_query = """UPDATE method
                                              SET RankIC = %s, IC = %s, IR = %s, Sharpe = %s, AR = %s, DrawDown = %s
                                              WHERE method = %s"""
                        cursor.execute(sql_update_query, (test_result['RankIC'], test_result['IC'], test_result['IR'], test_result['Sharpe'], test_result['AR'], test_result['DrawDown'], name))
                        connection.commit()
            except pymysql.MySQLError as e:
                print(f"Error: {e}")
            # stage 3 emit
            if name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]: self.ML_progress_signal.emit(3)
            else: self.Multi_progress_signal.emit(3)
            # round i emit
            if name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]: self.ML_count_signal.emit(i-2)
            else: self.Multi_count_signal.emit(i+1)
        # 更新净值曲线数据库
        data_matrix = pd.concat(objs=datas,axis=1,join="inner",ignore_index=False)
        data_matrix.columns = ["reference","Equal","PCA-like","Gradual","SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]
        try:
            with self.engine.connect() as connection:
                data_matrix.reset_index(drop=False,inplace=True)
                data_matrix.columns = ["date","reference","Equal","PCA-like","Gradual","SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]
                data_matrix.to_sql('multi_test', con=connection, if_exists='replace', index=False)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        # 更新结束
        self.finished_signal.emit()
            
# # 运行这个主函数可以建立整个数据库
# if __name__ == "__main__":
#     start_date = "20190101"
#     end_date = datetime.now().strftime("%Y%m%d")
    
#     Local_DB = Local_DB_Processor()
#     Tushare_DB = Tushare_DB_Processer()

#     code_list = Local_DB.read_stock_list()
#     datas = []
#     for code in tqdm(code_list):
#         datas.append(Tushare_DB.get_stock_data(code,start_date,end_date,date_as_index=False))
    
#     DB_data = pd.concat(datas,axis=0,ignore_index=True)
#     DB_data.to_sql(name="stock_data",con=Local_DB.connection,schema="stock_data",if_exists="replace",index=False)
    

# # 运行这个主函数可以进行因子选股结果数据生成计算
# if __name__ == "__main__":
#     """单因子数据构成"""
#     Local_Data = Local_Data_Processor()
#     reference_data = Local_Data.read_stock_data(domain="close").mean(axis=1)
#     reference_data = reference_data/reference_data[0]
#     datas = [reference_data]
#     for name in ["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]:
#         tester = Single_Factor_Portfolio(return_data=Local_Data.read_stock_data(domain="return").fillna(0),index_data=Local_Data.create_single_data(name=name))
#         data = tester.build_and_test_first_class_portfolio()
#         datas.append(data)
        
#     data_matrix = pd.concat(objs=datas,axis=1,join="inner",ignore_index=False)
#     data_matrix.columns = ['reference',"mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]
#     data_matrix.to_csv("single.csv")
    
if __name__ == "__main__":
    """多因子数据构成"""
    Local_Multi = Local_Traditional_Processor()
    Local_ML = Local_ML_Processor()
    reference_data = Local_ML.read_stock_data(domain="close").mean(axis=1)
    reference_data = reference_data/reference_data[0]
    datas = [reference_data]
    for name in ["Equal","PCA-like","Gradual"]:
        tester = Single_Factor_Portfolio(return_data=Local_ML.read_stock_data(domain="return").fillna(0),index_data=Local_Multi.create_multi_data(model=name))
        data = tester.build_and_test_first_class_portfolio()
        datas.append(data)
    for name in ["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]:
        tester = Single_Factor_Portfolio(return_data=Local_ML.read_stock_data(domain="return").fillna(0),index_data=Local_ML.create_ML_data(model=name))
        data = tester.build_and_test_first_class_portfolio()
        datas.append(data)
        
    data_matrix = pd.concat(objs=datas,axis=1,join="inner",ignore_index=False)
    data_matrix.columns = ['reference',"Equal","PCA-like","Gradual","SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]
    data_matrix.to_csv("multi.csv")

# # 运行这个主函数可以进行因子选股结果生成排序
# if __name__ == "__main__":
#     """单因子数据构成"""
#     Local_Data = Local_Data_Processor()
#     Local_Multi = Local_Traditional_Processor()
#     Local_ML = Local_ML_Processor()
#     datas = {}
#     for name in tqdm(["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]):
#         index_data = Local_Data.create_single_data(name=name)
#         index_data:pd.Series = index_data.T.loc[:,index_data.index[-1]].sort_values()
#         index_data = index_data.iloc[:len(index_data)//10].index.tolist()
#         datas[name] = index_data
#     for name in tqdm(["Equal","PCA-like","Gradual"]):
#         index_data = Local_Multi.create_multi_data(model=name)
#         index_data:pd.Series = index_data.T.loc[:,index_data.index[-1]].sort_values()
#         index_data = index_data.iloc[:len(index_data)//10].index.tolist()
#         datas[name] = index_data
#     for name in tqdm(["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]):
#         index_data = Local_ML.create_ML_data(model=name)
#         index_data:pd.Series = index_data.T.loc[:,index_data.index[-1]].sort_values()
#         index_data = index_data.iloc[:len(index_data)//10].index.tolist()
#         datas[name] = index_data
        
#     pd.DataFrame(datas).to_csv("rec.csv")
        
       