from operator import concat
import os
import json
from re import I
from time import strftime
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

key = '4b7841486d776f6436364a65547742'

url = 'http://openapi.seoul.go.kr:8088/4b7841486d776f6436364a65547742/json/BukChonInOutPeopleInfo/%s/%s' %(0, 999)
resp = requests.get(url)
data2 = resp.text
dict_data = json.loads(data2)
df1 = pd.DataFrame(dict_data['BukChonInOutPeopleInfo']['row'])
df1['ENDTIME'] = pd.to_datetime(df1['ENDTIME'])
df1['MONTH'] = df1['ENDTIME'].dt.month
df1['WEEKDAY'] = df1['ENDTIME'].dt.weekday
df1['DAY'] = df1['ENDTIME'].dt.day
df1['HOUR'] = df1['ENDTIME'].dt.hour


for i in range(1,3):
    start_num = i * 1000
    final_num = start_num + 999
    url = 'http://openapi.seoul.go.kr:8088/4b7841486d776f6436364a65547742/json/BukChonInOutPeopleInfo/%s/%s' %(str(start_num), str(final_num))
    resp1 = requests.get(url)
    data1 = resp1.text
    dict_data1 = json.loads(data1)
    
    df2 = pd.DataFrame(dict_data1['BukChonInOutPeopleInfo']['row'])
    df2['ENDTIME'] = pd.to_datetime(df2['ENDTIME'])
    df2['MONTH'] = df2['ENDTIME'].dt.month
    df2['WEEKDAY'] = df2['ENDTIME'].dt.weekday
    df2['DAY'] = df2['ENDTIME'].dt.day
    df2['HOUR'] = df2['ENDTIME'].dt.hour
    

    # weekday 는 월(0) - 일(6) 이다.
    df1 = pd.concat([df1,df2])
    print(i)


plt.figure(figsize=(60,60))

dfcam1 = df1.loc[df1['DEVICEID'] == 1]
dfcam2 = df1.loc[df1['DEVICEID'] == 2]
dfcam4 = df1.loc[df1['DEVICEID'] == 4]


sns.barplot(data = dfcam4, x = 'MONTH', y = 'INCOUNT')
sns.barplot(data = dfcam4, x = 'HOUR', y = 'INCOUNT')
sns.barplot(data = dfcam4, x = 'WEEKDAY', y = 'INCOUNT')

sns.barplot(data = dfcam2, x = 'MONTH', y = 'INCOUNT')
sns.barplot(data = dfcam2, x = 'HOUR', y = 'INCOUNT')
sns.barplot(data = dfcam2, x = 'WEEKDAY', y = 'INCOUNT')


sns.barplot(data = dfcam1, x = 'MONTH', y = 'INCOUNT')
sns.barplot(data = dfcam1, x = 'HOUR', y = 'INCOUNT')
sns.barplot(data = dfcam1, x = 'WEEKDAY', y = 'INCOUNT')
plt.show()









