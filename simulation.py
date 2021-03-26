import csv

import pandas as pd
import talib
import numpy as np

from models import Traider, Journal, StartegyBase, Stock, StrategyMACD_Day

data = pd.read_csv('data/hour_data.csv', index_col=0, parse_dates=True)
data.index.name = 'date'
data = data[data['figi'] == 'BBG004730N88']
# print(len(data))
df = data[-700:]
data_limit_MACD = 33
# data_limit_MACD = 0

balance = 0
amount = 200

journal = Journal()
traider = Traider(balance, journal, amount)
stock = Stock(traider, journal)

params = {'loss_level': 0.003, 'profit_level': 0.02}
params = {'loss_level': 0.003,
          'profit_level': 0.02,
          'macd_level':0,
          'target_stability':0
          }

loss = params['loss_level']
profit = params['profit_level']
macd_level = params['macd_level']
target_stability = params['target_stability']

for i in range(data_limit_MACD, len(df)):
    data_ = df[:i + 1]
    # print(data_[-1:])
    # print(talib.MACD(data_['Close']))
    traider.trade(data_, strategy=StrategyMACD_Day(loss_level=loss, profit_level=profit, macd_level=macd_level,
                                                   target_stability=target_stability))
    # traider.trade(data_, strategy=StartegyBase())
    stock.day_trade(data_[i:i + 1])

print(journal.get_orders())
journal.save_to_csv()


def search_limits():
    for profit in np.linspace(0.01, 0.05, num=5):
        res = []
        for loss in np.linspace(0.001, 0.01, num=10):
            for macd_level in np.linspace(0.05, 0.5, num=10):
                for target_stability in np.linspace(0, 6, num=6):
                    for i in range(data_limit_MACD, len(df)):
                        data_ = df[:i + 1]
                        # print(data_[-1:])
                        # print(talib.MACD(data_['Close']))
                        traider.trade(data_, strategy=StrategyMACD_Day(loss_level=loss, profit_level=profit,
                                                                       macd_level=macd_level,
                                                                       target_stability=int(target_stability)))
                        stock.day_trade(data_[i:i + 1])
                    try:
                        exp = {
                            'loss': round(loss, 3),
                            'profit': round(profit, 3),
                            'macd_level': round(macd_level, 2),
                            'target_stability': int(target_stability),

                        }
                        if journal.get_orders()[-1:]['status'].values[0] == 'close':
                            balance_res = journal.get_orders()[-1:]['balance'].values[0]
                        else:
                            balance_res = journal.get_orders()[-2:-1]['balance'].values[0]
                    except IndexError:
                        continue
                    exp['balance'] = round(balance_res, 0)
                    print(exp)
                    res.append(exp)
                    traider.restart()

        with open(f'data/exp_loss_profit_{round(profit, 3)}.csv', 'w', newline='') as f_n:
            F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(res[0].keys()),
                                        quoting=csv.QUOTE_NONNUMERIC)
            F_N_WRITER.writeheader()
            for d in res:
                F_N_WRITER.writerow(d)

# search_limits()

# print(journal.get_limits())
# print(talib.MACD(df['Close'])[2])
