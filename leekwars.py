#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import pprint
import random
import time
import base64

"""
    
   TODO: COMBATS SOLO, FARMER, TEAM, BATTLE_ROYAL
         REGISTER TOURNAMENT 
    
"""

# global vars
cookies = {}
garden = {}
farmer = {}

"""
    General API functions
"""

def api_login(login, password):
    global cookies, farmer
    url = "https://leekwars.com/api/farmer/login"
    data = {
        'login': login,
        'password': password,
    }

    r = requests.post(url, data=data, cookies=cookies)
    farmer = r.json()['farmer'];
    cookies = r.cookies.get_dict();

    print("Loged as", farmer['login'])
    

def api_getGarden():
    global garden
    url = "https://leekwars.com/api/garden/get/$"
    r = requests.get(url, cookies=cookies)
    garden = r.json()['garden']

def api_waitForFightResult(idFight):
    hasEnded = False
    sleepTime = 0.5
    while not hasEnded:
        url = "https://leekwars.com/api/fight/get/" + str(idFight)

        r = requests.post(url, cookies=cookies, data={
            'token': '$',
            'fight_id': str(idFight),
        })
        result = r.json()['fight']
        if result['status'] == 1:
            hasEnded = True
            if result['winner'] == 0:
                print("Match null")
            elif result['winner'] == 1:
                print("Winner: ", result['team1_name'])
            else:
                print("Winner: ", result['team2_name'])
        else:
            time.sleep(sleepTime)
            sleepTime *= 2
            sleepTime = min(sleepTime, 2)

"""
    Generic codes
"""

def getMinOpponent(json):
    opponents = json['opponents']
    enemy = opponents[0]
    for op in opponents:
        if op['talent'] < enemy['talent']:
            enemy = op
    return enemy

"""
    API solo fight
"""

def api_attackSolo(leek_id, enemy):
    print("Attack", enemy['name'], 'id', enemy['id'], 'talent', enemy['talent'], "  with leek", farmer['leeks'][str(leek_id)]['name'])
    
    url = "https://leekwars.com/api/garden/start-solo-fight"

    r = requests.post(url, cookies=cookies, data={
        'leek_id': leek_id,
        'target_id': enemy['id'],
        'token': '$',
    })
    idFight = r.json()['fight']
    print("Fight id", idFight, end="  ")
    api_waitForFightResult(idFight)
    

def doFight(leek):
    url = "https://leekwars.com/api/garden/get-leek-opponents/" + str(leek) + "/$"

    r = requests.post(url, cookies=cookies, data={
        'leek_id': leek,
        'token': '$',
    })
    # pprint.pprint(r.json())
    enemy = getMinOpponent(r.json())
    for op in r.json()['opponents']:
        if int(op['id']) in [40509, 47609, 48029, 49065]:
            enemy = op
    
    api_attackSolo(leek, enemy)
    
    
    
def doSoloFights():
    leeks = list(farmer['leeks'].items())
    for idFight in range(garden['fights']):
        name = leeks[0][1]['name']
        bddID = leeks[0][0]
        
        doFight(bddID)
        
        
        leeks = leeks[1:] + leeks[0:1]
    """for leek, nbFight in garden['solo_fights'].items():
        print("========== Search for a fight, leek", farmer['leeks'][str(leek)]['name'])
        for iFight in range(nbFight):
            doFight(leek)"""


"""
    API Farmer fight
"""

def api_attackFarmer(farmer):
    print("Attack farmer", farmer['name'], "id", farmer['id'])
    url = "https://leekwars.com/api/garden/start-farmer-fight"
    r = requests.post(url, cookies=cookies, data={
        'token': '$',
        'target_id': str(farmer['id'])
    })
    # pprint.pprint(r.json())
    api_waitForFightResult(r.json()['fight'])

def api_doFarmerFights():
    print("========== Farmer fights")
    for numFight in range(garden['farmer_fights']):
        url = "https://leekwars.com/api/garden/get-farmer-opponents/$"

        r = requests.post(url, cookies=cookies, data={
            'token': '$',
        })
        # pprint.pprint(r.json())
        
        enemy = getMinOpponent(r.json())
        api_attackFarmer(enemy)
        
"""
    API Team fight
"""

def api_attackTeam(teamEnemy, myComposition):
    print("========== Attack Team", teamEnemy['name'], "id", teamEnemy['id'])
    url = "https://leekwars.com/api/garden/start-team-fight"
    r = requests.post(url, cookies=cookies, data={
        'token': '$',
        'composition_id': str(myComposition['id']),
        'target_id': str(teamEnemy['id']),
    })
    # pprint.pprint(r.json())
    api_waitForFightResult(r.json()['fight'])

def api_doTeamFights():
    print("========== Team fights")
    for composition in garden['my_compositions']:
        for numFight in range(composition['fights']):
            url = "https://leekwars.com/api/garden/get-composition-opponents/"+str(composition['id']) + "/$"
            r = requests.post(url, cookies=cookies, data={
                'token': '$',
                'composition': composition['id'],
            })
            #pprint.pprint(r.json())
            
            enemy = getMinOpponent(r.json())
            api_attackTeam(enemy, composition)

"""
    Tournaments
"""
def registerTournaments():
    print("========== Register tournaments")
    for leekId, leek in farmer['leeks'].items():
        # pprint.pprint(leek)
        url = "https://leekwars.com/api/leek/register-tournament"
        r = requests.post(url, cookies=cookies, data={
            'token': '$',
            'leek_id': leekId,
        })
    # farmer
    url = "https://leekwars.com/api/farmer/register-tournament"
    r = requests.post(url, cookies=cookies, data={ 'token': '$'})

def main():
    api_login(input(), input())
    #pprint.pprint(farmer)
    api_getGarden()
    pprint.pprint(garden)
    
    pprint.pprint(farmer)
    doSoloFights()
    #api_doFarmerFights()
    """api_doTeamFights()
    registerTournaments()"""


main()
