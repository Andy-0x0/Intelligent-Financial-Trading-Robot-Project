# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QSizePolicy, QLabel,
                               QSpacerItem, QTableWidgetItem, QVBoxLayout, QWidget)

from PySide6.QtCharts import QChartView

from qfluentwidgets import (ProgressBar, ProgressRing, SegmentedWidget,
                            SubtitleLabel, StrongBodyLabel, SubtitleLabel, 
                            TableWidget, ListView, DatePicker,
                            HorizontalSeparator, VerticalSeparator,
                            PrimaryPushButton,TransparentPushButton)

from qframelesswindow.webengine import FramelessWebEngineView


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class MatplotlibLineWidget(QWidget):
    # ÏßÍ¼µÄMatplotlib
    def __init__(self,parent):
        super(MatplotlibLineWidget, self).__init__(parent=parent)
        self.setObjectName(u"Ui_MatplotLib")
        self.setupUi()
    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.fig = plt.figure(figsize=(10, 6))
        self.mpl = FigureCanvas(self.fig)
        self.layout.addWidget(self.mpl)
    def drawGraph(self,ori_df:pd.DataFrame):
        self.ori_df = ori_df.iloc[::5,:]
        self.ori_df = self.ori_df.interpolate(method='akima').ffill().bfill()
        self.lower_bound = ori_df.min().min()
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Test Data', fontsize=15)
        self.ax.set_xlabel('Date', fontsize=12)
        self.ax.set_ylabel('Value', fontsize=12)

        self.ax.grid(True, axis='y', linestyle='--', linewidth=0.5)
        self.ax.grid(False, axis='x')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['left'].set_visible(False)
        
        colors = ['#0066cc', '#ff9933', '#339966']
        for i, column in enumerate(self.ori_df.columns):
            self.ax.plot(self.ori_df.index, self.ori_df[column], lw=0.97, color=colors[i], label=column)
            y = self.ori_df[column].values
            self.ax.fill_between(self.ori_df.index, y, self.lower_bound, color=colors[i], alpha=0.2, where=(y > self.lower_bound), interpolate=True)
        self.ax.legend(fontsize=10, shadow=True, frameon=False)
        self.mpl.draw() 
        
class MatplotlibBarWidget(QWidget):
    # ÖùÍ¼µÄMatplotlib
    def __init__(self,parent):
        super(MatplotlibBarWidget, self).__init__(parent=parent)
        self.setObjectName(u"Ui_MatplotLib")
        self.setupUi()
    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.fig = plt.figure(figsize=(10, 6))
        self.mpl = FigureCanvas(self.fig)
        self.layout.addWidget(self.mpl)
    def drawGraph(self,rank_dict:dict):
        self.codes = list(rank_dict.keys())[:30]
        self.counts = [rank_dict[code] for code in self.codes]
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Recommend Stocks', fontsize=15)
        self.ax.set_ylabel('Recommend Count', fontsize=12)

        self.ax.grid(True, axis='y', linestyle='--', linewidth=0.5)
        self.ax.grid(False, axis='x')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['left'].set_visible(False)
        
        x_postition = range(len(self.codes))
        self.ax.bar(x=x_postition,height=self.counts)
        self.ax.set_xticks(x_postition)
        self.ax.set_xticklabels(self.codes,rotation=90,ha='center',va='top')
        
        
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.tick_top()

        self.mpl.draw() 

