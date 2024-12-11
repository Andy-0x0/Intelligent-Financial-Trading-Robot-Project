import pandas as pd
import sys


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,QStringListModel, QThread, Signal,
    QSize, QTime, QUrl, Qt, Slot)
from PySide6.QtGui import ( QIcon, QCloseEvent, QKeySequence,QCursor)
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget, QListWidgetItem,QMenu,
    QTableWidgetItem, QVBoxLayout, QWidget, QTreeWidget,QTreeWidgetItem)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QGraphicsDropShadowEffect

from qfluentwidgets import SplitFluentWindow, FluentIcon

from API_DB import (Local_DB_Processor, Remote_DB_Processer,
                    Update_Rec_Thread,
                    Check_Thread, Update_Local_DB_Thread,
                    Update_Remote_DB_Thread_for_Standard,
                    Update_Remote_DB_Thread_for_Multi)
from UI import Ui_StockInfo, Ui_PortfolioInfo, Ui_MixSup

class Win_Main(SplitFluentWindow):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowIcon(QIcon("MrSakamoto-small.ico"))
        
        self.Local_DB = Local_DB_Processor()
        self.Remote_DB = Remote_DB_Processer()
        
        self.Win_MixSup = Win_MixSup(self.Local_DB,self.Remote_DB,self)
        self.Win_StockInfo = Win_StockInfo(self.Local_DB,self)
        self.Win_PortfolioInfo = Win_PortfolioInfo(self.Local_DB,self.Remote_DB,self)
        
        self.addSubInterface(self.Win_MixSup,FluentIcon.ACCEPT,"总成")
        self.addSubInterface(self.Win_StockInfo,FluentIcon.BOOK_SHELF,'单因子')
        self.addSubInterface(self.Win_PortfolioInfo,FluentIcon.DOCUMENT,'多因子')
    def closeEvent(self, origin_closeEvent:QCloseEvent):
        super().closeEvent(origin_closeEvent)
        self.Local_DB.close_connection()
        self.Remote_DB.close_connection()
        print("closed")
        
