# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QTableWidgetItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (ListView, TableWidget, 
                            ProgressRing,ProgressBar,
                            PushButton, PrimaryPushButton,
                            StrongBodyLabel, SubtitleLabel,
                            VerticalSeparator)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D



class Matplotlib3DWidget(QWidget):
    def __init__(self,parent):
        super(Matplotlib3DWidget, self).__init__(parent=parent)
        self.setObjectName(u"Ui_MatplotLib")
        self.setupUi()
    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.fig = plt.figure(figsize=(10, 6))
        self.mpl = FigureCanvas(self.fig)
        # self.mpl_ntb = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl)
        # self.layout.addWidget(self.mpl_ntb)
    def drawGraph(self,df:pd.DataFrame):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111,projection='3d')
        X = np.arange(df.shape[0])  # 使用行数作为 X 轴
        Y = np.arange(df.shape[1])  # 使用列数作为 Y 轴
        X, Y = np.meshgrid(X, Y)      # 创建网格
        Z = df.values.T  # Z 数据

        # 绘制曲面
        self.ax.plot_surface(X, Y, Z, cmap='viridis')  # 使用 'viridis' 颜色映射
        # 设置标签
        self.ax.set_xlabel('time range')
        self.ax.set_ylabel('type range')
        self.ax.set_zlabel('value')
        self.mpl.draw() 

################################################################################
## Form generated from reading UI file 'stock_infoxHwpka.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

