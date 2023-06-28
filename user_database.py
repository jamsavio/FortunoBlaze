# -*- coding: utf-8 -*-
import sqlite3

class UserDatabase:
    def __init__(self, db_file="user.db"):
        self.db_file = db_file

    def add_estrategia(self, padrao, previsao):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estrategias (padrao, previsao) VALUES (?, ?)", (padrao, previsao))
        conn.commit()
        conn.close()

    def del_estrategias(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estrategias")
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'estrategias'")
        conn.commit()
        conn.close()

    def list_estrategias(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT padrao, previsao
                          FROM estrategias''')
        estrategias = cursor.fetchall()
        conn.close()

        estrategias_list = []
        for estrategia in estrategias:
            estrategia_dict = {'padrao': estrategia[0].split(), 'previsao': estrategia[1]}
            estrategias_list.append(estrategia_dict)

        return estrategias_list
    
    def config_gerenciamento_masaniello(self, gerenciamento, operacoes, acertos, riscoCiclo, reiniciarCiclo, stopWin, stopLoss, cobrirBranco, tipoGerenciamento):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("UPDATE gerenciamento SET gerenciamento = ?, operacoes = ?, acertos = ?, riscoCiclo = ?, reiniciarCiclo = ?, stopWin = ?, stopLoss = ?, cobrirBranco = ?, tipoGerenciamento = ?", 
                       (gerenciamento, operacoes, acertos, riscoCiclo, reiniciarCiclo, stopWin, stopLoss, cobrirBranco, tipoGerenciamento))
        conn.commit()
        conn.close()
    
    def config_gerenciamento_maofixa(self, gerenciamento, stopWin, stopLoss, cobrirBranco, valorMaoFixa):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("UPDATE gerenciamento SET gerenciamento = ?, stopWin = ?, stopLoss = ?, cobrirBranco = ?, valorMaoFixa = ?", 
                       (gerenciamento, stopWin, stopLoss, cobrirBranco, valorMaoFixa))
        conn.commit()
        conn.close()
    
    def get_gerenciamento(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gerenciamento")
        gerenciamento_data = cursor.fetchall()
        conn.close()

        gerenciamento_dict = {}
        for gerenciamento in gerenciamento_data:
            gerenciamento_dict = {'nomeGerenciamento': gerenciamento[0], 
                                'operacoes': gerenciamento[1], 
                                'acertos': gerenciamento[2], 
                                'riscoCiclo': gerenciamento[3], 
                                'reiniciarCiclo': gerenciamento[4], 
                                'stopWin': gerenciamento[5], 
                                'stopLoss': gerenciamento[6], 
                                'cobrirBranco': gerenciamento[7], 
                                'tipoGerenciamento': gerenciamento[8], 
                                'valorMaoFixa': gerenciamento[9]}
        return gerenciamento_dict
    
    def set_login(self, email, senha):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        data_user = self.get_login()
        if len(data_user) == 2:
            cursor.execute("UPDATE usuario SET email = ?, senha = ?", (email, senha))
        else:
            cursor.execute("INSERT INTO usuario (email, senha) VALUES (?, ?)", (email, senha))

        conn.commit()
        conn.close()
    
    def del_login(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario")
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'usuario'")
        conn.commit()
        conn.close()
    
    def get_login(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        data = cursor.fetchall()
        conn.close()

        data_dict = {}
        for data_user in data:
            data_dict = {'email': data_user[0],
                         'senha': data_user[1]}
        
        return data_dict