#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import pprint
cookies = {}

"""
    General functions
"""

def login(pseudo, password):
    global cookies
    url = "http://www.manawyrd.fr/login.php"
    data = {
        'username': pseudo,
        'password': password,
        'login': "Connexion",
    }

    r = requests.post(url, data=data, cookies=cookies)
    webpage = r.text
    cookies = r.cookies.get_dict();
    return webpage
    #print(txt)
    #pprint.pprint(cookies)
    
    
def getMyrims(pseudo, password):
    searchValue = "../images/template/myrins_off.png"
    while searchValue:
        print("Try to get Myrims")
        webpage = login(pseudo, password)
        if not searchValue in webpage:
            searchValue = False
            print("SUCCESS")
        
    

def main():
    pseudo = input()
    password = input()
    # login('Aronar', 'SKYWALKER596t@')
    getMyrims(pseudo, password)
    # pprint.pprint(cookies)

main()