class Win_MixSup(QWidget,Ui_MixSup):
    method_list = ["mom-rob","mom-dif-rob","MACD-rob","RSI-rob","Vol-rob","Amo-rob","VWR-rob","VUS-rob","STD-rob","ATR-rob","Vot-Idea",
                   "Equal","PCA-like","Gradual","SVM","DecTree","XGBoost","LSTM","GRU","LSTM-Att","GRU-Att"]
    def __init__(self,Local_DB:Local_DB_Processor,Remote_DB:Remote_DB_Processer,parent=None):
        super(Win_MixSup,self).__init__(parent=parent)
        self.Local_DB = Local_DB
        self.Remote_DB = Remote_DB
        self.setupUi(self)
        self.add_shadow(self.RecFrame)
        self.add_shadow(self.LeverFrame)
        # 进程设置
        self.update_rec_processor = Update_Rec_Thread(len(self.method_list))
        self.update_rec_processor.count_signal.connect(self.flush_Update_Rec)
        self.update_rec_processor.finished_signal.connect(self.finish_Update_Rec)
        # 控件设置
        self.LeverSlider.valueChanged.connect(self.do_SliderChange)
        self.LeverSlider.setValue(5)
        self.LeverGraph.drawGraph(self.Remote_DB.read_index_data())
        self.RecRing.setRange(0,len(self.method_list))
        self.RecListModel = QStringListModel(self.method_list)
        self.RecList.setModel(self.RecListModel)
        self.RecLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RecLabel.setText(f"{0}/{len(self.method_list)}")
        self.ExeRecUpdate.clicked.connect(self.do_update_rec)
    ### 按钮控制槽函数    
    def do_SliderChange(self,num):
        self.LeverRate.setText(f"{num/10}%")
    def do_update_rec(self):
        self.ExeRecUpdate.setEnabled(False)
        self.update_rec_processor.start()
    ### 进程控制槽函数
    @Slot(int)
    def flush_Update_Rec(self,count:int):
        """刷新Update进度"""
        self.RecRing.setValue(count)
        self.RecLabel.setText(f"{count}/{len(self.method_list)}")
    @Slot()
    def finish_Update_Rec(self):
        """推荐列表更新完成"""
        self.update_rec_processor.quit()
        self.update_rec_processor.wait()
        self.ExeRecUpdate.setEnabled(True)
        QMessageBox.information(self,"更新完成","推荐列表更新完成",QMessageBox.Ok)
    ### 特效函数
    def add_shadow(self,module):
        """阴影特效"""
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
        
        
class Win_StockInfo(QWidget,Ui_StockInfo):
    def __init__(self,Local_DB:Local_DB_Processor,parent=None):
        super(Win_StockInfo,self).__init__(parent=parent)
        self.Local_DB = Local_DB
        self.setupUi(self)
        self.add_shadow(self.StatusFrame)
        self.add_shadow(self.UpdateFrame)
        self.init_table_and_rings()
        # 状态检查进程设置
        self.check_processer = Check_Thread(self.stock_count)
        self.check_processer.count_signal.connect(self.flush_Status)
        self.check_processer.finished_signal.connect(self.finish_Status)
        # 更新进程设置
        self.update_processer = Update_Local_DB_Thread()
        self.update_processer.count_signal.connect(self.flush_Update)
        self.update_processer.finished_signal.connect(self.finish_Update)
        self.update_processer.tushare_failure_signal.connect(self.tushare_failure)
        # 按钮控件设置
        self.ExeStatusCheck.clicked.connect(self.do_check_status)
        self.ExeUpdate.clicked.connect(self.do_update)    
    def init_table_and_rings(self):
        # read info 
        self.stock_info = self.Local_DB.read_stock_info()
        self.stock_count = self.stock_info.shape[0]
        # init table
        self.StockInfoTable.clearContents()
        self.StockInfoTable.setRowCount(self.stock_info.shape[0])
        for i in range(self.stock_info.shape[0]):
            for j in range(self.stock_info.shape[1]):
                self.StockInfoTable.setItem(i,j,QTableWidgetItem(self.stock_info.iloc[i,j]))
        # init status ring
        self.StatusRing.setRange(0,self.stock_info.shape[0])
        self.StatusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.StatusLabel.setText(f"{0}/{self.stock_info.shape[0]}")
        # init update ring
        self.UpdateRing.setRange(0,self.stock_info.shape[0])
        self.UpdateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.UpdateLabel.setText(f"{0}/{self.stock_info.shape[0]}")
    ### 按钮控制槽函数    
    def do_check_status(self):
        self.check_processer.start()
        self.ExeStatusCheck.setEnabled(False)
    def do_update(self):
        self.update_processer.start()
        self.ExeUpdate.setEnabled(False)   
    ### 进程控制槽函数
    @Slot(int)
    def flush_Status(self,count:int):
        """刷新Status检查进度"""
        self.StatusRing.setValue(count)
        self.StatusLabel.setText(f"{count}/{self.stock_info.shape[0]}")
    @Slot()
    def finish_Status(self):
        """Status检查完成"""
        self.check_processer.quit()
        self.check_processer.wait()
        self.ExeStatusCheck.setEnabled(True)
        QMessageBox.information(self,"检查完成","所有股票状态正常",QMessageBox.Ok)
    @Slot(int)
    def flush_Update(self,count:int):
        """刷新Update进度"""
        self.UpdateRing.setValue(count)
        self.UpdateLabel.setText(f"{count}/{self.stock_info.shape[0]}")
    @Slot()
    def finish_Update(self):
        """Update完成"""
        # self.update_processer.Local_DB.close_connection()
        self.update_processer.quit()
        self.update_processer.wait()
        self.ExeUpdate.setEnabled(True)
        QMessageBox.information(self,"更新完成","所有股票更新完成",QMessageBox.Ok)
    @Slot()
    def tushare_failure(self):
        """大概是tushare炸了"""
        QMessageBox.warning(self,"tushare错误！！","有可能tushare炸了，有可能代码写错了，但是更有可能tushare炸了！！！",QMessageBox.Ok)
    ### 特效函数
    def add_shadow(self,module):
        """阴影特效"""
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
        
