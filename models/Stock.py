class Stock():

    def __init__(self, traider, journal):
        self.traider = traider
        self.journal = journal
        self.data = {}

    def day_trade(self, day_data):
        stop_loss = None
        take_profit = None
        self.data = [data for data in day_data.T.to_dict().values()][0]
        limits = self.journal.get_limits()
        open_limits = limits[limits['status'] == 'open']
        # print(open_limits)
        if not open_limits.empty:
            direction = list(open_limits[open_limits['action'] == 'stop_loss']['direction'])[0]
            stop_loss = list(open_limits[open_limits['action'] == 'stop_loss']['price'])
            take_profit = list(open_limits[open_limits['action'] == 'take_profit']['price'])
            stop_loss = stop_loss[0] if stop_loss else None
            take_profit = take_profit[0] if take_profit else None
            if direction == 'sell':
                action = 'buy'
                if self.data['High'] >= stop_loss:
                    self.traider.new_order(day_data, type='close', action=action, price='', stop_loss_price=stop_loss,
                                           source='stop_loss')
                elif take_profit and self.data['Low'] <= take_profit:
                    self.traider.new_order(day_data, type='close', action=action, price='',
                                           take_profit_price=take_profit,
                                           source='take_profit')
            else:
                action = 'sell'
                if self.data['Low'] <= stop_loss:
                    self.traider.new_order(day_data, type='close', action=action, price='', stop_loss_price=stop_loss,
                                           source='stop_loss')
                elif take_profit and self.data['High'] >= take_profit:
                    self.traider.new_order(day_data, type='close', action=action, price='',
                                           take_profit_price=take_profit,
                                           source='take_profit')
        # print(self.data['Close'])
