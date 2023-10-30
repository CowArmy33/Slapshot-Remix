class Colour:
    def __init__(self, r:int, g:int, b:int):
        self.R = r
        self.G = g
        self.B = b
    def compare(self, colour: Colour):
        "Returns False if two colors are too close to eachother in terms of RGB"
        r = self.R = colour.R
        g = self.G = colour.G
        b = self.B = colour.B
        if r + g + b > 76:
            return False
        return True
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getNorm(self):
        return (self.R/255,self.G/255,self.B/255)    
    def getInverse(self):
        return (255-self.R, 255-self.G, 255-self.B)

def getValidColours(c1: Colour, c2: Colour):
    "Takes two input colours and returns a valid set of colours, will invert away team if too close, and if still causing trouble, will just return Red and Blue"
    if c1.compare(c2):
        return (c1, c2)
    r, g, b = c2.getInverse()
    c2 = Colour(r,g,b)
    if c1.compare(c2):
        return(c1,c2)
    red = Colour(205, 47, 16)
    r, g, b = red.getInverse()
    blue = Colour(r,g,b)
    return(red, blue)

class Team:
    def __init__(self, teamName: str, discordId: str, colour: Colour, image: str):
        self.teamName = teamName
        self.discordId = discordId
        self.colour = colour
        self.image = image
class Game:
    def __init__(self, homeTeam: Team, awayTeam: Team, hour, minute):
        self.time = (hour, minute)
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
    def __repr__(self) -> str:
        string = f"{self.time}, {self.homeTeam}, {self.awayTeam}"
        return string

