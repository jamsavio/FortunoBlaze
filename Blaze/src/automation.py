# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

class Bot:
    driver = None
    BASE_URL = ""
    LOGIN_SUCCESS = None
    ACCOUNT_BALANCE = {}
    isDemo = False
    lucro = 0
    quantWin = 0
    quantLoss = 0
    ui_monitoramento = None
    monitor = None

    def __init__(self, ui_monitoramento, monitor):
        self.ui_monitoramento = ui_monitoramento
        self.monitor = monitor
        self.BASE_URL = 'https://blaze.com/pt/games/double'

    def Start(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1300,1000")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        chrome_options.add_argument("--log-level=3")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_position(500, 0, windowHandle="current")
        self.driver.get(self.BASE_URL)
       
    def Stop(self):    
        self.driver.quit()
    
    def BalanceNewValue(self, valor):
        self.ACCOUNT_BALANCE["saldo"] += valor 
    
    def Login(self, email, password):
        error = None
        
        try:
            wait = WebDriverWait(self.driver, 10)
            LOGIN_BUTTON = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div/div/div[1]/a')))
            LOGIN_BUTTON.click()
            
            time.sleep(1)
            EMAIL_INPUT = self.driver.find_elements(By.CLASS_NAME, 'input-wrapper')[0].find_element(By.TAG_NAME, 'input')
            EMAIL_INPUT.send_keys(email)
            
            time.sleep(0.2)
            PASSWORD_INPUT = self.driver.find_elements(By.CLASS_NAME, 'input-wrapper')[1].find_element(By.TAG_NAME, 'input')
            PASSWORD_INPUT.send_keys(password)
            
            time.sleep(0.2)
            SUBMIT_BUTTON = self.driver.find_element(By.CLASS_NAME, 'submit')
            SUBMIT_BUTTON.click()
            
            self.LOGIN_SUCCESS = True
        except Exception as e:
            error = [False, e]
        finally:
            if error:
                self.LOGIN_SUCCESS = False
                return error
            else:
                return [self.LOGIN_SUCCESS, None]
    
    def Get_Balance(self, valor):
        balanceResult = None
        balance = None 
        symbol = None

        self.lucro = 0
        self.quantWin = 0
        self.quantLoss = 0

        if not self.isDemo:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='header']/div[2]/div/div[2]/div/div[3]/div/a/div/div/div[1]"))
            )
            balance_description = element.text

            if "R$" in balance_description:
                symbol = "R$"
            elif "$" in balance_description:
                symbol = "$"
            elif "€" in balance_description:
                symbol = "€"

            balance = float(balance_description.replace(symbol+" ", "").replace(',', '.'))
        else:
            balance = valor
            symbol = "R$"

        balanceResult = {"saldo": balance, "symbol": symbol}
        self.ACCOUNT_BALANCE = balanceResult
        return balanceResult

    def is_driver_active(self):
        try:
            self.driver.title 
            return True
        except:
            return False
    
    def Bet(self, game, bets, return_results, lastSequence):
        try:
            POPUP = self.driver.find_element(By.XPATH, '//*[@id="root"]/main/div[3]/div/div[1]/i') 
            POPUP.click() 
        except:
            pass

        if game == "double":
            return self.BetDouble(bets, return_results, lastSequence)
    
    def BetDouble(self, bets, return_results, lastSequence):
        total_bet = 0
        
        for bet in bets:
            if isinstance(bet['color'], str) == False:
                return ["Stop","Use apenas B, P ou V nos campos da previsão"]
            
            if bet['color'].upper() == "B" or bet['color'].upper() == "P" or bet['color'].upper() == "V":
                pass
            else:
                return ["Stop","Use apenas B, P ou V nos campos da previsão"]
            
            if isinstance(bet['amount'], str):
                return ["Stop", "Valor da aposta está em formato incorreto"]
            
            if bet['amount'] < 0.1:
                total_bet += 0.1
            else:
                total_bet += bet['amount']
            
        if total_bet > self.ACCOUNT_BALANCE["saldo"]:
            return ["Stop", "Você não tem dinheiro suficiente"]
        
        current_status = None
        while current_status != "waiting" and not self.ui_monitoramento.isPressedTurnOn:
            current_status = requests.get('https://blaze.com/api/roulette_games/current')
            if current_status.status_code == 200:
                    current_status = current_status.json()['status']
            time.sleep(1)
        
        if not self.isDemo:
            bet_window_time = self.driver.find_element(By.XPATH, '//*[@id="roulette-timer"]/div/div[2]/span').text
            bet_window_time = bet_window_time.split(":")[0]
                
            if bet_window_time == "" or (bet_window_time != "" and int(bet_window_time) < 3):
                return [False, "Janela de tempo curta demais"]

        if not self.monitor.ConfirmLastDoubles(lastSequence):
            return [False, "Janela de tempo encerrada"]

        if self.ui_monitoramento.isPressedTurnOn:
            return [False, "O bot foi desligado manualmente"]
        
        if not self.isDemo:
            INPUT_AMOUNT = self.driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input')
            RED_BUTTON = self.driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[1]')
            BLACK_BUTTON = self.driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[3]')
            WHITE_BUTTON = self.driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[2]')
            BET_BUTTON = self.driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button')
            
            for bet in bets:
                
                INPUT_AMOUNT.clear()
                INPUT_AMOUNT.send_keys(str(bet['amount']))
                time.sleep(0.2)

                if bet['color'].lower() == "v":
                    RED_BUTTON.click()
                elif bet['color'].lower() == "p":
                    BLACK_BUTTON.click()
                elif bet['color'].lower() == "b":
                    WHITE_BUTTON.click()
                
                time.sleep(0.2)
                BET_BUTTON.click()
        
        if return_results == True:

            current_result = None
            current_status = None
            while current_status != "complete":
                result = requests.get('https://blaze.com/api/roulette_games/current')
                if result.status_code == 200:
                    current_status = result.json()['status']
                    current_result = result.json()
                time.sleep(1)
            
            result_color = None
            multiplier = None
            
            if current_result['color'] == 0:
                result_color = "B"
                multiplier = 14
            elif current_result['color'] == 1:
                result_color = "V"
                multiplier = 1
            elif current_result['color'] == 2:
                result_color = "P"
                multiplier = 1
            
            bet_results = []
            total_result = 0
            
            for bet in bets:
                result = None
                if bet['color'] == result_color:
                    result = bet['amount'] * multiplier
                else:
                    result = 0 - bet['amount']
                
                total_result += result
                bet_results.append({ "color": bet['color'], "amount": result})
                
            return [total_result, bet_results]
