# -*- coding: utf-8 -*-
import sys
import random
import pymysql
import pandas as pd

from typing import Literal 

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,QMargins,
    QMetaObject, QObject, QPoint, QRect,QStringListModel,
    QSize, QThread, QTime, QUrl, Qt, QPointF,Signal, Slot)

from PySide6.QtGui import (QIcon, QCloseEvent, QKeySequence,QCursor,
    QPainter,QPen,QLinearGradient,QColor,QBrush,QFont)

from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget, QListWidgetItem, QMenu,
    QTableWidgetItem, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem,
    QMainWindow, QMessageBox, QGraphicsDropShadowEffect)

from PySide6.QtCharts import (QChartView, QChart, 
                              QLineSeries, QAreaSeries, QValueAxis,QBarSet,QStackedBarSeries,QBarCategoryAxis)

from qfluentwidgets import (SplitFluentWindow,FluentIcon,MessageBox,SplashScreen,
                            InfoBar,InfoBarPosition,InfoBarIcon,FlyoutAnimationType)

from qframelesswindow import FramelessWindow

from UI import Ui_Form, Ui_Overall, Ui_Single_Stock

import tempfile #暂存文件位置
from plotly.io import to_html
import plotly.graph_objs as go
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")#,category=UserWarning)

class Data_Loading_Thread(QThread):
    # signals
    count = int(0)
    countSignal = Signal(int)
    finished_signal = Signal()
    def __init__(self) -> None:
        super(Data_Loading_Thread,self).__init__()
    def run(self):
        # program running below
        self.__setup_connection()
        self.__read_index_info()
        self.__read_method_info()
        self.__read_index_data()
        self.__read_method_data()
        self.__process_index_data()
        self.__read_rec_data()
        self.__close_connection()
        # program running above
        self.finished_signal.emit()
    def __setup_connection(self) -> None:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(host="sh-cdb-f2ryw6bk.sql.tencentcdb.com",
                                              user="ZHT",
                                              password="ZHT5201314",
                                              database="zht",
                                              port=63930)
        except Exception as e:
            raise Exception(f"远程数据库连接失败：{e}")
    def __read_index_info(self):
        """读取单因子信息"""
        SQL = """SELECT name, type, RankIC, IC, IR, Sharpe, AR, DrawDown, Discription
                 FROM indicator"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",category=UserWarning)
            self.single_info = pd.read_sql(sql=SQL,con=self.connection)
        self.single_info.set_index(keys="name",inplace=True)
    def __read_method_info(self):
        """读取复合因子信息"""
        SQL = """SELECT method, type, RankIC, IC, IR, Sharpe, AR, DrawDown, Discription
                 FROM method"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",category=UserWarning)
            self.multi_info = pd.read_sql(sql=SQL,con=self.connection)
        self.multi_info.set_index(keys="method",inplace=True)
    def __read_index_data(self):
        """读取单因子数据"""
        SQL = """SELECT * FROM single_test"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",category=UserWarning)
            self.single_data = pd.read_sql(sql=SQL,con=self.connection)
        self.single_data['date'] = pd.to_datetime(self.single_data['date'])
        self.single_data.set_index(keys='date',inplace=True)
        self.single_adjusted_data = ((self.single_data.diff()/self.single_data.shift(1))*self.single_data/(self.single_data.rolling(window=2).std())*0.005).cumsum()+1
    def __read_method_data(self):
        """读取复合因子数据"""
        SQL = """SELECT * FROM multi_test"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",category=UserWarning)
            self.multi_data = pd.read_sql(sql=SQL,con=self.connection)
        self.multi_data['date'] = pd.to_datetime(self.multi_data['date'])
        self.multi_data.set_index(keys='date',inplace=True)
        self.multi_adjusted_data = ((self.multi_data.diff()/self.multi_data.shift(1))*self.multi_data/(self.multi_data.rolling(window=2).std())*0.008).cumsum()+1
        self.multi_adjusted_data.dropna(inplace=True)
    def __process_index_data(self):
        """生成调整数据的"""
        self.single_adjusted_info = pd.concat(objs=[(1-(self.single_adjusted_data/self.single_adjusted_data.cummax()).min()),
                                                   (self.single_adjusted_data.loc[self.single_adjusted_data.index[-1],:]/self.single_adjusted_data.loc[self.single_adjusted_data.index[1],:]-1)*365/len(self.single_adjusted_data),
                                                   (self.single_adjusted_data.loc[self.single_adjusted_data.index[-1],:]/self.single_adjusted_data.loc[self.single_adjusted_data.index[1],:]-1)/self.single_adjusted_data.std()],axis=1)
        self.single_adjusted_info.columns = ["DrawDown","AR","Sharpe"]
        self.multi_adjusted_info = pd.concat(objs=[(1-(self.multi_adjusted_data/self.multi_adjusted_data.cummax()).min()),
                                                   (self.multi_adjusted_data.loc[self.multi_adjusted_data.index[-1],:]/self.multi_adjusted_data.loc[self.multi_adjusted_data.index[0],:]-1)*365/len(self.multi_adjusted_data),
                                                   (self.multi_adjusted_data.loc[self.multi_adjusted_data.index[-1],:]/self.multi_adjusted_data.loc[self.multi_adjusted_data.index[0],:]-1)/self.multi_adjusted_data.std()],axis=1)
        self.multi_adjusted_info.columns = ["DrawDown","AR","Sharpe"]
    def __read_rec_data(self):
        """读取推荐列表数据"""
        SQL = """SELECT * FROM rec"""
        self.rec_data = pd.read_sql(sql=SQL,con=self.connection,index_col="index")
        self.rec_code = {}
        for i in range(self.rec_data.shape[0]):
            for j in range(self.rec_data.shape[1]):
                if self.rec_data.iloc[i,j] not in list(self.rec_code.keys()):
                    self.rec_code[self.rec_data.iloc[i,j]] = 0
                else: self.rec_code[self.rec_data.iloc[i,j]] = self.rec_code[self.rec_data.iloc[i,j]]+30-i
        self.rec_code = dict(sorted(self.rec_code.items(),key=lambda item:item[1],reverse=True))
    def __close_connection(self) -> None:
        """关闭数据库连接"""
        self.connection.close()
    def get_single_list(self):
        """获取单因子列表"""
        return self.single_info.index.tolist()
    def get_multi_list(self):
        """获取多因子列表"""
        return self.multi_info.index.tolist()
    def get_single_data(self,name:Literal["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]):
        """获取单因子数据"""
        temp_data = pd.concat(objs=[self.single_data['reference'],self.single_data[name],self.single_adjusted_data[name]],axis=1,join="inner",ignore_index=False)
        temp_data.columns = ['reference',name,f"{name}-adjusted"]
        temp_data['reference'] = temp_data['reference']-1
        temp_data['reference'] = temp_data['reference']/3
        temp_data['reference'] = temp_data['reference']+1
        return temp_data
    def get_multi_data(self,name:Literal["SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]):
        """获取多因子数据"""
        temp_data = pd.concat(objs=[self.multi_data['reference'],self.multi_data[name],self.multi_adjusted_data[name]],axis=1,join="inner",ignore_index=False)
        temp_data.columns = ['reference',name,f"{name}-adjusted"]
        temp_data['reference'] = temp_data['reference']-1
        temp_data['reference'] = temp_data['reference']/3
        temp_data['reference'] = temp_data['reference']+1
        return temp_data
    def get_rec_list(self,name:Literal["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea"]):
        """获取推荐列表"""
        return self.rec_data[name].tolist()

class Win_Waiting(FramelessWindow):
    def __init__(self, Data_Loader:Data_Loading_Thread):
        super().__init__()
        # waiting for data
        self.Data_Loader = Data_Loader
        self.Data_Loader.finished_signal.connect(self.finish)
        self.Data_Loader.start()

        self.resize(700, 600)
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.setWindowIcon(QIcon("MrSakamoto-small.ico"))

        # Create a splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        
    @Slot()
    def finish(self):
        print("done")
        self.close()


class Main_Win(SplitFluentWindow):
    def __init__(self, Data_Loader:Data_Loading_Thread, parent=None):
        super().__init__(parent=parent)
        self.Data_Loader = Data_Loader
        self.Data_Loader.finished_signal.connect(self.load_data_finished)
        self.Win_Overall = Win_Overall(self.Data_Loader,self)
        self.Win_Single = Win_Single(self.Data_Loader,self)
        self.Win_Multi  = Win_Multi(self.Data_Loader,self)
        self.Win_Single_Stock = Win_Single_Stock(self)
        self.addSubInterface(self.Win_Overall,FluentIcon.ALBUM,'总结')
        self.addSubInterface(self.Win_Single,FluentIcon.DOCUMENT,'单因子')
        self.addSubInterface(self.Win_Multi,FluentIcon.DICTIONARY,'多因子')
        self.addSubInterface(self.Win_Single_Stock,FluentIcon.BOOK_SHELF,'个股')
        
    @Slot()
    def load_data_finished(self):
        self.show()
        self.setMicaEffectEnabled(True)
        
    def closeEvent(self, origin_closeEvent:QCloseEvent):
        super().closeEvent(origin_closeEvent)
        print("closed")
        
class Win_Overall(QWidget,Ui_Overall):
    def __init__(self, Data_Loader:Data_Loading_Thread, parent=None):
        super(Win_Overall,self).__init__(parent=parent)
        self.setupUi(self)
        self.Data_Loader = Data_Loader
        self.Data_Loader.finished_signal.connect(self.load_data_finished)
        self.add_shadow(self.GraphFrame)
        self.add_shadow(self.StartegyRec)
        self.add_shadow(self.LeverFrame)
        self.add_shadow(self.RecentralFrame)
    def add_shadow(self,module):
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
    @Slot()
    def load_data_finished(self):
        self.LeverRing.setRange(0,100)
        self.RecentralMaxBar.setRange(0,10)
        self.RecentralMinBar.setRange(0,10)
        self.RecentralMeanBar.setRange(0,100)
        self.LeverRing.setValue(5)
        self.RecentralMaxBar.setValue(8)
        self.RecentralMinBar.setValue(6)
        self.RecentralMeanBar.setValue(76)
        self.Graph.drawGraph(self.Data_Loader.rec_code)
        self.Reference.addItem("   AR   ","   AR   ",self.test)
        self.Reference.addItem("DrawDown","DrawDown",self.test)
        self.Reference.addItem(" Sharpe "," Sharpe ",self.test)
        self.Reference.setCurrentItem("   AR   ")
        self.Method_prog_Rank_1.setRange(0,100)
        self.Method_prog_Rank_2.setRange(0,100)
        self.Method_prog_Rank_3.setRange(0,100)
        self.Method_prog_Rank_4.setRange(0,100)
        self.Method_prog_Rank_5.setRange(0,100)
        self.test()
        # 设置今日日期
        self.EndDatePicker.setDate(QDate.currentDate())
    def test(self):
        domain = self.Reference._currentRouteKey.strip()
        temp_data = pd.concat(objs=[self.Data_Loader.single_info[domain],self.Data_Loader.multi_info[domain]],axis=0)
        if domain == "DrawDown": temp_data.sort_values(inplace=True)
        else :temp_data.sort_values(ascending=False,inplace=True)
        self.Method_Rank_1.setText(temp_data.index[0])
        self.Method_Rank_2.setText(temp_data.index[1])
        self.Method_Rank_3.setText(temp_data.index[2])
        self.Method_Rank_4.setText(temp_data.index[3])
        self.Method_Rank_5.setText(temp_data.index[4])
        if domain == "Sharpe":
            self.Method_Rate_Rank_1.setText(f"{temp_data.iloc[0]:.2f}")
            self.Method_Rate_Rank_2.setText(f"{temp_data.iloc[1]:.2f}")
            self.Method_Rate_Rank_3.setText(f"{temp_data.iloc[2]:.2f}")
            self.Method_Rate_Rank_4.setText(f"{temp_data.iloc[3]:.2f}")
            self.Method_Rate_Rank_5.setText(f"{temp_data.iloc[4]:.2f}")
            self.Method_prog_Rank_1.setValue(int(10*abs(temp_data.iloc[0])))
            self.Method_prog_Rank_2.setValue(int(10*abs(temp_data.iloc[1])))
            self.Method_prog_Rank_3.setValue(int(10*abs(temp_data.iloc[2])))
            self.Method_prog_Rank_4.setValue(int(10*abs(temp_data.iloc[3])))
            self.Method_prog_Rank_5.setValue(int(10*abs(temp_data.iloc[4])))
        else:
            self.Method_Rate_Rank_1.setText(f"{temp_data.iloc[0]*100:.2f}%")
            self.Method_Rate_Rank_2.setText(f"{temp_data.iloc[1]*100:.2f}%")
            self.Method_Rate_Rank_3.setText(f"{temp_data.iloc[2]*100:.2f}%")
            self.Method_Rate_Rank_4.setText(f"{temp_data.iloc[3]*100:.2f}%")
            self.Method_Rate_Rank_5.setText(f"{temp_data.iloc[4]*100:.2f}%")
            self.Method_prog_Rank_1.setValue(int(100*abs(temp_data.iloc[0])))
            self.Method_prog_Rank_2.setValue(int(100*abs(temp_data.iloc[1])))
            self.Method_prog_Rank_3.setValue(int(100*abs(temp_data.iloc[2])))
            self.Method_prog_Rank_4.setValue(int(100*abs(temp_data.iloc[3])))
            self.Method_prog_Rank_5.setValue(int(100*abs(temp_data.iloc[4])))
            
            

class Win_Single(QWidget,Ui_Form):
    def __init__(self, Data_Loader:Data_Loading_Thread, parent=None):
        super(Win_Single,self).__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("Win_Single")
        self.Data_Loader = Data_Loader
        self.Data_Loader.finished_signal.connect(self.load_data_finished)
        self.add_shadow(self.MainFrame)
        self.add_shadow(self.TextFrame)
        self.add_shadow(self.RankICFrame)
        self.add_shadow(self.ICFrame)
        self.add_shadow(self.IRFrame)
        self.add_shadow(self.SharpeFrame)
        self.add_shadow(self.AnnualReturnFrame)
        self.add_shadow(self.DrawDownFrame)
        self.FunctionList.clicked.connect(self.load_into_interface)
        
    def init_list_and_ring(self):
        self.single_list_model = QStringListModel(self.Data_Loader.get_single_list())
        self.FunctionList.setModel(self.single_list_model)
        self.RankICRing.setRange(0,100)
        self.ICRing.setRange(0,100)
        self.IRRing.setRange(0,100)
        self.SharpeRing.setRange(0,100)
        self.AnnualReturnRing.setRange(0,100)
        self.DrawDownRing.setRange(0,100)
     
    def load_into_interface(self,name):
        name = self.single_list_model.data(name)
        self.FunctionTitle.setText(f"【{name}】")
        self.FunctionLabel.setText(QCoreApplication.translate("Form", self.Data_Loader.single_info.loc[name,'Discription'], None))
        # 设置参数环
        self.RankICRing.setValue(int(100*abs(self.Data_Loader.single_info.loc[name,'RankIC'])))
        self.ICRing.setValue(int(100*abs(self.Data_Loader.single_info.loc[name,'IC'])))
        self.IRRing.setValue(int(100*abs(self.Data_Loader.single_info.loc[name,'IR'])))
        self.SharpeRing.setValue(int(10*abs(self.Data_Loader.single_info.loc[name,'Sharpe'])))
        self.AnnualReturnRing.setValue(int(100*abs(self.Data_Loader.single_info.loc[name,'AR'])))
        self.DrawDownRing.setValue(int(100*abs(self.Data_Loader.single_info.loc[name,'DrawDown'])))
        # 设置参数
        self.RankIC.setText(f"{self.Data_Loader.single_info.loc[name,'RankIC']*100:.2f}%")
        self.IC.setText(f"{self.Data_Loader.single_info.loc[name,'IC']*100:.2f}%")
        self.IR.setText(f"{self.Data_Loader.single_info.loc[name,'IR']*100:.2f}%")
        self.Sharpe.setText(f"{self.Data_Loader.single_info.loc[name,'Sharpe']:.2f}")
        self.AnnualReturn.setText(f"{self.Data_Loader.single_info.loc[name,'AR']*100:.2f}%")
        self.DrawDown.setText(f"{self.Data_Loader.single_info.loc[name,'DrawDown']*100:.2f}%")
        # 对比数据导入
        self.TableWidget.setItem(0,0,QTableWidgetItem(f"{self.Data_Loader.single_info.loc[name,'Sharpe']:.2f}"))
        self.TableWidget.setItem(0,1,QTableWidgetItem(f"{self.Data_Loader.single_adjusted_info.loc[name,'Sharpe']:.2f}"))
        self.TableWidget.setItem(1,0,QTableWidgetItem(f"{self.Data_Loader.single_info.loc[name,'AR']*100:.2f}%"))
        self.TableWidget.setItem(1,1,QTableWidgetItem(f"{self.Data_Loader.single_adjusted_info.loc[name,'AR']*100:.2f}%"))
        self.TableWidget.setItem(2,0,QTableWidgetItem(f"{self.Data_Loader.single_info.loc[name,'DrawDown']*100:.2f}%"))
        self.TableWidget.setItem(2,1,QTableWidgetItem(f"{self.Data_Loader.single_adjusted_info.loc[name,'DrawDown']*100:.2f}%"))
        # 推荐列表导入
        self.rec_list_model = QStringListModel(self.Data_Loader.get_rec_list(name=name))
        self.RecList.setModel(self.rec_list_model)
        # 绘制
        self.Graph.drawGraph(self.Data_Loader.get_single_data(name))
    def add_shadow(self,module):
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
    @Slot()
    def load_data_finished(self):
        self.init_list_and_ring()
        
class Win_Multi(QWidget,Ui_Form):
    def __init__(self, Data_Loader:Data_Loading_Thread, parent=None):
        super(Win_Multi,self).__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName("Win_Multi")
        self.Data_Loader = Data_Loader
        self.Data_Loader.finished_signal.connect(self.load_data_finished)
        self.add_shadow(self.MainFrame)
        self.add_shadow(self.TextFrame)
        self.add_shadow(self.RankICFrame)
        self.add_shadow(self.ICFrame)
        self.add_shadow(self.IRFrame)
        self.add_shadow(self.SharpeFrame)
        self.add_shadow(self.AnnualReturnFrame)
        self.add_shadow(self.DrawDownFrame)
        self.FunctionList.clicked.connect(self.load_into_interface)
        
    def init_list_and_ring(self):
        self.multi_list_model = QStringListModel(self.Data_Loader.get_multi_list())
        self.FunctionList.setModel(self.multi_list_model)
        self.RankICRing.setRange(0,100)
        self.ICRing.setRange(0,100)
        self.IRRing.setRange(0,100)
        self.SharpeRing.setRange(0,100)
        self.AnnualReturnRing.setRange(0,100)
        self.DrawDownRing.setRange(0,100)
     
    def load_into_interface(self,name):
        name = self.multi_list_model.data(name)
        self.FunctionTitle.setText(name)
        self.FunctionLabel.setText(self.Data_Loader.multi_info.loc[name,'Discription'])
        # 设置参数环
        self.RankICRing.setValue(int(100*abs(self.Data_Loader.multi_info.loc[name,'RankIC'])))
        self.ICRing.setValue(int(100*abs(self.Data_Loader.multi_info.loc[name,'IC'])))
        self.IRRing.setValue(int(100*abs(self.Data_Loader.multi_info.loc[name,'IR'])))
        self.SharpeRing.setValue(int(10*abs(self.Data_Loader.multi_info.loc[name,'Sharpe'])))
        self.AnnualReturnRing.setValue(int(100*abs(self.Data_Loader.multi_info.loc[name,'AR'])))
        self.DrawDownRing.setValue(int(100*abs(self.Data_Loader.multi_info.loc[name,'DrawDown'])))
        # 设置参数
        self.RankIC.setText(f"{self.Data_Loader.multi_info.loc[name,'RankIC']*100:.2f}%")
        self.IC.setText(f"{self.Data_Loader.multi_info.loc[name,'IC']*100:.2f}%")
        self.IR.setText(f"{self.Data_Loader.multi_info.loc[name,'IR']*100:.2f}%")
        self.Sharpe.setText(f"{self.Data_Loader.multi_info.loc[name,'Sharpe']:.2f}")
        self.AnnualReturn.setText(f"{self.Data_Loader.multi_info.loc[name,'AR']*100:.2f}%")
        self.DrawDown.setText(f"{self.Data_Loader.multi_info.loc[name,'DrawDown']*100:.2f}%")
        # 对比数据导入
        self.TableWidget.setItem(0,0,QTableWidgetItem(f"{self.Data_Loader.multi_info.loc[name,'Sharpe']:.2f}"))
        self.TableWidget.setItem(0,1,QTableWidgetItem(f"{self.Data_Loader.multi_adjusted_info.loc[name,'Sharpe']:.2f}"))
        self.TableWidget.setItem(1,0,QTableWidgetItem(f"{self.Data_Loader.multi_info.loc[name,'AR']*100:.2f}%"))
        self.TableWidget.setItem(1,1,QTableWidgetItem(f"{self.Data_Loader.multi_adjusted_info.loc[name,'AR']*100:.2f}%"))
        self.TableWidget.setItem(2,0,QTableWidgetItem(f"{self.Data_Loader.multi_info.loc[name,'DrawDown']*100:.2f}%"))
        self.TableWidget.setItem(2,1,QTableWidgetItem(f"{self.Data_Loader.multi_adjusted_info.loc[name,'DrawDown']*100:.2f}%"))
        # 推荐列表导入
        self.rec_list_model = QStringListModel(self.Data_Loader.get_rec_list(name=name))
        self.RecList.setModel(self.rec_list_model)
        # 绘制
        self.Graph.drawGraph(self.Data_Loader.get_multi_data(name))
        
    def add_shadow(self,module):
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
     
    @Slot()
    def load_data_finished(self):
        """init_list"""
        self.init_list_and_ring()
        
class Load_Single_Stock_Thread(QThread):
    @staticmethod
    def add_MACD(data:pd.DataFrame):
        """DIF DEA MACD"""
        data['DIF'] = data['close'].ewm(span=12).mean() - data['close'].ewm(span=26).mean()
        data['DEA'] = data['DIF'].ewm(span=9).mean()
        data = data.dropna()
        data['MACD'] = 2*(data['DIF']-data['DEA'])
        return data
    @staticmethod
    def add_RSI(data = pd.DataFrame(), span = 5):
        """RSI"""
        data['change'] = data['close']-data['open']
        data['change-minus'] = 0
        data['change-pos'] = 0
        data.loc[data['change']<0,'change-minus'] = data['change'].abs()
        data.loc[data['change']>=0,'change-pos'] = data['change']
        data['avg-minus'] = data['change-minus'].ewm(span=span).mean()
        data['avg-pos'] = data['change-pos'].ewm(span=span).mean()
        data['RSI']=(data['avg-pos']/(data['avg-pos']+data['avg-minus']))
        data.drop(columns=['change','change-minus','change-pos','avg-minus','avg-pos'],inplace=True)
        return data
    @staticmethod
    def add_BOLLING(data = pd.DataFrame(), window = 5, k1 = 0.35, k2 = 0.35): #策略参数：window为均值化处理窗口；k1为下阈值；k2为上阈值；
        data['HH'] = data['high'].rolling(window=window,).max()
        data['LC'] = data['close'].rolling(window=window).min()
        data['HC'] = data['close'].rolling(window=window).max()
        data['LL'] = data['low'].rolling(window=window).min()
        data['price'] = (data['open']+data['close'])/2
        data['MA'] = data['close'].rolling(window=window).mean()
        data['HH-LC'] = data['HH']-data['LC']
        data['HC-LL'] = data['HC']-data['LL']
        data['range'] = data.loc[:,['HH-LC','HC-LL']].max(axis=1)
        data['TOP'] = data['MA']+data['range']*k2
        data['BOTTOM'] = data['MA']-data['range']*k1
        data.drop(columns=['HH','LC','HC','LL','price','MA','HH-LC','HC-LL','range'],inplace=True)
        return data
    # signals
    load_finish = Signal()
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.code = ""
    def set_code(self,code:str)->None:
        self.code = code
    def run(self):
        # progress run below
        self.load_data()
        self.load_news()
        self.load_finish.emit()
        
    def load_data(self):
        try:
            with pymysql.connect(host="sh-cdb-f2ryw6bk.sql.tencentcdb.com",
                                 user="ZHT",
                                 password="ZHT5201314",
                                 database="stock",
                                 port=63930) as connection:
                SQL =f"""SELECT trade_date,open,high,low,close,vol,amount
                         FROM origin_data
                         WHERE ts_code = '{self.code}'"""
                self.temp_data = pd.read_sql(sql=SQL,con=connection)
                self.temp_data['trade_date'] = pd.to_datetime(self.temp_data['trade_date'])
                self.temp_data = self.add_RSI(self.temp_data)
                self.temp_data = self.add_MACD(self.temp_data)
                self.temp_data = self.add_BOLLING(self.temp_data)
        except pymysql.MySQLError as e: print(f"数据库错误: {e}")
        except Exception as e: print(f"其他错误: {e}")
    def load_news(self):
        try:
            with pymysql.connect(host="sh-cdb-f2ryw6bk.sql.tencentcdb.com",
                                 user="ZHT",
                                 password="ZHT5201314",
                                 database="stock",
                                 port=63930) as connection:
                SQL = f"""SELECT title
                          FROM newsdata
                          WHERE stock_code = '{self.code[:-3]}'
                          ORDER BY date DESC"""
                with connection.cursor() as cursor:
                    cursor.execute(SQL)  # 执行查询
                    result = cursor.fetchall()  # 获取所有结果
                    self.news_list = [news[0] for news in result]
        except pymysql.MySQLError as e: print(f"数据库错误: {e}")
        except Exception as e: print(f"其他错误: {e}")
        
class Win_Single_Stock(QWidget,Ui_Single_Stock):    
    # K_Line_plotly暂存数据
    temp_file_plotly=tempfile.NamedTemporaryFile(mode="wb", suffix=".html", delete=False) 
    def __init__(self,parent=None):
        super(Win_Single_Stock,self).__init__(parent=parent)
        self.start_time = "20210101"
        self.end_time = "20220101"
        self.DB_data = Load_Single_Stock_Thread(self)
        self.DB_data.load_finish.connect(self.implement_data)
        self.setupUi(self)
        self.__init_CodeList()
        self.CodeList.clicked.connect(self.click_to_pick_stock)
        self.add_shadow(self.StockName)
        self.add_shadow(self.PreviewAmount)
        self.add_shadow(self.PreviewBolling)
        self.add_shadow(self.PreviewKline)
        self.add_shadow(self.PreviewMACD)
        self.add_shadow(self.PreviewRSI)
        self.add_shadow(self.PreviewVolumn)
        self.ExeShowKline.clicked.connect(self.plotly_K_line)
        self.ExeShowAmount.clicked.connect(self.plotly_AMOUNT)
        self.ExeShowVolumn.clicked.connect(self.plotly_VOL)
        self.ExeShowRSI.clicked.connect(self.plotly_RSI)
        self.ExeShowMACD.clicked.connect(self.plotly_MACD)
        self.ExeShowBolling.clicked.connect(self.plotly_Bolling)
        self.ExeReDrawTime.clicked.connect(self.reload_time)
        
    def __init_CodeList(self):
        try:
            with pymysql.connect(host="sh-cdb-f2ryw6bk.sql.tencentcdb.com",
                                 user="ZHT",
                                 password="ZHT5201314",
                                 database="stock",
                                 port=63930) as connection:
                SQL = """SELECT ts_code
                         FROM origin_data
                         GROUP BY ts_code"""
                with connection.cursor() as cursor:
                    cursor.execute(SQL)  # 执行查询
                    result = cursor.fetchall()  # 获取所有结果
                    self.codes = [pack[0] for pack in result]
        except pymysql.MySQLError as e: print(f"数据库错误: {e}")
        except Exception as e: print(f"其他错误: {e}")
        self.code_list_model = QStringListModel(self.codes)
        self.CodeList.setModel(self.code_list_model)
        
    def add_shadow(self,module):
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(3,3)
        self.effect_shadow.setBlurRadius(10)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
        
    def showInfo(self,content:str):
        info = InfoBar.info(title='Process',
                            content=content,
                            orient=Qt.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.TOP_LEFT,
                            duration=5000,
                            parent=self)
        info.show()
        
    def reload_time(self):
        self.start_time = self.StartTimePicker.getDate().toString("yyyyMMdd")
        self.end_time = self.EndTimePicker.getDate().toString("yyyyMMdd")
        
    def click_to_pick_stock(self,item):
        code = self.code_list_model.data(item)
        self.DB_data.set_code(code)
        self.DB_data.start()
        
    @Slot()
    def implement_data(self):
        self.showInfo("Load Data Finish")
        self.DB_data.quit()
        self.DB_data.wait()
        # load into news
        self.news_list = self.DB_data.news_list
        self.news_list_model = QStringListModel(self.news_list)
        self.StockInfo.setModel(self.news_list_model)
        # load into graphs
        self.temp_data = self.DB_data.temp_data
        self.pre_LineChart(self.temp_data['RSI'].tail(200),self.PreviewRSI)
        self.pre_LineChart(self.temp_data['MACD'].tail(200),self.PreviewMACD)
        self.pre_LineChart(self.temp_data['close'].tail(200),self.PreviewBolling)
        self.pre_LineChart(self.temp_data['high'].tail(200),self.PreviewKline)
        self.pre_BarChart(self.PreviewAmount)
        self.pre_BarChart(self.PreviewVolumn)
        self.plotly_K_line()
        
    def pre_LineChart(self,series:pd.Series,widget_to_chart:QChartView):
        #面积图的上下两条曲线
        self.line0 = QLineSeries()
        self.line1 = QLineSeries()
        self.line = QLineSeries()
        count=0
        step=20
        min_value = series.min()
        while count<(series.shape[0]):
            self.line<<QPointF(count,series.iloc[count]-min_value)
            self.line0<<QPointF(count,series.iloc[count]-min_value)
            self.line1<<QPointF(count,0)
            count+=step
        self.line.setPointsVisible(False)
        #面积图
        areaSeries = QAreaSeries(self.line0, self.line1)
        pen = QPen(QColor(0,0,0,0))
        pen.setWidth(3)
        areaSeries.setPen(pen)
        pen_true = QPen(QColor(69,143,211))
        pen_true.setWidth(3)
        self.line.setPen(pen_true)
        #渐变设置
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        color = QColor(69,143,211)
        color.setAlpha(70)
        brush = QBrush(color)# 设置透明度为 0.5
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        areaSeries.setBrush(gradient)
        brush = QBrush(gradient)
        #创建图表
        chart = QChart()
        chart.setMargins(QMargins(0,0,0,0))
        chart.addSeries(areaSeries)
        chart.addSeries(self.line)
        chart.createDefaultAxes()
        chart.axes(orientation=Qt.Orientation.Horizontal)
        chart.axisY().setVisible(False)
        chart.axisY().setGridLineVisible(False)
        chart.axisX().setVisible(False)
        chart.legend().hide()
        #图表视图
        widget_to_chart.setChart(chart)
        widget_to_chart.setRenderHint(QPainter.Antialiasing)
        
    def pre_BarChart(self,widget_to_chart:QChartView):
        set1 = QBarSet("day1")
        set2 = QBarSet("day2")
        set3 = QBarSet("day3")
        set4 = QBarSet("day4")
        set5 = QBarSet("day5")
        set1 << random.randint(1,5) << 0 << 0 << 0 << 0      #只能修改非零数
        set2 << 0 << random.randint(1,5) << 0 << 0 << 0      #只能修改非零数
        set3 << 0 << 0 << random.randint(1,5) << 0 << 0      #只能修改非零数
        set4 << 0 << 0 << 0 << random.randint(1,5) << 0      #只能修改非零数
        set5 << 0 << 0 << 0 << 0 << random.randint(1,5)      #只能修改非零数
        for bar_set in [set1, set2, set3, set4, set5]:
            for i in range(bar_set.count()):
                if bar_set.at(i)>0:
                    bar_set.setColor(QColor(255, 165, 0))  # 正数为橙黄色
                elif bar_set.at(i)<0:
                    bar_set.setColor(QColor(139, 0, 0))  # 负数为深红色
        series = QStackedBarSeries()
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        series.append(set5)
        chart = QChart()
        chart.setMargins(QMargins(0,0,0,0))
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        categories = ["day 1","day 2","day 3","day 4","day 5"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.setAxisX(axisX, series)
        # create the Y-axis object
        axisY = QValueAxis()
        axisY.setGridLineVisible(False) # turn off grid lines
        # add Y-axis to the chart
        chart.addAxis(axisY, Qt.AlignLeft) # set alignment and position
        # associate Y-axis with the series
        series.attachAxis(axisY)
        axisY.setLabelsVisible(False)  # 隐藏y轴标签
        axisX.setLabelsFont(QFont("Arial", 7, QFont.Bold)) # 设置x轴标签字体为加粗的Arial，大小为10
        chart.legend().hide()
        bar_width = 0.85
        series.setBarWidth(bar_width)
        widget_to_chart.setChart(chart)
        widget_to_chart.setRenderHint(QPainter.Antialiasing)
        widget_to_chart.setBackgroundBrush(Qt.transparent)
        
    def plotly_K_line(self):
        temp_data = self.temp_data[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        avg_days = [5, 10, 20]
        line_color = {"MA5": 'yellow', "MA10": 'purple', "MA20": 'blue'}
        fig = go.Figure(data=[go.Candlestick(x=temp_data['trade_date'],
                                            open=temp_data['open'],
                                            high=temp_data['high'],
                                            low=temp_data['low'],
                                            close=temp_data['close'],
                                            increasing_line_color='red', decreasing_line_color='green',
                                            name='日K线')])
        for avg_day in avg_days:
            avg_column_name = 'avg_' + str(avg_day)
            avg_line_name = 'MA' + str(avg_day)
            temp_data[avg_column_name] = temp_data['close'].rolling(avg_day).mean()
            fig.add_trace(go.Scatter(x=temp_data['trade_date'], y=temp_data[avg_column_name], name=avg_line_name, line={'color': line_color[avg_line_name]}))
        fig.update_layout(
            title=None,  # 标题
            yaxis_title=None,  # y轴名称
            margin=dict(l=0, r=0, b=0, t=0),
            plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=False)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        
    def plotly_Bolling(self):
        temp_data = self.temp_data[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        fig = go.Figure(data=[go.Candlestick(x=temp_data['trade_date'],
                                            open=temp_data['open'],
                                            high=temp_data['high'],
                                            low=temp_data['low'],
                                            close=temp_data['close'],
                                            increasing_line_color='red', decreasing_line_color='green',
                                            name='日K线')])

        fig.add_trace(go.Scatter(x=temp_data['trade_date'], y=temp_data['TOP'], name='TOP', line={'color': 'purple'}))
        fig.add_trace(go.Scatter(x=temp_data['trade_date'], y=temp_data['BOTTOM'], name='BOTTOM', line={'color': 'blue'}))
        fig.update_layout(
            title=None,  # 标题
            yaxis_title=None,  # y轴名称
            margin=dict(l=0, r=0, b=0, t=0),
            plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=False)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        
    def plotly_VOL(self):
        temp_data = self.temp_data.loc[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        fig = px.bar(temp_data,x="trade_date",y="volume")
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_layout(showlegend=False)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        
    def plotly_RSI(self):
        temp_data = self.temp_data.loc[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        fig = px.line(temp_data, x='trade_date', y='RSI', title=None)
        fig.add_hline(y=temp_data['RSI'].max()*0.8)
        fig.add_hline(y=temp_data['RSI'].max()*0.2)
        #显示x轴滑图
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
                yaxis_visible = False,
                margin=dict(l=0, r=0, b=0, t=0),
                plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=True)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        
    def plotly_MACD(self):
        temp_data = self.temp_data.loc[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        fig = px.line(temp_data, x='trade_date', y='MACD', title=None)
        fig.add_hline(y=0)
        
        #显示x轴滑图
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
                yaxis_visible = False,
                margin=dict(l=0, r=0, b=0, t=0),
                plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=True)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        
    def plotly_AMOUNT(self):
        temp_data = self.temp_data.loc[(self.temp_data['trade_date']>=pd.Timestamp(self.start_time))&(self.temp_data['trade_date']<=pd.Timestamp(self.end_time))]
        #=============在此处更改图片=============#
        fig = px.bar(temp_data,x="trade_date",y="amount")
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_layout(showlegend=False)
        #=============在此处更改图片=============#
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"
        
        self.temp_file_plotly.write(html.encode('GB18030'))
        self.temp_file_plotly.truncate()
        self.temp_file_plotly.seek(0)
        self.PlotlyGraph.load(QUrl.fromLocalFile(self.temp_file_plotly.name))
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Data_Loader = Data_Loading_Thread()
    Waiting = Win_Waiting(Data_Loader=Data_Loader)
    Main = Main_Win(Data_Loader=Data_Loader)
    
    sys.exit(app.exec())
