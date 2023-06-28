# -*- coding: utf-8 -*-
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal

class JanelaEstrategias():
    class Signals(QObject):
        avancar = pyqtSignal()

    inputsObj = []
    DEFAULT_ICON = None
    PRESSED_ICON = None
    signals = None

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()
    
        self.view_estrategias = uic.loadUi("resources/ui/tela_estrategias.ui")
        
        self.DEFAULT_ICON = QIcon("resources/assets/estrategia/ButtonAddStrategy (6).png")  
        self.PRESSED_ICON = QIcon("resources/assets/estrategia/ButtonAddStrategy (7).png")  

        self.view_estrategias.ButtonAdd.clicked.connect(self.addInputs)
        self.view_estrategias.ButtonAdd.pressed.connect(self.changeButtonIconPressed)  
        self.view_estrategias.ButtonAdd.released.connect(self.changeButtonIconReleased)  

        self.view_estrategias.ButtonNext.clicked.connect(self.nextScreen)

        self.view_estrategias.move(0, 0)

        for i in range(0,10):
            self.addInputs(i)
        
        self.inputsObj[0].setFocus()
    
    def addInputs(self, i):
        if len(self.inputsObj) >= 10:
            i = len(self.inputsObj)

        widget = QtWidgets.QLineEdit()
        widget.setObjectName(f"padrao {i}")
        widget.setFixedHeight(20)
        widget.setStyleSheet("background-color: #9D7612;\n"
    "border-color: #725509;\n"
    "border-radius: 6px;\n"
    "color: white;\n"
    "padding-left: 5px;")  
        widget.setMaxLength(60)
        
        widget2 = QtWidgets.QLineEdit()
        widget2.setObjectName(f"previsao {i}")
        widget2.setFixedSize(60,20)
        widget2.setStyleSheet("background-color: #9D7612;\n"
    "border-color: #725509;\n"
    "border-radius: 6px;\n"
    "color: white;\n"
    "padding-left: 25px;")
        widget2.setMaxLength(1)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(widget, 0, 0, alignment=Qt.AlignTop)
        grid.addWidget(widget2, 0, 1, alignment=Qt.AlignTop)
        self.view_estrategias.verticalLayout.addLayout(grid)

        self.inputsObj.append(grid.itemAt(0).widget())

    def changeButtonIconPressed(self):
        self.view_estrategias.ButtonAdd.setIcon(self.PRESSED_ICON)

    def changeButtonIconReleased(self):
        self.view_estrategias.ButtonAdd.setIcon(self.DEFAULT_ICON)
    
    def nextScreen(self):
        self.signals.avancar.emit()

    def show(self):
        self.view_estrategias.show()
    
    def hide(self):
        self.view_estrategias.hide()
    
    def getEstrategias(self):
        estrategias = self.view_estrategias.findChildren(QLineEdit)
        return estrategias

    def getEstrategiaByName(self, nome):
        estrategia = self.view_estrategias.findChild(QLineEdit, nome)
        return estrategia