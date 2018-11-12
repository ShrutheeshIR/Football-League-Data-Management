import mysql.connector
from google_images_download import google_images_download
response = google_images_download.googleimagesdownload()

from flask import Flask, request, render_template,url_for,redirect
#from predictions import predAttendance
import json
#from predictions import predGoalPlayer



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Fkafka",
  database="footballproject"
)
print(mydb)
mycursor = mydb.cursor()



app = Flask(__name__)

session=dict()

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
            except:
                print('uhyi76ygkyb')
                error = 'Invalid Credentials. Please try again.'
                return render_template('login.html', error=error)

            return redirect(url_for('home'))
    return render_template('login.html', error=error)


 

@app.route("/fand2")
def hello():
  y = request.args.get('val')
  z = request.args.get('x1')

  if(y=='ts'):
    query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.P  order by count(goal.GID) desc;"
    print(query)
    mycursor.execute(query)
    alltimetable = mycursor.fetchall()[:5]
    alltimetable = enumerate(alltimetable)
    query = "select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.P  order by count(goal.GID) desc;"
    mycursor.execute(query)
    seastable = mycursor.fetchall()[:5]
    seastable = enumerate(seastable)
  if(y=='a'):
    query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(session['tid']) + " group by goal.AP  order by count(goal.GID) desc;"
    print(query)
    mycursor.execute(query)
    alltimetable = mycursor.fetchall()[:5]
    alltimetable = enumerate(alltimetable)
    query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(session['tid']) + " group by goal.AP  order by count(goal.GID) desc;"
    mycursor.execute(query)
    seastable = mycursor.fetchall()[:5]
    seastable = enumerate(seastable)
  if(y=='yc'):
    query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
    print(query)
    mycursor.execute(query)
    alltimetable = mycursor.fetchall()[:5]
    alltimetable = enumerate(alltimetable)
    query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and matches.season='2017/18' and event.`Type`='Y' group by event.P  order by count(event.EID) desc;"
    mycursor.execute(query)
    seastable = mycursor.fetchall()[:5]
    seastable = enumerate(seastable)
  if(y=='rc'):
    query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
    print(query)
    mycursor.execute(query)
    alltimetable = mycursor.fetchall()[:5]
    alltimetable = enumerate(alltimetable)
    query="select player.FN,player.LN,count(event.EID) from teams,matches,player,event where player.PID=event.P and matches.MID=event.MID and event.TID=teams.TID and teams.TID="+ str(session['tid']) + " and matches.season='2017/18' and event.`Type`='R' group by event.P  order by count(event.EID) desc;"
    mycursor.execute(query)
    seastable = mycursor.fetchall()[:5]
    seastable = enumerate(seastable)
    
    


  return render_template("tableandgraph.html", val=y, x1=z, alltimetable=alltimetable, seastable = seastable)

@app.route("/fan", methods=["GET","POST"])
def home():

  if request.method == 'POST':
    try:
      playername = request.form['Player']
      print(playername)
      
    except:
      matchname = request.form['Match']
    
    player={}
    print('h73i632yb')
    query = "select player.pid, player.FN, player.LN, player.Coun, player.DOB, player.Pos from player where CONCAT(player.FN, ' ',player.LN) like '%" + playername + "%'"
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
  topscor = mycursor.fetchall()
  query="select distinct player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.P and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(x) + " group by goal.P  order by count(goal.GID) desc;"
  print(query)
  mycursor.execute(query)
  seastopscor = mycursor.fetchall()
  query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and goal.TID=teams.TID and teams.TID=" + str(x) + " group by goal.AP  order by count(goal.GID) desc;"
  mycursor.execute(query)
  topassist = mycursor.fetchall()
  query="select player.FN,player.LN,count(goal.GID) from teams,matches,player,goal where player.PID=goal.AP and matches.MID=goal.MID and matches.season='2017/18' and goal.TID=teams.TID and teams.TID="+ str(x) + " group by goal.AP  order by count(goal.GID) desc;"
  mycursor.execute(query)
  seastopassist = mycursor.fetchall()
  query="select count(*) from goal where goal.TID="+str(x)+" and goal.Type!='O'"
  mycursor.execute(query)
  Allgoals = mycursor.fetchall()
  print(Allgoals)  
  query="select count(*) from matches where matches.HT="+str(x)+" or matches.AT="+str(x)
  mycursor.execute(query)
  AllGames = mycursor.fetchall()
  query="select count(*) from event where event.Type='Y' and event.TID="+str(x)
  mycursor.execute(query)
  AllYellow = mycursor.fetchall()
  query="select count(*) from event where event.Type='R' and event.TID="+str(x)
  mycursor.execute(query)
  AllRed = mycursor.fetchall()
  query="select HT, AT, HG, AG from matches,teams where (matches.HT=teams.TID or matches.AT=teams.TID) and teams.TID="+str(x) + " order by matches.Date desc,matches.Time desc limit 3;"
  mycursor.execute(query)
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



  print(RecMatch)  
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
  

  print(x)
  return render_template('index.html', x=x, allyellow = AllYellow[0][0],allred = AllRed[0][0] ,allgoals=Allgoals[0][0], allgames=AllGames[0][0], teamname=teamname, teamshortname=teamshortname, topgoalscorer=topgoalscorer, topassist=topassist, seasontopgoalscorer=seasontopgoalscorer, seasontopassist=seasontopassist, recentgame = RecMatch, type=session['type'])

@app.route("/player")
def match():


  return render_template("player.html")



if __name__ == '__main__':
    app.run(debug=True)