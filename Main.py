from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
import threading
import requests, json 
from datetime import datetime
from Location import IPLocation #Userfile for location webscraper
import sys
from Weather import weather_now, weather_now_2 #Userfile for weather dataframe
import numpy as np
import pandas as pd
import settings #Userfile for global variables
from Google_cal import calendar_events

#forces the Weather file to generate the weather and store it in the settings file
weather_now()
weather_now_2()

#****MAIN APPLICATION****

#Update the calendar page based on user input
def calendar_update():
    temp_table = np.array([[0,0]])
    table = pd.DataFrame(columns = ["date", "event"])
    table = calendar_events(temp_table,table)
    table.drop_duplicates(inplace = True)
    value = ui.calendarWidget.selectedDate()
    table = table[(table['date'] == value)]
    table = table[['event']].to_numpy(dtype = "str")
    ui.listWidget.clear()
    for event in table:
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 226, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        ui.listWidget.addItem(item)
        item.setText(str(event)[2:-2])

#call weather_now and store dataframe
def call_weather_now():
    weather_data = pd.DataFrame(weather_now_2())
    ui.templabel_2.setText(str(round(settings.weather_response['main']['temp'])) + " °c")
    ui.templabel.setText(str(round(settings.weather_response['main']['temp'])) + " °c")
    ui.todayhigh.setText(str(round(settings.weather_response['main']['temp_max'])))
    ui.todaylow.setText(str(round(settings.weather_response['main']['temp_min'])))
    ui.todayhigh_2.setText(str(round(settings.weather_response['main']['temp_max'])))
    ui.todaylow_2.setText(str(round(settings.weather_response['main']['temp_min'])))
    ui.weather_icon.setPixmap(QtGui.QPixmap(settings.weather_response['weather'][0]['icon'] + "@2x.png"))
    ui.weather_icon_2.setPixmap(QtGui.QPixmap(settings.weather_response['weather'][0]['icon'] + "@2x.png"))

#Updates the labels with current time and updates the day/night image every time it is called
def time_output():
    print("threading works")

    now = datetime.now()
    ui.caltime_2.setText(now.strftime("%I") + ":" +  now.strftime("%M"))
    ui.caltime.setText(now.strftime("%I") + ":" +  now.strftime("%M"))

    sunrise_time = (datetime.fromtimestamp(settings.forecast_response["city"]["sunrise"]))
    sunset_time = (datetime.fromtimestamp(settings.forecast_response["city"]["sunset"])) 

    if now > sunrise_time and now < sunset_time:
                ui.label_2.setHidden(True)
                ui.label.setHidden(False)
    elif now > sunset_time:
                ui.label_2.setHidden(False)
                ui.label.setHidden(True)

#Timer objects 
def timerfortime():
    min_5_timer = threading.Timer(10, call_weather_now).start()
    sec_timer = threading.Timer(5, time_output).start()
    hour_timer = threading.Timer(3,calendar_update).start()

