import pandas as pd

from models import Traider, Journal, StartegyBase, Stock, StrategyMACD

data = pd.read_csv('data/day_data.csv', index_col=0, parse_dates=True)
data.index.name = 'date'
data = data[data['figi'] == 'BBG004730N88']
journal = Journal()
traider = Traider(0, journal)
stock = Stock(traider, journal)
df = data[-50:-1]
for i in range(len(df)):
    data_ = df[:i + 1]
    #print(data_[i:i + 1])
    traider.trade(data_, strategy=StrategyMACD())
    stock.day_trade(data_[i:i + 1])

print(journal.get_orders())
print(journal.get_limits())
