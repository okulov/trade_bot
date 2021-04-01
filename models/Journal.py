import csv
import datetime
import os

import pandas as pd


class Journal():
    columns = ['date', 'amount', 'sum', 'action', 'price', 'status']
    columns_orders = columns + ['income', 'balance', 'source']
    columns_limits = columns + ['id_order', 'direction']

    def __init__(self, mode=None):
        self.limits = pd.DataFrame([], columns=self.columns_limits)
        self.orders = pd.DataFrame([], columns=self.columns_orders)
        self.mode = mode
        self.name_file_limits = f'journals/limits_{datetime.datetime.now().strftime("%d_%m_%y_%H_%M")}.csv'
        self.name_file_orders = f'journals/orders_{datetime.datetime.now().strftime("%d_%m_%y_%H_%M")}.csv'
        self.create_files()

    def write_order(self, order):
        self.write_record_to_file(self.name_file_orders, order)
        if self.mode == 'debug':
            print(order)
        order['date'] = [order['date']]
        self.orders = self.orders.append(pd.DataFrame.from_dict(order), ignore_index=True)

    def get_orders(self):
        return self.orders

    def write_limit(self, limit):
        self.write_record_to_file(self.name_file_limits, limit)
        if self.mode == 'debug':
            print(limit)
        limit['date'] = [limit['date']]
        self.limits = self.limits.append(pd.DataFrame(limit), ignore_index=True)

    def get_limits(self):
        return self.limits

    def change_value(self, index, column, new, type):
        if type == 'orders':
            self.orders.at[index, column] = new
        else:
            self.limits.loc[self.limits['id_order'] == index, column] = new

    def clear(self):
        self.__init__()

    def save_to_csv(self):
        data = [record for record in self.get_orders().T.to_dict().values()]

        # print(data)
        with open(f'journals/journal_orders.csv', 'w', newline='') as f_n:
            F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(data[0].keys()),
                                        quoting=csv.QUOTE_NONNUMERIC)
            F_N_WRITER.writeheader()
            for d in data:
                F_N_WRITER.writerow(d)

    def write_record_to_file(self, file_name, data):
        with open(file_name, 'r+', newline='') as f:
            F_N_WRITER = csv.DictWriter(f, fieldnames=list(data.keys()),
                                        quoting=csv.QUOTE_NONNUMERIC)
            if os.stat(file_name).st_size == 0:
                F_N_WRITER.writeheader()
            else:
                f.seek(0, 2)
            F_N_WRITER.writerow(data)

    def create_files(self):
        with open(self.name_file_limits, 'w') as f:
            pass
        with open(self.name_file_orders, 'w') as f:
            pass
