import os
import sys
import json

import numpy as np

from datetime import datetime
from riotwatcher import RiotWatcher, ApiError

# CONSTANTS
REGION_NA = 'na1'
GAMEMODES = set([400,420,430,440,700]) #https://developer.riotgames.com/game-constants.html

# One of these is created for every match.
class Row:
    win = None
    playerID = None
    championID = None
    firstDragon = None
    firstInhibitor = None
    firstBaron = None
    allyBaronKills = None
    enemyBaronKills = None
    riftHerald = None
    firstBlood = None
    allySide = None
    firstTower = None
    allyTowerKills = None
    enemyTowerKills = None
    allyDragonKills = None
    enemyDragonKills = None
    allyInhibitorKills = None
    enemyInhibitorKills = None
    firstBloodAssist = None
    visionScore = None
    damageToObjectives = None
    damageToChampions = None
    ccScore = None
    kills = None
    deaths = None
    assists = None
    goldEarned = None
    champLevel = None
    firstInhibitorAssist = None
    visionWardsPurchased = None
    totalHealed = None
    championMasteryLevel = None
    firstBloodKill = None
    firstTowerAssist = None
    fiveMinuteXPDelta = None
    fiveMinuteGoldDelta = None
    wardKills = None

try:
    riot_key = os.environ['RIOT_API_KEY']
except KeyError as e:
    print("Please set the RIOT_API_KEY env variable.")
    sys.exit(1)


# TODO region should be configurable
watcher = RiotWatcher(riot_key)

# Fetch first 20 games from summoner
def fetchGames(summonerName):
    # We go from summoner name to accountId to matchList.
    # TODO err catch if there's no arg or if summoner not found
    targetId = watcher.summoner.by_name(REGION_NA, summonerName)["accountId"]
    matchList = watcher.match.matchlist_by_account(REGION_NA, targetId, queue=GAMEMODES, champion=set([targetChampId]))["matches"]

    for match in matchList:
        # For each match, construct a row
        r = Row()

        champId = match["champion"]
        matchId = match["gameId"] # This is sometimes called gameId in the riot api doc, sometimes matchId (blech)

        # Need the actual match object
        matchObject = watcher.match.by_id(REGION_NA, matchId)

        # Figure out which team is friendly and which is enemy by the champId, via the side code (100 is blue, 200 is red - whoever made this API should be shot)
        allySideId = [participant["teamId"] for participant in matchObject["participants"] if participant["championId"] == champId][0]

        # Fetch team-level stats
        for team in matchObject["teams"]:
            # Fill in either Ally or Enemy team vars
            if team["teamId"] == allySideId:
                r.firstDragon = "Ally" if team["firstDragon"] else None
                r.firstBaron = "Ally" if team["firstBaron"] else None
                r.firstInhibitor = "Ally" if team["firstInhibitor"] else None
                r.firstBlood = "Ally" if team["firstBlood"] else None
                r.allyBaronKills = team["baronKills"]
                r.riftHerald = "Ally" if team["firstRiftHerald"] else None
                r.allySide = "Blue" if team["teamId"] == 100 else "Red"
                r.firstTower = "Ally" if team["firstTower"] else None
                r.allyTowerKills = team["towerKills"]
                r.allyDragonKills = team["dragonKills"]
                r.allyInhibitorKills = team["inhibitorKills"]
                r.win = 1 if team["win"] == "Win" else 0
            else:
                r.firstDragon = "Enemy" if team["firstDragon"] else None
                r.firstBaron = "Enemy" if team["firstBaron"] else None
                r.firstInhibitor = "Enemy" if team["firstInhibitor"] else None
                r.firstBlood = "Enemy" if team["firstBlood"] else None
                r.riftHerald = "Enemy" if team["firstRiftHerald"] else None
                r.firstTower = "Enemy" if team["firstTower"] else None
                r.enemySide = "Blue" if team["teamId"] == 100 else "Red"
                r.enemyBaronKills = team["baronKills"]
                r.enemyTowerKills = team["towerKills"]
                r.enemyDragonKills = team["dragonKills"]
                r.enemyInhibitorKills = team["inhibitorKills"]


