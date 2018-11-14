import plotly
import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import json
import numpy as np
import pandas as pd
import scipy

def predyellowcardweek(tid=None):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="battlefield4",
    database="footballmanagement"
    )

    mycursor = mydb.cursor()

    if tid==None:
        mycursor.execute("select count(eid),matches.mid from event,matches where event.`Type`='Y' and event.mid=matches.mid and matches.season='2017/18' group by event.mid order by mid asc;")
    else:
        mycursor.execute("select count(eid),matches.mid from event,matches where event.`Type`='Y' and event.tid="+str(tid)+" and event.mid=matches.mid and matches.season='2017/18' group by event.mid order by mid asc;")

    myresult = mycursor.fetchall()
    # print(myresult)
    x1 = list()
    ctr=0
    for x in myresult:
        x1.append((ctr,x[0]))
        ctr=ctr+1

    # print(x1)
    x=x1

    points = np.array(x)

    x = points[:,0]
    y = points[:,1]

    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)

    x_new = np.linspace(0, 40, 50)
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
        text='Chelsea expected goals',
        showarrow=False
    )

    layout = go.Layout(
        title='Polynomial Fit',
        annotations=[annotation]
    )

    data = [trace1,trace2]
    fig = go.Figure(data=data, layout=layout)

    # py.plot(data, filename='interpolation-and-extrapolation')
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    print(data)
    return graphJSON