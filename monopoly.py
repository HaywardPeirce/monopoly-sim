from random import *
import json
import csv

def getProperties():
    with open('properties.json') as sources_file:    
        properties = json.load(sources_file)
    
    #print properties
    
    return properties
    
def getPlaces():
    with open('places.json') as sources_file:    
        properties = json.load(sources_file)
    
    #print properties
    
    for prop in properties:
        #print prop
        prop['Count'] = 0
        
        #print prop
    
    return properties
        
def playAGame(numTurnLimit):
    
    #print "playing a game"
    
    numTurnsPlayed = 0
    
    
    
    #print numTurnLimit
    
    #print numTurnsPlayed
    
    while numTurnsPlayed < numTurnLimit:
        #loop through players turns
        
        #print "playing turn number: " + str(numTurnsPlayed)
        
        for player in players:
            playATurn(player)
            
        numTurnsPlayed += 1
    
def playATurn(player):
    #steps in a turn: roll, move, pay rent, maybe roll again
    
    #print "playing a turn"
    
    rollCount = 0
    
    roll = rollDice()
        
    while True:
        if rollCount == 2:
            break
        
        #print player.position
        
        #print players[player]
        
        player.position += sum(roll)
        
        if player.position > 40:
            player.position = (player.position - 40)
        
        if isProperty(player.position):
            calculatedRent(player, sum(roll))
        
        recordPosition(player.position)
        
        rollCount += 1
        
        roll = rollDice()   
    
#Generates a random number from 1 to 6 simulating rolling a die
def rollDice():
    dice = []
    dice.append(randrange(1,7))
    dice.append(randrange(1,7))
    
    #return list of dice roll values
    return dice
    

    
def calculatedRent(player, roll):
    
    for prop in properties:
        if prop['Position'] == player.position:
            raw_rent = prop['Rent']
            
            if raw_rent == '*':
                # average of the possible values of 4 or 10 times the dice roll
                rent = 7*roll
            elif raw_rent == '**':    
                #hard coded average rent for each of the four possible rent values of 25, 50, 100, 200
                rent = 93.75
            else: rent = float(raw_rent)
            
            #print type(rent)
    
            player.money -= rent
            
            for place in places:
                if place['Position'] == player.position:
                    place['Revenue'] += rent
            
            break
    
    if player.money < 0:
        player.money = 0

#check whether the place that was landed on is a rent-paying property
def isProperty(position):
    for item in places:
        if item['Position'] == position:
            return True
    
    return False

#record the position that was landed on
def recordPosition(position):
    #print position
    
    for place in places:
        if place['Position'] == position:
            #print place['Count']
            place['Count'] += 1
            #print place['Count']

#generate the report of what places got the most traffic/rent (print/send to file) 
def makeReport():
    print "After " + str(gamesPlayed) + " games played:"
    
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['Property', 'Percentage', 'Avg_Revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        for prop in properties:
            for place in places:
                if place['Position'] == prop['Position']:
                    percent = '%.3f'%(float(place['Count'])/float(numberPlayers*numGamesLimit*numTurnLimit)*100)
                    print prop['Name'] + "Percent landed on: " + str(percent) + "% Revenue earned per game: $" + str(place['Revenue']/numGamesLimit)
                    writer.writerow({'Property': prop['Name'], 'Percentage': percent, 'Avg_Revenue': place['Revenue']/numGamesLimit})

gamesPlayed = 0 

#number of games to run through
numGamesLimit = 1000
numTurnLimit = 30

numberPlayers = 4

properties = getProperties()
places = getPlaces()

#player class
class Player(object):
    money = 0
    position = 0
    inJailCount = 0
    propertyList = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, money, position, inJailCount, propertyList):
        self.money = money
        self.position = position
        self.inJailCount = inJailCount
        self.propertyList = propertyList

players = []

for player in range(numberPlayers):
    players.append(Player(0,0,0,[]))

while gamesPlayed < numGamesLimit:
    #play a game
    playAGame(numTurnLimit)
        #play a turn
    gamesPlayed +=1
    
makeReport()