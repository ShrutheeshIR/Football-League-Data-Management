import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector


def fun(tid1, tid2):

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Fkafka",
  database="footballproject"
  )
  print(mydb)
  mycursor = mydb.cursor()
  mycursor.execute("select MID,matches.AG from matches,teams where matches.season='2017/18' and matches.at=teams.TID and teams.tid="+str(tid1)+" union select mid,matches.HG from matches,teams where matches.season='2017/18' and matches.ht=teams.TID and teams.tid="+str(tid1)+" order by mid asc;")
  myresult = mycursor.fetchall()
  # print(myresult)
  df1 = pd.DataFrame(myresult, columns=['Match', 'Goals'])
  # print(df1)
  mycursor.execute("select MID,matches.AG from matches,teams where matches.season='2017/18' and matches.at=teams.TID and teams.tid="+str(tid2)+" union select mid,matches.HG from matches,teams where matches.season='2017/18' and matches.ht=teams.TID and teams.tid="+str(tid2)+" order by mid asc;")
  myresult = mycursor.fetchall()
  df2 = pd.DataFrame(myresult, columns=['Match', 'Goals'])
  # print(df2)
  
  # print(myresult)
  # df2 = pd.DataFrame(myresult)
  # model = ExponentialSmoothing(df1['Goals'].tolist(), seasonal='mul', seasonal_periods=12).fit()
  # pred = model.predict(start=test.index[0], end=test.index[-1])
  if df1['Goals'].mean() > df2['Goals'].mean():
    print('WIN')
  elif df1['Goals'].mean() < df2['Goals'].mean():
    print('LOSS')
  else:
    print('DRAW')

fun(12, 7)
