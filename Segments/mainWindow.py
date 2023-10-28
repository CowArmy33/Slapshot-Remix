import customtkinter as tk
from Segments.scheduledGame import Team, Game
from Segments.statPuller import Stat, StatPuller
from tkinter import colorchooser
import json
DEFAULTSPACING = 10
FRAMESPACING = 0
ROOTFRAMESPACING = 20


class mainWindow:
    settingsFile = "SlapStreamConf.cfg"
    settings = {}
    teamsList = []
    gamesList = []
    homeScore = 0
    awayScore = 0
    def saveSettings():
        with open(mainWindow.settingsFile, "w") as g:
            json.dump(mainWindow.settings, g)
    def loadSettings():
        with open(mainWindow.settingsFile, "r") as g:
            mainWindow.settings = json.load(g)
    def addhomeScore():
        mainWindow.homeScore +=1
    def subhomescore():
        mainWindow.homeScore -=1
    def addawayScore():
        mainWindow.awayScore +=1
    def subawayScore():
        mainWindow.awayScore -=1

    def pullStats(self):
        try:
            statslist = [x for x, y, in mainWindow.settings.items() if y == 1]
            stats = StatPuller(mainWindow.settings["matches_input"]).getStats(statslist)
            print(stats)
        except:
            print("Something went wrong with pulling stats")
        #TODO: Spit out the HTML file


    def __init__(self) -> None:
        mainWindow.loadSettings()

        self.root = tk.CTk()

        self.root.geometry("500x500")

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

        self.addHome = tk.CTkButton(master=self.scorePanelHome, text="Add to Home", command=mainWindow.addawayScore)
        self.addHome.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.addAway = tk.CTkButton(
            master=self.scorePanelAway, text="Add to Away", command=mainWindow.addawayScore)
        self.addAway.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.subHome = tk.CTkButton(
            master=self.scorePanelHome, text="Sub from Home", command=mainWindow.subhomescore)
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
        self.awayTeamPicker = tk.CTkOptionMenu(master=self.awayTeamPickerFrame)
        self.awayTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.homeTeamPicker = tk.CTkOptionMenu(master=self.homeTeamPickerFrame)
        self.homeTeamPicker.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.FlipTeamsButton = tk.CTkButton(
            master=self.frame1, text="Flip Teams")
        self.FlipTeamsButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.prepStreamButton = tk.CTkButton(
            master=self.frame1, text="Prepare Stats")
        self.prepStreamButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.fetchStatsButton = tk.CTkButton(
            master=self.frame1, text="Fetch Last Period", command=self.pullStats)
        self.fetchStatsButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

        self.newGameButton = tk.CTkButton(
            master=self.frame1, text="Add Game", command=addGameWindow)
        self.newGameButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.configButton = tk.CTkButton(master = self.frame1, text="Open Config", command=StatChooser)
        self.configButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)

    def start(self):
        self.root.mainloop()


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
        self.timeHour = self.newEntry("Hour")
        self.timeMinute = self.newEntry("Minute")
        self.moogleButton = tk.CTkButton(master=self.frame1, text="Add Game", command=self.out)
        self.moogleButton.pack(padx=DEFAULTSPACING, pady=DEFAULTSPACING)
        self.root.mainloop()
    
    def out(self):
        homeTeam = self.homeTeamPicker.get()
        awayTeam = self.awayTeamPicker.get()
        hour = int(self.timeHour.get())
        minute = int(self.timeMinute.get())
        g = Game(homeTeam=homeTeam, awayTeam=awayTeam, hour=hour, minute= minute)
        mainWindow.gamesList.append(g)
        print(g)
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
    def __init__(self) -> None:
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
        self.fields["obs_ip"].insert(0, mainWindow.settings.get("obs_ip", ""))
        self.fields["obs_port"].insert(0, mainWindow.settings.get("obs_port", ""))
        self.fields["matches_input"].insert(0, mainWindow.settings.get("matches_input", ""))
        
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
    def saveSettings(self):
        for key, value in self.fields.items():
            mainWindow.settings[key] = value.get()
        mainWindow.saveSettings()
        self.root.destroy() 