import pandas as pd

s1 = pd.Series([5, 6, 7])
s2 = pd.Series([7, 8, 9])

df = pd.DataFrame([list(s1), list(s2)], columns=["A", "B", "C"])
#print(df)
df = df.append(pd.DataFrame([[5, 6, 7]], columns=["A", "B", "C"]), ignore_index=True)
#print(df)
df = df.append(pd.DataFrame([list(s2)], columns=["A", "B", "C"]), ignore_index=True)
#print(df)
dic = {'A':[10], 'B':[34], 'D':[33.54]}
#print(pd.DataFrame(dic))
df = df.append(pd.DataFrame(dic), ignore_index=True)
#print(df)
df.at[len(df)-1, 'C'] = 83.444
print(df)
# a = df[-1:]
# print(type(a.values))
# print(type(a['D'].values[0]))
# print(a['D'].values[0])
# df = pd.DataFrame([], columns=["A", "B", "C"])
# print(len(df))
# a = df[-1:]
# print(a)
# df.set_index('A')
# print(df.T.to_dict('list'))
#df[df['B']==8]['A']=4
df.loc[df['B']==8,'A'] = 4
print(df)