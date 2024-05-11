import os
import json


bannedStats = ['goal_succ_rate', 'possession_percentage','overtime_goals','conceded_goals','losses','wins','overtime_losses','ties','shutouts_against','contributed_goals','faceoffs_lost','was_mercy_ruled','overtime_wins','game_winning_goals','primary_assists','possession_time_sec']

class Stat:
    def __init__(self, name, x, flip) -> None:
        self.statName = name
        flip = not flip
        if not flip:
            self.statHomeScore, self.statAwayScore = StatPuller.retStat(name, x)
        else:
            self.statAwayScore, self.statHomeScore = StatPuller.retStat(name, x)
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
    def __init__(self, dirIn, auto: bool, flip: bool) -> None:
        self.matchedDir = f"{dirIn}\\Matches"
        self.autoStats = auto
        self.flip = flip
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
                possesion = Stat("possession_time_sec", x, self.flip)
                total = possesion.statAwayScore + possesion.statHomeScore
                possesion.statName = "possession_percentage"
                possesion.statAwayScore = round(100*(possesion.statAwayScore/total))
                possesion.statHomeScore = round(100*(possesion.statHomeScore/total))
                possesion.bestPlayer = (possesion.bestPlayer[0], round(100*(possesion.bestPlayer[1]/total)))
                stats[stat] = possesion
            elif stat == "goal_succ_rate":
                goals = Stat("goals", x, self.flip)
                shots = Stat("shots", x, self.flip)
                goals.statAwayScore = round(100*(goals.statAwayScore/shots.statAwayScore))
                goals.statHomeScore = round(100*(goals.statHomeScore/shots.statHomeScore))
                goals.statName = "goal_succ_rate"
                
                goals.bestPlayer = (goals.bestPlayer[0], self.getBestShotAcc(goals.bestPlayer[0], x))
                stats[stat] = goals
            else:
                stats[stat] = Stat(stat, x, self.flip)
        allKnownStats = set()
        for player in x['players']:
            player = player["stats"]
            for stat in player:
                ss = Stat(stat, x, self.flip)
                allKnownStats.add(ss)
        for stat in allKnownStats:
            stat: Stat
            if min(stat.statAwayScore, stat.statHomeScore) / max(stat.statAwayScore, stat.statHomeScore) < .2 and stat.statName not in bannedStats and stats.get(stat.statName) == None and self.autoStats:
                stats[stat.statName] = stat



        return stats

