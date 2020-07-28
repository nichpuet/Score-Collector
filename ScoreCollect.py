
from twilio.rest import Client
import requests
import json
from datetime import datetime

hockeyKey = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=9"
pandakey = "rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo"
favsLol = ['Gen.G', 'Griffin']
#Add favs for counter strike
#Add favs for Overwatch League

def jPrint(obj):
    text = json.dumps(obj,indent=1)
    print(text)

def prepHock():
    response = requests.get(hockeyKey)
    r = response.json()
    #jPrint(r)
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
            sendText(gameSend, records, "NHL\tFINAL")
    elif (gameState == "Live"):
        gameSend = homeName[0:3].upper() + " ("+str(homeScore)+") vs ("+str(awayScore)+") "+awayName[0:3].upper()
        records = str(homeWins)+ "/"+ str(homeLoss)+ "\t\t      "+str(awayWins)+ "/"+ str(awayLoss)
        sendText(gameSend, records, "NHL\tLIVE")

def prepLol():
    response = requests.get("https://api.pandascore.co/lol/matches?token=rjA_pWn2b0NohfOPbAfFcNamnLkWimENmiZ4_m8z48FQBbiKKKo")
    r = response.json()
    for i in r:
        league = i['league']['name']
        if (league == 'KeSPA Cup'):
            try:
                teamA = i['opponents'][0]['opponent']['name']
                teamB = i['opponents'][1]['opponent']['name']
            except:
                teamA = 'null'
                teamB = 'null'
            for k in favsLol:
                if (teamA == k or teamB == k):
                    gameTime = i['scheduled_at']

                    gameTimeHour = gameTime[11:16]
                    gameTimeDate = gameTime[0:10].replace('-','/')

                    temp = teamA + " vs " + teamB
                    tempName = teamA + " vs " + teamB + " " + gameTimeDate + " " + gameTimeHour

                    print(tempName)
                    #currently adds double of the last instant to list


def sendText(gameSend, records, sport):
    account_sid = 'ACfc01b14476a7a182b92c7c137b5d9e8d'
    auth_token = '573dafe05f656858a64df5eeb6f026cc'
    client = Client(account_sid, auth_token)
    sendable = sport+"\n"+gameSend+ "\n"+ records
    message = client.messages \
                    .create(
                         body=sendable ,
                         from_='+13658000812',
                         to='+15197033066'
                     )

    print(message.sid)

def main():
    #sendText()
    print()
    prepHock()
    #prepLol()
    print()

main()
