# -*- coding: utf-8 -*-
import requests
import datetime
import threading
import time

class Monitor():
    __padraoEncontrado = None
    breakThreads = False
    sequenciaPadraoG = None
    previsaoPadraoG = None
    exception = False

    def __init__(self, padroes):
        self.padroes = padroes

    def Monitoring(self):
        self.__padraoEncontrado = None
        threads = []

        for valor in self.padroes:
            sequenciaPadrao = [padrao.upper() for padrao in valor["padrao"]]
            previsaoPadrao = valor["previsao"].upper()

            t = threading.Thread(target=self.__MonitorThread, args=(sequenciaPadrao, previsaoPadrao))
            t.start()
            threads.append(t)

        while threads:
            if self.exception:
                break
            if self.__padraoEncontrado or self.breakThreads:
                for t in threads:
                    t.join()
                return self.__padraoEncontrado
            time.sleep(0.1)
        

    def __MonitorThread(self, sequenciaPadrao, previsaoPadrao):
        try:
            while not self.breakThreads:
                lastDoubles = self.__GetLastDoubles()["items"]
                colors = ([item['color'] for item in lastDoubles])[::-1]

                if len(sequenciaPadrao) > len(colors):
                    break
                elif self.__padraoEncontrado:
                    break
                else:
                    lastColors = colors[-len(sequenciaPadrao):]
                    
                    sequenciaPadraoFormatted = [lastColors[i] if lastColors[i] in el else el for i, el in enumerate(sequenciaPadrao)]
                    
                    self.sequenciaPadraoG = " ".join(sequenciaPadrao)
                    self.previsaoPadraoG = previsaoPadrao
                    
                    if sequenciaPadraoFormatted == lastColors:
                        self.__padraoEncontrado = {"padrao": sequenciaPadraoFormatted, "previsao": previsaoPadrao}
                        break
                        
                time.sleep(1)
        except Exception as e:
            try:
                print("tentando se conectar novamente em 3 segundos")
                time.sleep(3)
                self.__MonitorThread(sequenciaPadrao, previsaoPadrao)
                return
            except Exception as e:
                self.exception = True
                return

    @staticmethod
    def __GetLastDoubles():
        try:
            response = requests.get("https://blaze.com/api/roulette_games/recent")

            if response:
                result = {
                    "items": [{"color": "B" if i["color"] == 0 else "V" if i["color"] == 1 else "P",
                            "value": i["roll"], "created_date": datetime.datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")}
                            for i in response.json()]
                        }
                return result
        except:
            pass
    
    def ConfirmLastDoubles(self, lastSequence):
        lastDoubles = self.__GetLastDoubles()["items"]
        colors = ([item['color'] for item in lastDoubles])[::-1]
        lastColors = colors[-len(lastSequence):]
        sequenciaPadraoFormatted = [lastColors[i] if lastColors[i] in el else el for i, el in enumerate(lastSequence)]
        return lastColors == sequenciaPadraoFormatted

    '''@staticmethod
    def __GetLastCrashs():
        response = requests.get("https://blaze.com/api/crash_games/recent")

        if response:
            result = {
                "items": [{"color": "preto" if float(i["crash_point"]) < 2 else "verde", "value": i["crash_point"]}
                          for i in response.json()]}
            return result
        return False'''