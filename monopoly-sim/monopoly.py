from random import *
import json
import csv



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

def getProperties():
    with open('../monopoly-sim/properties.json') as sources_file:    
        properties = json.load(sources_file)
    
    #print properties
    
    return properties
    
def getPlaces():
    with open('../monopoly-sim/places.json') as sources_file:    
        properties = json.load(sources_file)
    
    #print properties
    
    for prop in properties:
        #print prop
        prop['Count'] = 0
        
        #print prop
    
    return properties

#load in the list of properties (spots that can earn revenue)
properties = getProperties()
#load in the list of places (every spot on the board)
places = getPlaces()




      
#play through a game of `numTurnLimit` turns
def playAGame(numTurnLimit, players):
    
    #print "playing a game"
    
    numTurnsPlayed = 0
    
    #print numTurnLimit
    
    #print numTurnsPlayed
    
    while numTurnsPlayed < numTurnLimit:
        
        #print "playing turn number: " + str(numTurnsPlayed)
        
        #loop through players turns
        for player in players:
            playATurn(player)
            
        numTurnsPlayed += 1

#play the turn of `player`
def playATurn(player):
    #steps in a turn: roll, move, pay rent, maybe roll again
    
    #print "playing a turn"
    
    rollCount = 0
    
    roll = rollDice()
        
    while True:
        #if this is the players third roll, and it's another double, move the player to jail and end their turn
        if rollCount == 2 and roll[0] == roll[1]:
            player.position = 11
            break
        elif rollCount == 2:
            break
        
        #print player.position
        
        #print players[player]
        
        #add the roll to their current position
        player.position += sum(roll)
        
        #if the player end up past go, move them back round to the beginning of the count
        if player.position > 40:
            player.position = (player.position - 40)
        
        #if this is a rent-paying property
        if isProperty(player.position):
            #check how much rent they owe
            calculatedRent(player, sum(roll))
        
        #increment how many times someone landed on the spot
        recordPosition(player.position)
        
        rollCount += 1
        
        #if the player rolled doubles, roll the dice again for their next turn
        if roll[0] == roll[1]:
            roll = rollDice()
        
#Generates a random number from 1 to 6 simulating rolling a die
def rollDice():
    dice = []
    dice.append(randrange(1,7))
    dice.append(randrange(1,7))
    
    #return list of dice roll values
    return dice
    

#calculate the rent owed by `player` this roll
def calculatedRent(player, roll):
    
    #loop through list of properties to find the one the player is currently on
    #TODO: is there a way to select the property from the list if properties by index?
    for prop in properties:
        if prop['Position'] == player.position:
            
            #lookup what the basic rent for the property is
            #TODO: figure out a way add in hotels later on in the game
            raw_rent = prop['Rent']
            
            #if the rent for the propery is based on the roll
            if raw_rent == '*':
                # average of the possible values of 4 or 10 times the dice roll
                rent = 7*roll
            #if the rent is based on the one of 4 random rent values
            elif raw_rent == '**':    
                #hard coded average rent for each of the four possible rent values of 25, 50, 100, 200
                rent = 93.75
            #if the rent is not `*` or `**`, the it is based on the initial basic value
            else: rent = float(raw_rent)
            
            #print type(rent)
            
            #subtract the rent from the player
            #TODO: they have to make money. have them buy properties later on?
            #player.money -= rent
            
            #loop through to assign the earned rent to the place on the board
            for place in places:
                if place['Position'] == player.position:
                    place['Revenue'] += rent
            
            break
    
    # if player.money < 0:
    #     player.money = 0

#check whether the place that was landed on is a rent-paying property
def isProperty(position):
    for item in places:
        #if the position is on the list of places, all of which earn rent
        if item['Position'] == position:
            return True
    
    return False

#record the position that was landed on to add to the counter
def recordPosition(position):
    #print position
    
    for place in places:
        if place['Position'] == position:
            #print place['Count']
            place['Count'] += 1
            #print place['Count']

#generate the CSV report of what places got the most traffic/rent (print/send to file) 
def makeCSVReport():
    print("After " + str(gamesPlayed) + " games played:")
    
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['Property', 'Percentage', 'Avg_Revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        
        for prop in properties:
            for place in places:
                if place['Position'] == prop['Position']:
                    percent = '%.3f'%(float(place['Count'])/float(numberPlayers*numGamesLimit*numTurnLimit)*100)
                    print(prop['Name'] + "Percent landed on: " + str(percent) + "% Revenue earned per game: $" + str(place['Revenue']/numGamesLimit))
                    writer.writerow({'Property': prop['Name'], 'Percentage': percent, 'Avg_Revenue': place['Revenue']/numGamesLimit})
                    
def makeReport(numGamesLimit, numTurnLimit, numberPlayers):
    
    #list of dictionaries of entries that have earned rent revenue
    returnList = []
    
    for prop in properties:
        for place in places:
            
            #if the position and property currently being itterated through match (so we can pull info from both lists)
            if place['Position'] == prop['Position']:
                
                #percentage of time the place was landed on as a percentage of the total number of turns that were plays in the simulation
                percent = '%.3f'%(float(place['Count'])/float(numberPlayers*numGamesLimit*numTurnLimit)*100)
                #print(prop['Name'] + "Percent landed on: " + str(percent) + "% Revenue earned per game: $" + str(place['Revenue']/numGamesLimit))
                #writer.writerow({'Property': prop['Name'], 'Percentage': percent, 'Avg_Revenue': place['Revenue']/numGamesLimit})
                
                #create a temp python dictionary for the rent-earning property's entry
                tempDict = {'Property': prop['Name'], 'Position': place['Position'], 'Percentage': percent, 'Avg_Revenue': place['Revenue']/numGamesLimit}
                returnList.append(tempDict)
    
    return returnList
    

#setup running through the allotted number of games
def calculateGames(numGames):
    
    #number of games that have been played so far
    gamesPlayed = 0 
    
    #number of games to run through
    numGamesLimit = 1000
    
    #number of turns to run through to constitute a game
    numTurnLimit = 30
    
    #number of players to simulate the game for
    numberPlayers = 4
    
    players = []
    
    numGamesLimit = numGames

    #initialize players as players
    for player in range(numberPlayers):
        players.append(Player(0,0,0,[]))
    
    while gamesPlayed < numGamesLimit:
        #play a game
        playAGame(numTurnLimit, players)
            #play a turn
        gamesPlayed +=1
    
    return makeReport(numGamesLimit,numTurnLimit, numberPlayers)




def main():
    #ask user for input of who many numbers they would like to calculate for
    
    numGamesLimit = int(input("How many games would you like to simulate? "))
    
    numberList = calculateGames(numGamesLimit)
    
    print(numberList)
    
    #makeCSVReport(numGamesLimit, numTurnLimit, numberPlayers)
    
if __name__ == '__main__':
    main()