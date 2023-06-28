# -*- coding: utf-8 -*-
class Masaniello():
    capitalRisco = 100
    numeroOperacoes = 10
    numeroOperacoesGanho = 5
    payout = 2
    tipoGerenciamento = None
    # ------------------
    PLANILHA_PATH = "Blaze/masaniello.xlsx"
    cedulaParam = {"capitalRisco": "N12", 
                  "numeroOperacoes": "N13",
                  "numeroOperacoesGanho": "N14",
                  "payout": "N15",
                  "tipoGerenciamento": "N16"}
    
    app = None
    wb = None
    ws = None
    # ------------------
    linhaOp = 3
    colunaOp = {"resultado": "C",
                "investimento": "D",
                "ciclo": "I"}


    def __init__(self, wb, app, capitalRisco, numeroOperacoes, numeroOperacoesGanho, tipoGerenciamento="Normal", payout=2):
        self.capitalRisco = capitalRisco
        self.numeroOperacoes = numeroOperacoes
        self.numeroOperacoesGanho = numeroOperacoesGanho
        self.payout = payout
        self.tipoGerenciamento = tipoGerenciamento
        self.wb = wb
        self.ws = wb.sheets["Calculadora"]
        self.app = app
        self.alterarParametros(capitalRisco, numeroOperacoes, numeroOperacoesGanho, tipoGerenciamento, payout)
    
    def __lerCedula(self, linha, coluna):
        cedula = coluna.upper()+str(linha)
        valor = self.ws.range(cedula).value
        return valor
    
    def alterarParametros(self, capitalR, numeroOp, numeroOpGanho, tipoGerenciamento, payoutOp=2):
        self.ws.range(self.cedulaParam["capitalRisco"]).value = capitalR
        self.ws.range(self.cedulaParam["numeroOperacoes"]).value = numeroOp
        self.ws.range(self.cedulaParam["numeroOperacoesGanho"]).value = numeroOpGanho
        self.ws.range(self.cedulaParam["payout"]).value = payoutOp
        self.ws.range(self.cedulaParam["tipoGerenciamento"]).value = tipoGerenciamento

    def get_ciclo_status_ultima_op(self):
        befGerenciamento = self.ws.range(self.cedulaParam["tipoGerenciamento"]).value
        if befGerenciamento != "Normal":
            self.ws.range(self.cedulaParam["tipoGerenciamento"]).value = "Normal"
            linha = self.linhaOp - 1 
            ciclo = self.__lerCedula(linha, self.colunaOp["ciclo"])
            self.ws.range(self.cedulaParam["tipoGerenciamento"]).value = befGerenciamento
            return ciclo
        return None      

    def obterValorInvestimento(self, coberturaNoBranco=False):
        valor = self.__lerCedula(self.linhaOp, self.colunaOp["investimento"])
        if isinstance(valor, str):
            return False

        if not coberturaNoBranco:
            valor = round(float(valor), 2) if valor > 0.1 else 0.1
            return {"aposta": valor, "cobertura": 0}
        else:
            valor = round(float(valor), 2) if valor > 0.2 else 0.2
            cobertura = 0.1
            while cobertura*14 < valor-cobertura:
                cobertura+=0.01
            return {"aposta": round(valor-cobertura,2), "cobertura": round(cobertura,2)}

    def escreveResultadoOp(self, status, retorno=None):
        cedula = self.colunaOp["resultado"]+str(self.linhaOp)
        self.ws.range(cedula).value = status

        #troca para a planilha 'algoritmo' e atualiza o lucro para fazer o cálculo do próximo valor de investimento
        if retorno != None:
            cedula = "D"+str(self.linhaOp)
            self.ws = self.wb.sheets["algoritmo"]
            self.ws.range(cedula).value = retorno

            #volta para a planilha 'calculadora'
            self.ws = self.wb.sheets["Calculadora"]

        ciclo = self.__lerCedula(self.linhaOp, self.colunaOp["ciclo"])
        self.linhaOp += 1

        return ciclo
    
