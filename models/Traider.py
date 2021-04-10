import pandas as pd

from models import Journal, Strategy


class Traider():

    def __init__(self, balance, journal: Journal, amount=20, simulate=True, sandbox=True, figi=''):
        self.start_balance = balance
        self.balance = balance
        self.journal = journal
        self.amount = amount
        self.simulate = simulate
        self.sandbox = sandbox
        self.figi = figi

    def trade(self, data: pd.DataFrame, strategy: Strategy):
        amount = self.amount
        result_strategy = strategy(data)
        is_possible = False
        type_deal = ''
        if self.journal.get_orders().empty:
            is_possible = True
            type_deal = 'open'
        elif self.journal.get_orders()[-1:]['status'].values[0] == 'close':
            is_possible = True
            type_deal = 'open'
        elif self.journal.get_orders()[-1:]['action'].values[0] != result_strategy['action']:
            is_possible = True
            type_deal = 'close'
        if is_possible:
            if result_strategy['activity']:
                self.new_order(data,
                               amount=amount,
                               type=type_deal,
                               action=result_strategy['action'],
                               stop_loss_price=result_strategy['stop_loss'],
                               take_profit_price=result_strategy['take_profit'],
                               source='strategy'
                               )

    def new_order(self, data, type, action, amount='', price='', stop_loss_price='', take_profit_price='', source=''):
        coef = -1 if action == 'buy' else 1
        amount = amount if amount else self.amount
        stop_loss = None
        take_profit = None
        price = float(data[-1:]['Open'].values[0]) if not price else price
        if source != 'strategy':
            if stop_loss_price:
                price = stop_loss_price
            if take_profit_price:
                price = take_profit_price
        #date = data[-1:].index.tolist()[0:1][0]
        #print(date)
        order = {
            'date': data[-1:].index.tolist()[0:1][0],
            'price': price,
            'amount': amount,
            'action': action,
            'sum': round(coef * price * amount, 2),
            'status': type,
            'source': source
        }
        self.balance += float(order['sum'])
        order['income'] = 0
        order['balance'] = self.balance

        if type == 'open':
            if stop_loss_price:
                stop_loss = {
                    'date': data[-1:].index.tolist()[0:1][0],
                    'price': stop_loss_price,
                    'amount': amount,
                    'action': 'stop_loss',
                    'sum': '',
                    'id_order': len(self.journal.get_orders()),
                    'status': 'open',
                    'direction': action
                }
            if take_profit_price:
                take_profit = {
                    'date': data[-1:].index.tolist()[0:1][0],
                    'price': take_profit_price,
                    'amount': amount,
                    'action': 'take_profit',
                    'sum': '',
                    'id_order': len(self.journal.get_orders()),
                    'status': 'open',
                    'direction': action
                }
        if type == 'close':
            ind = len(self.journal.get_orders()) - 1
            self.journal.change_value(index=ind, column='status', new='close', type='orders')
            self.journal.change_value(index=ind, column='status', new='close', type='limits')
            income = coef * (price - float(self.journal.get_orders().loc[ind]['price'])) * amount
            order['income'] = round(income, 2)
            # print(self.journal.get_orders().loc[ind]['price'])

        if self.simulate:
            self.fix_transaction(order)
            if stop_loss:
                self.set_limit(stop_loss)
            if take_profit:
                self.set_limit(take_profit)
        else:
            self.trade_on_stock(order)
            if stop_loss:
                self.set_on_stock(stop_loss)
            if take_profit:
                self.set_on_stock(take_profit)

    def fix_transaction(self, order: dict):
        self.journal.write_order(order)

    def set_limit(self, limit):
        self.journal.write_limit(limit)

    def trade_on_stock(self, order: dict):
        pass

    def set_on_stock(self, limit: dict):
        pass

    def restart(self):
        self.balance = self.start_balance
        self.journal.clear()