class Ui_StockInfo(object):
    def setupUi(self, StockInfo):
        if not StockInfo.objectName():
            StockInfo.setObjectName(u"StockInfo")
        StockInfo.resize(407, 400)
        # StockInfo.setMaximumSize(QSize(410, 410))
        StockInfo.setStyleSheet(u"background-color: rgb(250, 250, 250);")
        self.verticalLayout_4 = QVBoxLayout(StockInfo)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(StockInfo)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_4.addWidget(self.label)

        self.frame = QFrame(StockInfo)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.StockInfoTable = TableWidget(self.frame)
        if (self.StockInfoTable.columnCount() < 2):
            self.StockInfoTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.StockInfoTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.StockInfoTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.StockInfoTable.setObjectName(u"StockInfoTable")
        self.StockInfoTable.setMinimumSize(QSize(260, 0))
        self.StockInfoTable.setMaximumSize(QSize(260, 16777215))

        self.horizontalLayout.addWidget(self.StockInfoTable)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.StatusFrame = QFrame(self.frame)
        self.StatusFrame.setObjectName(u"StatusFrame")
        self.StatusFrame.setMinimumSize(QSize(111, 171))
        self.StatusFrame.setMaximumSize(QSize(111, 171))
        self.StatusFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.StatusFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.StatusRing = ProgressRing(self.StatusFrame)
        self.StatusRing.setObjectName(u"StatusRing")

        self.verticalLayout.addWidget(self.StatusRing)

        self.StatusLabel = StrongBodyLabel(self.StatusFrame)
        self.StatusLabel.setObjectName(u"StatusLabel")

        self.verticalLayout.addWidget(self.StatusLabel)

        self.ExeStatusCheck = PushButton(self.StatusFrame)
        self.ExeStatusCheck.setObjectName(u"ExeStatusCheck")

        self.verticalLayout.addWidget(self.ExeStatusCheck)


        self.verticalLayout_3.addWidget(self.StatusFrame)

        self.UpdateFrame = QFrame(self.frame)
        self.UpdateFrame.setObjectName(u"UpdateFrame")
        self.UpdateFrame.setMinimumSize(QSize(111, 171))
        self.UpdateFrame.setMaximumSize(QSize(111, 171))
        self.UpdateFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout_2 = QVBoxLayout(self.UpdateFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.UpdateRing = ProgressRing(self.UpdateFrame)
        self.UpdateRing.setObjectName(u"UpdateRing")

        self.verticalLayout_2.addWidget(self.UpdateRing)

        self.UpdateLabel = StrongBodyLabel(self.UpdateFrame)
        self.UpdateLabel.setObjectName(u"UpdateLabel")

        self.verticalLayout_2.addWidget(self.UpdateLabel)

        self.ExeUpdate = PrimaryPushButton(self.UpdateFrame)
        self.ExeUpdate.setObjectName(u"ExeUpdate")

        self.verticalLayout_2.addWidget(self.ExeUpdate)


        self.verticalLayout_3.addWidget(self.UpdateFrame)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addWidget(self.frame)


        self.retranslateUi(StockInfo)

        QMetaObject.connectSlotsByName(StockInfo)
    # setupUi

    def retranslateUi(self, StockInfo):
        StockInfo.setWindowTitle(QCoreApplication.translate("StockInfo", u"Form", None))
        self.label.setText("")
        ___qtablewidgetitem = self.StockInfoTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("StockInfo", u"\u80a1\u7968\u4ee3\u7801", None));
        ___qtablewidgetitem1 = self.StockInfoTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("StockInfo", u"\u80a1\u7968\u72b6\u6001", None));
        self.StatusLabel.setText(QCoreApplication.translate("StockInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.ExeStatusCheck.setText(QCoreApplication.translate("StockInfo", u"\u72b6\u6001\u68c0\u67e5", None))
        self.UpdateLabel.setText(QCoreApplication.translate("StockInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.ExeUpdate.setText(QCoreApplication.translate("StockInfo", u"\u66f4\u65b0\u6570\u636e", None))
    # retranslateUi


################################################################################
## Form generated from reading UI file 'portfolio_infouinKiMNz.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (ListView, ProgressBar, ProgressRing, PushButton,
    StrongBodyLabel, SubtitleLabel, VerticalSeparator)

class Ui_PortfolioInfo(object):
    def setupUi(self, PortfolioInfo):
        if not PortfolioInfo.objectName():
            PortfolioInfo.setObjectName(u"PortfolioInfo")
        PortfolioInfo.resize(404, 501)
        self.horizontalLayout = QHBoxLayout(PortfolioInfo)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Standard = QFrame(PortfolioInfo)
        self.Standard.setObjectName(u"Standard")
        self.verticalLayout_2 = QVBoxLayout(self.Standard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.headspace1 = QLabel(self.Standard)
        self.headspace1.setObjectName(u"headspace1")
        self.headspace1.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_2.addWidget(self.headspace1)

        self.StandardTitle = SubtitleLabel(self.Standard)
        self.StandardTitle.setObjectName(u"StandardTitle")

        self.verticalLayout_2.addWidget(self.StandardTitle)

        self.StandardList = ListView(self.Standard)
        self.StandardList.setObjectName(u"StandardList")
        self.StandardList.setMinimumSize(QSize(111, 0))
        self.StandardList.setMaximumSize(QSize(111, 16777215))

        self.verticalLayout_2.addWidget(self.StandardList)

        self.StandardFrame = QFrame(self.Standard)
        self.StandardFrame.setObjectName(u"StandardFrame")
        self.StandardFrame.setMinimumSize(QSize(111, 200))
        self.StandardFrame.setMaximumSize(QSize(111, 200))
        self.StandardFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.StandardFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.StandardBar = ProgressBar(self.StandardFrame)
        self.StandardBar.setObjectName(u"StandardBar")

        self.verticalLayout.addWidget(self.StandardBar)

        self.StandardRing = ProgressRing(self.StandardFrame)
        self.StandardRing.setObjectName(u"StandardRing")

        self.verticalLayout.addWidget(self.StandardRing)

        self.StandardLabel = StrongBodyLabel(self.StandardFrame)
        self.StandardLabel.setObjectName(u"StandardLabel")

        self.verticalLayout.addWidget(self.StandardLabel)

        self.ExeStandardUpdate = PushButton(self.StandardFrame)
        self.ExeStandardUpdate.setObjectName(u"ExeStandardUpdate")

        self.verticalLayout.addWidget(self.ExeStandardUpdate)


        self.verticalLayout_2.addWidget(self.StandardFrame)


        self.horizontalLayout.addWidget(self.Standard)

        self.VerticalSeparator = VerticalSeparator(PortfolioInfo)
        self.VerticalSeparator.setObjectName(u"VerticalSeparator")

        self.horizontalLayout.addWidget(self.VerticalSeparator)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.Multi = QFrame(PortfolioInfo)
        self.Multi.setObjectName(u"Multi")
        self.verticalLayout_3 = QVBoxLayout(self.Multi)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.headspace2 = QLabel(self.Multi)
        self.headspace2.setObjectName(u"headspace2")
        self.headspace2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_3.addWidget(self.headspace2)

        self.MultiTitle = SubtitleLabel(self.Multi)
        self.MultiTitle.setObjectName(u"MultiTitle")

        self.verticalLayout_3.addWidget(self.MultiTitle)

        self.MultiList = ListView(self.Multi)
        self.MultiList.setObjectName(u"MultiList")
        self.MultiList.setMinimumSize(QSize(111, 0))
        self.MultiList.setMaximumSize(QSize(111, 16777215))

        self.verticalLayout_3.addWidget(self.MultiList)

        self.MultiFrame = QFrame(self.Multi)
        self.MultiFrame.setObjectName(u"MultiFrame")
        self.MultiFrame.setMinimumSize(QSize(111, 200))
        self.MultiFrame.setMaximumSize(QSize(111, 200))
        self.MultiFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.verticalLayout_4 = QVBoxLayout(self.MultiFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.MultiBar = ProgressBar(self.MultiFrame)
        self.MultiBar.setObjectName(u"MultiBar")

        self.verticalLayout_4.addWidget(self.MultiBar)

        self.MultiRing = ProgressRing(self.MultiFrame)
        self.MultiRing.setObjectName(u"MultiRing")

        self.verticalLayout_4.addWidget(self.MultiRing)

        self.MultiLabel = StrongBodyLabel(self.MultiFrame)
        self.MultiLabel.setObjectName(u"MultiLabel")

        self.verticalLayout_4.addWidget(self.MultiLabel)


        self.verticalLayout_3.addWidget(self.MultiFrame)


        self.gridLayout.addWidget(self.Multi, 0, 0, 1, 1)

        self.ML = QFrame(PortfolioInfo)
        self.ML.setObjectName(u"ML")
        self.verticalLayout_5 = QVBoxLayout(self.ML)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.headspace3 = QLabel(self.ML)
        self.headspace3.setObjectName(u"headspace3")
        self.headspace3.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_5.addWidget(self.headspace3)

        self.MLTitle = SubtitleLabel(self.ML)
        self.MLTitle.setObjectName(u"MLTitle")

        self.verticalLayout_5.addWidget(self.MLTitle)

        self.MLList = ListView(self.ML)
        self.MLList.setObjectName(u"MLList")
        self.MLList.setMinimumSize(QSize(111, 0))
        self.MLList.setMaximumSize(QSize(111, 16777215))

        self.verticalLayout_5.addWidget(self.MLList)

        self.MLFrame = QFrame(self.ML)
        self.MLFrame.setObjectName(u"MLFrame")
        self.MLFrame.setMinimumSize(QSize(111, 200))
        self.MLFrame.setMaximumSize(QSize(111, 200))
        self.MLFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.verticalLayout_6 = QVBoxLayout(self.MLFrame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.MLBar = ProgressBar(self.MLFrame)
        self.MLBar.setObjectName(u"MLBar")

        self.verticalLayout_6.addWidget(self.MLBar)

        self.MLRing = ProgressRing(self.MLFrame)
        self.MLRing.setObjectName(u"MLRing")

        self.verticalLayout_6.addWidget(self.MLRing)

        self.MLLabel = StrongBodyLabel(self.MLFrame)
        self.MLLabel.setObjectName(u"MLLabel")

        self.verticalLayout_6.addWidget(self.MLLabel)


        self.verticalLayout_5.addWidget(self.MLFrame)


        self.gridLayout.addWidget(self.ML, 0, 1, 1, 1)

        self.ExeMultiUpdate = PushButton(PortfolioInfo)
        self.ExeMultiUpdate.setObjectName(u"ExeMultiUpdate")

        self.gridLayout.addWidget(self.ExeMultiUpdate, 1, 0, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(PortfolioInfo)

        QMetaObject.connectSlotsByName(PortfolioInfo)
    # setupUi

    def retranslateUi(self, PortfolioInfo):
        PortfolioInfo.setWindowTitle(QCoreApplication.translate("PortfolioInfo", u"Form", None))
        self.headspace1.setText("")
        self.StandardTitle.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:15pt;\">\u5355\u56e0\u5b50</span></p></body></html>", None))
        self.StandardLabel.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.ExeStandardUpdate.setText(QCoreApplication.translate("PortfolioInfo", u"\u66f4\u65b0\u7ec4\u5408", None))
        self.headspace2.setText("")
        self.MultiTitle.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\">\u591a\u56e0\u5b50</p></body></html>", None))
        self.MultiLabel.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.headspace3.setText("")
        self.MLTitle.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\">ML\u56e0\u5b50</p></body></html>", None))
        self.MLLabel.setText(QCoreApplication.translate("PortfolioInfo", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.ExeMultiUpdate.setText(QCoreApplication.translate("PortfolioInfo", u"\u66f4\u65b0\u7ec4\u5408", None))
    # retranslateUi



################################################################################
## Form generated from reading UI file 'overall-adjusteraETzgm.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (HorizontalSeparator, ListView, ProgressBar, ProgressRing,
    PushButton, Slider, StrongBodyLabel, VerticalSeparator)

class Ui_MixSup(object):
    def setupUi(self, MixSup):
        if not MixSup.objectName():
            MixSup.setObjectName(u"MixSup")
        MixSup.resize(424, 562)
        self.verticalLayout_3 = QVBoxLayout(MixSup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(MixSup)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

        self.verticalLayout_3.addWidget(self.label)

        self.LeverFrame = QFrame(MixSup)
        self.LeverFrame.setObjectName(u"LeverFrame")
        self.LeverFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.LeverFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.LeverUpper = QFrame(self.LeverFrame)
        self.LeverUpper.setObjectName(u"LeverUpper")
        self.horizontalLayout = QHBoxLayout(self.LeverUpper)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.LeverGraph = Matplotlib3DWidget(self.LeverUpper)
        self.LeverGraph.setObjectName(u"LeverGraph")
        self.LeverGraph.setMinimumSize(QSize(360, 260))

        self.horizontalLayout.addWidget(self.LeverGraph)

        self.LeverSlider = Slider(self.LeverUpper)
        self.LeverSlider.setObjectName(u"LeverSlider")
        self.LeverSlider.setMinimumSize(QSize(20, 0))
        self.LeverSlider.setMaximumSize(QSize(20, 16777215))
        self.LeverSlider.setOrientation(Qt.Vertical)
        self.LeverSlider.setInvertedAppearance(False)
        self.LeverSlider.setInvertedControls(False)
        self.LeverSlider.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout.addWidget(self.LeverSlider)


        self.verticalLayout.addWidget(self.LeverUpper)

        self.HorizontalSeparator = HorizontalSeparator(self.LeverFrame)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout.addWidget(self.HorizontalSeparator)

        self.LeverUnder = QFrame(self.LeverFrame)
        self.LeverUnder.setObjectName(u"LeverUnder")
        self.LeverUnder.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.LeverUnder)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.LeverTitle = StrongBodyLabel(self.LeverUnder)
        self.LeverTitle.setObjectName(u"LeverTitle")
        self.LeverTitle.setMinimumSize(QSize(80, 20))
        self.LeverTitle.setMaximumSize(QSize(80, 20))

        self.horizontalLayout_2.addWidget(self.LeverTitle)

        self.LeverRate = StrongBodyLabel(self.LeverUnder)
        self.LeverRate.setObjectName(u"LeverRate")
        self.LeverRate.setMinimumSize(QSize(40, 20))
        self.LeverRate.setMaximumSize(QSize(40, 20))

        self.horizontalLayout_2.addWidget(self.LeverRate)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.LeverUnder)


        self.verticalLayout_3.addWidget(self.LeverFrame)

        self.RecFrame = QFrame(MixSup)
        self.RecFrame.setObjectName(u"RecFrame")
        self.RecFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);border-radius:10px;")
        self.horizontalLayout_3 = QHBoxLayout(self.RecFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.RecList = ListView(self.RecFrame)
        self.RecList.setObjectName(u"RecList")

        self.horizontalLayout_3.addWidget(self.RecList)

        self.VerticalSeparator = VerticalSeparator(self.RecFrame)
        self.VerticalSeparator.setObjectName(u"VerticalSeparator")

        self.horizontalLayout_3.addWidget(self.VerticalSeparator)

        self.RecUpdatreFrame = QFrame(self.RecFrame)
        self.RecUpdatreFrame.setObjectName(u"RecUpdatreFrame")
        self.RecUpdatreFrame.setMinimumSize(QSize(111, 171))
        self.RecUpdatreFrame.setMaximumSize(QSize(111, 171))
        self.RecUpdatreFrame.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.RecUpdatreFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.RecRing = ProgressRing(self.RecUpdatreFrame)
        self.RecRing.setObjectName(u"RecRing")

        self.verticalLayout_2.addWidget(self.RecRing)

        self.RecLabel = StrongBodyLabel(self.RecUpdatreFrame)
        self.RecLabel.setObjectName(u"RecLabel")

        self.verticalLayout_2.addWidget(self.RecLabel)

        self.ExeRecUpdate = PushButton(self.RecUpdatreFrame)
        self.ExeRecUpdate.setObjectName(u"ExeRecUpdate")

        self.verticalLayout_2.addWidget(self.ExeRecUpdate)


        self.horizontalLayout_3.addWidget(self.RecUpdatreFrame)


        self.verticalLayout_3.addWidget(self.RecFrame)


        self.retranslateUi(MixSup)

        QMetaObject.connectSlotsByName(MixSup)
    # setupUi

    def retranslateUi(self, MixSup):
        MixSup.setWindowTitle(QCoreApplication.translate("MixSup", u"Form", None))
        self.label.setText("")
        self.LeverTitle.setText(QCoreApplication.translate("MixSup", u"\u6760\u6746\u7387\u8c03\u6574\uff1a", None))
        self.LeverRate.setText(QCoreApplication.translate("MixSup", u"0.5%", None))
        self.RecLabel.setText(QCoreApplication.translate("MixSup", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">100/100</span></p></body></html>", None))
        self.ExeRecUpdate.setText(QCoreApplication.translate("MixSup", u"\u66f4\u65b0\u63a8\u8350", None))
    # retranslateUi

