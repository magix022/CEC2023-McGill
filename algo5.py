import pandas as pd
import pulp as pulp

df1 = pd.read_csv("table1_clean.csv")
df3 = pd.read_csv("table3_clean.csv")
# df3 = df3.drop(columns=['Urgency','Time to ship from Canada to Country (days)','Date Resource is Required by (yyyy-mm-dd)'])

# #print smallest country request 
df4 = pd.merge(df3, df1[['Key', 'UnitPrice']], on='Key')
df4['TotalPrice'] = df4['UnitPrice'] * df4['Quantity']

# print(df4)

print(df4.groupby('Country').sum().sort_values('TotalPrice').head(1))
# Get all rows from Cocoa Islands
# print(df3.loc[df3['Country'] == 'Cook Islands (the)'])