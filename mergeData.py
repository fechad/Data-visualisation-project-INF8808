import pandas as pd
import numpy as np

# with open('./Hydro_Pascal/src1.csv') as f:
#     print(f)

dfP = pd.read_csv('./Hydro_Pascal/src1.csv',sep=';',encoding="cp1252",decimal=',')
dfP = pd.concat([dfP, pd.read_csv('./Hydro_Pascal/src2.csv',sep=';',encoding="cp1252",decimal=',')], ignore_index=True)
dfP = pd.concat([dfP, pd.read_csv('./Hydro_Pascal/src3.csv',sep=';',encoding="cp1252",decimal=',')], ignore_index=True)
dfP = pd.concat([dfP, pd.read_csv('./Hydro_Pascal/src4.csv',sep=';',encoding="cp1252",decimal=',')], ignore_index=True)
dfP = pd.concat([dfP, pd.read_csv('./Hydro_Pascal/src5.csv',sep=';',encoding="cp1252",decimal=',')], ignore_index=True)

dfF = pd.read_csv('./Hydro_Fedwin/src1.csv',sep=';',encoding="cp1252")
dfF = pd.concat([dfF, pd.read_csv('./Hydro_Fedwin/src2.csv',sep=';',encoding="cp1252")], ignore_index=True)
dfF = pd.concat([dfF, pd.read_csv('./Hydro_Fedwin/src3.csv',sep=';',encoding="cp1252")], ignore_index=True)
dfF = pd.concat([dfF, pd.read_csv('./Hydro_Fedwin/src4.csv',sep=';',encoding="cp1252")], ignore_index=True)
dfF = pd.concat([dfF, pd.read_csv('./Hydro_Fedwin/src5.csv',sep=';',encoding="cp1252")], ignore_index=True)

dfF.set_axis(dfP.columns, axis=1, inplace=True)
print(dfF.iloc[1])
print(dfP.iloc[1])
df = pd.concat([dfP,dfF], ignore_index=True)
df['Date et heure'] = pd.to_datetime(df['Date et heure'])
print(type(df['Date et heure'][1]))
print(pd.Timestamp(2022, 6, 7, 00))
df = df.drop(df[pd.DatetimeIndex(df['Date et heure']) < pd.Timestamp(2022, 6, 7, 00)].index)
# print(dfP)
# print(dfF)
pd.set_option('display.max_rows', 4)
df.sort_values("Date et heure",inplace=True)
print(df)

df.to_csv('./out.csv',index=False,index_label=False,sep=";",encoding="cp1252")
# print("KWH min: ")
print("KWH min: " + str(df['kWh'].min()))
print("KWH max: " + str(df['kWh'].max()))
print("KWH mean: " + str(df['kWh'].mean()))
print("KWH median: " + str(df['kWh'].median()))
print("T min: " + str(df['Température moyenne (°C)'].min()))
print("T max: " + str(df['Température moyenne (°C)'].max()))
print("T mean: " + str(df['Température moyenne (°C)'].mean()))
print("T median: " + str(df['Température moyenne (°C)'].median()))
print(df.count)
