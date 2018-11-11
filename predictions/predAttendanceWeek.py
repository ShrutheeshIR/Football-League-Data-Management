import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly
import json
import numpy as np
import pandas as pd
import scipy



def predattweek():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="battlefield4",
    database="footballmanagement"
    )    
    mycursor = mydb.cursor()

    mycursor.execute("select matches.mid, matches.Attendance from matches,teams where matches.season='2017/18' and matches.HT=teams.TID and teams.shortname='Chelsea';")

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

    x_new = np.linspace(0, 50, 50)
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
        text='Expected attendance at the Bridge',
        showarrow=False
    )

    layout = go.Layout(
        title='Polynomial Fit',
        annotations=[annotation]
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    # py.iplot(fig, filename='interpolation-and-extrapolation')
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON