import plotly
import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import json
import numpy as np
import pandas as pd
import scipy

def graphgoalteamweek(tid=None):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="battlefield4",
    database="footballmanagement"
    )

    mycursor = mydb.cursor()

    if tid==None:
        mycursor.execute("select MID,sum(matches.AG) from matches,teams where matches.season='2017/18' and matches.at=teams.TID group by matches.date union select mid,sum(matches.HG) from matches,teams where matches.season='2017/18' and matches.ht=teams.TID group by matches.date order by mid asc;")
    else:
        mycursor.execute("select MID,matches.AG from matches,teams where matches.season='2017/18' and matches.at=teams.TID and teams.tid="+str(tid)+" union select mid,matches.HG from matches,teams where matches.season='2017/18' and matches.ht=teams.TID and teams.tid="+str(tid)+" order by mid asc;")

    myresult = mycursor.fetchall()
    # print(myresult)
    x1 = list()
    ctr=0
    for x in myresult:
        x1.append((ctr,int(x[1])))
        ctr=ctr+1

    # print(x1)
    x=x1

    points = np.array(x)

    x = points[:,0]
    y = points[:,1]
    # ctr=0
    # for ii in y:
    #     y[ctr]=float(y[ctr])
    #     print(type(y[ctr]))
    #     ctr+=1
    # ctr=0
    # for ii in x:
    #     x[ctr]=float(x[ctr])
    #     print(type(x[ctr]))
    #     ctr+=1
    print(type(x[0]))
    print(type(y[0]))
    print(type(x))
    print(type(y))
    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)

    x_new = np.linspace(0, 50, 50)
    y_new = f(x_new)

    trace1 = go.Scatter(
        x=x,
        y=y,
        # mode='markers',
        # name='Data',
        # marker=dict(
        #     size=12
        # )
    )

    # trace2 = go.Scatter(
    #     x=x_new,
    #     y=y_new,
    #     mode='lines',
    #     name='Fit'
    # )

    # annotation = go.Annotation(
    #     x=6,
    #     y=-4.5,
    #     text='Chelsea expected goals',
    #     showarrow=False
    # )

    # layout = go.Layout(
    #     title='Polynomial Fit',
    #     annotations=[annotation]
    # )

    data = [trace1]
    # fig = go.Figure(data=data, layout=layout)

    # py.plot(data, filename='interpolation-and-extrapolation')
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON