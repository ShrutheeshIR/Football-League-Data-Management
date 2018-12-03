import mysql.connector
import classes
import attrclass
# from google_images_download import google_images_download
# response = google_images_download.googleimagesdownload()

from flask import Flask, request, render_template,url_for,redirect
from predictions import predAttendance,predAttendanceWeek,predGoalPlayer,predGoalTeam,predGoalTeamWeek,predPoints,predYellow,predYellowCardWeek,predRedCard

from graphs import graphAttendance,graphAttendanceWeek,graphGoalPlayer,graphGoalTeam,graphGoalTeamWeek,graphPoints,graphRedCard,graphYellowCard,graphYellowCardWeek
import json
import pymongo
#from predictions import predGoalPlayer

obj = attrclass.attr()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["footballleague"]
mycol = mydb["userreport"]

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="battlefield4",
  database="footballmanagement"
)
print(mydb)
mycursor = mydb.cursor()



app = Flask(__name__)

session=dict()
signupstuff=dict()

@app.route('/', methods=['GET', 'POST'])
def login():
    
    error = None
    if request.method == 'POST':
        
        
            session['username']=request.form['username']
            session['password']=request.form['password']

            mycursor = mydb.cursor()

            mycursor.execute("SELECT tid,typ FROM user where usn=\'"+ session['username']+"\' and pass=\'"+session['password']+"\'")

            myresult = mycursor.fetchall()
            try:
                session['tid'] = myresult[0][0]
                session['type'] = myresult[0][1]
                print('***********************')
                print(session)
            except:
                print('uhyi76ygkyb')
                error = 'Invalid Credentials. Please try again.'
                return render_template('login.html', error=error)

            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/report")
def report():
  myquery = { "username": session['username'] }

  mydoc = mycol.find(myquery)
  ctr=0
  graphs1=list()
  heads=list()
  for x in mydoc:
    ctr+=1
    print(type(x))
    print(x)
    graphs1.append(json.loads(x['report1']))
    heads.append(x['heading1'])
    print(type(x['report1']))
    try:
      graphs1.append(json.loads(x['report2']))
      heads.append(x['heading2'])
    except:
      continue
  print(graphs1)
  # print("***************************************")
  # print(type(graphs1[0][0]['x'][0]))

  print('----------------------------'+str(type(graphs1[0][0])))
  graphs=enumerate(graphs1)
  grap = enumerate(graphs1)
  # heads=enumerate(heads)    

  return render_template('chart.html',graph=graphs,grap=grap,heads=heads)

@app.route("/fand2")
def hello():
  y = request.args.get('val')
  z = request.args.get('x1')
  playersFromDB = list()
  h1="Here's a graph."
  h2="Here's a graph."

  if(session['type']=='m'):

    if(y=='ts'):    
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and goal.TID=teams.TID  group by goal.P  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID group by goal.P  order by count(goal.GID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      print('---------------'+session['type'] + '-----------')

      # graphJSON=predGoalTeam.goalteam(session['tid'])
      # graphJSON1=predGoalTeamWeek.goalteamweek(session['tid'])
      graphJSON=graphGoalTeam.graphgoalteam()
      h1="Goals per season Vs Season Number"
      h2="Goals per gameweek Vs Season Number"
      graphJSON1=graphGoalTeamWeek.graphgoalteamweek()
      print("QQQQQQQQQQQQQQQQQQQQQQQQq"+z)
      if z=='2':      
        graphJSON=predGoalTeam.goalteam()      
        graphJSON1=predGoalTeamWeek.goalteamweek()
      
    if(y=='a'):
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID group by goal.AP  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=None
      graphJSON1=None
    if(y=='yc'):
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      ycardevent = classes.eventyc(obj.player,obj.time1,obj.ref)
      ycardevent.getplayer()
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and matches.season='2017/18' and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      for somei in range(0,5):
        playersFromDB.append( classes.player(seastable[somei][0]+seastable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      seastable = enumerate(seastable)
      h1="Yellow Card per season Vs Season Number"
      h2="Yellow Card per gameweek Vs Season Number"
      graphJSON=graphYellowCard.graphyellowcard()
      graphJSON1=graphYellowCardWeek.graphyellowcardweek()
      if z=='2':      
        graphJSON=predYellow.predyellowcard()
        graphJSON1=predYellowCardWeek.predyellowcardweek()
    if(y=='rc'):
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      rcard = classes.eventrc(obj.player,obj.time1,obj.ref)
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and matches.season='2017/18' and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      for somei in range(0,5):
        playersFromDB.append( classes.player(seastable[somei][0]+seastable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      seastable = enumerate(seastable)
      graphJSON=graphRedCard.graphredcard()
      h1="Red Cards per season Vs Season Number"
      graphJSON1=None
      if z=='2':      
        graphJSON=predRedCard.predredcard()  

      if graphJSON != None  and (z=='0' or z=='2'):
        mydict = { "username": session['username'], "report1": graphJSON,"heading1":h1 }
        x = mycol.insert_one(mydict)    
        
      return render_template("tableandgraph.html", val=y, x1=z, alltimetable=alltimetable, typ=session['type'], seastable = seastable,graphJSON=graphJSON)
      
      
    if(y=='at'):
      query="select substring(season,1,4),substring(season,5,7),avg(attendance) from matches group by season order by season desc ;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      matchplayed=classes.match(obj.ht,obj.at,obj.ref,alltimetable[0][2])
      alltimetable = enumerate(alltimetable)
      query="select concat(t1.shortname,' vs'),t2.shortname,attendance from matches,teams as t1,teams as t2 where t1.tid=ht and t2.tid=at and season='2017/18';"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=graphAttendance.graphatt()
      graphJSON1=graphAttendanceWeek.graphattweek()
      h1="Average Attendance per season Vs Season Number"
      h2="Attendance per gameweek Vs Season Number"
      if z=='2':      
        graphJSON=predAttendance.predatt()
        graphJSON1=predAttendanceWeek.predattweek()

  else:
    if(y=='ts'):    
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.P  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.P  order by count(goal.GID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      print('---------------'+session['type'] + '-----------')

      # graphJSON=predGoalTeam.goalteam(session['tid'])
      # graphJSON1=predGoalTeamWeek.goalteamweek(session['tid'])
      graphJSON=graphGoalTeam.graphgoalteam(session['tid'])
      graphJSON1=graphGoalTeamWeek.graphgoalteamweek(session['tid'])
      h1="Goals per season Vs Season Number"
      h2="Goals per gameweek Vs Season Number"
      print("QQQQQQQQQQQQQQQQQQQQQQQQq"+z)
      if z=='2':      
        graphJSON=predGoalTeam.goalteam(session['tid'])      
        graphJSON1=predGoalTeamWeek.goalteamweek(session['tid'])
      
    if(y=='a'):
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.AP  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(session['tid']) + " group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=None
      graphJSON1=None
    if(y=='yc'):
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      ycardevent = classes.eventyc(obj.player,obj.time1,obj.ref)
      ycardevent.getdetails()
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and matches.season='2017/18' and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=graphYellowCard.graphyellowcard(session['tid'])
      graphJSON1=graphYellowCardWeek.graphyellowcardweek(session['tid'])
      h1="Yellow Card per season Vs Season Number"
      h2="Yellow Card per gameweek Vs Season Number"
      if z=='2':      
        graphJSON=predYellow.predyellowcard(session['tid'])
        graphJSON1=predYellowCardWeek.predyellowcardweek(session['tid'])
    if(y=='rc'):
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      rcard = classes.eventrc(obj.player,obj.time1,obj.ref)
      rcard.getdetails()
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and matches.season='2017/18' and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=graphRedCard.graphredcard(session['tid'])
      h1="Red Cards per season Vs Season Number"
      #h2="Goals per gameweek Vs Season Number"
      graphJSON1=None
      if z=='2':      
        graphJSON=predRedCard.predredcard(session['tid'])      

      if graphJSON != None  and (z=='0' or z=='2'):
        mydict = { "username": session['username'], "report1": graphJSON,"heading1":h1 }
        x = mycol.insert_one(mydict)
        
      return render_template("tableandgraph.html", val=y, x1=z, alltimetable=alltimetable, typ=session['type'], seastable = seastable,graphJSON=graphJSON)
    
    
    if(y=='at'):
      query="select substring(season,1,4),substring(season,5,7),avg(attendance) from matches where  ht="+str(session['tid'])+" group by season order by season desc ;"
      print(query)
      mycursor.execute(query)
      alltimetable = mycursor.fetchall()[:5]
      matchplayed=classes.match(obj.ht,obj.at,obj.ref,alltimetable[0][2])
      matchplayed.getdetails()
      for somei in range(0,5):
        playersFromDB.append( classes.player(alltimetable[somei][0]+alltimetable[somei][1],obj.getdob(),obj.getpos,obj.tid))
      alltimetable = enumerate(alltimetable)
      query="select concat(t1.shortname,' vs'),t2.shortname,attendance from matches,teams as t1,teams as t2 where t1.tid=ht and t2.tid=at and season='2017/18' and ht="+str(session['tid'])+";"
      mycursor.execute(query)
      seastable = mycursor.fetchall()[:5]
      seastable = enumerate(seastable)
      graphJSON=graphAttendance.graphatt(session['tid'])
      graphJSON1=graphAttendanceWeek.graphattweek(session['tid'])
      h1="Average Attendance per season Vs Season Number"
      h2="Attendance per gameweek Vs Season Number"
      if z=='2':      
        graphJSON=predAttendance.predatt(session['tid'])
        graphJSON1=predAttendanceWeek.predattweek(session['tid'])

  if graphJSON != None and graphJSON1!=None and (z=='0' or z=='2'):
    print(h1+h2)
    mydict = { "username": session['username'], "report1": graphJSON,"report2":graphJSON1,"heading1":h1,"heading2":h2 }
    x = mycol.insert_one(mydict)
  # print("********************")
  # print(type(graphJSON[0]['x'][0]))
  # print("********************")
  return render_template("tableandgraph.html", val=y, x1=z, alltimetable=alltimetable,typ=session['type'], seastable = seastable,graphJSON=graphJSON,graphJSON1=graphJSON1)

@app.route("/fan", methods=["GET","POST"])
def home():
  try:

    if request.method == 'POST':
      try:
        playername = request.form['Player']
        print(playername)
        
      except:
        matchname = request.form['Match']
      
      player={}
      print('h73i632yb')
      query = "select player.pid, player.FN, player.LN, player.Coun, player.DOB, player.Pos from player where CONCAT(player.FN, ' ',player.LN) like '%" + playername + "%' limit 5"
      print(query)
      mycursor.execute(query)
      playdet = mycursor.fetchall()[:5]
      pid = playdet[0][0]
      player['Name'] = playdet[0][1]+playdet[0][2]
      player['Country']=playdet[0][3]
      player['Position']=playdet[0][5]
      player['DOB']=playdet[0][4]
      query = "Select count(GID) from Goal where goal.P = "+str(pid)+" and goal.Type <> 'O' "
      mycursor.execute(query)
      player['AllTimeGoals'] = mycursor.fetchall()[0][0]
      query = "Select count(GID) from Goal where goal.AP = "+str(pid)+" and goal.Type <> 'O' "
      mycursor.execute(query)
      player['AllTimeAssists'] = mycursor.fetchall()[0][0]
      query = "Select count(GID) from Goal, matches where goal.P = "+str(pid)+" and goal.Type <> 'O' and goal.MID=matches.MID and matches.Season='2017/18'"
      mycursor.execute(query)
      player['SeasonGoals'] = mycursor.fetchall()[0][0]
      query = "Select count(GID) from Goal,matches where goal.AP = "+str(pid)+" and goal.Type <> 'O' and goal.MID=matches.MID and matches.Season='2017/18'"
      mycursor.execute(query)
      player['SeasonAssists'] = mycursor.fetchall()[0][0]
      
      return render_template("player.html", player=player)


    print("aaaaaaaaaaaaaaaa")
    if session['type'] != 'm':
      x = session['tid']
      #mycursor.execute("SELECT count(Goal_ID) from goal_table where Player_ID=2064 and type != 'O'")
      #myresult1 = mycursor.fetchall()
      #mycursor.execute("select player_table.First_Name,player_table.Last_Name,count(goal_table.Goal_ID) from team_table,match_table,player_table,goal_table where player_table.Player_ID=goal_table.Player_ID and match_table.Match_ID=goal_table.Match_ID and goal_table.Team_ID=team_table.Team_ID and team_table.Short_Name='Man Utd' group by goal_table.Player_ID  order by count(goal_table.Goal_ID) desc;")
      #myresult1 = mycursor.fetchall()

      somestring = "SELECT DISTINCT Team_Name, ShortName from teams where TID=" + str(x)
      mycursor.execute(somestring)

      teamdet=mycursor.fetchall()
      teamname = teamdet[0][0]
      teamshortname = teamdet[0][1]
      #arguments = {"keywords":"Wayne Rooney","single_image":True, "limit":1}   #creating list of arguments
      #absolute_image_paths = response.download(arguments)
      #print(absolute_image_paths)
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID="+ str(x) + " group by goal.P  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------1111")
      topscor = mycursor.fetchall()
      query="select distinct player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(x) + " group by goal.P  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      print("---------------2222")
      seastopscor = mycursor.fetchall()
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(x) + " group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------3333")
      topassist = mycursor.fetchall()
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(x) + " group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------4444")
      seastopassist = mycursor.fetchall()
      query="select count(*) from goal where goal.TID="+str(x)+" and goal.Type!='O'"
      mycursor.execute(query)
      print("---------------5555")
      Allgoals = mycursor.fetchall()
      print(Allgoals)  
      query="select count(*) from matches where matches.HT="+str(x)+" or matches.AT="+str(x)
      mycursor.execute(query)
      print("---------------6666")
      AllGames = mycursor.fetchall()
      query="select count(*) from event where event.Type='Y' and event.TID="+str(x)
      mycursor.execute(query)
      print("---------------7777")
      AllYellow = mycursor.fetchall()
      query="select count(*) from event where event.Type='R' and event.TID="+str(x)
      mycursor.execute(query)
      print("---------------8888")
      AllRed = mycursor.fetchall()
      query="select HT, AT, HG, AG from matches,teams where (matches.HT=teams.TID or matches.AT=teams.TID) and teams.TID="+str(x) + " order by matches.Date desc,matches.Time desc limit 3;"
      mycursor.execute(query)
      print("---------------9999")
      RecentMatches = mycursor.fetchall()
      RecMatch = []
      for i in RecentMatches:

        print('*******')
        print(i)
        dic = {}
        dic['HG'] = i[2]
        dic['AG'] = i[3]
        if str(i[0]) == str(x):

          query="select Team_Name from teams where TID="+str(i[1])
          mycursor.execute(query)
          tn = mycursor.fetchall()

          dic['tn']=tn[0][0]
          if dic['HG']-dic['AG'] > 0:
            dic['color'] = 'green'
          elif dic['HG']-dic['AG'] < 0:
            dic['color'] = 'red'

          else:
            dic['color'] = 'gray'

        if str(i[1]) == str(x):

          query="select Team_Name from teams where TID="+str(i[0])
          mycursor.execute(query)
          tn = mycursor.fetchall()
          dic['tn']=tn[0][0]


          if dic['AG']-dic['HG'] > 0:
            dic['color'] = 'green'
          elif dic['AG']-dic['HG'] < 0:
            dic['color'] = 'red'
          else:
            dic['color'] = 'gray'
        RecMatch.append(dic)

      topgoalscorer = {'First_Name':topscor[0][0], 'Second_Name' : topscor[0][1], 'GoalsScored':topscor[0][2]}
      topassist = {'First_Name':topassist[0][0], 'Second_Name' : topassist[0][1], 'GoalsAssisted':topassist[0][2]}
      seasontopgoalscorer = {'First_Name':seastopscor[0][0], 'Second_Name' : seastopscor[0][1], 'GoalsScored':seastopscor[0][2]}
      seasontopassist = {'First_Name':seastopassist[0][0], 'Second_Name' : seastopassist[0][1], 'GoalsAssisted':seastopassist[0][2]}
      

      print(x)
      return render_template('index.html', x=x, allyellow = AllYellow[0][0],allred = AllRed[0][0] ,allgoals=Allgoals[0][0], allgames=AllGames[0][0], teamname=teamname, teamshortname=teamshortname, topgoalscorer=topgoalscorer, topassist=topassist, seasontopgoalscorer=seasontopgoalscorer, seasontopassist=seasontopassist, recentgame = RecMatch, type=session['type'])

    
    else:
      #mycursor.execute("SELECT count(Goal_ID) from goal_table where Player_ID=2064 and type != 'O'")
      #myresult1 = mycursor.fetchall()
      #mycursor.execute("select player_table.First_Name,player_table.Last_Name,count(goal_table.Goal_ID) from team_table,match_table,player_table,goal_table where player_table.Player_ID=goal_table.Player_ID and match_table.Match_ID=goal_table.Match_ID and goal_table.Team_ID=team_table.Team_ID and team_table.Short_Name='Man Utd' group by goal_table.Player_ID  order by count(goal_table.Goal_ID) desc;")
      #myresult1 = mycursor.fetchall()
      print("ttttttttttt")
      query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and goal.TID=teams.TID  group by goal.P  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------1111")
      topscor = mycursor.fetchall()
      query="select distinct player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID group by goal.P  order by count(goal.GID) desc;"
      print(query)
      mycursor.execute(query)
      print("---------------2222")
      seastopscor = mycursor.fetchall()
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------3333")
      topassist = mycursor.fetchall()
      query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID group by goal.AP  order by count(goal.GID) desc;"
      mycursor.execute(query)
      print("---------------4444")
      seastopassist = mycursor.fetchall()
      query="select count(*) from goal where goal.Type!='O'"
      mycursor.execute(query)
      print("---------------5555")
      Allgoals = mycursor.fetchall()
      print(Allgoals)  
      query="select count(*) from matches"
      mycursor.execute(query)
      AllGames = mycursor.fetchall()
      query="select count(*) from event where event.Type='Y'"
      mycursor.execute(query)
      AllYellow = mycursor.fetchall()
      query="select count(*) from event where event.Type='R'"
      mycursor.execute(query)
      AllRed = mycursor.fetchall()
      query="select HT, AT, HG, AG from matches,teams where (matches.HT=teams.TID or matches.AT=teams.TID) order by matches.Date desc,matches.Time desc limit 6;"
      mycursor.execute(query)
      RecentMatches = mycursor.fetchall()
      RecMatch = []
      for xa,i in enumerate(RecentMatches):
        if xa%2==0:
          continue
        print('*******')
        print(i)
        dic = {}
        dic['HG'] = i[2]
        dic['AG'] = i[3]

        query="select Team_Name from teams where TID="+str(i[0])
        mycursor.execute(query)
        tn = mycursor.fetchall()
        dic['tn']=tn[0][0]
        query="select Team_Name from teams where TID="+str(i[1])
        mycursor.execute(query)
        tn = mycursor.fetchall()
        dic['an']=tn[0][0]
        
        if dic['HG']-dic['AG'] > 0:
          dic['color'] = 'green'
        elif dic['HG']-dic['AG'] < 0:
          dic['color'] = 'red'

        else:
          dic['color'] = 'gray'

        RecMatch.append(dic)


    #query="select HG, AG from event where event.Type='R' and event.TID="+str(x)
    #mycursor.execute(query)
    #AllRed = mycursor.fetchall()
    #query="select HG, AG from event where event.Type='R' and event.TID="+str(x)
    #mycursor.execute(query)
    #AllRed = mycursor.fetchall()
    
    
    
    
      topgoalscorer = {'First_Name':topscor[0][0], 'Second_Name' : topscor[0][1], 'GoalsScored':topscor[0][2]}
      topassist = {'First_Name':topassist[0][0], 'Second_Name' : topassist[0][1], 'GoalsAssisted':topassist[0][2]}
      seasontopgoalscorer = {'First_Name':seastopscor[0][0], 'Second_Name' : seastopscor[0][1], 'GoalsScored':seastopscor[0][2]}
      seasontopassist = {'First_Name':seastopassist[0][0], 'Second_Name' : seastopassist[0][1], 'GoalsAssisted':seastopassist[0][2]}
      
      return render_template('mgmt.html', allyellow = AllYellow[0][0],allred = AllRed[0][0] ,allgoals=Allgoals[0][0], allgames=AllGames[0][0], topgoalscorer=topgoalscorer, topassist=topassist, seasontopgoalscorer=seasontopgoalscorer, seasontopassist=seasontopassist, recentgame = RecMatch, type=session['type'])
  except:
    return render_template('error.html')

@app.route("/signup" , methods=['GET', 'POST'])
def signup():

  error = None
  if request.method == 'POST':
        
            print('hello')
            signupstuff['username']=request.form['username']
            signupstuff['psw']=request.form['psw']
            signupstuff['acctype']=request.form['acctype']
            signupstuff['teamname']=request.form['teamname']
            print(signupstuff)
            
            mycursor = mydb.cursor()
            print("insert into user values(\'"+signupstuff['username']+"\' , \'"+signupstuff['psw']+"\', "+str(signupstuff['teamname'])+" , \'"+signupstuff['acctype'] +"\') ;")
            mycursor.execute("insert into user values(\'"+signupstuff['username']+"\' , \'"+signupstuff['psw']+"\', "+str(signupstuff['teamname'])+" , \'"+signupstuff['acctype'] +"\') ;")
            mydb.commit()

            # myresult = mycursor.fetchall()
            # try:
            #     session['tid'] = myresult[0][0]
            #     session['type'] = myresult[0][1]
            #     print('***********************')
            #     print(session)
            # except:
            #     print('uhyi76ygkyb')
            #     error = 'Invalid Credentials. Please try again.'
            #     return render_template('login.html', error=error)

            return redirect(url_for('login'))
  print('zzz')

  return render_template("signup.html")
@app.route("/player")
def match():


  return render_template("player.html")



if __name__ == '__main__':
    app.run(debug=True)