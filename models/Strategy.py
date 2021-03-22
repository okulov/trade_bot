import random
import talib
import pandas as pd


class Strategy():

    def __init__(self):
        self.data: pd.DataFrame
        self.activity: bool
        self.action: str
        self.stop_loss: str
        self.take_profit: str
        self.result = {}

    def calculate(self):
        pass

    def __call__(self, data):
        self.data = data[:-1]
        self.today = data[-1:]
        self.calculate()
        self.result = {'activity': self.activity,
                       'action': self.action,
                       'stop_loss': self.stop_loss,
                       'take_profit': self.take_profit}
        return self.result


class StartegyBase(Strategy):
    def calculate(self):
        self.activity = True
        self.action = random.choice(['buy', 'sell'])
        coef = -1 if self.action == 'buy' else 1
        self.stop_loss = self.today['Open'].values[0] + coef * self.today['Open'].values[0] * 0.01
        self.take_profit = self.today['Open'].values[0] + (-1) * coef * self.today['Open'].values[0] * 0.05

class StrategyMACD(Strategy):
    def calculate(self):
        print(self.data['Close'])
        # macd = talib.MACD(self.data['Close'])
        # print(macd)
        self.activity = True
        self.action = random.choice(['buy', 'sell'])
        coef = -1 if self.action == 'buy' else 1
        self.stop_loss = self.today['Open'].values[0] + coef * self.today['Open'].values[0] * 0.01
        self.take_profit = self.today['Open'].values[0] + (-1) * coef * self.today['Open'].values[0] * 0.05