################################################################################
## Form generated from reading UI file 'templateerRodN.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(897, 834)
        Form.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.horizontalLayout_4 = QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.FunctionList = ListView(Form)
        self.FunctionList.setObjectName(u"FunctionList")
        self.FunctionList.setMinimumSize(QSize(150, 0))
        self.FunctionList.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_4.addWidget(self.FunctionList)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.PortfolioProgressBar = ProgressBar(Form)
        self.PortfolioProgressBar.setObjectName(u"PortfolioProgressBar")
        self.PortfolioProgressBar.setMinimumSize(QSize(200, 4))
        self.horizontalLayout.addWidget(self.PortfolioProgressBar)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.MainFrame = QFrame(Form)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_10 = QHBoxLayout(self.MainFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 5, 5, 5)
        self.Graph = MatplotlibLineWidget(self.MainFrame)
        self.Graph.setObjectName(u"Graph")
        self.Graph.setMinimumSize(QSize(470, 260))
        # self.Graph.setMaximumSize(QSize(400, 230))
        self.horizontalLayout_10.addWidget(self.Graph)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.TableWidget = TableWidget(self.MainFrame)
        if (self.TableWidget.columnCount() < 2):
            self.TableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.TableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.TableWidget.rowCount() < 3):
            self.TableWidget.setRowCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.TableWidget.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.TableWidget.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.TableWidget.setVerticalHeaderItem(2, __qtablewidgetitem4)
        self.TableWidget.setObjectName(u"TableWidget")
        self.TableWidget.setMinimumSize(QSize(301, 160))
        self.TableWidget.setMaximumSize(QSize(301, 160))
        self.verticalLayout_4.addWidget(self.TableWidget)
        self.horizontalLayout_10.addLayout(self.verticalLayout_4)
        self.gridLayout_2.addWidget(self.MainFrame, 1, 0, 1, 3)
        self.TextFrame = QFrame(Form)
        self.TextFrame.setObjectName(u"TextFrame")
        self.TextFrame.setStyleSheet(u"border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.TextFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.FunctionTitle = SubtitleLabel(self.TextFrame)
        self.FunctionTitle.setObjectName(u"FunctionTitle")
        self.FunctionTitle.setMinimumSize(QSize(150, 50))
        self.FunctionTitle.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout.addWidget(self.FunctionTitle)
        self.FunctionLabel = StrongBodyLabel(self.TextFrame)
        self.FunctionLabel.setObjectName(u"FunctionLabel")
        self.FunctionLabel.setMinimumSize(QSize(150, 200))
        self.FunctionLabel.setMaximumSize(QSize(300, 16777215))
        self.FunctionLabel.setMargin(0)
        self.verticalLayout.addWidget(self.FunctionLabel)
        self.gridLayout_2.addWidget(self.TextFrame, 0, 0, 1, 1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.ICFrame = QFrame(Form)
        self.ICFrame.setObjectName(u"ICFrame")
        self.ICFrame.setMinimumSize(QSize(130, 60))
        self.ICFrame.setMaximumSize(QSize(130, 60))
        self.ICFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_3 = QHBoxLayout(self.ICFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ICTitle = StrongBodyLabel(self.ICFrame)
        self.ICTitle.setObjectName(u"ICTitle")

        self.verticalLayout_3.addWidget(self.ICTitle)

        self.IC = StrongBodyLabel(self.ICFrame)
        self.IC.setObjectName(u"IC")

        self.verticalLayout_3.addWidget(self.IC)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.ICRing = ProgressRing(self.ICFrame)
        self.ICRing.setObjectName(u"ICRing")
        self.ICRing.setMinimumSize(QSize(50, 50))
        self.ICRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_3.addWidget(self.ICRing)


        self.gridLayout.addWidget(self.ICFrame, 0, 1, 1, 1)

        self.RankICFrame = QFrame(Form)
        self.RankICFrame.setObjectName(u"RankICFrame")
        self.RankICFrame.setMinimumSize(QSize(130, 60))
        self.RankICFrame.setMaximumSize(QSize(130, 60))
        self.RankICFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_2 = QHBoxLayout(self.RankICFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.RankICTitle = StrongBodyLabel(self.RankICFrame)
        self.RankICTitle.setObjectName(u"RankICTitle")

        self.verticalLayout_2.addWidget(self.RankICTitle)

        self.RankIC = StrongBodyLabel(self.RankICFrame)
        self.RankIC.setObjectName(u"RankIC")

        self.verticalLayout_2.addWidget(self.RankIC)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.RankICRing = ProgressRing(self.RankICFrame)
        self.RankICRing.setObjectName(u"RankICRing")
        self.RankICRing.setMinimumSize(QSize(50, 50))
        self.RankICRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_2.addWidget(self.RankICRing)


        self.gridLayout.addWidget(self.RankICFrame, 0, 0, 1, 1)

        self.DrawDownFrame = QFrame(Form)
        self.DrawDownFrame.setObjectName(u"DrawDownFrame")
        self.DrawDownFrame.setMinimumSize(QSize(130, 60))
        self.DrawDownFrame.setMaximumSize(QSize(130, 60))
        self.DrawDownFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_8 = QHBoxLayout(self.DrawDownFrame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.DrawDownTitle = StrongBodyLabel(self.DrawDownFrame)
        self.DrawDownTitle.setObjectName(u"DrawDownTitle")
        self.DrawDownTitle.setEnabled(False)

        self.verticalLayout_8.addWidget(self.DrawDownTitle)

        self.DrawDown = StrongBodyLabel(self.DrawDownFrame)
        self.DrawDown.setObjectName(u"DrawDown")

        self.verticalLayout_8.addWidget(self.DrawDown)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)

        self.DrawDownRing = ProgressRing(self.DrawDownFrame)
        self.DrawDownRing.setObjectName(u"DrawDownRing")
        self.DrawDownRing.setMinimumSize(QSize(50, 50))
        self.DrawDownRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_8.addWidget(self.DrawDownRing)


        self.gridLayout.addWidget(self.DrawDownFrame, 2, 1, 1, 1)

        self.AnnualReturnFrame = QFrame(Form)
        self.AnnualReturnFrame.setObjectName(u"AnnualReturnFrame")
        self.AnnualReturnFrame.setMinimumSize(QSize(130, 60))
        self.AnnualReturnFrame.setMaximumSize(QSize(130, 60))
        self.AnnualReturnFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_9 = QHBoxLayout(self.AnnualReturnFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.AnnualReturnTitle = StrongBodyLabel(self.AnnualReturnFrame)
        self.AnnualReturnTitle.setObjectName(u"AnnualReturnTitle")

        self.verticalLayout_9.addWidget(self.AnnualReturnTitle)

        self.AnnualReturn = StrongBodyLabel(self.AnnualReturnFrame)
        self.AnnualReturn.setObjectName(u"AnnualReturn")

        self.verticalLayout_9.addWidget(self.AnnualReturn)


        self.horizontalLayout_9.addLayout(self.verticalLayout_9)

        self.AnnualReturnRing = ProgressRing(self.AnnualReturnFrame)
        self.AnnualReturnRing.setObjectName(u"AnnualReturnRing")
        self.AnnualReturnRing.setMinimumSize(QSize(50, 50))
        self.AnnualReturnRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_9.addWidget(self.AnnualReturnRing)


        self.gridLayout.addWidget(self.AnnualReturnFrame, 2, 0, 1, 1)

        self.IRFrame = QFrame(Form)
        self.IRFrame.setObjectName(u"IRFrame")
        self.IRFrame.setMinimumSize(QSize(130, 60))
        self.IRFrame.setMaximumSize(QSize(130, 60))
        self.IRFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_7 = QHBoxLayout(self.IRFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.IRTitle = StrongBodyLabel(self.IRFrame)
        self.IRTitle.setObjectName(u"IRTitle")

        self.verticalLayout_7.addWidget(self.IRTitle)

        self.IR = StrongBodyLabel(self.IRFrame)
        self.IR.setObjectName(u"IR")

        self.verticalLayout_7.addWidget(self.IR)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.IRRing = ProgressRing(self.IRFrame)
        self.IRRing.setObjectName(u"IRRing")
        self.IRRing.setMinimumSize(QSize(50, 50))
        self.IRRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_7.addWidget(self.IRRing)


        self.gridLayout.addWidget(self.IRFrame, 1, 0, 1, 1)

        self.SharpeFrame = QFrame(Form)
        self.SharpeFrame.setObjectName(u"SharpeFrame")
        self.SharpeFrame.setMinimumSize(QSize(130, 60))
        self.SharpeFrame.setMaximumSize(QSize(130, 60))
        self.SharpeFrame.setStyleSheet(u"border-radius:10px;")
        self.horizontalLayout_6 = QHBoxLayout(self.SharpeFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.SharpeTitle = StrongBodyLabel(self.SharpeFrame)
        self.SharpeTitle.setObjectName(u"SharpeTitle")

        self.verticalLayout_6.addWidget(self.SharpeTitle)

        self.Sharpe = StrongBodyLabel(self.SharpeFrame)
        self.Sharpe.setObjectName(u"Sharpe")

        self.verticalLayout_6.addWidget(self.Sharpe)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.SharpeRing = ProgressRing(self.SharpeFrame)
        self.SharpeRing.setObjectName(u"SharpeRing")
        self.SharpeRing.setMinimumSize(QSize(50, 50))
        self.SharpeRing.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_6.addWidget(self.SharpeRing)


        self.gridLayout.addWidget(self.SharpeFrame, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)

        self.RecList = ListView(Form)
        self.RecList.setObjectName(u"RecList")
        self.RecList.setMinimumSize(QSize(150, 0))
        self.RecList.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.RecList, 0, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_10)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.TableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Origin", None));
        ___qtablewidgetitem1 = self.TableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Adjusted", None));
        ___qtablewidgetitem2 = self.TableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Sharpe", None));
        ___qtablewidgetitem3 = self.TableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"AR", None));
        ___qtablewidgetitem4 = self.TableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"DrawDown", None));
        self.FunctionTitle.setText(QCoreApplication.translate("Form", u"", None))
        self.FunctionLabel.setText(QCoreApplication.translate("Form", u"", None))
        self.ICTitle.setText(QCoreApplication.translate("Form", u"IC", None))
        self.IC.setText("")
        self.RankICTitle.setText(QCoreApplication.translate("Form", u"RankIC", None))
        self.RankIC.setText("")
        self.DrawDownTitle.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u56de\u64a4", None))
        self.DrawDown.setText("")
        self.AnnualReturnTitle.setText(QCoreApplication.translate("Form", u"\u5e74\u5316\u6536\u76ca", None))
        self.AnnualReturn.setText("")
        self.IRTitle.setText(QCoreApplication.translate("Form", u"IR", None))
        self.IR.setText("")
        self.SharpeTitle.setText(QCoreApplication.translate("Form", u"Sharpe", None))
        self.Sharpe.setText("")
    # retranslateUi

################################################################################
## Form generated from reading UI file 'overallCdyIAN.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

class Ui_Overall(object):
    def setupUi(self, Overall):
        if not Overall.objectName():
            Overall.setObjectName(u"Overall")
        Overall.resize(770, 700)
        Overall.setMinimumSize(QSize(770, 700))
        self.gridLayout_2 = QGridLayout(Overall)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.StartegyRec = QFrame(Overall)
        self.StartegyRec.setObjectName(u"StartegyRec")
        # self.StartegyRec.setMinimumSize(QSize(330, 330))
        self.StartegyRec.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.StartegyRec)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.SubtitleLabel = SubtitleLabel(self.StartegyRec)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.verticalLayout.addWidget(self.SubtitleLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Method_Rank_1 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rank_1.setObjectName(u"Method_Rank_1")
        self.Method_Rank_1.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.Method_Rank_1)

        self.Method_prog_Rank_1 = ProgressBar(self.StartegyRec)
        self.Method_prog_Rank_1.setObjectName(u"Method_prog_Rank_1")
        self.Method_prog_Rank_1.setMaximumSize(QSize(100, 4))

        self.horizontalLayout_2.addWidget(self.Method_prog_Rank_1)

        self.Method_Rate_Rank_1 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rate_Rank_1.setObjectName(u"Method_Rate_Rank_1")
        self.Method_Rate_Rank_1.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.Method_Rate_Rank_1)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Method_Rank_2 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rank_2.setObjectName(u"Method_Rank_2")
        self.Method_Rank_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.Method_Rank_2)

        self.Method_prog_Rank_2 = ProgressBar(self.StartegyRec)
        self.Method_prog_Rank_2.setObjectName(u"Method_prog_Rank_2")
        self.Method_prog_Rank_2.setMaximumSize(QSize(100, 4))

        self.horizontalLayout_3.addWidget(self.Method_prog_Rank_2)

        self.Method_Rate_Rank_2 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rate_Rank_2.setObjectName(u"Method_Rate_Rank_2")
        self.Method_Rate_Rank_2.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.Method_Rate_Rank_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Method_Rank_3 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rank_3.setObjectName(u"Method_Rank_3")
        self.Method_Rank_3.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.Method_Rank_3)

        self.Method_prog_Rank_3 = ProgressBar(self.StartegyRec)
        self.Method_prog_Rank_3.setObjectName(u"Method_prog_Rank_3")
        self.Method_prog_Rank_3.setMaximumSize(QSize(100, 4))

        self.horizontalLayout_4.addWidget(self.Method_prog_Rank_3)

        self.Method_Rate_Rank_3 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rate_Rank_3.setObjectName(u"Method_Rate_Rank_3")
        self.Method_Rate_Rank_3.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_4.addWidget(self.Method_Rate_Rank_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.Method_Rank_4 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rank_4.setObjectName(u"Method_Rank_4")
        self.Method_Rank_4.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.Method_Rank_4)

        self.Method_prog_Rank_4 = ProgressBar(self.StartegyRec)
        self.Method_prog_Rank_4.setObjectName(u"Method_prog_Rank_4")
        self.Method_prog_Rank_4.setMaximumSize(QSize(100, 4))

        self.horizontalLayout_5.addWidget(self.Method_prog_Rank_4)

        self.Method_Rate_Rank_4 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rate_Rank_4.setObjectName(u"Method_Rate_Rank_4")
        self.Method_Rate_Rank_4.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.Method_Rate_Rank_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.Method_Rank_5 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rank_5.setObjectName(u"Method_Rank_5")
        self.Method_Rank_5.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.Method_Rank_5)

        self.Method_prog_Rank_5 = ProgressBar(self.StartegyRec)
        self.Method_prog_Rank_5.setObjectName(u"Method_prog_Rank_5")
        self.Method_prog_Rank_5.setMaximumSize(QSize(100, 4))

        self.horizontalLayout_6.addWidget(self.Method_prog_Rank_5)

        self.Method_Rate_Rank_5 = StrongBodyLabel(self.StartegyRec)
        self.Method_Rate_Rank_5.setObjectName(u"Method_Rate_Rank_5")
        self.Method_Rate_Rank_5.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.Method_Rate_Rank_5)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.Reference = SegmentedWidget(self.StartegyRec)
        self.Reference.setObjectName(u"Reference")

        self.horizontalLayout.addWidget(self.Reference)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout_2.addWidget(self.StartegyRec, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.LeverFrame = QFrame(Overall)
        self.LeverFrame.setObjectName(u"LeverFrame")
        self.LeverFrame.setMinimumSize(QSize(110, 170))
        self.LeverFrame.setMaximumSize(QSize(110, 170))
        self.LeverFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout_2 = QVBoxLayout(self.LeverFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.LeverTitle = StrongBodyLabel(self.LeverFrame)
        self.LeverTitle.setObjectName(u"LeverTitle")

        self.verticalLayout_2.addWidget(self.LeverTitle)

        self.LeverRing = ProgressRing(self.LeverFrame)
        self.LeverRing.setObjectName(u"LeverRing")

        self.verticalLayout_2.addWidget(self.LeverRing)

        self.LeverRate = StrongBodyLabel(self.LeverFrame)
        self.LeverRate.setObjectName(u"LeverRate")

        self.verticalLayout_2.addWidget(self.LeverRate)


        self.gridLayout.addWidget(self.LeverFrame, 0, 0, 1, 1)

        self.RecentralFrame = QFrame(Overall)
        self.RecentralFrame.setObjectName(u"RecentralFrame")
        self.RecentralFrame.setMinimumSize(QSize(180, 170))
        self.RecentralFrame.setMaximumSize(QSize(300, 170))
        self.RecentralFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout_3 = QVBoxLayout(self.RecentralFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.RecentralMaxTitle = StrongBodyLabel(self.RecentralFrame)
        self.RecentralMaxTitle.setObjectName(u"RecentralMaxTitle")

        self.verticalLayout_3.addWidget(self.RecentralMaxTitle)

        self.RecentralMaxBar = ProgressBar(self.RecentralFrame)
        self.RecentralMaxBar.setObjectName(u"RecentralMaxBar")
        self.RecentralMaxBar.setMaximumSize(QSize(1111111, 4))
        self.RecentralMaxBar.setOrientation(Qt.Horizontal)

        self.verticalLayout_3.addWidget(self.RecentralMaxBar)

        self.RecentralMinTitle = StrongBodyLabel(self.RecentralFrame)
        self.RecentralMinTitle.setObjectName(u"RecentralMinTitle")

        self.verticalLayout_3.addWidget(self.RecentralMinTitle)

        self.RecentralMinBar = ProgressBar(self.RecentralFrame)
        self.RecentralMinBar.setObjectName(u"RecentralMinBar")

        self.verticalLayout_3.addWidget(self.RecentralMinBar)

        self.RecentralMeanTitle = StrongBodyLabel(self.RecentralFrame)
        self.RecentralMeanTitle.setObjectName(u"RecentralMeanTitle")

        self.verticalLayout_3.addWidget(self.RecentralMeanTitle)

        self.RecentralMeanBar = ProgressBar(self.RecentralFrame)
        self.RecentralMeanBar.setObjectName(u"RecentralMeanBar")

        self.verticalLayout_3.addWidget(self.RecentralMeanBar)

        self.RecentralConclusionTitle = StrongBodyLabel(self.RecentralFrame)
        self.RecentralConclusionTitle.setObjectName(u"RecentralConclusionTitle")

        self.verticalLayout_3.addWidget(self.RecentralConclusionTitle)


        self.gridLayout.addWidget(self.RecentralFrame, 0, 1, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.StartDateTitle = StrongBodyLabel(Overall)
        self.StartDateTitle.setObjectName(u"StartDateTitle")

        self.verticalLayout_5.addWidget(self.StartDateTitle)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.StartDatePicker = DatePicker(Overall)
        self.StartDatePicker.setObjectName(u"StartDatePicker")
        self.StartDatePicker.setDate(QDate(2019, 1, 4))

        self.horizontalLayout_8.addWidget(self.StartDatePicker)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.EndDateTitle = StrongBodyLabel(Overall)
        self.EndDateTitle.setObjectName(u"EndDateTitle")

        self.verticalLayout_5.addWidget(self.EndDateTitle)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.EndDatePicker = DatePicker(Overall)
        self.EndDatePicker.setObjectName(u"EndDatePicker")

        self.horizontalLayout_7.addWidget(self.EndDatePicker)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.gridLayout.addLayout(self.verticalLayout_5, 1, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.GraphFrame = QFrame(Overall)
        self.GraphFrame.setObjectName(u"GraphFrame")
        self.GraphFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout_4 = QVBoxLayout(self.GraphFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.HorizontalSeparator = HorizontalSeparator(self.GraphFrame)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout_4.addWidget(self.HorizontalSeparator)

        self.Graph = MatplotlibBarWidget(self.GraphFrame)
        self.Graph.setObjectName(u"Graph")
        self.Graph.setMinimumSize(QSize(300, 220))
        self.Graph.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_4.addWidget(self.Graph)


        self.gridLayout_2.addWidget(self.GraphFrame, 1, 0, 1, 2)


        self.retranslateUi(Overall)

        QMetaObject.connectSlotsByName(Overall)
    # setupUi

    def retranslateUi(self, Overall):
        Overall.setWindowTitle(QCoreApplication.translate("Overall", u"Form", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\">\u8fd1\u671f\u7b56\u7565\u63a8\u8350</p></body></html>", None))
        self.Method_Rank_1.setText(QCoreApplication.translate("Overall", u"Strong body label", None))
        self.Method_Rate_Rank_1.setText(QCoreApplication.translate("Overall", u"Rate", None))
        self.Method_Rank_2.setText(QCoreApplication.translate("Overall", u"Strong body label", None))
        self.Method_Rate_Rank_2.setText(QCoreApplication.translate("Overall", u"Rate", None))
        self.Method_Rank_3.setText(QCoreApplication.translate("Overall", u"Strong body label", None))
        self.Method_Rate_Rank_3.setText(QCoreApplication.translate("Overall", u"Rate", None))
        self.Method_Rank_4.setText(QCoreApplication.translate("Overall", u"Strong body label", None))
        self.Method_Rate_Rank_4.setText(QCoreApplication.translate("Overall", u"Rate", None))
        self.Method_Rank_5.setText(QCoreApplication.translate("Overall", u"Strong body label", None))
        self.Method_Rate_Rank_5.setText(QCoreApplication.translate("Overall", u"Rate", None))
        self.LeverTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">\u6760\u6746\u7387\u7cfb\u6570</span></p></body></html>", None))
        self.LeverRate.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">0.5%</span></p></body></html>", None))
        self.RecentralMaxTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">\u4e2d\u5fc3\u5316\u7cfb\u6570-\u6700\u5927\u503c:8</span></p></body></html>", None))
        self.RecentralMinTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">\u4e2d\u5fc3\u5316\u7cfb\u6570-\u6700\u5c0f\u503c:6</span></p></body></html>", None))
        self.RecentralMeanTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">\u4e2d\u5fc3\u5316\u7cfb\u6570-\u5747\u503c:7,6</span></p></body></html>", None))
        self.RecentralConclusionTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\">\u5224\u65ad\uff1a<span style=\" color:#ff0000;\">\u975e\u7e41\u8363</span></p></body></html>", None))
        self.StartDateTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Start date </span></p></body></html>", None))
        self.EndDateTitle.setText(QCoreApplication.translate("Overall", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">End date </span></p></body></html>", None))
    # retranslateUi


