import csv

import pandas as pd


class Journal():
    columns = ['date', 'amount', 'sum', 'action', 'price', 'status']
    columns_orders = columns + ['income', 'balance', 'source']
    columns_limits = columns + ['id_order', 'direction']

    def __init__(self):
        self.limits = pd.DataFrame([], columns=self.columns_limits)
        self.orders = pd.DataFrame([], columns=self.columns_orders)

    def write_order(self, order):
        self.orders = self.orders.append(pd.DataFrame(order), ignore_index=True)

    def get_orders(self):
        return self.orders

    def write_limit(self, limit):
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

        #print(data)
        with open(f'journals/journal_orders.csv', 'w', newline='') as f_n:
            F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(data[0].keys()),
                                        quoting=csv.QUOTE_NONNUMERIC)
            F_N_WRITER.writeheader()
            for d in data:
                F_N_WRITER.writerow(d)
