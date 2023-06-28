# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

class JanelaLogin():
    class Signals(QObject):
        login_successful = pyqtSignal()

    versao = "v1.0.1"
    view_login = None
    signals = None

    def __init__(self, email=None, senha=None):
        super().__init__()
        self.signals = self.Signals()

        self.view_login = uic.loadUi("resources/ui/tela_login.ui")
        self.view_login.move(0, 0)

        self.view_login.versaoLabel = QtWidgets.QLabel(self.view_login.centralwidget)
        self.view_login.versaoLabel.setGeometry(QtCore.QRect(173, 460, 41, 16))
        self.view_login.versaoLabel.setStyleSheet("font-weight: bold;\ncolor: white;")
        self.view_login.versaoLabel.setObjectName("versaoLabel")
        _translate = QtCore.QCoreApplication.translate
        self.view_login.versaoLabel.setText(_translate("JanelaPrincipal", self.versao))

        self.view_login.ButtonLogin.clicked.connect(self.buttonLoginClicked)

        if email != None and senha != None:
            self.view_login.inputLogin.setText(email)
            self.view_login.inputPassword.setText(senha)

        self.view_login.inputLogin.setFocus()

    def buttonLoginClicked(self):
        if self.view_login.findChild(QtWidgets.QLabel, 'TextLogLogin'):
            self.view_login.TextLogLogin.setVisible(False)

        self.signals.login_successful.emit()
    
    def getCredenciais(self):
        data_user = {'email': self.view_login.inputLogin.text(),
                     'senha': self.view_login.inputPassword.text()}
        return data_user
    
    def show(self):
        self.view_login.show()
    
    def hide(self):
        self.view_login.hide()

    def lembrarCredenciais(self):
        if self.view_login.lembrarCredenciaisRadio.isChecked():
            return True
        return False
    
    def logLogin(self, texto):
        if not self.view_login.findChild(QtWidgets.QLabel, 'TextLogLogin'):
            self.view_login.TextLogLogin = QtWidgets.QLabel(self.view_login.centralwidget)
            self.view_login.TextLogLogin.setGeometry(QtCore.QRect(1, 373, 381, 61))
            self.view_login.TextLogLogin.setStyleSheet("font-weight: bold;\n"
                                                    "color: #DBA417;")
            self.view_login.TextLogLogin.setAlignment(QtCore.Qt.AlignCenter)
            self.view_login.TextLogLogin.setObjectName("TextLogLogin")

        _translate = QtCore.QCoreApplication.translate
        self.view_login.TextLogLogin.setText(_translate("JanelaPrincipal", str(texto)))
        self.view_login.TextLogLogin.setVisible(True)