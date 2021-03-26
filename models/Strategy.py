import random
import talib
import pandas as pd
import numpy as np


class Strategy():

    def __init__(self, *arg, **params):
        self.data: pd.DataFrame
        self.trend: str
        self.activity: bool
        self.action = ''
        self.stop_loss = ''
        self.take_profit = ''
        self.result = {}
        self.params = params

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
    def __init__(self, *arg, **params):
        super().__init__(self, *arg, **params)
        self.macd: list
        self.macd_stability = 0
        self.target_stability = self.params['target_stability']

    def calculate(self):

        loss_level = self.params['loss_level']
        profit_level = self.params['profit_level']
        macd_level = self.params['macd_level']

        local_trend = ''
        macd = talib.MACD(self.data['Close'])
        open_price = self.today['Open'].values[0]
        last_close = self.data['Close'][-3:].values
        no_empty = not (True in macd[2][-3:].isna().values)
        if no_empty:
            # print(macd[2])
            local_trend = self.define_trend(macd[2][-3:].values, macd_level)
        if local_trend in ['no_change', 'false_change', 'maybe_change', '']:
            self.activity = False
        elif local_trend in ['change_up', 'change_down']:
            self.activity = True
            if local_trend == 'change_up':
                self.action = 'buy'
            elif local_trend == 'change_down':
                self.action = 'sell'

        if self.activity:
            coef = -1 if self.action == 'buy' else 1
            # if self.action == 'buy':
            #     loss_level = min(last_close) if min(
            #         last_close) < open_price else open_price + coef * open_price * 2 / 100
            # else:
            #     loss_level = max(last_close) if max(
            #         last_close) > open_price else open_price + coef * open_price * 2 / 100
            # loss_level = 0.003
            # profit_level = 0.02
            self.stop_loss = open_price + coef * open_price * loss_level
            # self.stop_loss = loss_level
            self.take_profit = open_price + (-1) * coef * open_price * profit_level

    def define_trend(self, macd_values, macd_level=0):
        m1, m2, m3 = macd_values
        # print(m1,m2,m3)
        result = 'no_change'
        # print(abs(np.mean([m1, m2, m3])))
        if abs(np.mean([m1, m2, m3])) > macd_level:
            # Пересечения с нулем линии macdhist
            if m2 > 0 and m3 > 0 and m1 < 0:
                result = 'change_up'
            elif m2 < 0 and m3 < 0 and m1 > 0:
                result = 'change_down'
            elif (m2 > 0 and m3 < 0 and m1 < 0) or (m2 < 0 and m3 > 0 and m1 > 0):
                result = 'false_change'
            elif (m2 < 0 and m3 < 0 and m1 < 0) or (m2 > 0 and m3 > 0 and m1 > 0):
                result = 'no_change'
            elif (m2 < 0 and m3 > 0 and m1 < 0) or (m2 > 0 and m3 < 0 and m1 > 0):
                result = 'maybe_change'

            # Проверка на смену тренда
            if (m2 < m3 and m2 < m1):
                if self.macd_stability >= self.target_stability:
                    result = 'change_up'
                    self.macd_stability = 0
                else:
                    self.macd_stability = 0
            elif (m2 > m3 and m2 > m1):
                if self.macd_stability >= self.target_stability:
                    result = 'change_down'
                    self.macd_stability = 0
                else:
                    self.macd_stability = 0

            # # Проверка на смену тренда
            # if (m2 < m3 and m2 < m1):
            #     result = 'maybe_change'
            # elif (m2 > m3 and m2 > m1):
            #     result = 'maybe_change'

            # Проверка на сохранение тренда
            if (m2 < m3 and m2 > m1):
                result = 'change_up'
                self.macd_stability += 1
            elif (m2 > m3 and m2 < m1):
                result = 'change_down'
                self.macd_stability += 1

        # temp = random.choice(['no_change', 'change_up', 'change_down', 'false_change', 'maybe_change'])
        # print(result)
        return result