class Win_PortfolioInfo(QWidget,Ui_PortfolioInfo):
    def __init__(self,Local_DB:Local_DB_Processor,Remote_DB:Remote_DB_Processer,parent=None):
        super(Win_PortfolioInfo,self).__init__(parent=parent)
        self.Local_DB = Local_DB
        self.Remote_DB = Remote_DB
        self.setupUi(self)
        self.add_shadow(self.StandardFrame)
        self.add_shadow(self.MultiFrame)
        self.add_shadow(self.MLFrame)
        self.init_table_and_rings()
        # 单因子进程设置
        self.update_Standard_process = Update_Remote_DB_Thread_for_Standard()
        self.update_Standard_process.count_signal.connect(self.flush_Standard)
        self.update_Standard_process.progress_signal.connect(self.progress_Standard)
        self.update_Standard_process.finished_signal.connect(self.finish_Standard)
        # 多因子进程设置
        self.update_Multi_process = Update_Remote_DB_Thread_for_Multi()
        self.update_Multi_process.Multi_count_signal.connect(self.flush_Multi)
        self.update_Multi_process.Multi_progress_signal.connect(self.progress_Multi)
        self.update_Multi_process.ML_count_signal.connect(self.flush_ML)
        self.update_Multi_process.ML_progress_signal.connect(self.progress_ML)
        self.update_Multi_process.finished_signal.connect(self.finish_Multi)
        # 按钮控件设置
        self.ExeStandardUpdate.clicked.connect(self.do_update_Stantard)
        self.ExeMultiUpdate.clicked.connect(self.do_update_Multi)
    def init_table_and_rings(self):
        # read info 
        self.indicator_info    = self.Remote_DB.read_index_info()
        self.method_info       = self.Remote_DB.read_method_info()
        self.Multi_method_info = self.method_info[self.method_info['type']=='Multi']
        self.ML_method_info    = self.method_info[self.method_info['type']=='LM']
        # init list
        self.Standard_list_model = QStringListModel(self.indicator_info['name'].tolist())
        self.Multi_list_model    = QStringListModel(self.Multi_method_info['method'].tolist())
        self.ML_list_model       = QStringListModel(self.ML_method_info['method'].tolist())
        self.StandardList.setModel(self.Standard_list_model)
        self.MultiList.setModel(self.Multi_list_model)
        self.MLList.setModel(self.ML_list_model)
        # init Standard ring and bar
        self.StandardRing.setRange(0,self.indicator_info.shape[0])
        self.StandardBar.setRange(0,3)
        self.StandardLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.StandardLabel.setText(f"{0}/{self.indicator_info.shape[0]}")
        # init Multi ring and bar
        self.MultiRing.setRange(0,self.Multi_method_info.shape[0])
        self.MultiBar.setRange(0,3)
        self.MultiLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.MultiLabel.setText(f"{0}/{self.Multi_method_info.shape[0]}")
        # init ML ring and bar
        self.MLRing.setRange(0,self.ML_method_info.shape[0])
        self.MLBar.setRange(0,3)
        self.MLLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.MLLabel.setText(f"{0}/{self.ML_method_info.shape[0]}")
    ### 按钮控制槽函数    
    def do_update_Stantard(self):
        self.update_Standard_process.start()
        self.ExeStandardUpdate.setEnabled(False)  
    def do_update_Multi(self):
        self.update_Multi_process.start()
        self.ExeMultiUpdate.setEnabled(False)
    ### 进程控制槽函数
    @Slot(int)
    def flush_Standard(self,count:int):
        """刷新Standard进度"""
        self.StandardRing.setValue(count)
        self.StandardLabel.setText(f"{count}/{self.indicator_info.shape[0]}")
    @Slot(int)
    def progress_Standard(self,count:int):
        """刷新Standard进度"""
        self.StandardBar.setValue(count)
    @Slot()
    def finish_Standard(self):
        """Standard更新完成"""
        self.update_Standard_process.quit()
        self.update_Standard_process.wait()
        self.ExeStandardUpdate.setEnabled(True)
        QMessageBox.information(self,"更新完成","单因子更新完成",QMessageBox.Ok)
    @Slot(int)
    def flush_Multi(self,count:int):
        """刷新Multi进度"""
        self.MultiRing.setValue(count)
        self.MultiLabel.setText(f"{count}/{self.Multi_method_info.shape[0]}")
    @Slot(int)
    def progress_Multi(self,count:int):
        """刷新Multi进度"""
        self.MultiBar.setValue(count)
    @Slot(int)
    def flush_ML(self,count:int):
        """刷新Multi进度"""
        self.MLRing.setValue(count)
        self.MLLabel.setText(f"{count}/{self.ML_method_info.shape[0]}")
    @Slot(int)
    def progress_ML(self,count:int):
        """刷新Multi进度"""
        self.MLBar.setValue(count)
    @Slot()
    def finish_Multi(self):
        """Multi更新完成"""
        self.update_Multi_process.quit()
        self.update_Multi_process.wait()
        self.ExeMultiUpdate.setEnabled(True)
        QMessageBox.information(self,"更新完成","多因子更新完成",QMessageBox.Ok)
    ### 特效函数
    def add_shadow(self,module):
        """阴影特效"""
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2,2)
        self.effect_shadow.setBlurRadius(6)
        self.effect_shadow.setColor(Qt.gray)
        module.setGraphicsEffect(self.effect_shadow)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Win_Main()
    Main.show()
    
    # Login.setMicaEffectEnabled(True)
    sys.exit(app.exec())



