import requests
from datetime import datetime, timedelta
import pandas as pd
import os

def get_puuid(summoner_name, region, tag , api_key):
    api_url = (
        "https://" + 
        region +
        ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" +
        summoner_name + "/" + tag +
        "?api_key=" +
        api_key
    )
    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid  

def get_mastery(puuid , server , api_key):
    api_url = (
        "https://" + 
        server + 
        ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/" +
        puuid + 
        "?api_key=" + 
        api_key
    )
    resp = requests.get(api_url)
    player_mastery = resp.json()
    return player_mastery
def get_player_data(puuid , region , server , api_key):
    api_url_acc = (
        "https://" + 
        region + 
        ".api.riotgames.com/riot/account/v1/accounts/by-puuid/" +
        puuid + 
        "?api_key=" + 
        api_key
    )

    api_url_sum = (
        "https://" + 
        server + 
        ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" +
        puuid + 
        "?api_key=" + 
        api_key
    )
    resp_acc = requests.get(api_url_acc)
    account_info = resp_acc.json()
    gamename = account_info['gameName']
    tag = account_info['tagLine']

    resp_sum = requests.get(api_url_sum)
    summoner_info = resp_sum.json()
    id = summoner_info['id']
    account_id = summoner_info['accountId']
    level = summoner_info['summonerLevel']

    return puuid , gamename , tag , id , account_id , level
    


def get_champion_mastery(champion , today):
    puuid = champion['puuid']
    championId = champion['championId']
    championLevel = champion['championLevel']
    championpoint = champion['championPoints']
    last_update = today
    return puuid , championId , championLevel , championpoint , last_update




today = datetime.now()
api_key = "RGAPI-97ac8550-95f6-4e9c-8973-9d1b055c5866"
summoner_name = 'fighter21z'
region = 'asia'
tag = '4514'
massregion = 'sea'
server = 'th2'

puuid = get_puuid(summoner_name,region,tag,api_key)
player_mastery = get_mastery(puuid,server,api_key)

puuid , gamename , tag , id , account_id , level = get_player_data(puuid , region , server , api_key)
account_info = {
    'puuid' :[], 
    'gamename' :[],
    'tag':[],
    'id' :[], 
    'account_id' :[] ,
    'level' :[]
}
account_info['puuid'].append(puuid)
account_info['gamename'].append(gamename)
account_info['tag'].append(tag)
account_info['id'].append(id)
account_info['account_id'].append(account_id)
account_info['level'].append(level)


champion_mastery = {
    'puuid' :[],
    'championId' :[],
    'championLevel' :[],
    'championpoint' :[],
    'last_update' :[]
}
for champion in player_mastery:
    puuid , championId , championlevel , championpoint , last_update = get_champion_mastery(champion , today)
    champion_mastery['puuid'].append(puuid)
    champion_mastery['championId'].append(championId)
    champion_mastery['championLevel'].append(championlevel)
    champion_mastery['championpoint'].append(championpoint)
    champion_mastery['last_update'].append(last_update)




championmasterydf= pd.DataFrame(champion_mastery)

print(championmasterydf)
accountinfodf = pd.DataFrame(account_info)
print(accountinfodf)

pathacc = r"C:\workspace1\Riot API\Data\PlayerInfo"
filenameacc = "account_" + summoner_name +".csv"

pathmas = r"C:\workspace1\Riot API\Data\PlayerMastery"
filenamemas = "mas_" + summoner_name + ".csv"

championmasterydf.to_csv(os.path.join(pathmas , filenamemas) , index = False)
accountinfodf.to_csv(os.path.join(pathacc , filenameacc) , index = False)