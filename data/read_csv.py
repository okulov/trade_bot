import numpy as np
import csv

data = []
for i in np.linspace(0.01, 0.05, num=5):
    print(i)
    file = f'exp_loss_profit_{round(i,3)}.csv'
    with open(file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        HEADERS = reader.fieldnames
        for row in reader:
            data.append(row)
print(data[1:10])
print(len(data))
with open(f'exp_loss_params.csv', 'w', newline='') as f_n:
    F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(data[0].keys()),
                                quoting=csv.QUOTE_NONNUMERIC)
    F_N_WRITER.writeheader()
    for d in data:
        F_N_WRITER.writerow(d)