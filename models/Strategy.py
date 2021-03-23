import random
import talib
import pandas as pd


class Strategy():

    def __init__(self):
        self.data: pd.DataFrame
        self.trend: str
        self.activity: bool
        self.action = ''
        self.stop_loss = ''
        self.take_profit = ''
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


class StrategyMACD_Day(Strategy):
    def __init__(self):
        super().__init__()
        self.macd: list

    def define_trend(self):
        temp = random.choice(['no_change', 'change_up', 'change_down', 'false_change', 'maybe_change'])
        return temp

    def calculate(self):
        macd = talib.MACD(self.data['Close'])
        local_trend = self.define_trend()
        if local_trend in ['no_change', 'false_change', 'maybe_change']:
            self.activity = False
        elif local_trend in ['change_up', 'change_down']:
            self.activity = True
            if local_trend == 'change_up':
                self.action = 'buy'
            elif local_trend == 'change_down':
                self.action = 'sell'

        if self.activity:
            coef = -1 if self.action == 'buy' else 1
            self.stop_loss = self.today['Open'].values[0] + coef * self.today['Open'].values[0] * 0.01
            self.take_profit = self.today['Open'].values[0] + (-1) * coef * self.today['Open'].values[0] * 0.05
