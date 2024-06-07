import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import time



def get_puuid(summoner_name, region, tag , api_key):
    api_url = (
        "https://" + 
        region +
        ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" +
        summoner_name + "/" + tag +
        "?api_key=" +
        api_key
    )
    print(api_url)
    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid  

def get_match(puuid ,massregion, starttime , endtime , api_key):
    api_url = (
        "https://" +
        massregion +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid +
        "/ids?" +
        "startTime=" + starttime +
        "&endTime=" + endtime +
        "&start=0&count=20&api_key=" +
        api_key
    )
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids  

def get_match_data(match_id, mass_region, api_key):
    api_url = (
        "https://" + 
        mass_region + 
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id + 
        "?api_key=" + 
        api_key
    )
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 10 seconds")
            time.sleep(10)
            continue
        if resp.status_code == 404:
            print("404")
            return '404'
        match_data = resp.json()
        return match_data     

def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data

def match_info_data(match_data):
    gamematchid = match_data['metadata']['matchId']
    gameCreation = match_data['info']['gameCreation']
    gameCreation = datetime.fromtimestamp( gameCreation /1000 )    
    gameCreation = gameCreation.strftime("%Y-%m-%d %H:%M:%S")
    gameDuration = round(match_data['info']['gameDuration'] / 60 , 2)
    gamemode = match_data['info']['gameMode']
    gameversion = match_data['info']['gameVersion']

    
    return gamematchid , gameCreation , gameDuration , gamemode , gameversion

def findplayer(match_data):
    participants = match_data['metadata']['participants']
    return participants

def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    champion = player_data['championId']
    k = player_data['kills']
    d = player_data['deaths']
    a = player_data['assists']
    win = player_data['win']
     
    return champion , k , d , a , win



today = datetime.now()
#today = datetime(2024, 5, 2)
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = (today - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
today_epoch = today.timestamp()
yesterday_epoch = yesterday.timestamp()    
matchinfodatalist = {
    'matchId' :[],
    'gameCreation' :[],
    'gameDuration' :[],
    'gameMode' :[],
    'gameVersion':[]
}

playerdatamatch = {
    'matchId' :[],
    'puuid' :[],
    'championId': [],
    'kills': [],
    'deaths': [],
    'assists': [],
    'win': []

}

api_key = ""  #apikey

region = '' #region
massregion = '' #massregion
sum_list = [[]] #list of player
for i in range(len(sum_list)):
    puuid = get_puuid(sum_list[i][0],region,sum_list[i][1],api_key)
    starttime = str(int(yesterday_epoch))
    endtime = str(int(today_epoch))
    match_ids = get_match(puuid , massregion , starttime , endtime , api_key)


    for match_id in match_ids:
        if len(match_ids) > 0:
            match_data = get_match_data(match_id, massregion, api_key)
            #print(match_id)
            if match_data == '404':
                pass
            else:
                gamematchid , gamecreation , gameduration , gamemode , gameversion = match_info_data(match_data)
                matchinfodatalist['matchId'].append(gamematchid)
                matchinfodatalist['gameCreation'].append(gamecreation)
                matchinfodatalist['gameDuration'].append(gameduration)
                matchinfodatalist['gameMode'].append(gamemode)
                matchinfodatalist['gameVersion'].append(gameversion)
                participants = findplayer(match_data) 
                for player in participants:
                    champion , k , d , a , win = find_player_data(match_data, player)
                    playerdatamatch['matchId'].append(gamematchid)
                    playerdatamatch['puuid'].append(player)
                    playerdatamatch['championId'].append(champion)
                    playerdatamatch['kills'].append(k)
                    playerdatamatch['deaths'].append(d)
                    playerdatamatch['assists'].append(a)
                    playerdatamatch['win'].append(win)

        else:
            print('Data not found')


    #print(matchinfodatalist)
    #print(playerdatamatch)

matchinfodf = pd.DataFrame(matchinfodatalist)
playermatchdf = pd.DataFrame(playerdatamatch)
print(len(matchinfodf))
print(len(playermatchdf))
matchinfodf = matchinfodf.drop_duplicates()
playermatchdf = playermatchdf.drop_duplicates()

print(matchinfodf)
print(playermatchdf)

day = yesterday.strftime("%Y-%m-%d")
pathhis = r"C:\workspace1\Riot API\Data\MatchHistory"
filenamehis = "match_" + "_" + day +".csv"

pathscore = r"C:\workspace1\Riot API\Data\MatchScore"
filenamescore = "score_" + "_" + day +".csv"

matchinfodf.to_csv(os.path.join(pathhis , filenamehis) , index = False)
playermatchdf.to_csv(os.path.join(pathscore , filenamescore) , index = False)
 
        