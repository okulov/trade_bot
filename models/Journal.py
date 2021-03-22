import pandas as pd


class Journal():
    columns = ['date', 'amount', 'sum', 'action', 'price', 'status']
    columns_orders = columns + ['balance', 'source']
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
