from Segments.timestamp import getRelative, getStamp
from colorspacious import deltaE
class Colour:
    def __init__(self, r:int, g:int, b:int):
        self.R = r
        self.G = g
        self.B = b
    def compare(self, colour):
        "Returns True if the colours are fine to use"
        print(self.getRGB())
        print(colour.getRGB())
        dist = deltaE(self.getRGB(), colour.getRGB(), "sRGB255")
        print(f"Dist = {dist}")
        if dist > 17:
            print("True")
            return True
        print("False")
        return False
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getNorm(self):
        return (self.R/255,self.G/255,self.B/255)    
    def getInverse(self):
        return (255-self.R, 255-self.G, 255-self.B)
    def getHex(self):
        return '%02x%02x%02x' % self.getRGB()
    def __repr__(self) -> str:
        string = f"R: {self.R}, G: {self.G}, B: {self.B}"
        return string
    @staticmethod
    def Hex(value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip('#')
        lv = len(value)
        r,g,b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return Colour(r, g, b)

def getValidColours(c1: Colour, c2: Colour):
    "Takes two input colours and returns a valid set of colours, will invert away team if too close, and if still causing trouble, will just return Red and Blue"
    if c1.compare(c2):
        return (c1, c2)
    r, g, b = c2.getInverse()
    c2 = Colour(r,g,b)
    for c, v in c1.__dict__.items():
        print(c, v)
    for c, v in c2.__dict__.items():
        print(c, v)
    if c1.compare(c2):
        return(c1,c2)
    red = Colour(205, 47, 16)
    r, g, b = red.getInverse()
    blue = Colour(r,g,b)
    return(red, blue)

class Team:
    """Logos are stored relative to StreamingAssets"""
    def __init__(self, teamName: str, accronym: str, discordId: str, colour: Colour, image: str, league: str, players: list[str]):
        self.teamName = teamName
        self.discordId = discordId
        self.colour = colour
        self.image = image
        self.players = players
        self.accronym = accronym
        self.league = league
    def newTeamColour(self, cIn: Colour):
        return Team(self.teamName,self.accronym,self.discordId,cIn,self.image,self.league, self.players)
    def __repr__(self):
        g = ""
        for key, value in self.__dict__.items():
            g = g + f"{key} : {value}\n"
        return g
class Game:
    def __init__(self, homeTeam: Team, awayTeam: Team, hour, minute):
        self.time = (hour, minute)

        c1, c2 = homeTeam.colour, awayTeam.colour
        c1, c2 = getValidColours(c1, c2)
        homeTeam, awayTeam = homeTeam.newTeamColour(c1), awayTeam.newTeamColour(c2)

        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.timeRel = getRelative(hour, minute)
        self.timeCon = getStamp(hour, minute)
    def __repr__(self) -> str:
        string = f"{self.time}, {self.homeTeam}, {self.awayTeam}"
        return string
    def getTime(self):
        PM = False
        time = None
        hour = self.time[0]
        if self.time[0] > 12: 
            hour = self.time[0] - 12
            PM = True
        minute = self.time[1]
        if minute < 10:
            minute = f"0{minute}"
        modifier = "AM"
        if PM:
            modifier = "PM"
        time = f"{hour}:{minute}{modifier}"
        return time

