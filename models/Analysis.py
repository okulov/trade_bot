import csv
import os

import pandas as pd
import numpy as np

from models import Journal, Traider


class Analysis():

    # процент успешных сделок
    # доля take_profit
    # доля stop_loss
    # доход по стратегии за весь период
    # средний доход по стратегии за месяц
    # средний доход по стратегии за неделю
    # средний доход по take_profit
    # средний доход по stop_loss

    def __init__(self, traider: Traider, journal: Journal):
        self.orders_file = journal.name_file_orders
        self.orders = []
        self.figi = traider.figi

    def score(self, name_file = None):
        print(self.orders_file)
        if os.stat(self.orders_file).st_size != 0:
            data = pd.read_csv(self.orders_file)
            result = {**self.get_params(), **self.get_scores(data)}
            print({**self.get_params(), **self.get_scores(data)})
            if name_file:
                with open(name_file, 'r+', newline='') as f_n:
                    F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(result.keys()),
                                                quoting=csv.QUOTE_NONNUMERIC)
                    if os.stat(name_file).st_size == 0:
                        F_N_WRITER.writeheader()
                    else:
                        f_n.seek(0, 2)
                    F_N_WRITER.writerow(result)


    def get_scores(self, data: pd.DataFrame):
        rate_success = round(len(data[data['income'] > 0]) / len(data) * 100, 2)
        rate_loss = round(len(data[data['source'] == 'stop_loss']) / len(data) * 100, 2)
        rate_profit = round(len(data[data['source'] == 'take_profit']) / len(data) * 100, 2)
        income_loss = round(np.mean(data[data['source'] == 'stop_loss']['income']), 2)
        income_profit = round(np.mean(data[data['source'] == 'take_profit']['income']), 2)
        profit_all = round(data['balance'][-1:].values[0] if data['status'][-1:].values[0] == 'close' else \
            data['balance'][-2:-1].values[0], 2)
        data['date'] = pd.to_datetime(data['date'])
        date_close = data[data['status'] == 'close']
        temp_df = date_close.groupby([date_close.date.dt.strftime('%Y-%m')], sort=True).income.agg(
                [('Sum', 'sum'), ('Average', 'mean')])
        profit_mounth = round(np.mean(temp_df['Average']), 2)
        temp_df = date_close.groupby([date_close.date.dt.strftime('%Y-%W')], sort=True).income.agg(
                [('Sum', 'sum'), ('Average', 'mean')])
        profit_week = round(np.mean(temp_df['Average']), 2)

        # print(data.head(50))
        scores = {
            'rate_success': rate_success,
            'rate_success': rate_success,
            'rate_loss': rate_loss,
            'rate_profit': rate_profit,
            'income_loss': income_loss,
            'income_profit': income_profit,
            'profit_all': profit_all,
            'profit_mounth': profit_mounth,
            'profit_week': profit_week,
        }
        return scores

    def get_params(self):
        params = {
            'figi': self.figi,
        }
        return params
