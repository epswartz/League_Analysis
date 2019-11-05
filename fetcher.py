import os
import sys
import json

import numpy as np

from datetime import datetime
from riotwatcher import RiotWatcher, ApiError

# CONSTANTS
REGION_NA = 'na1'
GAMEMODES = set([400,420,430,440,700]) #https://developer.riotgames.com/game-constants.html

try:
    riot_key = os.environ['RIOT_API_KEY']
except KeyError as e:
    print("Please set the RIOT_API_KEY env variable.")
    sys.exit(1)

# For now, arg 1 is summoner name and arg 2 is champ id. In future will read both from current game?

# TODO region should be configurable
watcher = RiotWatcher(riot_key)

# Fetch first 20 games from summoner
def fetchGames(summonerName):
    # We go from summoner name to accountId to matchList.
    # TODO err catch if there's no arg or if summoner not found
    targetId = watcher.summoner.by_name(REGION_NA, summonerName)["accountId"]
    matchList = watcher.match.matchlist_by_account(REGION_NA, targetId, queue=GAMEMODES, champion=set([targetChampId]))["matches"]

for match in matchList:
    champId = match["champion"]
    matchId = match["gameId"] # This is sometimes called gameId in the riot api doc, sometimes matchId (blech)

    # Need the actual match object so that we can see participantIdentities.
    matchObject = watcher.match.by_id(REGION_NA, matchId)

    # Need to find the participantId for the player we care about - we use this info to distinguish the players in the timeline data.
    targetParticipantId = -1
    for p in matchObject["participantIdentities"]:
        if p["player"]["accountId"] == targetId:
            targetParticipantId = p["participantId"]

    # Fetch timeline data for game

progress = 0
printProgressBar(progress, barLength, prefix = ' Processing Data:', suffix = 'Complete', length = 50)

# Store positions keyed by minute mark, that's what will eventually separate the visualization
positions = {}
for i in range(0, 7):
    positions[i] = {}
    positions[i]["x"] = []
    positions[i]["y"] = []


for tl in timeLines:
    if len(tl["frames"]) >= 10:
        # TODO handle remakes - they'll be shorter than 6 minutes and cause KeyError
        for i in range(0, 7): # First 6 frames are the first 6 minutes - these are minute 1 to 7 (minute 0 everyone is on base)
            #positions[i]["x"].append(10000)
            #positions[i]["y"].append(10000)
            positions[i]["x"].append( tl["frames"][i]["participantFrames"][str(targetParticipantId)]["position"]["x"])
            positions[i]["y"].append( tl["frames"][i]["participantFrames"][str(targetParticipantId)]["position"]["y"])

        progress += 1
        printProgressBar(progress, barLength, prefix = ' Processing Data:', suffix = 'Complete', length = 50)

# Build Heatmaps

# TODO loop over. For now just building heatmap for minute 1


heatmap, xedges, yedges = np.histogram2d(positions[1]["x"], positions[1]["y"], bins=50)
extent = [MAP_MIN_X, MAP_MAX_X, MAP_MIN_Y, MAP_MAX_Y]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.show()

#heatmap, xedges, yedges = np.histogram2d(np.array(positions[3]["x"]), np.array(positions[3]["y"]), bins=50)
#
#add(map_image, heatmap, alpha=0.7)
#
#plt.show()

