# -*- coding: utf-8 -*-
from PyQt5 import uic,QtWidgets,QtCore,QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal

class JanelaGerenciamento():
    class Signals(QObject):
        avancar = pyqtSignal()
        voltar = pyqtSignal()

    view_gerenciamento = None
    PRESSED_ICON_MAOFIXA = None
    DEFAULT_ICON_MAOFIXA = None
    PRESSED_ICON_MASANIELLO = None
    DEFAULT_ICON_MASANIELLO = None
    gerenciamentoEscolhido = None
    signals = None

    def __init__(self):
        super().__init__()
        self.signals = self.Signals()

        self.view_gerenciamento = uic.loadUi("resources/ui/tela_gerenciamento.ui")
        self.view_gerenciamento.move(0, 0)

        self.PRESSED_ICON_MAOFIXA = QIcon("resources/assets/gerenciamento/Rectangle Mão Fixa (2).svg")
        self.DEFAULT_ICON_MAOFIXA = QIcon("resources/assets/gerenciamento/Rectangle Mão Fixa (1).svg")
        self.PRESSED_ICON_MASANIELLO = QIcon("resources/assets/gerenciamento/Rectangle Masaniello (1).svg")
        self.DEFAULT_ICON_MASANIELLO = QIcon("resources/assets/gerenciamento/Rectangle Masaniello (2).svg")
        
        self.view_gerenciamento.MaoFixaButton.clicked.connect(self.MaoFixaForm)
        self.view_gerenciamento.MasanielloButton.clicked.connect(self.MasanielloForm)
        self.view_gerenciamento.ButtonNext.clicked.connect(self.nextScreen)
        self.view_gerenciamento.ButtonBack.clicked.connect(self.backScreen)
        
        self.MaoFixaFormCreate()
    
    def MaoFixaForm(self):
        self.view_gerenciamento.MaoFixaButton.setIcon(self.PRESSED_ICON_MAOFIXA)
        self.view_gerenciamento.MasanielloButton.setIcon(self.DEFAULT_ICON_MASANIELLO)
        self.view_gerenciamento.groupMasanielloBox.setVisible(False)
        self.view_gerenciamento.groupMaoFixaBox.setVisible(True)
        self.gerenciamentoEscolhido = "maofixa"
    
    def MasanielloForm(self):
        self.view_gerenciamento.MaoFixaButton.setIcon(self.DEFAULT_ICON_MAOFIXA)
        self.view_gerenciamento.MasanielloButton.setIcon(self.PRESSED_ICON_MASANIELLO)
        self.view_gerenciamento.groupMasanielloBox.setVisible(True)
        self.view_gerenciamento.groupMaoFixaBox.setVisible(False)
        self.gerenciamentoEscolhido = "masaniello"
    
    def MaoFixaFormCreate(self):
        self.view_gerenciamento.groupMaoFixaBox = QtWidgets.QGroupBox(self.view_gerenciamento.centralwidget)
        self.view_gerenciamento.groupMaoFixaBox.setGeometry(QtCore.QRect(65, 120, 261, 151))
        self.view_gerenciamento.groupMaoFixaBox.setStyleSheet("border-radius: 0px;")
        self.view_gerenciamento.groupMaoFixaBox.setTitle("")
        self.view_gerenciamento.groupMaoFixaBox.setObjectName("groupMaoFixaBox")
        self.view_gerenciamento.formLayoutWidgetMaoFixa = QtWidgets.QWidget(self.view_gerenciamento.groupMaoFixaBox)
        self.view_gerenciamento.formLayoutWidgetMaoFixa.setGeometry(QtCore.QRect(0, 0, 241, 131))
        self.view_gerenciamento.formLayoutWidgetMaoFixa.setObjectName("formLayoutWidgetMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout = QtWidgets.QFormLayout(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.formMaoFixaLayout.setContentsMargins(10, 0, 0, 0)
        self.view_gerenciamento.formMaoFixaLayout.setHorizontalSpacing(30)
        self.view_gerenciamento.formMaoFixaLayout.setVerticalSpacing(20)
        self.view_gerenciamento.formMaoFixaLayout.setObjectName("formMaoFixaLayout")
        self.view_gerenciamento.valorEntradaMaoFixaText = QtWidgets.QLabel(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.valorEntradaMaoFixaText.setStyleSheet("color: white;")
        self.view_gerenciamento.valorEntradaMaoFixaText.setObjectName("valorEntradaMaoFixaText")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.view_gerenciamento.valorEntradaMaoFixaText)
        self.view_gerenciamento.valorEntradaMaoFixaInput = QtWidgets.QLineEdit(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.valorEntradaMaoFixaInput.setObjectName("valorEntradaMaoFixaInput")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.view_gerenciamento.valorEntradaMaoFixaInput)
  
        self.view_gerenciamento.stopWinTextMaoFixa = QtWidgets.QLabel(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.stopWinTextMaoFixa.setStyleSheet("color: white;")
        self.view_gerenciamento.stopWinTextMaoFixa.setObjectName("stopWinTextMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.view_gerenciamento.stopWinTextMaoFixa)
        self.view_gerenciamento.stopWinInputMaoFixa = QtWidgets.QLineEdit(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.stopWinInputMaoFixa.setText("")
        self.view_gerenciamento.stopWinInputMaoFixa.setObjectName("stopWinInputMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.view_gerenciamento.stopWinInputMaoFixa)
        self.view_gerenciamento.stopLossTextMaoFixa = QtWidgets.QLabel(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.stopLossTextMaoFixa.setStyleSheet("color: white;")
        self.view_gerenciamento.stopLossTextMaoFixa.setObjectName("stopLossTextMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.view_gerenciamento.stopLossTextMaoFixa)
        self.view_gerenciamento.stopLossInputMaoFixa = QtWidgets.QLineEdit(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.stopLossInputMaoFixa.setText("")
        self.view_gerenciamento.stopLossInputMaoFixa.setObjectName("stopLossInputMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.view_gerenciamento.stopLossInputMaoFixa)
        self.view_gerenciamento.groupCobrirBrancoBoxMaoFixa = QtWidgets.QGroupBox(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.groupCobrirBrancoBoxMaoFixa.setTitle("")
        self.view_gerenciamento.groupCobrirBrancoBoxMaoFixa.setObjectName("groupCobrirBrancoBoxMaoFixa")
        self.view_gerenciamento.horizontalLayoutWidgetMaoFixa = QtWidgets.QWidget(self.view_gerenciamento.groupCobrirBrancoBoxMaoFixa)
        self.view_gerenciamento.horizontalLayoutWidgetMaoFixa.setGeometry(QtCore.QRect(0, 0, 137, 15))
        self.view_gerenciamento.horizontalLayoutWidgetMaoFixa.setObjectName("horizontalLayoutWidgetMaoFixa")
        self.view_gerenciamento.cobrirBrancoLayoutMaoFixa = QtWidgets.QHBoxLayout(self.view_gerenciamento.horizontalLayoutWidgetMaoFixa)
        self.view_gerenciamento.cobrirBrancoLayoutMaoFixa.setContentsMargins(0, 0, 0, 0)
        self.view_gerenciamento.cobrirBrancoLayoutMaoFixa.setObjectName("cobrirBrancoLayoutMaoFixa")
        self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa = QtWidgets.QRadioButton(self.view_gerenciamento.horizontalLayoutWidgetMaoFixa)
        self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setStyleSheet("color: white;")
        self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setChecked(True)
        self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setObjectName("cobrirBrancoSimRadioMaoFixa")
        self.view_gerenciamento.cobrirBrancoLayoutMaoFixa.addWidget(self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa)
        self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa = QtWidgets.QRadioButton(self.view_gerenciamento.horizontalLayoutWidgetMaoFixa)
        self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa.setStyleSheet("color: white;")
        self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa.setObjectName("cobrirBrancoNaoRadioMaoFixa")
        self.view_gerenciamento.cobrirBrancoLayoutMaoFixa.addWidget(self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa)
        self.view_gerenciamento.formMaoFixaLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.view_gerenciamento.groupCobrirBrancoBoxMaoFixa)
        self.view_gerenciamento.cobrirBrancoTextMaoFixa = QtWidgets.QLabel(self.view_gerenciamento.formLayoutWidgetMaoFixa)
        self.view_gerenciamento.cobrirBrancoTextMaoFixa.setStyleSheet("color: white;")
        self.view_gerenciamento.cobrirBrancoTextMaoFixa.setObjectName("cobrirBrancoTextMaoFixa")
        self.view_gerenciamento.formMaoFixaLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.view_gerenciamento.cobrirBrancoTextMaoFixa)
        
        _translate = QtCore.QCoreApplication.translate
        self.view_gerenciamento.valorEntradaMaoFixaText.setText(_translate("JanelaEstrategias", "Valor da Entrada"))
        self.view_gerenciamento.valorEntradaMaoFixaInput.setText(_translate("JanelaEstrategias", "2"))
        self.view_gerenciamento.stopWinTextMaoFixa.setText(_translate("JanelaEstrategias", "Stop Win"))
        self.view_gerenciamento.stopLossTextMaoFixa.setText(_translate("JanelaEstrategias", "Stop Loss"))
        self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setText(_translate("JanelaEstrategias", "Sim"))
        self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa.setText(_translate("JanelaEstrategias", "Não"))
        self.view_gerenciamento.cobrirBrancoTextMaoFixa.setText(_translate("JanelaEstrategias", "Cobrir o branco"))

        self.view_gerenciamento.groupMaoFixaBox.setVisible(False)
    
    def nextScreen(self):
        self.signals.avancar.emit()
    
    def backScreen(self):
        self.signals.voltar.emit()
    
    def show(self):
        self.view_gerenciamento.show()
    
    def hide(self):
        self.view_gerenciamento.hide()
    
    def getGerenciamento(self):
        data = {}

        if self.gerenciamentoEscolhido == "masaniello":
            reiniciarCiclo = 1 if self.view_gerenciamento.reiniciarCicloSimRadio.isChecked() else 0
            cobrirBranco = 1 if self.view_gerenciamento.cobrirBrancoSimRadio.isChecked() else 0

            data = {"gerenciamento": "masaniello",
                    "operacoes": self.view_gerenciamento.operacoesInput.text(),
                    "acertos": self.view_gerenciamento.acertosInput.text(),
                    "riscoCiclo": self.view_gerenciamento.riscoCicloInput.text(),
                    "reiniciarCiclo": reiniciarCiclo,
                    "stopWin": self.view_gerenciamento.stopWinInput.text(),
                    "stopLoss": self.view_gerenciamento.stopLossInput.text(),
                    "cobrirBranco": cobrirBranco,
                    "tipoGerenciamento": self.view_gerenciamento.tipoGerenciamentoComboBox.currentText()
                    }
        
        elif self.gerenciamentoEscolhido == "maofixa":
            cobrirBranco = 1 if self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.isChecked() else 0

            data = {"gerenciamento": "maofixa",
                    "stopWin": self.view_gerenciamento.stopWinInputMaoFixa.text(),
                    "stopLoss": self.view_gerenciamento.stopLossInputMaoFixa.text(),
                    "cobrirBranco": cobrirBranco,
                    "valorMaoFixa": self.view_gerenciamento.valorEntradaMaoFixaInput.text()
                    }
        return data

    def changeDataView(self, gerenciamento):
        if gerenciamento["nomeGerenciamento"] == "masaniello":
            self.MasanielloForm()
        elif gerenciamento["nomeGerenciamento"] == "maofixa":
            self.MaoFixaForm()
            
        self.view_gerenciamento.operacoesInput.setText(str(gerenciamento["operacoes"]))
        self.view_gerenciamento.acertosInput.setText(str(gerenciamento["acertos"]))
        self.view_gerenciamento.riscoCicloInput.setText(str(gerenciamento["riscoCiclo"]))

        if gerenciamento["reiniciarCiclo"] == True:
            self.view_gerenciamento.reiniciarCicloSimRadio.setChecked(True)
            self.view_gerenciamento.reiniciarCicloNaoRadio.setChecked(False)
        else:
            self.view_gerenciamento.reiniciarCicloSimRadio.setChecked(False)
            self.view_gerenciamento.reiniciarCicloNaoRadio.setChecked(True)
        
        self.view_gerenciamento.stopWinInput.setText(str(gerenciamento["stopWin"]))
        self.view_gerenciamento.stopLossInput.setText(str(gerenciamento["stopLoss"]))

        if gerenciamento["cobrirBranco"] == True:
            self.view_gerenciamento.cobrirBrancoSimRadio.setChecked(True)
            self.view_gerenciamento.cobrirBrancoNaoRadio.setChecked(False)
        else:
            self.view_gerenciamento.cobrirBrancoSimRadio.setChecked(False)
            self.view_gerenciamento.cobrirBrancoNaoRadio.setChecked(True)
        
        if gerenciamento["tipoGerenciamento"] == "Normal":
            self.view_gerenciamento.tipoGerenciamentoComboBox.setCurrentText('Normal')
        else:
            self.view_gerenciamento.tipoGerenciamentoComboBox.setCurrentText('Progressivo')

        self.view_gerenciamento.valorEntradaMaoFixaInput.setText(str(gerenciamento["valorMaoFixa"]))
        self.view_gerenciamento.stopWinInputMaoFixa.setText(str(gerenciamento["stopWin"]))
        self.view_gerenciamento.stopLossInputMaoFixa.setText(str(gerenciamento["stopLoss"]))

        if gerenciamento["cobrirBranco"] == True:
            self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setChecked(True)
            self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa.setChecked(False)
        else:
            self.view_gerenciamento.cobrirBrancoSimRadioMaoFixa.setChecked(False)
            self.view_gerenciamento.cobrirBrancoNaoRadioMaoFixa.setChecked(True)
            
if __name__ == '__main__':
    obj = JanelaGerenciamento()
    
    