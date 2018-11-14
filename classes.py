from graphs import graphGoalPlayer,graphGoalTeam

class player:
    def __init__(self,name1,dob1,pos1,tid1):
        self.name=name1
        self.dob=dob1
        self.position=pos1
        self.tid=tid1
    def getdetails(self):
        return self.name,self.dob,self.position
    def getStatsPreds(self):
        return graphGoalPlayer.graphgoalplayer()

class team:
    def __init__(self,name1,addr,tid1):
        self.name=name1
        self.address=addr
        self.tid=tid1
    def getdetails(self):
        return self.name,self.address
    def getStatsPreds(self):
        return graphGoalTeam.graphgoalteam(tid=tid)

class match:
    def __init__(self,homet,awayt,referee,attendance):
        self.ht=homet
        self.at=awayt
        self.ref=referee 
        self.att=attendance
    def getdetails(self):
        return self.ht,self.at,self.ref,self.att

class eventrc:
    def __init__(self,player1,time1,ref1):
        self.player=player1
        self.time=time1
        self.ref=ref1 
    def getdetails(self):
        return self.player,self.time,self.ref
    def gettime(self):
        return self.time
    def getplayer(self):
        return self.player
    def getteam(self):
        return self.player.tid


class eventyc:
    def __init__(self,player1,time1,ref1):
        self.player=player1
        self.time=time1
        self.ref=ref1 
    def getdetails(self):
        return self.player,self.time,self.ref
    def gettime(self):
        return self.time
    def getplayer(self):
        return self.player
    def getteam(self):
        return self.player.tid

class eventg:
    def __init__(self,player1,ap1,time1,type1):
        self.p=player1
        self.ap=ap1
        self.time=time1
        self.typepenalty=type1 
    def getdetails(self):
        return self.p,self.ap,self.time,self.typepenalty
    def gettime(self):
        return self.time
    def getplayer(self):
        return self.p
    def getassist(self):
        return self.ap
    def getteam(self):
        return self.p.tid
    def getgoaltype(self):
        return self.typepenalty