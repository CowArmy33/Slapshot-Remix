import os
import json

class Stat:
    def __init__(self, name, x) -> None:
        self.statName = name
        self.statHomeScore, self.statAwayScore = StatPuller.retStat(name, x)
        self.bestPlayer = StatPuller.getHighest(name, x)
    def __repr__(self) -> str:
        rpp = f"""
        Stat: {self.statName}
        Home: {self.statHomeScore}
        Away: {self.statAwayScore}
        Best Player: {self.bestPlayer}
        """
        return rpp
class StatPuller:
    def __init__(self, dirIn) -> None:
        self.matchedDir = f"{dirIn}\\Matches"

    def retStat(text, x):
        home = 0
        away = 0
        for g in x["players"]:
            if g["team"] == 'home':
                home += int(g["stats"].get(text, 0))
            else:
                away += int(g["stats"].get(text, 0))

        return home, away

    def getHighest(text, x):
        highest = ("None", 0)
        highestHome = ("None", 0)
        highestAway = ("None", 0)
        for g in x["players"]:
            stat = g["stats"].get(text, 0)
            if g["team"] == 'home' and stat > 0:
                if stat > highest[1]:
                    highest = (g["username"], stat)
                if stat > highestHome[1]:
                    highestHome = (g["username"], stat)
            elif stat > 0:
                if stat > highest[1]:
                    highest = (g["username"], stat)
                if stat > highestAway[1]:
                    highestAway = (g["username"], stat)
        return highest
    
    def getBestShotAcc(self, text, x):
        for g in x["players"]:
            if g["username"] == text:
                return round(100*(g["stats"].get("goals", 0) / g["stats"].get("shots", 1)))

    def getStats(self, array):
        
        file = max([self.matchedDir + f"\\{file}" for file in os.listdir(self.matchedDir)], key=os.path.getctime)
        x = open(file, "r")
        x = json.load(x)

        stats = {}
        for stat in array:
            if stat == "possession_percentage":
                possesion = Stat("possession_time_sec", x)
                total = possesion.statAwayScore + possesion.statHomeScore
                possesion.statName = "possession_percentage"
                possesion.statAwayScore = round(100*(possesion.statAwayScore/total))
                possesion.statHomeScore = round(100*(possesion.statHomeScore/total))
                possesion.bestPlayer = (possesion.bestPlayer[0], round(100*(possesion.bestPlayer[1]/total)))
                stats[stat] = possesion
            elif stat == "goal_succ_rate":
                goals = Stat("goals", x)
                shots = Stat("shots", x)
                goals.statAwayScore = round(100*(goals.statAwayScore/shots.statAwayScore))
                goals.statHomeScore = round(100*(goals.statHomeScore/shots.statHomeScore))
                goals.statName = "goal_succ_rate"
                
                goals.bestPlayer = (goals.bestPlayer[0], self.getBestShotAcc(goals.bestPlayer[0], x))
                stats[stat] = goals
            else:
                stats[stat] = Stat(stat, x)


        return stats

