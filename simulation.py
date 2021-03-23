import pandas as pd
import talib

from models import Traider, Journal, StartegyBase, Stock, StrategyMACD_Day

data = pd.read_csv('data/day_data.csv', index_col=0, parse_dates=True)
data.index.name = 'date'
data = data[data['figi'] == 'BBG004730N88']

df = data[-80:-1]
data_limit_MACD = 33

balance = 0
amount = 20

journal = Journal()
traider = Traider(balance, journal, amount)
stock = Stock(traider, journal)

for i in range(data_limit_MACD, len(df)):
    # print(i)
    data_ = df[:i + 1]
    # print(data_)
    # print(talib.MACD(data_['Close']))
    traider.trade(data_, strategy=StrategyMACD_Day())
    stock.day_trade(data_[i:i + 1])

print(journal.get_orders())
print(journal.get_limits())
#print(talib.MACD(df['Close'])[2])
