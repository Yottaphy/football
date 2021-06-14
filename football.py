import numpy as np
from operator import itemgetter
import os
import sys

class Team:
    def __init__(self, name, group):
        self.name         = name
        self.group        = group
        self.gamesplayed  = 0
        self.wins         = 0
        self.draws        = 0
        self.losses       = 0
        self.goalsfor     = 0
        self.goalsagainst = 0
        self.points       = 0

    def print(self):
        diff = self.goalsfor - self.goalsagainst
        for entry in [self.name,self.gamesplayed,self.wins,self.draws,self.losses,self.goalsfor, self.goalsagainst, f'{diff:+.0f}' , self.points]:
            print(str(entry).ljust(20), end='')
        print('')

    def printforfile(self):
        return self.name, self.group, self.gamesplayed, self.wins, self.draws, self.losses, self.goalsfor, self.goalsagainst, self.points


def findinlist(teamlist, home, away):
    homei = 37
    awayi = 37
    for i in range(len(teamlist)):
        if teamlist[i].name == home: homei = i
        if teamlist[i].name == away: awayi = i
    if homei ==37 or awayi ==37:
        print("Wrong name")
        return False
    return homei,awayi

def match(homename, awayname, goalshome, goalsaway, teamlist):
    homei, awayi =findinlist(teamlist, homename, awayname)
    home = teamlist[homei]
    away = teamlist[awayi]
    home.gamesplayed +=1
    away.gamesplayed +=1
    home.goalsfor     = goalshome
    home.goalsagainst = goalsaway
    away.goalsfor     = goalsaway
    away.goalsagainst = goalshome
    if goalshome > goalsaway: 
        home.wins   += 1
        home.points += 3
        away.losses += 1
    elif goalshome < goalsaway: 
        home.losses += 1
        away.points += 3
        away.wins   += 1
    else:
        home.draws  += 1
        home.points += 1
        away.points += 1
        away.draws  += 1
    return home, away

def displaygroup(teamlist, group):
    print("\nGROUP "+group)
    print(('').center(168,'—'))
    for i in ["Team","GP","W","D","L","GF","GA","Goal Avg."]:
        print(i.ljust(20), end='')
    print("Points")
    print(('').center(168,'—'))
    tuple =[]
    for i in range(len(teamlist)):
        if teamlist[i].group == group:
            tuple.append((i, teamlist[i].points, teamlist[i].goalsfor - teamlist[i].goalsagainst, teamlist[i].goalsfor))
    tuple.sort(key = itemgetter(3))
    tuple.sort(key = itemgetter(2))
    tuple.sort(key = itemgetter(1))
    tuple = tuple[::-1]
    for i in tuple:     
        teamlist[i[0]].print()
    print(('').center(168,'—'))

def initialise(filename):
    groups = ['A','B','C','D','E','F']
    teamlist =[]
    for group in groups:
        print("Group "+group)
        for i in range(0,4):
            name  = input("Team name: ")
            teamlist.append(Team(name, group))
    savefile(filename, teamlist)
    return teamlist 

def readfile(file):
    teamlist = []
    names, groups = np.genfromtxt(file, unpack=True, usecols=[0,1], dtype='str')
    gamesplayed, wins, draws, losses, goalsfor, goalsagainst, points =  np.genfromtxt(file, unpack=True, usecols=[2,3,4,5,6,7,8], dtype='int')
    # for i in range(len(names)):
    #     print(names[i], groups[i], gamesplayed[i], wins[i], draws[i], losses[i], goalsfor[i], goalsagainst[i], points[i])
    for i in range(len(names)):
        teamlist.append(Team(names[i], groups[i]))
        teamlist[i].gamesplayed = gamesplayed[i]
        teamlist[i].wins = wins[i]
        teamlist[i].draws = draws[i]
        teamlist[i].losses = losses[i]
        teamlist[i].goalsfor = goalsfor[i]
        teamlist[i].goalsagainst = goalsagainst[i]
        teamlist[i].points = points[i]
    return teamlist

def savefile(file, teamlist):
    f = open(file, "w+")
    for i in range(len(teamlist)):
        for j in teamlist[i].printforfile():
            f.write(str(j)+"\t")
        f.write('\n')
    f.close()

filename = sys.argv[1]
if not os.path.exists(filename):
    lis = initialise(filename)
else:
    lis = readfile(filename)
try: n = int(input('How many matches played today?: '))
except: pass
for i in range(0,n):
    home        = input('Home team: ')
    away        = input('Away team: ')
    goalshome   = int(input('How many goals scored by '+home+'?: '))
    goalsaway   = int(input('How many goals scored by '+away+'?: '))
    match(home, away, goalshome, goalsaway, lis)

groups = ['A','B','C','D','E','F']
try: choice = input('Display what group? (Write \'all\' for all groups): ').upper()
except: pass
os.system('clear')
if choice == 'ALL':
    for group in groups:
        displaygroup(lis, group)
else: displaygroup(lis, choice)

savefile(filename,lis)
