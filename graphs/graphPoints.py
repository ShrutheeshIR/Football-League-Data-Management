import plotly
import mysql.connector
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import json
import numpy as np
import pandas as pd
import scipy

def points(tid):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="battlefield4",
    database="footballmanagement"
    )

    mycursor = mydb.cursor()

    mycursor.execute("select mid,hg,ag,ht,matches.at from matches where matches.at="+str(tid)+" and season='2017/18' union select mid,hg,ag,ht,matches.at from matches where matches.ht=12 and season='2017/18' order by mid desc;")

    myresult = mycursor.fetchall()
    # print(myresult)
    x1 = list()
    ctr=0
    for x in myresult:
        homegoal=x[1]
        awaygoal=x[2]
        hometeam=x[3]
        awayteam=x[4]
        if homegoal==awaygoal:
            x1.append((ctr,1))
            ctr=ctr+1
            continue

        if(tid==hometeam):
            if homegoal>awaygoal:
                x1.append((ctr,3))
                ctr=ctr+1
            else:
                x1.append((ctr,0))
                ctr=ctr+1
        else:
            if homegoal>awaygoal:
                x1.append((ctr,0))
                ctr=ctr+1
            else:
                x1.append((ctr,3))
                ctr=ctr+1

        if ctr==5:
            break

    # print(x1)
    x=x1
    x=x[::-1]

    points = np.array(x)

    x = points[:,0]
    y = points[:,1]

    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)

    x_new = np.linspace(0, 6,10  )
    y_new = f(x_new)
    ctr11=0
    for iterating in y_new:
        if iterating<0:
            y_new[ctr11]=0
        elif iterating>3:
            y_new[ctr11]=3 
        ctr11+=1
    # print(y_new)

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
    #     text='Chelsea expected points',
    #     showarrow=False
    # )

    # layout = go.Layout(
    #     title='Polynomial Fit',
    #     annotations=[annotation]
    # )

    data = [trace1]
    # fig = go.Figure(data=data, layout=layout)

    # py.iplot(fig, filename='interpolation-and-extrapolation')
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
# points(10)