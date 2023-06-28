# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from resources.ui_login import JanelaLogin
from resources.ui_estrategias import JanelaEstrategias
from resources.ui_gerenciamento import JanelaGerenciamento
from resources.ui_monitoramento import JanelaMonitoramento
from user_database import UserDatabase
from Blaze.src.automation import Bot
from Blaze.src.monitor import Monitor
from Blaze.src.masaniello import Masaniello
import xlwings as xw
import pythoncom
import threading
import time
import sys
import atexit
import psutil
import requests
import jwt
from datetime import datetime
import ctypes

class Application():
    url_login = 'http://127.0.0.1:5000/login'
    data_user = {}
    user = None
    ui_login = None
    ui_estrategias = None
    ui_gerenciamento = None
    ui_monitoramento = None
    app = None

    bot = None
    monitor = None
    masaniello = None
    gerenciamento = None
    threads_monitor = []
    PLANILHA_PATH = "Blaze/masaniello.xlsx"
    
    def __init__(self, user, ui_login, ui_estrategias, ui_gerenciamento, ui_monitoramento):
        super().__init__()
        self.user = user
        self.ui_login = ui_login
        self.ui_estrategias = ui_estrategias
        self.ui_gerenciamento = ui_gerenciamento
        self.ui_monitoramento = ui_monitoramento

    def on_login_successful(self):
        self.data_user = self.ui_login.getCredenciais()

        if len(self.data_user) == 2:
            if self.ui_login.lembrarCredenciais():
                self.user.set_login(self.data_user['email'], self.data_user['senha'])
            else:
                self.user.del_login()

            if self.data_user['email'] == "micaelpbo@gmail.com" or self.data_user['email'] == "demo":
                if self.data_user['email'] == "micaelpbo@gmail.com":
                    self.data_user['exp'] = datetime.fromtimestamp(1893538800)
                self.ui_login.hide()
                self.ui_estrategias.show()
                self.get_strategy_data()
            else:
                texto = "Usuário ou senha inválidos!\nUse o login 'demo' para usar a conta de simulação."
                self.ui_login.logLogin(texto)

    def strategy_configured(self):
        self.update_strategy_data()
        self.ui_estrategias.hide()
        self.ui_gerenciamento.show()
        self.get_management_data()
    
    def management_configured(self):
        self.update_management_data()
        self.ui_gerenciamento.hide()
        self.ui_monitoramento.show()

    def management_backscreen(self):
        self.ui_gerenciamento.hide()
        self.ui_estrategias.show()
    
    def monitor_backscreen(self):
        logText = str(self.ui_monitoramento.getLogText()).lower()
        
        if self.monitor != None and self.monitor.breakThreads is False:
            self.monitorStop()
            monitor_backscreen_thread = threading.Thread(target=self.monitor_backscreen_thread, daemon=True)
            monitor_backscreen_thread.start()
        elif self.ui_monitoramento.getLogText() == False or "desligado" in logText or "stop win" in logText or "stop loss" in logText or "licença ativa" in logText:
            self.ui_monitoramento.hide()
            self.ui_gerenciamento.show()
    
    def monitor_backscreen_thread(self):
        while "desligado" not in self.ui_monitoramento.getLogText().lower():
            pass
        self.ui_monitoramento.isPressedTurnOn = True
        self.monitor = None
        self.ui_monitoramento.hide()
        self.ui_gerenciamento.show()
    
    def get_strategy_data(self):
        estrategias = self.user.list_estrategias()

        if len(estrategias) > 0:
            estrategias_input = self.ui_estrategias.getEstrategias()

            i=0
            for estrategia in estrategias:
                padrao = " ".join(estrategia["padrao"])

                if i+1 <= len(estrategias_input):
                    estrategias_input[i].setText(padrao)
                    estrategias_input[i+1].setText(estrategia["previsao"])
                    i+=2
                else:
                    indice_input = len(self.ui_estrategias.inputsObj)
                    self.ui_estrategias.addInputs(i)
                    padrao = self.ui_estrategias.getEstrategiaByName(f"padrao {indice_input}")
                    padrao.setText(padrao)
                    previsao = self.ui_estrategias.getEstrategiaByName(f"previsao {indice_input}")
                    previsao.setText(estrategia["previsao"])
                    i+=1

    def get_management_data(self):
        gerenciamento = self.user.get_gerenciamento()
        self.ui_gerenciamento.changeDataView(gerenciamento)  
    
    def update_strategy_data(self):
        self.user.del_estrategias()
        estrategias_input = self.ui_estrategias.getEstrategias()

        for i in range(0, int(len(estrategias_input)/2)):
            padrao = self.ui_estrategias.getEstrategiaByName(f"padrao {i}")
            previsao = self.ui_estrategias.getEstrategiaByName(f"previsao {i}")
            if padrao.text() != "" and previsao.text() != "":
                self.user.add_estrategia(padrao.text(), previsao.text())
    
    def update_management_data(self):
        data = self.ui_gerenciamento.getGerenciamento()
 
        if data["gerenciamento"] == "masaniello":
            self.user.config_gerenciamento_masaniello(
                                        "masaniello",
                                        data["operacoes"], 
                                        data["acertos"], 
                                        data["riscoCiclo"], 
                                        data["reiniciarCiclo"], 
                                        data["stopWin"], 
                                        data["stopLoss"], 
                                        data["cobrirBranco"], 
                                        data["tipoGerenciamento"])
        elif data["gerenciamento"] == "maofixa":
            self.user.config_gerenciamento_maofixa("maofixa",
                                                   data["stopWin"], 
                                                   data["stopLoss"], 
                                                   data["cobrirBranco"], 
                                                   data["valorMaoFixa"])
    
    def monitorStart(self):
        self.ui_monitoramento.isBetting = False
        self.ui_monitoramento.logText("Inicializando")

        if self.monitor != None:
            del self.monitor
        self.monitor = Monitor(self.user.list_estrategias())
    
        self.bot = Bot(self.ui_monitoramento, self.monitor) if self.bot == None else self.bot

        if self.ui_monitoramento.getTipoConta()=="Real":
            if 'exp' in self.data_user and self.data_user['exp'] > datetime.now():
                self.bot.isDemo = False 
            else:
                texto = "Para uso em conta real, é necessário uma licença ativa."
                self.monitorException(texto)
                return
        else:
            self.bot.isDemo = True 

        if not self.bot.is_driver_active() and not self.bot.isDemo:
            try:
                self.bot.Start()
                if not self.bot.isDemo:
                    login, reason = self.bot.Login(email=self.data_user['email'], password=self.data_user['senha'])
            except:
                texto = "Houve uma falha de conexão\n[ Verifique a conexão com a internet ]\nDesligado"
                self.monitorException(texto)
                self.close_excel()
                return
        try:
            self.balance = self.bot.Get_Balance(self.getContaDemoValor()) 
        except:
            self.monitorException()
            self.close_excel()
            self.ui_monitoramento.hide()
            self.ui_login.show()
            return
        
        ui_balance = self.balance["symbol"]+" "+str(self.balance["saldo"])
        self.bot.lucro = 0
        self.ui_monitoramento.inicioBancaText(ui_balance)
        self.ui_monitoramento.finalBancaText(ui_balance) 
        self.ui_monitoramento.quantWinText(0) 
        self.ui_monitoramento.quantLossText(0)
        self.ui_monitoramento.ganhoText("0")
    
        monitorThread = threading.Thread(target=self.monitorThread, daemon=True)
        monitorThread.start()
        self.threads_monitor.append(monitorThread)

        monitorLog = threading.Thread(target=self.monitorLog, daemon=True)
        monitorLog.start()
        self.threads_monitor.append(monitorLog)

    def getContaDemoValor(self):
        with open("saldo_inicial_demo.txt", "r") as arquivo:
            conteudo = arquivo.read()
            return float(conteudo)

    def monitorThread(self):    
        app_sheet = None
        wb = None
        self.gerenciamento = self.user.get_gerenciamento()

        if self.gerenciamento["nomeGerenciamento"] == "maofixa" and isinstance(self.gerenciamento["valorMaoFixa"], str):
            texto = "[ Valor da aposta está em formato incorreto ]\nDesligado"
            self.monitorException(texto)
            return
        elif isinstance(self.gerenciamento["stopWin"], str) and self.gerenciamento["stopWin"] != "":
            texto = "[ Valor do stop win está em formato incorreto ]\nDesligado"
            self.monitorException(texto)
            return 
        elif isinstance(self.gerenciamento["stopLoss"], str) and self.gerenciamento["stopLoss"] != "":
            texto = "[ Valor do stop loss está em formato incorreto ]\nDesligado"
            self.monitorException(texto)
            return
        
        if self.gerenciamento["nomeGerenciamento"] == "masaniello":
            pythoncom.CoInitialize()
            app_sheet = xw.App(visible=False)
            wb = app_sheet.books.open(self.PLANILHA_PATH)
            [wb.close() for wb in app_sheet.books if "Pasta" in wb.name]
            self.masaniello = Masaniello(wb,app_sheet,self.gerenciamento["riscoCiclo"],self.gerenciamento["operacoes"],self.gerenciamento["acertos"],self.gerenciamento["tipoGerenciamento"])

        while not self.monitor.breakThreads:
            monitor_retorno = self.monitor.Monitoring()
            if self.monitor.exception == True:
                texto = "Houve uma falha de conexão\n[ Verifique a conexão com a internet ]\nDesligado"
                self.monitorException(texto)
                self.close_excel()
                break

            doubleBet = False
            if monitor_retorno != None and self.monitor.sequenciaPadraoG != None:
                valorAposta = {}

                if self.gerenciamento["nomeGerenciamento"] == "masaniello":
                    try:
                        valorAposta = self.masaniello.obterValorInvestimento(True) if self.gerenciamento["cobrirBranco"] else self.masaniello.obterValorInvestimento()
                        if valorAposta == False:
                            texto = "[ Revise a janela de gerenciamento ]\nDesligado"
                            self.monitorException(texto)
                            break
                    except:
                        texto = "[ Erro ao tentar ler na planilha Masaniello ]\nDesligado"
                        self.monitorException(texto)
                        break

                elif self.gerenciamento["nomeGerenciamento"] == "maofixa":
                    if not self.gerenciamento["cobrirBranco"]:
                        valor = self.gerenciamento["valorMaoFixa"] if self.gerenciamento["valorMaoFixa"] > 0.1 else 0.1
                        valorAposta = {"aposta": valor, "cobertura": 0}
                    else:
                        valor = self.gerenciamento["valorMaoFixa"] if self.gerenciamento["valorMaoFixa"] > 0.2 else 0.2
                        cobertura = 0.1
                        while cobertura*14 < valor-cobertura:
                            cobertura+=0.01
                        valorAposta = {"aposta": round(valor-cobertura,2), "cobertura": round(cobertura,2)}
                
                self.ui_monitoramento.isBetting = True
                self.ui_monitoramento.logText("Padrão encontrado!\n" \
                                            "Padrão: "+self.monitor.sequenciaPadraoG+" | Previsão: "+self.monitor.previsaoPadraoG+"\n" \
                                            "[ Realizando aposta | Valor: "+str(valorAposta["aposta"])+" | Cobertura: "+str(valorAposta["cobertura"])+" ]")

                if self.gerenciamento["cobrirBranco"]:
                    doubleBet = self.bot.Bet(game="double", bets=[{ "color": monitor_retorno["previsao"], "amount": valorAposta["aposta"] },
                                                                { "color": "B", "amount": valorAposta["cobertura"] }], return_results=True, lastSequence = monitor_retorno["padrao"])
                else:
                    doubleBet = self.bot.Bet(game="double", bets=[{ "color": monitor_retorno["previsao"], "amount": valorAposta["aposta"] }], return_results=True, lastSequence = monitor_retorno["padrao"])

                if doubleBet[0] != False and doubleBet[0] != "Stop":
                    self.bot.lucro += doubleBet[0]
                    self.bot.BalanceNewValue(doubleBet[0])

                    retorno = None
                    if doubleBet[0] < 0:
                        if self.gerenciamento["nomeGerenciamento"] == "masaniello":
                            try:
                                retorno = self.masaniello.escreveResultadoOp("L")
                            except:
                                texto = "[ Erro ao tentar escrever na planilha Masaniello ]\nDesligado"
                                self.monitorException(texto)
                                break
                        self.bot.quantLoss += 1
                        self.ui_monitoramento.quantLossText(self.bot.quantLoss)
                    else:
                        if self.gerenciamento["nomeGerenciamento"] == "masaniello":
                            try:
                                retorno = self.masaniello.escreveResultadoOp("W")
                            except:
                                texto = "[ Erro ao tentar escrever na planilha Masaniello ]\nDesligado"
                                self.monitorException(texto)
                                break
                        self.bot.quantWin += 1
                        self.ui_monitoramento.quantWinText(self.bot.quantWin)

                    if (self.gerenciamento["reiniciarCiclo"]==True and retorno != None) or (self.bot.lucro <= self.gerenciamento["riscoCiclo"]*-1 and self.gerenciamento["nomeGerenciamento"] == "masaniello"):
                        ciclo = self.masaniello.get_ciclo_status_ultima_op()
                        retorno = retorno if ciclo is None else ciclo

                        if retorno.lower() == "ciclo com lucro" or retorno.lower() == "ciclo com perda":
                            wb.close()
                            app_sheet.quit()
                            app_sheet = xw.App(visible=False)
                            wb = app_sheet.books.open(self.PLANILHA_PATH)
                            [wb.close() for wb in app_sheet.books if "Pasta" in wb.name]
                            del self.masaniello
                            self.masaniello = Masaniello(wb,app_sheet,self.gerenciamento["riscoCiclo"],self.gerenciamento["operacoes"],self.gerenciamento["acertos"],self.gerenciamento["tipoGerenciamento"])
                            
                            if retorno.lower() == "ciclo com lucro":
                                self.ui_monitoramento.logText("Ciclo com lucro!\n[ Reiniciado ]")
                                time.sleep(3)
                            else:
                                self.ui_monitoramento.logText("Ciclo com perda\n[ Reiniciado ]")
                                time.sleep(3)
                    
                    self.ui_monitoramento.ganhoText(str(round(float(self.bot.lucro), 2)))
                    self.ui_monitoramento.finalBancaText(self.bot.ACCOUNT_BALANCE["symbol"]+" "+str(round(float(self.bot.ACCOUNT_BALANCE["saldo"]), 2)))

                    if (not isinstance(self.gerenciamento["stopWin"], str) and float(self.bot.lucro) >= float(self.gerenciamento["stopWin"])) or (not isinstance(self.gerenciamento["stopLoss"], str) and float(self.bot.lucro) <= float(self.gerenciamento["stopLoss"]*(-1))):
                        texto = "Stop Win. Parabéns!" if float(self.bot.lucro) >= float(self.gerenciamento["stopWin"]) else "Stop Loss"
                        self.monitorException(texto)
                        break

                elif doubleBet[0] == False:
                    self.ui_monitoramento.logText("Aposta cancelada\n[ "+str(doubleBet[1])+" ]")
                    time.sleep(3)
                else:
                    texto = self.ui_monitoramento.logText("Aposta cancelada\n[ "+str(doubleBet[1])+" ]\nDesligado")
                    self.monitorException(texto)
                    break
                self.ui_monitoramento.isBetting = False
            
        if self.masaniello != None:
            wb.close()
            app_sheet.quit()
    
    def monitorException(self, texto=""):
        self.ui_monitoramento.isBetting = True 
        self.ui_monitoramento.changeIconButtonStatus(self.ui_monitoramento.PRESSED_ICON_TURNON)
        self.ui_monitoramento.isPressedTurnOn = True
        self.monitor.breakThreads = True 
        self.ui_monitoramento.logText(texto)
        self.threads_monitor.clear()

    def monitorLog(self):
        while not self.monitor.breakThreads:
            sequenciaPadrao = self.monitor.sequenciaPadraoG

            if sequenciaPadrao != None:
                self.ui_monitoramento.logText("Padrão: "+sequenciaPadrao+"\nAnalisando")
                time.sleep(0.1)
                self.ui_monitoramento.logText("Padrão: "+sequenciaPadrao+"\nAnalisando.")
                time.sleep(0.1)
                self.ui_monitoramento.logText("Padrão: "+sequenciaPadrao+"\nAnalisando..")
                time.sleep(0.1)
                self.ui_monitoramento.logText("Padrão: "+sequenciaPadrao+"\nAnalisando...")
                time.sleep(0.1)
    
    def monitorStop(self):
        threadMonitorStop = threading.Thread(target=self.monitorStopThread, daemon=True)
        threadMonitorStop.start()

    def monitorStopThread(self):
        self.ui_monitoramento.changeIconButtonStatus(self.ui_monitoramento.PRESSED_ICON_TURNOFF_WAITING)
        self.monitor.breakThreads = True
        for t in self.threads_monitor:
            t.join()
        self.threads_monitor.clear()
        self.ui_monitoramento.logText("Desligado")
        self.ui_monitoramento.changeIconButtonStatus(self.ui_monitoramento.PRESSED_ICON_TURNON)
    
    def close_excel(self):
        try:
            excel_pid = None
            driver = None

            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'chromedriver.exe':
                    driver = proc.pid

                if proc.info['name'] == 'EXCEL.EXE':
                    try:
                        for handle in proc.open_files():
                            if 'masaniello.xlsx' in handle.path:
                                excel_pid = proc.pid
                                break
                    except:
                        pass

            if excel_pid:
                proc_obj = psutil.Process(excel_pid)
                proc_obj.terminate()
            
            if driver:
                proc_obj = psutil.Process(driver)
                proc_obj.terminate()

            if self.bot.is_driver_active():
                self.bot.Stop()
        except:
            pass

if __name__ == '__main__':
    kernel32 = ctypes.WinDLL('kernel32')
    is_debugged = kernel32.IsDebuggerPresent

    if is_debugged():
        ctypes.windll.kernel32.TerminateProcess(-1, 1)  

    app = QtWidgets.QApplication([])
    
    user = UserDatabase()
    data_user = user.get_login()

    loginObj = JanelaLogin(data_user["email"], data_user["senha"]) if len(data_user) == 2 else JanelaLogin()
    estrategiasObj = JanelaEstrategias()
    gerenciamentoObj = JanelaGerenciamento()
    monitoramentoObj = JanelaMonitoramento()
    application = Application(user, loginObj, estrategiasObj, gerenciamentoObj, monitoramentoObj)
    
    application.ui_login.signals.login_successful.connect(application.on_login_successful)
    application.ui_estrategias.signals.avancar.connect(application.strategy_configured)
    application.ui_gerenciamento.signals.avancar.connect(application.management_configured)
    application.ui_gerenciamento.signals.voltar.connect(application.management_backscreen)
    application.ui_monitoramento.signals.voltar.connect(application.monitor_backscreen)
    application.ui_monitoramento.signals.turnOff.connect(application.monitorStop) 
    application.ui_monitoramento.signals.turnOn.connect(application.monitorStart)  
    atexit.register(application.close_excel)
    
    application.ui_login.show()
    sys.exit(app.exec_())