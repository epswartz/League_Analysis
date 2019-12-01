import os
import sys
import json

import numpy as np

from datetime import datetime
from riotwatcher import RiotWatcher, ApiError

from row import Row, header


import re
nameRegex = re.compile('^[0-9a-zA-Z ]+$')

# CONSTANTS
REGION_NA = 'na1'
GAMEMODES = set([400,420,430,440,700]) #https://developer.riotgames.com/game-constants.html


try:
    riot_key = os.environ['RIOT_API_KEY']
except KeyError as e:
    print("Please set the RIOT_API_KEY env variable.")
    sys.exit(1)


# TODO region should be configurable
watcher = RiotWatcher(riot_key)

i = 0

with open("./data/names.txt") as f:
    names = f.read().splitlines()
    for n in names:
        i += 1
        try:
            name = n.replace("+", " ")
            if nameRegex.match(name) == None:
                #print("Chucking name:", n)
                continue
            targetId = watcher.summoner.by_name(REGION_NA, name)["accountId"]
            matchList = watcher.match.matchlist_by_account(REGION_NA, targetId, queue=GAMEMODES)["matches"]
            print(name)
            #print(i, "Name is good:", name)
        except Exception as e:
            pass
            #print("Error on name:", name, ":", e)
            #sys.exit(1)

