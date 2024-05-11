import json
import os
import requests
from Segments.scheduledGame import Colour, Team
def loadTeams(dir, link):
    "Returns a list of teams from the clubs file, give the directory one layer above StreamingAssets"
    dir = dir + r"\StreamingAssets\clubs.json"
    x = json.load(open(dir, "rb"))
    link = link.replace("/edit#", "/export?format=csv&")
    if link not in ['', None]:
        playerData = requests.get(link).content.decode().strip().splitlines()
        playerData = [x.split(",") for x in playerData]
        playerData = [[x[1], x[5]] for x in playerData]
    else:
        playerData = []
    lst = []
    for g in x:
        g: dict
        print(g)
        accr = g['acronym']
        name = g['name']
        img = g['logo']
        colour = g['colors']['home']['primary']
        discId = g.get("discId", None)
        players = [x[1] for x in playerData if x[0] == name]
        if len(players) == 0: players = None 
        league = g.get("league", None)
        #if os.path.exists(f"players\\{name}.txt"):
        #    with open(f"players\\{name}.txt") as f:           
        #        players = [x.strip() for x in f.readlines()]
        if league is not None:
            t = Team(name, accr, discId, Colour.Hex(colour), img, league, players)
            lst.append(t)
    return lst


