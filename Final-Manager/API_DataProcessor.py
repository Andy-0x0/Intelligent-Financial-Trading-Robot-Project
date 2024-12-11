import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
pd.set_option('display.unicode.east_asian_width', True)
from tqdm import tqdm

class Single_Factor_Portfolio:
    def __init__(self,return_data:pd.DataFrame,index_data:pd.DataFrame) -> None:
        self.return_data = return_data
        self.index_data = index_data
        self.check_shape()
    def check_shape(self) -> None:
        """单因子：【收益MATRIX】和【因子MATRIX】形状一致"""
        if self.return_data.shape != self.index_data.shape: 
            print(f"return_data.shape:{self.return_data.shape};index_data.shape:{self.index_data.shape}")
            raise Exception("警告：因子和收益率输入形状指标必须一致!")
        else: return
    def build_and_test_split_effect(self, layers:int = 10, Ascend:bool = True) -> None:
        """
        本函数用于计算分层效应：
        输入参数：layers: 分层效应层数；Ascend：因子选股排序是升序还是降序
        """
        return_data = self.return_data.T #将时序数据转为横截面数据
        index_data = self.index_data.T #将时序数据转为横截面数据
        return_time_series = return_data.columns.tolist()[1:] #取收益率时序编号
        index_time_series = index_data.columns.tolist()[:-1] #取因子时序编号
        time_series_length = len(index_time_series) #统计时序长度
        quant = index_data.shape[0]//layers #计算每一层的长度
        ReturnRate_series_list = [] #存放每日分层收益率
        for i in tqdm(range(time_series_length)):
            index_time = index_time_series[i]
            return_time = return_time_series[i]
            temp_data = pd.concat(objs=[index_data[index_time],return_data[return_time]],axis=1,ignore_index=False)
            temp_data[index_time] = temp_data[index_time].rank(ascending=Ascend)//quant+1
            temp_data.loc[temp_data[index_time]>layers,index_time]=layers
            ReturnRate_series_list.append(temp_data.groupby(by=index_time,as_index=True).mean().reset_index(drop=True))
        groupreturn_data = pd.concat(objs=ReturnRate_series_list,axis=1,join='outer',ignore_index=False).T.ffill()
        value_data = (groupreturn_data).cumsum(axis=0)+1
        for group in value_data.columns:
            value_data[group].plot()
        plt.legend([f'group{group+1}' for group in value_data.columns])
        plt.tight_layout(pad=0)
        plt.show()
        plt.figure('bar')
        final_value = value_data.loc[value_data.index[-1]]
        plt.bar(x=range(1,len(final_value)+1),height=final_value)
        plt.show()
    def build_and_test_first_class_portfolio(self, layers:int = 10, Ascend:bool = True, test:bool = False) -> None:
        """
        本函数用于计算首层投资组合的净值曲线：
        输入参数：
            layers: 分层效应层数
            Ascend：因子选股排序是升序还是降序
            test：True： 返回检验结果，格式为：{Sharpe:**,AR:**,DrawDown:**}
                  False：返回首层数据
        """
        return_data = self.return_data.T #将时序数据转为横截面数据
        index_data = self.index_data.T #将时序数据转为横截面数据
        return_time_series = return_data.columns.tolist()[1:] #取收益率时序编号
        index_time_series = index_data.columns.tolist()[:-1] #取因子时序编号
        time_series_length = len(index_time_series) #统计时序长度
        quant = index_data.shape[0]//layers #计算每一层的长度
        ReturnRate_series_list = [] #存放每日收益率
        Stock_list = []
        TradeAmount_list = []
        for i in tqdm(range(time_series_length)):
            
            index_time = index_time_series[i]
            return_time = return_time_series[i]
            temp_data = pd.concat(objs=[index_data[index_time],return_data[return_time]],axis=1,ignore_index=False)
            temp_data[index_time] = temp_data[index_time].rank(ascending=Ascend)//quant
            ReturnRate_series_list.append(temp_data.loc[temp_data[index_time]==0,return_time].mean())
            temp_Stock_list = temp_data.loc[temp_data[index_time]==0,return_time].index.tolist()
            TradeAmount_list.append(1-len(set(Stock_list)&set(temp_Stock_list))/quant)
            Stock_list = temp_Stock_list
        value_data = pd.DataFrame({'value':ReturnRate_series_list,'tradeAmount':TradeAmount_list})
        value_data.index = return_time_series
        value_data['value'] = value_data['value'].cumsum()+1
        value_data['value'] = (1-0.0005*value_data['tradeAmount'])*value_data['value']
        value_data = value_data.ffill().bfill()
        if test:
            return {"DrawDown":1-(value_data['value']/value_data['value'].cummax()).min(),
                    "AR":(value_data.loc[value_data.index[-1],'value']/value_data.loc[value_data.index[0],'value']-1)*365/len(value_data),
                    "Sharpe":(value_data.loc[value_data.index[-1],'value']/value_data.loc[value_data.index[0],'value']-1)/value_data['value'].std()},value_data[['value']]
        else: return value_data[['value']]
        
    def RankIC(self):
        return_rate_data = self.return_data.rank(axis=1)
        index_data = self.index_data.shift(1).rank(axis=1)
        return (return_rate_data.corrwith(other=index_data,axis=1).mean())
    def IC(self):
        return_rate_data = self.return_data
        index_data = self.index_data.shift(1)
        return (return_rate_data.corrwith(other=index_data,axis=1).mean())
    def IR(self):
        return_rate_data = self.return_data
        index_data = self.index_data.shift(1)
        IC_series = return_rate_data.corrwith(other=index_data,axis=1)
        return IC_series.mean()/IC_series.std()
