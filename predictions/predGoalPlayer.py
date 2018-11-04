import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

import numpy as np
import pandas as pd
import scipy

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="battlefield4",
  database="footballmanagement"
)

mycursor = mydb.cursor()

mycursor.execute("select matches.season,count(goal.GID) from goal,player,matches where goal.P=player.PID and player.FN='wayne' and player.ln='rooney' and goal.mid = matches.mid group by matches.season;")

myresult = mycursor.fetchall()
# print(myresult)
x1 = list()
ctr=0
for x in myresult:
    x1.append((ctr,x[1]))
    ctr=ctr+1

# print(x1)
x=x1

points = np.array(x)

x = points[:,0]
y = points[:,1]

z = np.polyfit(x, y, 3)
f = np.poly1d(z)

x_new = np.linspace(0, 18, 50)
y_new = f(x_new)

trace1 = go.Scatter(
    x=x,
    y=y,
    mode='markers',
    name='Data',
    marker=dict(
        size=12
    )
)

trace2 = go.Scatter(
    x=x_new,
    y=y_new,
    mode='lines',
    name='Fit'
)

annotation = go.Annotation(
    x=6,
    y=-4.5,
    text='Rooney expected goals',
    showarrow=False
)

layout = go.Layout(
    title='Polynomial Fit',
    annotations=[annotation]
)

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)

py.iplot(fig, filename='interpolation-and-extrapolation')