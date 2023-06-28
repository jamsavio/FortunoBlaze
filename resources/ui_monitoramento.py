# -*- coding: utf-8 -*-
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal, QSize

class JanelaMonitoramento():
    class Signals(QObject):
        voltar = pyqtSignal()
        turnOn = pyqtSignal()
        turnOff = pyqtSignal()

    isBetting = False
    PRESSED_ICON_TURNON = None
    PRESSED_ICON_TURNOFF = None
    PRESSED_ICON_TURNOFF_WAITING = None
    isPressedTurnOn = True
    signals = None

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

        self.view_monitoramento = uic.loadUi("resources/ui/tela_monitoramento.ui")
        self.view_monitoramento.move(0, 0)
        
        self.PRESSED_ICON_TURNON = QIcon("resources/assets/monitoramento/ButtonTurnOn.svg")  
        self.PRESSED_ICON_TURNOFF = QIcon("resources/assets/monitoramento/ButtonTurnOff.svg")  
        self.PRESSED_ICON_TURNOFF_WAITING = QIcon("resources/assets/monitoramento/ButtonTurnOffWaiting.png")  

        self.view_monitoramento.ButtonStatus.clicked.connect(self.statusMonitor)
        self.view_monitoramento.ButtonBack.clicked.connect(self.backScreen)
    
    def statusMonitor(self):
        icon1 = self.view_monitoramento.ButtonStatus.icon()
        icon2 = self.PRESSED_ICON_TURNOFF_WAITING

        pixmap1 = icon1.pixmap(icon1.actualSize(QSize(64, 64)))
        pixmap2 = icon2.pixmap(icon2.actualSize(QSize(64, 64)))
        
        if pixmap1.toImage() != pixmap2.toImage():
            if self.isPressedTurnOn:
                self.view_monitoramento.ButtonStatus.setIcon(self.PRESSED_ICON_TURNOFF)
                self.signals.turnOn.emit()

                logText = str(self.getLogText()).lower()
                if "licença ativa" not in logText:
                    self.isPressedTurnOn = False
            else:
                self.signals.turnOff.emit()
                self.isPressedTurnOn = True

    def changeIconButtonStatus(self, icon):
        self.view_monitoramento.ButtonStatus.setIcon(icon)
    
    def backScreen(self):
        self.signals.voltar.emit()
    
    def show(self):
        self.view_monitoramento.show()
    
    def hide(self):
        self.view_monitoramento.hide()
    
    def inicioBancaText(self, valor):
        if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'inicioBancaText'):
            self.view_monitoramento.inicioBancaText = QtWidgets.QLabel(self.view_monitoramento.centralwidget)
            self.view_monitoramento.inicioBancaText.setGeometry(QtCore.QRect(203, 248, 71, 20))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.view_monitoramento.inicioBancaText.setFont(font)
            self.view_monitoramento.inicioBancaText.setStyleSheet("color: #FFD012;")
            self.view_monitoramento.inicioBancaText.setObjectName("inicioBancaText")

        _translate = QtCore.QCoreApplication.translate
        self.view_monitoramento.inicioBancaText.setText(_translate("JanelaMonitoramento", str(valor)))
        self.view_monitoramento.inicioBancaText.setVisible(True)
    
    def finalBancaText(self, valor):
        if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'finalBancaText'):
            self.view_monitoramento.finalBancaText = QtWidgets.QLabel(self.view_monitoramento.centralwidget)
            self.view_monitoramento.finalBancaText.setGeometry(QtCore.QRect(203, 270, 71, 20))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.view_monitoramento.finalBancaText.setFont(font)
            self.view_monitoramento.finalBancaText.setStyleSheet("color: #FFD012;")
            self.view_monitoramento.finalBancaText.setObjectName("finalBancaText")

        _translate = QtCore.QCoreApplication.translate
        self.view_monitoramento.finalBancaText.setText(_translate("JanelaMonitoramento", str(valor)))
        self.view_monitoramento.finalBancaText.setVisible(True)
    
    def quantWinText(self, valor):
        if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'quantWinText'):
            self.view_monitoramento.quantWinText = QtWidgets.QLabel(self.view_monitoramento.winWidget)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(17)
            font.setBold(True)
            font.setWeight(75)
            self.view_monitoramento.quantWinText.setFont(font)
            self.view_monitoramento.quantWinText.setStyleSheet("color: #FFD012;;")
            self.view_monitoramento.quantWinText.setAlignment(QtCore.Qt.AlignCenter)
            self.view_monitoramento.quantWinText.setObjectName("quantWinText")
            self.view_monitoramento.winLayout.addWidget(self.view_monitoramento.quantWinText)

        _translate = QtCore.QCoreApplication.translate
        self.view_monitoramento.quantWinText.setText(_translate("JanelaMonitoramento", str(valor)))
    
    def quantLossText(self, valor):
        if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'quantLossText'):
            self.view_monitoramento.quantLossText = QtWidgets.QLabel(self.view_monitoramento.lossWidget)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(17)
            font.setBold(True)
            font.setWeight(75)
            self.view_monitoramento.quantLossText.setFont(font)
            self.view_monitoramento.quantLossText.setStyleSheet("color: #FFD012;")
            self.view_monitoramento.quantLossText.setAlignment(QtCore.Qt.AlignCenter)
            self.view_monitoramento.quantLossText.setObjectName("quantLossText")
            self.view_monitoramento.lossLayout.addWidget(self.view_monitoramento.quantLossText)

        _translate = QtCore.QCoreApplication.translate
        self.view_monitoramento.quantLossText.setText(_translate("JanelaMonitoramento", str(valor)))
    
    def logText(self, texto):
        if not self.isBetting or (texto != None and "analisando" not in texto.lower()):
            if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'logText'):
                self.view_monitoramento.logText = QtWidgets.QLabel(self.view_monitoramento.logWidget)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setBold(True)
                font.setWeight(75)
                self.view_monitoramento.logText.setFont(font)
                self.view_monitoramento.logText.setStyleSheet("color: white;")
                self.view_monitoramento.logText.setAlignment(QtCore.Qt.AlignCenter)
                self.view_monitoramento.logText.setObjectName("logText")
                self.view_monitoramento.logLayout.addWidget(self.view_monitoramento.logText) 

            _translate = QtCore.QCoreApplication.translate
            self.view_monitoramento.logText.setText(_translate("JanelaMonitoramento", str(texto)))
    
    def getLogText(self):
        try:
            if self.view_monitoramento.logText.text() != "":
                return self.view_monitoramento.logText.text()
            else:
                return False
        except:
            return False

    def ganhoText(self, valor):
        if not self.view_monitoramento.findChild(QtWidgets.QLabel, 'ganhoText'):
            self.view_monitoramento.ganhoText = QtWidgets.QLabel(self.view_monitoramento.ganhoWidget)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(18)
            font.setBold(True)
            font.setWeight(75)
            self.view_monitoramento.ganhoText.setFont(font)
            self.view_monitoramento.ganhoText.setStyleSheet("color: #C59E00;")
            self.view_monitoramento.ganhoText.setAlignment(QtCore.Qt.AlignCenter)
            self.view_monitoramento.ganhoText.setObjectName("ganhoText")
            self.view_monitoramento.ganhoLayout.addWidget(self.view_monitoramento.ganhoText)

        _translate = QtCore.QCoreApplication.translate
        self.view_monitoramento.ganhoText.setText(_translate("JanelaMonitoramento", str(valor)))

    def getTipoConta(self):
        return self.view_monitoramento.tipoContaBox.currentText()