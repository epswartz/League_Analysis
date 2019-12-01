import os
import sys
import json
import time
import numpy as np

from datetime import datetime
from riotwatcher import RiotWatcher, ApiError

from row import Row, header

print(header())

with open('champions.json', 'r') as f:
    champs_by_id = json.load(f)

with open('tags.json', 'r') as f:
    tags_by_champ = json.load(f)

# CONSTANTS
REGION_NA = 'na1'
GAMEMODES = set([400,420,430,440,700]) #https://developer.riotgames.com/game-constants.html


sys.stderr.write("----- NEW RUN -----")
sys.stderr.flush()

try:
    riot_key = os.environ['RIOT_API_KEY']
except KeyError as e:
    print("Please set the RIOT_API_KEY env variable.")
    sys.exit(1)


# TODO region should be configurable
watcher = RiotWatcher(riot_key)

max_retries = 3

# Fetch first 20 games from summoner
def fetchGames(summonerName):
    # We go from summoner name to accountId to matchList.
    # TODO err catch if there's no arg or if summoner not found
    done = False
    retries = 0
    while not done:
        try:
            targetId = watcher.summoner.by_name(REGION_NA, summonerName)["accountId"]
            matchList = watcher.match.matchlist_by_account(REGION_NA, targetId, queue=GAMEMODES)["matches"]
            done = True
        except Exception as e:
            retries += 1
            if retries > max_retries:
                break
            sys.stderr.write(summonerName)
            sys.stderr.write(str(e))
            sys.stderr.write("\n")
            sys.stderr.flush()
            time.sleep(5)
    if not done:
        return
    max_games = 11
    i = 0
    for match in matchList:
        i += 1
        if i > max_games:
            break
        # For each match, construct a row
        r = Row()

        champId = match["champion"]
        matchId = match["gameId"] # This is sometimes called gameId in the riot api doc, sometimes matchId (blech)

        try:
            r.championName = champs_by_id[str(champId)]
            r.championClass = tags_by_champ[r.championName]
        except KeyError as e:
            # Champion wasn't found (should only be Senna)
            sys.stderr.write("Skipped a game for champion: ")
            sys.stderr.write(str(champId) + " ")
            sys.stderr.write(str(r.championName))
            sys.stderr.write("\n")
            continue

        #print(matchId)

        r.matchId = matchId
        r.summonerName = summonerName
        done = False
        retries = 0
        while not done:
            try:
                    matchObject = watcher.match.by_id(REGION_NA, matchId)
                    done = True
            except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        break
                    sys.stderr.write(summonerName)
                    sys.stderr.write(str(e))
                    sys.stderr.write("\n")
                    sys.stderr.flush()
                    time.sleep(5)
        if not done:
            continue
        # Need the actual match object

        if matchObject["gameDuration"] < 305: # 5 minutes plus a bit to guarantee I can get the 5 minute mark timeline frame
            continue

        # Figure out which team is friendly and which is enemy by the champId, via the side code (100 is blue, 200 is red
        # Also store the player for individual stuff.
        playerOfInterest = [participant for participant in matchObject["participants"] if participant["championId"] == champId][0]
        participantId = playerOfInterest["participantId"]
        #print(participantId)
        allySideId = playerOfInterest["teamId"]

        # Fetch team-level stats
        for team in matchObject["teams"]:
            # Fill in either Ally or Enemy team vars
            if team["teamId"] == allySideId:
                r.firstDragon = "Ally" if team["firstDragon"] else r.firstDragon
                r.firstBaron = "Ally" if team["firstBaron"] else r.firstBaron
                r.firstInhibitor = "Ally" if team["firstInhibitor"] else r.firstInhibitor
                r.firstBlood = "Ally" if team["firstBlood"] else r.firstBlood
                r.firstTower = "Ally" if team["firstTower"] else r.firstTower
                r.riftHerald = "Ally" if team["firstRiftHerald"] else r.riftHerald
                r.allyBaronKills = team["baronKills"]
                r.allySide = "Blue" if team["teamId"] == 100 else "Red"
                r.allyTowerKills = team["towerKills"]
                r.allyDragonKills = team["dragonKills"]
                r.allyInhibitorKills = team["inhibitorKills"]
                r.win = 1 if team["win"] == "Win" else 0
            else:
                r.firstDragon = "Enemy" if team["firstDragon"] else r.firstDragon
                r.firstBaron = "Enemy" if team["firstBaron"] else r.firstBaron
                r.firstInhibitor = "Enemy" if team["firstInhibitor"] else r.firstInhibitor
                r.firstBlood = "Enemy" if team["firstBlood"] else r.firstBlood
                r.riftHerald = "Enemy" if team["firstRiftHerald"] else r.riftHerald
                r.firstTower = "Enemy" if team["firstTower"] else r.firstTower
                r.enemySide = "Blue" if team["teamId"] == 100 else "Red"
                r.enemyBaronKills = team["baronKills"]
                r.enemyTowerKills = team["towerKills"]
                r.enemyDragonKills = team["dragonKills"]
                r.enemyInhibitorKills = team["inhibitorKills"]

        # Collect individual stats about the player's performance
        s = playerOfInterest["stats"]

        if r.firstBlood != None:
            r.firstBloodAssist = s["firstBloodAssist"]
            r.firstBloodKill = s["firstBloodKill"]

        if r.firstInhibitor != None:
            r.firstInhibitorAssist = s["firstInhibitorAssist"]

        if r.firstTower != None:
            r.firstTowerAssist = s["firstTowerAssist"]

        r.visionScore = s["visionScore"]
        r.damageToObjectives = s["damageDealtToObjectives"]
        r.damageToChampions = s["totalDamageDealtToChampions"]
        r.ccScore = s["totalTimeCrowdControlDealt"]
        r.kills = s["kills"]
        r.deaths = s["deaths"]
        r.assists = s["assists"]
        r.goldEarned = s["goldEarned"]
        r.champLevel = s["champLevel"]
        r.visionWardsPurchased = s["visionWardsBoughtInGame"]
        r.totalHealed = s["totalHeal"]
        r.wardKills = s["wardsKilled"]

        done = False
        retries = 0
        while not done:
            try:
                    tl = watcher.match.timeline_by_match(REGION_NA, matchId)
                    done = True
            except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        break
                    sys.stderr.write(summonerName)
                    sys.stderr.write(str(e))
                    sys.stderr.write("\n")
                    sys.stderr.flush()
                    time.sleep(5)
        if not done:
            continue
        # Get 5 minute mark data
        fiveMinuteFrame = tl["frames"][5] # there's a 0 minute frame too
        POIframe = fiveMinuteFrame["participantFrames"][str(participantId)]

        POIFiveMinuteGold = POIframe["totalGold"]
        POIFiveMinuteXP = POIframe["xp"]

        avgFiveMinuteGold = sum(f["totalGold"] for k,f in fiveMinuteFrame["participantFrames"].items()) / 10
        avgFiveMinuteXP = sum(f["xp"] for k,f in fiveMinuteFrame["participantFrames"].items()) / 10

        r.fiveMinuteGoldDelta = POIFiveMinuteGold - avgFiveMinuteGold
        r.fiveMinuteXPDelta = POIFiveMinuteXP - avgFiveMinuteXP
        done = False
        retries = 0
        while not done:
            try:
                    encryptedId = watcher.summoner.by_name(REGION_NA, summonerName)["id"]
                    r.championMastery = watcher.champion_mastery.by_summoner_by_champion(REGION_NA,encryptedId, champId)["championPoints"]
                    done = True
            except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        break
                    sys.stderr.write(summonerName)
                    sys.stderr.write(str(e))
                    sys.stderr.write("\n")
                    sys.stderr.flush()
                    time.sleep(5)
        if not done:
            continue
        # Print the row
        print(r.format(), flush=True)

with open(sys.argv[1]) as f:
    names = f.read().splitlines()
    for n in names:
        fetchGames(n)
