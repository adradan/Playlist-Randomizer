import pandas as pd

data = {'Artist': ['Daniel Caesar', 'Billie Eilish'],
        'ID': ['123123123', 'asdfasdf']}
# data = {'Name':['Tom', 'nick', 'krish', 'jack'],
#         'Age':[20, 21, 19, 18]}

df = pd.DataFrame(data)
print(df)
df.loc['Daniel Caesar', 'Anotha'] = 'AHA'
print(df)