################################################################################
## Form generated from reading UI file 'singleInisoH.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################



class Ui_Single_Stock(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Ui_Single_Stock")
        Form.resize(1155, 862)
        Form.setStyleSheet(u"background-color: rgba(255, 255, 255, 255);")
        self.verticalLayout_9 = QVBoxLayout(Form)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.TopSpacer = QLabel(Form)
        self.TopSpacer.setObjectName(u"TopSpacer")
        self.TopSpacer.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_9.addWidget(self.TopSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.CodeList = ListView(Form)
        self.CodeList.setObjectName(u"CodeList")
        self.CodeList.setMinimumSize(QSize(200, 0))
        self.CodeList.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.CodeList)

        self.VerticalSeparator = VerticalSeparator(Form)
        self.VerticalSeparator.setObjectName(u"VerticalSeparator")

        self.horizontalLayout_3.addWidget(self.VerticalSeparator)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.StockName = SubtitleLabel(Form)
        self.StockName.setObjectName(u"StockName")
        self.StockName.setMaximumSize(QSize(16777215, 30))
        self.StockName.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")
        self.StockName.setMargin(0)
        self.StockName.setProperty("strikeOut", False)

        self.verticalLayout.addWidget(self.StockName)

        self.StockInfo = ListView(Form)
        self.StockInfo.setObjectName(u"StockInfo")
        self.StockInfo.setMinimumSize(QSize(300, 200))
        self.StockInfo.setMaximumSize(QSize(300, 400))

        self.verticalLayout.addWidget(self.StockInfo)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        self.PreviewMACD = QChartView(Form)
        self.PreviewMACD.setObjectName(u"PreviewMACD")
        self.PreviewMACD.setMinimumSize(QSize(200, 120))
        self.PreviewMACD.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")
        self.verticalLayout_2.addWidget(self.PreviewMACD)
        self.ExeShowMACD = PrimaryPushButton(Form)
        self.ExeShowMACD.setObjectName(u"ExeShowMACD")
        self.verticalLayout_2.addWidget(self.ExeShowMACD)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.PreviewBolling = QChartView(Form)
        self.PreviewBolling.setObjectName(u"PreviewBolling")
        self.PreviewBolling.setMinimumSize(QSize(200, 120))
        self.PreviewBolling.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")

        self.verticalLayout_4.addWidget(self.PreviewBolling)

        self.ExeShowBolling = PrimaryPushButton(Form)
        self.ExeShowBolling.setObjectName(u"ExeShowBolling")

        self.verticalLayout_4.addWidget(self.ExeShowBolling)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.PreviewVolumn = QChartView(Form)
        self.PreviewVolumn.setObjectName(u"PreviewVolumn")
        self.PreviewVolumn.setMinimumSize(QSize(200, 120))
        self.PreviewVolumn.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")

        self.verticalLayout_6.addWidget(self.PreviewVolumn)

        self.ExeShowVolumn = PrimaryPushButton(Form)
        self.ExeShowVolumn.setObjectName(u"ExeShowVolumn")

        self.verticalLayout_6.addWidget(self.ExeShowVolumn)


        self.gridLayout.addLayout(self.verticalLayout_6, 0, 2, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.PreviewRSI = QChartView(Form)
        self.PreviewRSI.setObjectName(u"PreviewRSI")
        self.PreviewRSI.setMinimumSize(QSize(200, 120))
        self.PreviewRSI.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")

        self.verticalLayout_3.addWidget(self.PreviewRSI)

        self.ExeShowRSI = PrimaryPushButton(Form)
        self.ExeShowRSI.setObjectName(u"ExeShowRSI")

        self.verticalLayout_3.addWidget(self.ExeShowRSI)


        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.PreviewAmount = QChartView(Form)
        self.PreviewAmount.setObjectName(u"PreviewAmount")
        self.PreviewAmount.setMinimumSize(QSize(200, 120))
        self.PreviewAmount.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")

        self.verticalLayout_5.addWidget(self.PreviewAmount)

        self.ExeShowAmount = PrimaryPushButton(Form)
        self.ExeShowAmount.setObjectName(u"ExeShowAmount")

        self.verticalLayout_5.addWidget(self.ExeShowAmount)


        self.gridLayout.addLayout(self.verticalLayout_5, 1, 1, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.PreviewKline = QChartView(Form)
        self.PreviewKline.setObjectName(u"PreviewKline")
        self.PreviewKline.setMinimumSize(QSize(200, 120))
        self.PreviewKline.setStyleSheet(u"background-color: rgb(255, 255, 255); border-radius:10px;")

        self.verticalLayout_7.addWidget(self.PreviewKline)

        self.ExeShowKline = PrimaryPushButton(Form)
        self.ExeShowKline.setObjectName(u"ExeShowKline")

        self.verticalLayout_7.addWidget(self.ExeShowKline)


        self.gridLayout.addLayout(self.verticalLayout_7, 1, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.StartTimeLabel = StrongBodyLabel(Form)
        self.StartTimeLabel.setObjectName(u"StartTimeLabel")
        self.StartTimeLabel.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_2.addWidget(self.StartTimeLabel)

        self.StartTimePicker = DatePicker(Form)
        self.StartTimePicker.setObjectName(u"StartTimePicker")

        self.horizontalLayout_2.addWidget(self.StartTimePicker)

        self.EndTimeLabel = StrongBodyLabel(Form)
        self.EndTimeLabel.setObjectName(u"EndTimeLabel")
        self.EndTimeLabel.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_2.addWidget(self.EndTimeLabel)

        self.EndTimePicker = DatePicker(Form)
        self.EndTimePicker.setObjectName(u"DatePicker_2")

        self.horizontalLayout_2.addWidget(self.EndTimePicker)

        self.ExeReDrawTime = TransparentPushButton(Form)
        self.ExeReDrawTime.setObjectName(u"ExeReDrawTime")

        self.horizontalLayout_2.addWidget(self.ExeReDrawTime)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.PlotlyGraph = FramelessWebEngineView(Form)
        self.PlotlyGraph.setObjectName(u"PlotlyGraph")
        self.PlotlyGraph.setMinimumSize(QSize(0, 300))

        self.verticalLayout_8.addWidget(self.PlotlyGraph)


        self.horizontalLayout_3.addLayout(self.verticalLayout_8)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.TopSpacer.setText("")
        self.StockName.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:15pt;\">CODE</span></p></body></html>", None))
        self.ExeShowMACD.setText(QCoreApplication.translate("Form", u"MACD", None))
        self.ExeShowBolling.setText(QCoreApplication.translate("Form", u"Bolling", None))
        self.ExeShowVolumn.setText(QCoreApplication.translate("Form", u"Volumn", None))
        self.ExeShowRSI.setText(QCoreApplication.translate("Form", u"RSI", None))
        self.ExeShowAmount.setText(QCoreApplication.translate("Form", u"Amount", None))
        self.ExeShowKline.setText(QCoreApplication.translate("Form", u"K-Line", None))
        self.StartTimeLabel.setText(QCoreApplication.translate("Form", u"Start Time", None))
        self.EndTimeLabel.setText(QCoreApplication.translate("Form", u"End Time", None))
        self.ExeReDrawTime.setText(QCoreApplication.translate("Form", u"Load", None))
    # retranslateUi