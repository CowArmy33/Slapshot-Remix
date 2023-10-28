class Team:
    def __init__(self, teamName, discordId, colour):
        self.teamName = teamName
        self.discordId = discordId
        self.colour = colour
class Game:
    def __init__(self, homeTeam: Team, awayTeam: Team, hour, minute):
        self.time = (hour, minute)
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
    def __repr__(self) -> str:
        string = f"{self.time}, {self.homeTeam}, {self.awayTeam}"
        return string