class Ui_App(object):
    def setupUi(self, Application):
        Application.setObjectName("Application")
        Application.resize(800, 480)
        Application.setMinimumSize(QtCore.QSize(800, 480))
        Application.setMaximumSize(QtCore.QSize(800, 480))
        font = QtGui.QFont()
        font.setPointSize(8)
        Application.setFont(font)
        Application.setMouseTracking(False)
        Application.setTabletTracking(False)
        Application.setAutoFillBackground(False)
        Application.setStyleSheet("")
        Application.setTabPosition(QtWidgets.QTabWidget.East)
        Application.setTabShape(QtWidgets.QTabWidget.Rounded)
        Application.setIconSize(QtCore.QSize(93, 80))
        Application.setUsesScrollButtons(False)
        Application.setDocumentMode(True)
        Application.setTabsClosable(False)
        Application.setTabBarAutoHide(True)
        self.home = QtWidgets.QWidget()
        self.home.setAutoFillBackground(False)
        self.home.setObjectName("home")
        self.homeback = QtWidgets.QLabel(self.home)
        self.homeback.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.homeback.setText("")
        self.homeback.setPixmap(QtGui.QPixmap("pink-3200x1800-white-abstract-stock-hd-1679.jpg"))
        self.homeback.setScaledContents(True)
        self.homeback.setObjectName("homeback")
        self.label = QtWidgets.QLabel(self.home)
        self.label.setGeometry(QtCore.QRect(240, 20, 81, 81))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("day.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.home)
        self.label_2.setGeometry(QtCore.QRect(240, 20, 81, 81))
        self.label_2.setStyleSheet("")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("night.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.caltime_2 = QtWidgets.QLabel(self.home)
        self.caltime_2.setEnabled(True)
        self.caltime_2.setGeometry(QtCore.QRect(15, 10, 210, 91))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(60)
        font.setBold(False)
        font.setWeight(50)
        self.caltime_2.setFont(font)
        self.caltime_2.setStyleSheet("COLOR: beige")
        self.caltime_2.setAlignment(QtCore.Qt.AlignCenter)
        self.caltime_2.setOpenExternalLinks(False)
        self.caltime_2.setObjectName("caltime_2")
        self.templabel_2 = QtWidgets.QLabel(self.home)
        self.templabel_2.setGeometry(QtCore.QRect(400, 40, 141, 61))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(44)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.templabel_2.setFont(font)
        self.templabel_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.templabel_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.templabel_2.setAutoFillBackground(False)
        self.templabel_2.setStyleSheet("color: yellow")
        self.templabel_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.templabel_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.templabel_2.setLineWidth(0)
        self.templabel_2.setTextFormat(QtCore.Qt.AutoText)
        self.templabel_2.setScaledContents(False)
        self.templabel_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.templabel_2.setWordWrap(True)
        self.templabel_2.setObjectName("templabel_2")
        self.weatherback_4 = QtWidgets.QLabel(self.home)
        self.weatherback_4.setGeometry(QtCore.QRect(415, 120, 31, 31))
        self.weatherback_4.setText("")
        self.weatherback_4.setPixmap(QtGui.QPixmap("Down_arrow.png"))
        self.weatherback_4.setScaledContents(True)
        self.weatherback_4.setObjectName("weatherback_4")
        self.weatherback_5 = QtWidgets.QLabel(self.home)
        self.weatherback_5.setGeometry(QtCore.QRect(300, 115, 31, 31))
        self.weatherback_5.setText("")
        self.weatherback_5.setPixmap(QtGui.QPixmap("Up_arrow.png"))
        self.weatherback_5.setScaledContents(True)
        self.weatherback_5.setObjectName("weatherback_5")
        self.todayhigh_2 = QtWidgets.QLabel(self.home)
        self.todayhigh_2.setGeometry(QtCore.QRect(335, 90, 81, 91))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(44)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.todayhigh_2.setFont(font)
        self.todayhigh_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.todayhigh_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.todayhigh_2.setAutoFillBackground(False)
        self.todayhigh_2.setStyleSheet("color : yellow")
        self.todayhigh_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.todayhigh_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.todayhigh_2.setLineWidth(0)
        self.todayhigh_2.setTextFormat(QtCore.Qt.AutoText)
        self.todayhigh_2.setScaledContents(False)
        self.todayhigh_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.todayhigh_2.setWordWrap(True)
        self.todayhigh_2.setObjectName("todayhigh_2")
        self.todaylow_2 = QtWidgets.QLabel(self.home)
        self.todaylow_2.setGeometry(QtCore.QRect(450, 90, 151, 91))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(44)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.todaylow_2.setFont(font)
        self.todaylow_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.todaylow_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.todaylow_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.todaylow_2.setAutoFillBackground(False)
        self.todaylow_2.setStyleSheet("color : yellow")
        self.todaylow_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.todaylow_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.todaylow_2.setLineWidth(0)
        self.todaylow_2.setTextFormat(QtCore.Qt.AutoText)
        self.todaylow_2.setScaledContents(False)
        self.todaylow_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.todaylow_2.setWordWrap(True)
        self.todaylow_2.setObjectName("todaylow_2")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("clock_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Application.addTab(self.home, icon, "")
        self.calendar = QtWidgets.QWidget()
        self.calendar.setObjectName("calendar")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.calendar)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 10, 330, 330))
        self.calendarWidget.setBaseSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.calendarWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Leelawadee")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setStyleSheet("")
        self.calendarWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarback = QtWidgets.QLabel(self.calendar)
        self.calendarback.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.calendarback.setText("")
        self.calendarback.setPixmap(QtGui.QPixmap("148643.jpg"))
        self.calendarback.setScaledContents(True)
        self.calendarback.setObjectName("calendarback")
        self.listWidget = QtWidgets.QListWidget(self.calendar)
        self.listWidget.setGeometry(QtCore.QRect(350, 10, 360, 461))
        self.listWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.listWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setStyleSheet("background: transparent")
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget.setAutoScroll(True)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setTabKeyNavigation(False)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.listWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setMovement(QtWidgets.QListView.Free)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setWordWrap(True)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 226, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(20)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 226, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.listWidget.addItem(item)
        self.caltime = QtWidgets.QLabel(self.calendar)
        self.caltime.setEnabled(True)
        self.caltime.setGeometry(QtCore.QRect(10, 350, 330, 120))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(73)
        font.setBold(True)
        font.setWeight(75)
        self.caltime.setFont(font)
        self.caltime.setStyleSheet("COLOR: beige")
        self.caltime.setAlignment(QtCore.Qt.AlignCenter)
        self.caltime.setOpenExternalLinks(False)
        self.caltime.setObjectName("caltime")
        self.calendarback.raise_()
        self.calendarWidget.raise_()
        self.listWidget.raise_()
        self.caltime.raise_()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("calendar-flatrotated.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Application.addTab(self.calendar, icon1, "")
        self.weather = QtWidgets.QWidget()
        self.weather.setObjectName("weather")
        self.weathericon = QtWidgets.QLabel(self.weather)
        self.weathericon.setGeometry(QtCore.QRect(10, 10, 150, 150))
        self.weathericon.setText("")
        self.weathericon.setObjectName("weathericon")
        self.templabel = QtWidgets.QLabel(self.weather)
        self.templabel.setGeometry(QtCore.QRect(220, 30, 281, 111))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(72)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.templabel.setFont(font)
        self.templabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.templabel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.templabel.setAutoFillBackground(False)
        self.templabel.setStyleSheet("color : yellow")
        self.templabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.templabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.templabel.setLineWidth(0)
        self.templabel.setTextFormat(QtCore.Qt.AutoText)
        self.templabel.setScaledContents(False)
        self.templabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.templabel.setWordWrap(True)
        self.templabel.setObjectName("templabel")
        self.weatherback = QtWidgets.QLabel(self.weather)
        self.weatherback.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.weatherback.setText("")
        self.weatherback.setPixmap(QtGui.QPixmap("sdfg.jpg"))
        self.weatherback.setScaledContents(False)
        self.weatherback.setObjectName("weatherback")
        self.todayhigh = QtWidgets.QLabel(self.weather)
        self.todayhigh.setGeometry(QtCore.QRect(620, 60, 81, 91))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.todayhigh.setFont(font)
        self.todayhigh.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.todayhigh.setFocusPolicy(QtCore.Qt.NoFocus)
        self.todayhigh.setAutoFillBackground(False)
        self.todayhigh.setStyleSheet("color : yellow")
        self.todayhigh.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.todayhigh.setFrameShadow(QtWidgets.QFrame.Plain)
        self.todayhigh.setLineWidth(0)
        self.todayhigh.setTextFormat(QtCore.Qt.AutoText)
        self.todayhigh.setScaledContents(False)
        self.todayhigh.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.todayhigh.setWordWrap(True)
        self.todayhigh.setObjectName("todayhigh")
        self.todaylow = QtWidgets.QLabel(self.weather)
        self.todaylow.setGeometry(QtCore.QRect(620, 130, 151, 91))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.todaylow.setFont(font)
        self.todaylow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.todaylow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.todaylow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.todaylow.setAutoFillBackground(False)
        self.todaylow.setStyleSheet("color : yellow")
        self.todaylow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.todaylow.setFrameShadow(QtWidgets.QFrame.Plain)
        self.todaylow.setLineWidth(0)
        self.todaylow.setTextFormat(QtCore.Qt.AutoText)
        self.todaylow.setScaledContents(False)
        self.todaylow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.todaylow.setWordWrap(True)
        self.todaylow.setObjectName("todaylow")
        self.weatherback_2 = QtWidgets.QLabel(self.weather)
        self.weatherback_2.setGeometry(QtCore.QRect(580, 85, 31, 31))
        self.weatherback_2.setText("")
        self.weatherback_2.setPixmap(QtGui.QPixmap("Up_arrow.png"))
        self.weatherback_2.setScaledContents(True)
        self.weatherback_2.setObjectName("weatherback_2")
        self.weatherback_3 = QtWidgets.QLabel(self.weather)
        self.weatherback_3.setGeometry(QtCore.QRect(580, 155, 31, 31))
        self.weatherback_3.setText("")
        self.weatherback_3.setPixmap(QtGui.QPixmap("Down_arrow.png"))
        self.weatherback_3.setScaledContents(True)
        self.weatherback_3.setObjectName("weatherback_3")
        self.weatherback.raise_()
        self.weathericon.raise_()
        self.templabel.raise_()
        self.todayhigh.raise_()
        self.todaylow.raise_()
        self.weatherback_2.raise_()
        self.weatherback_3.raise_()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("WEATHER.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Application.addTab(self.weather, icon2, "")
        
        self.alarm = QtWidgets.QWidget()
        self.alarm.setObjectName("alarm")
        self.bar1 = QtWidgets.QProgressBar(self.alarm)
        self.bar1.setGeometry(QtCore.QRect(520, 80, 171, 21))
        self.bar1.setStyleSheet("")
        self.bar1.setMinimum(-50)
        self.bar1.setMaximum(50)
        self.bar1.setProperty("value", 0)
        self.bar1.setAlignment(QtCore.Qt.AlignCenter)
        self.bar1.setTextVisible(True)
        self.bar1.setInvertedAppearance(False)
        self.bar1.setObjectName("bar1")
        self.lcdNumber1 = QtWidgets.QLCDNumber(self.alarm)
        self.lcdNumber1.setGeometry(QtCore.QRect(520, 20, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber1.setFont(font)
        self.lcdNumber1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber1.setSmallDecimalPoint(False)
        self.lcdNumber1.setDigitCount(7)
        self.lcdNumber1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber1.setProperty("value", 200.0)
        self.lcdNumber1.setProperty("intValue", 200)
        self.lcdNumber1.setObjectName("lcdNumber1")
        self.lcdNumber2 = QtWidgets.QLCDNumber(self.alarm)
        self.lcdNumber2.setGeometry(QtCore.QRect(520, 120, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber2.setFont(font)
        self.lcdNumber2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber2.setSmallDecimalPoint(False)
        self.lcdNumber2.setDigitCount(7)
        self.lcdNumber2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber2.setProperty("value", 200.0)
        self.lcdNumber2.setProperty("intValue", 200)
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.bar2 = QtWidgets.QProgressBar(self.alarm)
        self.bar2.setGeometry(QtCore.QRect(520, 180, 171, 21))
        self.bar2.setStyleSheet("")
        self.bar2.setMinimum(0)
        self.bar2.setProperty("value", 50)
        self.bar2.setAlignment(QtCore.Qt.AlignCenter)
        self.bar2.setTextVisible(True)
        self.bar2.setInvertedAppearance(False)
        self.bar2.setObjectName("bar2")
        self.lcdNumber3 = QtWidgets.QLCDNumber(self.alarm)
        self.lcdNumber3.setGeometry(QtCore.QRect(520, 220, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber3.setFont(font)
        self.lcdNumber3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber3.setSmallDecimalPoint(False)
        self.lcdNumber3.setDigitCount(7)
        self.lcdNumber3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber3.setProperty("value", 200.0)
        self.lcdNumber3.setProperty("intValue", 200)
        self.lcdNumber3.setObjectName("lcdNumber3")
        self.bar3 = QtWidgets.QProgressBar(self.alarm)
        self.bar3.setGeometry(QtCore.QRect(520, 280, 171, 21))
        self.bar3.setStyleSheet("")
        self.bar3.setMinimum(0)
        self.bar3.setProperty("value", 50)
        self.bar3.setAlignment(QtCore.Qt.AlignCenter)
        self.bar3.setTextVisible(True)
        self.bar3.setInvertedAppearance(False)
        self.bar3.setObjectName("bar3")
        self.lcdNumber4 = QtWidgets.QLCDNumber(self.alarm)
        self.lcdNumber4.setGeometry(QtCore.QRect(520, 340, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber4.setFont(font)
        self.lcdNumber4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber4.setSmallDecimalPoint(False)
        self.lcdNumber4.setDigitCount(7)
        self.lcdNumber4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber4.setProperty("value", 200.0)
        self.lcdNumber4.setProperty("intValue", 200)
        self.lcdNumber4.setObjectName("lcdNumber4")
        self.bar4 = QtWidgets.QProgressBar(self.alarm)
        self.bar4.setGeometry(QtCore.QRect(520, 400, 171, 21))
        self.bar4.setStyleSheet("")
        self.bar4.setMinimum(0)
        self.bar4.setProperty("value", 50)
        self.bar4.setAlignment(QtCore.Qt.AlignCenter)
        self.bar4.setTextVisible(True)
        self.bar4.setInvertedAppearance(False)
        self.bar4.setObjectName("bar4")
        self.Today = QtWidgets.QPushButton(self.alarm)
        self.Today.setGeometry(QtCore.QRect(50, 260, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.Today.setFont(font)
        self.Today.setAutoFillBackground(False)
        self.Today.setStyleSheet("background: transparent; color: Yellow")
        self.Today.setCheckable(False)
        self.Today.setDefault(False)
        self.Today.setFlat(False)
        self.Today.setObjectName("Today")
        self.stockback = QtWidgets.QLabel(self.alarm)
        self.stockback.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.stockback.setText("")
        self.stockback.setPixmap(QtGui.QPixmap("iceberg-minimalism-7v.jpg"))
        self.stockback.setScaledContents(True)
        self.stockback.setObjectName("stockback")
        self.lcdNumber5 = QtWidgets.QLCDNumber(self.alarm)
        self.lcdNumber5.setGeometry(QtCore.QRect(50, 80, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber5.setFont(font)
        self.lcdNumber5.setStyleSheet("color: yellow")
        self.lcdNumber5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber5.setSmallDecimalPoint(False)
        self.lcdNumber5.setDigitCount(7)
        self.lcdNumber5.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber5.setProperty("value", 200.0)
        self.lcdNumber5.setProperty("intValue", 200)
        self.lcdNumber5.setObjectName("lcdNumber5")
        self.Total = QtWidgets.QPushButton(self.alarm)
        self.Total.setGeometry(QtCore.QRect(50, 360, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.Total.setFont(font)
        self.Total.setAcceptDrops(True)
        self.Total.setStyleSheet("background: transparent; color: Yellow")
        self.Total.setCheckable(False)
        self.Total.setChecked(False)
        self.Total.setDefault(False)
        self.Total.setFlat(False)
        self.Total.setObjectName("Total")
        self.stockback.raise_()
        self.bar1.raise_()
        self.lcdNumber1.raise_()
        self.lcdNumber2.raise_()
        self.bar2.raise_()
        self.lcdNumber3.raise_()
        self.bar3.raise_()
        self.lcdNumber4.raise_()
        self.bar4.raise_()
        self.Today.raise_()
        self.lcdNumber5.raise_()
        self.Total.raise_()
        self.weather_icon = QtWidgets.QLabel(self.home)
        self.weather_icon.setGeometry(QtCore.QRect(505, 35, 70, 70))
        self.weather_icon.setStyleSheet("")
        self.weather_icon.setText("")
        self.weather_icon.setPixmap(QtGui.QPixmap("10d@2x.png"))
        self.weather_icon.setScaledContents(True)
        self.weather_icon.setObjectName("weather_icon")
        self.weather_icon_2 = QtWidgets.QLabel(self.weather)
        self.weather_icon_2.setGeometry(QtCore.QRect(380, 20, 130, 130))
        self.weather_icon_2.setStyleSheet("")
        self.weather_icon_2.setText("")
        self.weather_icon_2.setPixmap(QtGui.QPixmap("10d@2x.png"))
        self.weather_icon_2.setScaledContents(True)
        self.weather_icon_2.setObjectName("weather_icon")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("alarmclockflat_106001 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Application.addTab(self.alarm, icon3, "")

        self.retranslateUi(Application)
        Application.setCurrentIndex(0)
        self.calendarWidget.clicked['QDate'].connect(calendar_update)
        self.Today.clicked.connect(self.lcdNumber1.showNormal)
        QtCore.QMetaObject.connectSlotsByName(Application)

    def retranslateUi(self, Application):
        _translate = QtCore.QCoreApplication.translate
        Application.setWindowTitle(_translate("Application", "TabWidget"))
        self.caltime_2.setText(_translate("Application", "11:00"))
        self.templabel_2.setText(_translate("Application", "35C"))
        self.todayhigh_2.setText(_translate("Application", "-35"))
        self.todaylow_2.setText(_translate("Application", "-36"))
        self.listWidget.setSortingEnabled(False)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Application", "Event 1"))
        item = self.listWidget.item(1)
        item.setText(_translate("Application", "Event 2"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.caltime.setText(_translate("Application", "11:00"))
        self.templabel.setText(_translate("Application", "35C"))
        self.todayhigh.setText(_translate("Application", "35"))
        self.todaylow.setText(_translate("Application", "-36"))
        self.bar1.setFormat(_translate("Application", "%p%"))
        self.Today.setText(_translate("Application", "Today"))
        self.Total.setText(_translate("Application", "Total"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Application = QtWidgets.QTabWidget()
    ui = Ui_App()
    ui.setupUi(Application)
    Application.show()
    timerfortime()
    sys.exit(app.exec_())