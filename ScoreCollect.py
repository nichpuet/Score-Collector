
import requests
import json
from datetime import datetime, timedelta

hockeyKey = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=9"
pandakey = "rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"
favsLol = ['Team Liquid', 'Team SoloMid', 'Top Esports', 'T1', 'DRX', 'G2 Esports', 'SK Gaming', 'Fnatic']
#Add favs for counter strike
#Add favs for Overwatch League

def jPrint(obj):
    text = json.dumps(obj,indent=1)
    print(text)

def prepHock():
    response = requests.get(hockeyKey)
    r = response.json()
    jPrint(r)
    awayName = r['dates'][0]['games'][0]['teams']['away']['team']['name']
    awayScore = r['dates'][0]['games'][0]['teams']['away']['score']
    awayWins = r['dates'][0]['games'][0]['teams']['away']['leagueRecord']['wins']
    awayLoss = r['dates'][0]['games'][0]['teams']['away']['leagueRecord']['losses']
    homeName = r['dates'][0]['games'][0]['teams']['home']['team']['name']
    homeScore = r['dates'][0]['games'][0]['teams']['home']['score']
    homeWins = r['dates'][0]['games'][0]['teams']['home']['leagueRecord']['wins']
    homeLoss = r['dates'][0]['games'][0]['teams']['home']['leagueRecord']['losses']

    gameState = r['dates'][0]['games'][0]['status']['abstractGameState']
    if (gameState == "Final"):
        now = datetime.now()
        current = now.strftime("%H")
        if (int(current) >= 22 or int(current) <= 2):
            gameSend = homeName[0:3].upper() + " ("+str(homeScore)+") vs ("+str(awayScore)+") "+awayName[0:3].upper()
            records = str(homeWins)+ "/"+ str(homeLoss)+ "\t\t      "+str(awayWins)+ "/"+ str(awayLoss)
            sendable = "" + gameSend + "\n" + records
            sendText(sendable)
    elif (gameState == "Live"):
        gameSend = homeName[0:3].upper() + " ("+str(homeScore)+") vs ("+str(awayScore)+") "+awayName[0:3].upper()
        records = str(homeWins)+ "/"+ str(homeLoss)+ "\t\t      "+str(awayWins)+ "/"+ str(awayLoss)
        sendable = "" + gameSend + "\n" + records
        sendText(sendable)

def prepLol():
    naString = "https://api.pandascore.co/leagues/league-of-legends-lcs/matches?token=rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"
    euString = "https://api.pandascore.co/leagues/league-of-legends-lec/matches?token=rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"
    krString = "https://api.pandascore.co/leagues/league-of-legends-lck-champions-korea/matches?token=rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"
    cnString = "https://api.pandascore.co/leagues/league-of-legends-lpl-china/matches?token=rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"

    pandaString = [naString, euString, krString, cnString]
    for i in pandaString:
        response = requests.get(i)
        r = response.json()
        for i in r:
            league = i['league']['name']
            if (league == 'LPL' or league == 'LCS' or league == 'LCK'or league == "LEC"):
                
                try:
                    teamA = i['opponents'][0]['opponent']['name']
                    teamB = i['opponents'][1]['opponent']['name']
                
                except:
                    teamA = 'null'
                    teamB = 'null'

                #print(league, teamA, teamB)
                formattedGames = []
                for k in favsLol:
                    
                    if (teamA == k or teamB == k):
                        gameTime = i['scheduled_at']

                        gameTimeHour = gameTime[11:16]
                        gameTimeDate = gameTime[0:10]
                        
                        year = datetime.now().year
                        month = datetime.now().month
                        day = datetime.now().day
                        currdate = '{}-{}-{}'.format(year, month, day)
                        currdate = datetime.strptime(currdate, '%Y-%m-%d')
                        gameTimeDateD = datetime.strptime(gameTimeDate, '%Y-%m-%d')

                        delta = gameTimeDateD - currdate

                        if delta.days < 10 and delta.days >= 0:
                            matchName = teamA + " vs " + teamB + " " + gameTimeDate + " " + gameTimeHour
                            if matchName in formattedGames:
                                pass
                            else: 
                                formattedGames.append(matchName)
                                print(matchName)
                                #currently adds double of the last instant to list


def sendText(sendable):
    #Should send the message to phone
    x = sendable

def main():
    #sendText()
    print()
    #prepHock()
    prepLol()
    print()

main()
