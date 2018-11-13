import plotly
import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import json
import numpy as np
import pandas as pd
import scipy

def goalteam(tid):
    # print("booo")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="battlefield4",
    database="footballmanagement"
    )


    mycursor = mydb.cursor()

    mycursor.execute("select matches.Season,count(goal.GID) from goal,matches,teams where goal.mid=matches.mid and goal.tid=teams.tid and teams.tid="+str(tid)+" group by matches.season;")

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
    print("hello")
    x_new = np.linspace(0, 30, 50)
    y_new = f(x_new)
    print(y_new)

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

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    # # py.plot(fig, filename='interpolation-and-extrapolation')
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # # print(graphJSON)
    # points = np.array([(1, 1), (2, 4), (3, 1), (9, 3)])

    # x = points[:,0]
    # y = points[:,1]

    # z = np.polyfit(x, y, 3)
    # f = np.poly1d(z)

    # x_new = np.linspace(0, 10, 50)
    # y_new = f(x_new)

    # trace1 = go.Scatter(
    #     x=x,
    #     y=y,
    #     mode='markers',
    #     name='Data',
    #     marker=dict(
    #         size=12
    #     )
    # )

    # trace2 = go.Scatter(
    #     x=x_new,
    #     y=y_new,
    #     mode='lines',
    #     name='Fit'
    # )

    # annotation = go.Annotation(
    #     x=6,
    #     y=-4.5,
    #     text='$0.43X^3 - 0.56X^2 + 16.78X + 10.61$',
    #     showarrow=False
    # )

    # layout = go.Layout(
    #     title='Polynomial Fit in Python',
    #     annotations=[annotation]
    # )

    # data = [trace1, trace2]
    # fig = go.Figure(data=data, layout=layout)

    # py.plot(data, filename='interpolation-and-extrapolation')
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print(graphJSON)

    # count = 500
    # xScale = np.linspace(0, 100, count)
    # yScale = np.random.randn(count)
 
    # # Create a trace
    # trace = go.Scatter(
    #     x = xScale,
    #     y = yScale
    # )
 
    # data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON