import customtkinter as tk
import Segments.leaderboardgen
from Segments.scheduledGame import Team, Game, Colour, getValidColours
from Segments.statPuller import Stat, StatPuller
from Segments.sheetGen import makeStats
from Segments.teamLoader import loadTeams
from Segments.teamSetter import setTeams
from Segments.schedule import createSchedule
from tkinter import colorchooser
import json
import os
import pickle
DEFAULTSPACING = 10
FRAMESPACING = 0
ROOTFRAMESPACING = 20


class mainWindow:
    settingsFile = "SlapStreamConf.cfg"
    settings = {}
    teamsList = []
    gamesList = []
    homeTeam = None
    awayTeam = None
    homeScore = 0
    awayScore = 0
    def saveSettings():
        with open(mainWindow.settingsFile, "w") as g:
            json.dump(mainWindow.settings, g)
    def loadSettings():
        if os.path.exists(mainWindow.settingsFile):
            with open(mainWindow.settingsFile, "r") as g:
                mainWindow.settings = json.load(g)
    def addhomeScore():
        mainWindow.homeScore +=1
        with open(os.path.join(mainWindow.settings['asset_output'],"Home","scoreHome.txt"), "w") as f:
                f.write(str(mainWindow.homeScore))
    def subhomeScore():
        mainWindow.homeScore -=1
        with open(os.path.join(mainWindow.settings['asset_output'],"Home","scoreHome.txt"), "w") as f:
                f.write(str(mainWindow.homeScore))
    def addawayScore():
        mainWindow.awayScore +=1
        with open(os.path.join(mainWindow.settings['asset_output'],"Away","scoreAway.txt"), "w") as f:
                f.write(str(mainWindow.awayScore))
    def subawayScore():
        mainWindow.awayScore -=1
        with open(os.path.join(mainWindow.settings['asset_output'],"Away","scoreAway.txt"), "w") as f:
                f.write(str(mainWindow.awayScore))
    def importTeams():
        if os.path.exists("teams.pckl"):
            mainWindow.teamsList = pickle.load(open("teams.pckl", "rb"))
    def saveTeams(self):
        pickle.dump(mainWindow.teamsList, open("teams.pckl", "wb"))
    def pullStats(self):
        try:
            statslist = [x for x, y, in mainWindow.settings.items() if y == 1]
            stats = StatPuller(mainWindow.settings["matches_input"], mainWindow.settings["auto_stats"], self.flipTeamsToggle.get()).getStats(statslist)
            print(stats)
        except:
            print("Something went wrong with pulling stats")
        makeStats(stats, mainWindow.homeTeam, mainWindow.awayTeam, self.settings['asset_output'])
    def resolveTeam(self, name: str):
        t = [x for x in mainWindow.teamsList if x.teamName == name][0]
        t: Team
        return t
    def swapTeams(self):
        tmp = mainWindow.homeTeam
        mainWindow.homeTeam = mainWindow.awayTeam
        mainWindow.awayTeam = tmp
        setTeams(self.homeTeam,self.awayTeam, self.settings["asset_output"], mainWindow.settings["matches_input"])
        tmp = mainWindow.homeScore
        mainWindow.homeScore = mainWindow.awayScore
        mainWindow.awayScore = tmp
        with open(os.path.join(mainWindow.settings['asset_output'],"Home","scoreHome.txt"), "w") as f:
                f.write(str(mainWindow.homeScore))
        with open(os.path.join(mainWindow.settings['asset_output'],"Away","scoreAway.txt"), "w") as f:
                f.write(str(mainWindow.awayScore))
    def copyClubs(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(f"clubs set {mainWindow.awayTeam.accronym} {mainWindow.homeTeam.accronym}")
        self.root.update()

    def __init__(self) -> None:
        mainWindow.loadSettings()
        mainWindow.importTeams()

        self.root = tk.CTk()
        #self.root.geometry("500x500")

        self.frame1 = tk.CTkFrame(master=self.root)
        self.frame1.pack(expand=True, padx=ROOTFRAMESPACING,
                         pady=ROOTFRAMESPACING, fill="both")

        self.scorePanel = tk.CTkFrame(master=self.frame1)
        self.scorePanel.pack(padx=FRAMESPACING, pady=FRAMESPACING)

        self.scorePanelHome = tk.CTkFrame(master=self.scorePanel)
        self.scorePanelHome.pack(
            side=tk.LEFT, padx=FRAMESPACING, pady=FRAMESPACING)
        self.scorePanelAway = tk.CTkFrame(master=self.scorePanel)
        self.scorePanelAway.pack(
            side=tk.RIGHT, pady=FRAMESPACING, padx=FRAMESPACING)

        self.addHome = tk.CTkButton(master=self.scorePanelHome, text="Add to Home", command=mainWindow.addhomeScore)
        self.addHome.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.addAway = tk.CTkButton(
            master=self.scorePanelAway, text="Add to Away", command=mainWindow.addawayScore)
        self.addAway.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.subHome = tk.CTkButton(
            master=self.scorePanelHome, text="Sub from Home", command=mainWindow.subhomeScore)
        self.subHome.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.subAway = tk.CTkButton(
            master=self.scorePanelAway, text="Sub from Away", command=mainWindow.subawayScore)
        self.subAway.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.teamPickerFrame = tk.CTkFrame(master=self.frame1)
        self.teamPickerFrame.pack(padx=FRAMESPACING, pady=FRAMESPACING)

        self.homeTeamPickerFrame = tk.CTkFrame(master=self.teamPickerFrame)
        self.homeTeamPickerFrame.pack(
            padx=FRAMESPACING, pady=FRAMESPACING, side=tk.LEFT)

        self.awayTeamPickerFrame = tk.CTkFrame(master=self.teamPickerFrame)
        self.awayTeamPickerFrame.pack(
            padx=FRAMESPACING, pady=FRAMESPACING, side=tk.RIGHT)

        self.awayTeamPickerLable = tk.CTkLabel(
            master=self.awayTeamPickerFrame, text="Away Team")
        self.awayTeamPickerLable.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.homeTeamPickerLable = tk.CTkLabel(
            master=self.homeTeamPickerFrame, text="Home Team")
        self.homeTeamPickerLable.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        choices = [x.teamName for x in mainWindow.teamsList]
        self.awayTeamPicker = tk.CTkOptionMenu(master=self.awayTeamPickerFrame, values= choices, command=self.changeTeams)
        self.awayTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.homeTeamPicker = tk.CTkOptionMenu(master=self.homeTeamPickerFrame, values= choices, command=self.changeTeams)
        self.homeTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.FlipTeamsButton = tk.CTkButton(
            master=self.frame1, text="Flip Teams", command=self.swapTeams)
        self.FlipTeamsButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.showCommandButton = tk.CTkButton(
            master=self.frame1, text="Copy Clubs Command", command=self.copyClubs)
        self.showCommandButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.prepStreamButton = tk.CTkButton(
            master=self.frame1, text="Prepare Stats", command=self.createLadderAndOthers)
        self.prepStreamButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.fetchStatsButton = tk.CTkButton(
            master=self.frame1, text="Fetch Last Period", command=self.pullStats)
        self.fetchStatsButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.flipTeamsToggle = tk.CTkCheckBox(
            master=self.frame1, text="Flip Stats")
        self.flipTeamsToggle.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.newGameButton = tk.CTkButton(
            master=self.frame1, text="Add Game", command=addGameWindow)
        self.newGameButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.newGameButton = tk.CTkButton(
            master=self.frame1, text="Set Game", command=setGameWindow)
        self.newGameButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.configButton = tk.CTkButton(master = self.frame1, text="Open Config", command=lambda: StatChooser(self))
        self.configButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

    def createLadderAndOthers(self):
        homeTeam = mainWindow.homeTeam
        homeTeam = mainWindow.awayTeam
        awayTeam = self.resolveTeam(self.awayTeamPicker.get())

        Segments.leaderboardgen.genBoard(homeTeam, awayTeam, self.teamsList, self.settings["statsheet_link"], self.settings["asset_output"], self.settings["matches_input"])

    def changeTeams(self, _):
        "This should be removed later, as the program should transition to a Game system"

        homeTeam = self.resolveTeam(self.homeTeamPicker.get())
        awayTeam = self.resolveTeam(self.awayTeamPicker.get())

        c1, c2 = homeTeam.colour, awayTeam.colour
        c1, c2 = getValidColours(c1, c2)
        homeTeam, awayTeam = homeTeam.newTeamColour(c1), awayTeam.newTeamColour(c2)

        mainWindow.homeTeam = homeTeam
        mainWindow.awayTeam = awayTeam

        setTeams(homeTeam,awayTeam, self.settings["asset_output"], mainWindow.settings["matches_input"])


    def start(self):
        self.root.mainloop()


class setGameWindow:
    def __init__(self) -> None:
        self.root = tk.CTk()
        self.frame1 = tk.CTkFrame(master=self.root)
        self.frame1.pack(expand=True, padx=ROOTFRAMESPACING,
                         pady=ROOTFRAMESPACING, fill="both")
        for game in mainWindow.gamesList:
            self.newGame(game)
        self.root.mainloop()

    def newGame(self, game: Game):
        def printGame():
            homeTeam = game.homeTeam
            awayTeam = game.awayTeam

            c1, c2 = homeTeam.colour, awayTeam.colour
            c1, c2 = getValidColours(c1, c2)
            homeTeam, awayTeam = homeTeam.newTeamColour(c1), awayTeam.newTeamColour(c2)

            mainWindow.homeTeam = homeTeam
            mainWindow.awayTeam = awayTeam
            setTeams(homeTeam, awayTeam, mainWindow.settings["asset_output"], mainWindow.settings["matches_input"])
            #TODO: Make the program set the teams accordingly
        self.base = tk.CTkFrame(master = self.frame1)
        self.parts = dict()
        self.parts["nameTest"] = tk.CTkLabel(master = self.base)
        self.parts["nameTest"].configure(text=f"{game.homeTeam.league}: {game.homeTeam.accronym} vs {game.awayTeam.accronym} - {game.getTime()}")
        self.parts["selectButton"] = tk.CTkButton(master = self.base, text="Choose", command=printGame)
        for x in self.parts.values():
            x.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
                   anchor='w')
        self.base.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
                   anchor='w')



class addGameWindow:
    def __init__(self) -> None:
        self.root = tk.CTk()
        self.frame1 = tk.CTkFrame(master=self.root)
        self.frame1.pack(expand=True, padx=ROOTFRAMESPACING,
                         pady=ROOTFRAMESPACING, fill="both")
        self.teamPickerFrame = tk.CTkFrame(master=self.frame1)
        self.teamPickerFrame.pack(padx=FRAMESPACING, pady=FRAMESPACING)

        self.homeTeamPickerFrame = tk.CTkFrame(master=self.teamPickerFrame)
        self.homeTeamPickerFrame.pack(
            padx=FRAMESPACING, pady=FRAMESPACING, side=tk.LEFT)

        self.awayTeamPickerFrame = tk.CTkFrame(master=self.teamPickerFrame)
        self.awayTeamPickerFrame.pack(
            padx=FRAMESPACING, pady=FRAMESPACING, side=tk.RIGHT)

        self.awayTeamPickerLable = tk.CTkLabel(
            master=self.awayTeamPickerFrame, text="Away Team")
        self.awayTeamPickerLable.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.homeTeamPickerLable = tk.CTkLabel(
            master=self.homeTeamPickerFrame, text="Home Team")
        self.homeTeamPickerLable.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.awayTeamPicker = tk.CTkOptionMenu(master=self.awayTeamPickerFrame)
        self.awayTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.homeTeamPicker = tk.CTkOptionMenu(master=self.homeTeamPickerFrame)
        self.homeTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.leagues = dict()
        self.leagueFrame = tk.CTkFrame(master = self.frame1)
        def setPro():
            self.leagues["PRO"].select()
            self.leagues["IM"].deselect()
            self.leagues["OPEN"].deselect()
            self.leagues["ALL"].deselect()
            setOptions("Pro")
        def setIM():
            self.leagues["PRO"].deselect()
            self.leagues["IM"].select()
            self.leagues["OPEN"].deselect()
            self.leagues["ALL"].deselect()
            setOptions("Intermediate")
        def setOpen():
            self.leagues["PRO"].deselect()
            self.leagues["IM"].deselect()
            self.leagues["OPEN"].select()
            self.leagues["ALL"].deselect()
            setOptions("Open")
        def setAll():
            self.leagues["PRO"].deselect()
            self.leagues["IM"].deselect()
            self.leagues["OPEN"].deselect()
            self.leagues["ALL"].select()
            setOptions("All")
        self.leagues["PRO"] = tk.CTkRadioButton(master = self.leagueFrame, text="Pro League", command=setPro)
        self.leagues["IM"] = tk.CTkRadioButton(master = self.leagueFrame, text="Intermediate League", command=setIM)
        self.leagues["OPEN"] = tk.CTkRadioButton(master = self.leagueFrame, text="Open League", command=setOpen)
        self.leagues["ALL"] = tk.CTkRadioButton(master = self.leagueFrame, text="All", command=setAll)
        for rad in self.leagues.values():
            rad.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING, anchor="w")
        self.leagueFrame.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        def setOptions(league: str):
            if league == "All":
                x = [g.teamName for g in mainWindow.teamsList]
            else:
                x = [g.teamName for g in mainWindow.teamsList if g.league == league]
            self.awayTeamPicker.configure(require_redraw=True, values=x)
            self.homeTeamPicker.configure(require_redraw=True, values=x)
            self.homeTeamPicker.set(x[0])
            self.awayTeamPicker.set(x[1])

        


        self.timeHour = self.newEntry("Hour")
        self.timeMinute = self.newEntry("Minute")
        self.moogleButton = tk.CTkButton(master=self.frame1, text="Add Game", command=self.out)
        self.moogleButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        setPro()
        self.root.mainloop()
    
    def out(self):
        homeTeam = mainWindow.resolveTeam(mainWindow, self.homeTeamPicker.get())
        awayTeam = mainWindow.resolveTeam(mainWindow, self.awayTeamPicker.get())
        hour = int(self.timeHour.get())
        minute = int(self.timeMinute.get())
        g = Game(homeTeam=homeTeam, awayTeam=awayTeam, hour=hour, minute= minute)
        mainWindow.gamesList.append(g)
        createSchedule(mainWindow.gamesList, mainWindow.settings["asset_output"], mainWindow.settings["matches_input"])
        self.root.destroy()
        

    def newEntry(self, text):
        frame = tk.CTkFrame(master = self.frame1)
        z = tk.CTkEntry(master = frame, placeholder_text=text)
        z.pack(padx=DEFAULTSPACING,pady=DEFAULTSPACING, side=tk.RIGHT)
        g = tk.CTkLabel(master = frame, text=text)
        g.pack(padx=DEFAULTSPACING,pady=DEFAULTSPACING, side=tk.LEFT)
        frame.pack(padx=DEFAULTSPACING,
                   pady=DEFAULTSPACING)
        return z
        
class StatChooser:
    def __init__(self, window: mainWindow) -> None:
        self.mainWind = window
        self.root = tk.CTk()
        self.frame1 = tk.CTkFrame(master=self.root)
        self.frame1.pack(expand=True, padx=ROOTFRAMESPACING,
                         pady=ROOTFRAMESPACING, fill="both")
        self.frame2 = tk.CTkFrame(master=self.frame1)
        self.frame2.pack(padx=DEFAULTSPACING,
                         pady=DEFAULTSPACING, side=tk.LEFT)
        self.fields = {}
        self.fields["passes"] = tk.CTkCheckBox(master = self.frame2, text = "Passes")
        self.fields["possession_time_sec"] = tk.CTkCheckBox(master = self.frame2, text = "Possesion (Sec)")
        self.fields["possession_percentage"] = tk.CTkCheckBox(master = self.frame2, text = "Possesion (%)")
        self.fields["takeaways"] = tk.CTkCheckBox(master = self.frame2, text = "Takeaways")
        self.fields["turnovers"] = tk.CTkCheckBox(master = self.frame2, text = "Turnovers")
        self.fields["score"] = tk.CTkCheckBox(master = self.frame2, text = "Player Score")
        self.fields["goals"] = tk.CTkCheckBox(master = self.frame2, text = "Goals")
        self.fields["goal_succ_rate"] = tk.CTkCheckBox(master = self.frame2, text = "Goal Succes Rate")
        self.fields["shots"] = tk.CTkCheckBox(master = self.frame2, text = "Shots")
        self.fields["faceoffs_won"] = tk.CTkCheckBox(master = self.frame2, text = "Faceoffs Won")
        self.fields["saves"] = tk.CTkCheckBox(master = self.frame2, text = "Saves")
        self.fields["blocks"] = tk.CTkCheckBox(master = self.frame2, text = "Blocks")
        self.fields["post_hits"] = tk.CTkCheckBox(master = self.frame2, text = "Post hits")
        self.fields["assists"] = tk.CTkCheckBox(master = self.frame2, text = "Assists")
        self.fields["secondary_assists"] = tk.CTkCheckBox(master=self.frame2, text="Three Man Plays")
        for key, value in self.fields.items():
            value: tk.CTkCheckBox
            if mainWindow.settings.get(key, 0):
                value.select()
        for x in self.fields.values():
            x.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
                   anchor='w')
        self.saveButton = tk.CTkButton(master = self.frame1, text="Save Config", command=self.saveSettings)
        self.saveButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
                  side=tk.BOTTOM)
        self.frame3 = tk.CTkFrame(master = self.frame1)
        self.frame3.pack(expand=True, padx=DEFAULTSPACING,
                         pady=DEFAULTSPACING, fill="both", side=tk.LEFT)
        self.fields["asset_output"] = self.addNew("Asset Output")
        self.fields["asset_output"].insert(0, mainWindow.settings.get("asset_output", ""))
        self.fields["matches_input"] = self.addNew("Slap Dir")
        self.fields["obs_ip"] = self.addNew("OBS Studio IP")
        self.fields["obs_port"] = self.addNew("OBS Studio Port")
        self.fields["statsheet_link"] = self.addNew("Current Season Team Data")
        self.fields["players_link"] = self.addNew("Current Season Player Data")
        self.fields["auto_stats"] = self.addNewCheckbox("Auto Stats")
        g = tk.CTkFrame(master=self.frame3)
        g.pack(padx=DEFAULTSPACING,pady=DEFAULTSPACING, expand=True, fill="both")
        b = tk.CTkButton(master = g, text="Reload Teams", command=self.reloadClubs)
        b.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
               side=tk.RIGHT, expand=True, fill="x")
        self.fields["players_link"].insert(0, mainWindow.settings.get("players_link", ""))
        self.fields["statsheet_link"].insert(0, mainWindow.settings.get("statsheet_link", ""))
        self.fields["obs_ip"].insert(0, mainWindow.settings.get("obs_ip", ""))
        self.fields["obs_port"].insert(0, mainWindow.settings.get("obs_port", ""))
        self.fields["matches_input"].insert(0, mainWindow.settings.get("matches_input", ""))
        if mainWindow.settings.get("auto_stats", False): self.fields["auto_stats"].select()
        
        self.root.mainloop()
    def addNew(self, text):
        g = tk.CTkFrame(master=self.frame3)
        g.pack(padx=DEFAULTSPACING,pady=DEFAULTSPACING, expand=True, fill="both")
        c = tk.CTkLabel(master = g, text=text)
        c.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
               side=tk.LEFT)
        b = tk.CTkEntry(master = g, placeholder_text="")
        b.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
               side=tk.RIGHT, expand=True, fill="x")
        return b
    def addNewCheckbox(self, text):
        g = tk.CTkFrame(master=self.frame3)
        g.pack(padx=DEFAULTSPACING,pady=DEFAULTSPACING, expand=True, fill="both")
        b = tk.CTkCheckBox(master = g, text=text)
        b.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING,
               side=tk.RIGHT, expand=True, fill="x")
        return b
    def saveSettings(self):
        for key, value in self.fields.items():
            if key =="matches_input":
                mainWindow.settings[key] = os.path.normpath(value.get())
            else:
                mainWindow.settings[key] = value.get()
        mainWindow.saveSettings()
        self.root.destroy() 
    def reloadClubs(self):
        mainWindow.teamsList = loadTeams(mainWindow.settings["matches_input"], mainWindow.settings["players_link"])
        x = [g.teamName for g in mainWindow.teamsList]
        self.mainWind.awayTeamPicker.configure(require_redraw=True, values=x)
        self.mainWind.saveTeams()