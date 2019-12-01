# One of these is created for every match.
class Row:
    def __init__(self):
        self.win = None
        self.championName = None
        self.championClass = None
        #self.playerID = None
        self.championID = None
        self.firstDragon = None
        self.firstInhibitor = None
        self.firstBaron = None
        self.allyBaronKills = None
        self.enemyBaronKills = None
        self.riftHerald = None
        self.firstBlood = None
        self.allySide = None
        self.firstTower = None
        self.allyTowerKills = None
        self.enemyTowerKills = None
        self.allyDragonKills = None
        self.enemyDragonKills = None
        self.allyInhibitorKills = None
        self.enemyInhibitorKills = None
        self.firstBloodAssist = None
        self.visionScore = None
        self.damageToObjectives = None
        self.damageToChampions = None
        self.ccScore = None
        self.kills = None
        self.deaths = None
        self.assists = None
        self.goldEarned = None
        self.champLevel = None
        self.firstInhibitorAssist = None
        self.visionWardsPurchased = None
        self.totalHealed = None
        self.championMastery = None
        self.firstBloodKill = None
        self.firstTowerAssist = None
        self.fiveMinuteXPDelta = None
        self.fiveMinuteGoldDelta = None
        self.wardKills = None
        self.matchId = None
        self.summonerName = None

    def format(self):
        return ",".join([str(getattr(self, prop)) for prop in dir(self) if not prop.startswith("_") and not prop == "format"])

def header():
    r = Row()
    return ",".join([prop for prop in dir(r) if not prop.startswith("_") and not prop == "format"])
