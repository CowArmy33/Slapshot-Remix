# Slapshot-Remix
This program is designed for people to stream the game Slapshot Rebound more easily in the OSL Region
Its intended to handle various tasks automatically for the streamer, such as:
- ✅ Changing Teams according to a drop down
- ✅ Fetching current season statistics
- ❌ Preparing public stream announcement timestamps
- ✅ Creating statboards based off of the current game
- ✅ Managing Series Score
- ✅ Easily preparing and handling multiple games
- ❌ Showcasing statistics during gameplay

# Install
There may be a bit of setup required by the user in order to use this, which will include python (preferably the latest version, but older ones may not have issues). There is a file called "requirements.txt", which contains a list of dependancies (not that many), which can be used to install everything needed. Simply run the command "pip install -r requirements.txt" with a terminal / command prompt open within that directory.

Next, you will need to download this repository, either through the download button on Github, or you may want to use the Github Command Line interface to clone this repository and update it in the future when more updates get made. It should not be too difficult to do this. And if you aren't sure how to, then please go ahead and Google it Otherwise, you can just download the repository at its current point in time, which may make getting updates a little bit more difficult. Either way works fine, just go ahead and do what you're more comfortable with. 

Once you have python installed and are ready to go and all dependancies set up, you can run the program by running "main.py".

You will then need to choose "Open Config" at the bottom, and set up the following fields:
  1. Asset Output: The directory where all of the assets this program produces should be placed into, just make sure you know where this is for when you set up OBS
  2. Slap Dir: Place the path to the "Slapshot_Data" folder into here, if you don't know how to find this google "Steam how to find game directory", and explore from there
  3. Current Season Team Data: The link to the google sheet for the season (MAKE SURE YOU COPY THE LINK WHILE YOU ARE ON THE "S## Team Data" PAGE OTHERWISE THINGS MAY BREAK)
  4. Current Season Player Data: The link to the google sheet for the season (MAKE SURE YOU COPY THE LINK WHILE YOU ARE ON THE "S## Player Data" PAGE OTHERWISE THINGS MAY BREAK)

The OBS Studio IP and Port fields currently do not do anything and exist for future usage, so don't worry about those yet. You may configure any of the other settings freely (Auto Stats will use a predetermined threshold to include statistics on the stats screen alongside your other choices)

Now you will need to make sure your clubs.json is up to date, and your "Logos" folder is too. There currently isn't an easy way to ensure this, so you may need to either ask me or check the #streamers chat in the OSL for the latest drop

Finally, once you have ensured clubs is up to date, click "Save Config", Open the config again, and THEN click Reload Teams, and save again (It's to do with the order in which settings are saved just roll with it please otherwise it probably won't work). This will loade all of the teams

With a quick restart of the program you should be good to go!

# Introduction and Setup
This section will cover what each part of the program does going from top to bottom
### Series Points
There are four buttons at the top of the program that are used to add and subtract series points from teams, this is mainly to be used in finals situations, but also proves useful for moments when the in game scoreboard may not reflect the current score and you need to use an alternative (someone forgets periods or the lobby crashes and you need to restart who knows)
It should be very self explanitory
### Team Selector
The team dropdown section here isn't actually intended for usage, but more for debuging, it DOES allow you to select what team is on what side of the screen and visually confirm if certain parts of the program are working as intended, but it doesn't hook up properly with some of the features and is more of a scrap that I left in from testing so people can verify the colours are correct quicker.
### Flip Teams
Fully flips the sides teams are on both in stream elements and internally so you can make the overlays match the game properly, although you may need to add and subtract a series point from both teams just to get the file writers to update correctly, and if you do this you may or may not want to re-use the "Copy Clubs Command" button
### Copy Clubs Command
This button will copy the command to set the team clubs appropriately straight to your clipboard so you don't need to remember accronyms, nor think about which team is home or away (for some reason, in the custom menu the team on the left hand side of the lobby has their color changed to the second entry in the clubs command instead of the first, which screwed with my head a bit but you don't have to worry about it at alla anymore)
### Prepare Stats
This will generate the matchup stats between the teams in the currently selected Game (see "Set Game" and "Add Game"), and will also generate the Season Ladder for the League these teams are in. This will NOT WORK if no game is currently selected, so you will probably want to do that.
### Fetch Last Period
Will make the stats screen for the game (passes, possesion, etc). Uses the latest log file in the slapshot directory, so ensure that the period is finished when using this, otherwise stats may not reflect the current game
### Flip Stats
Most likely will not need this at all, but this toggle will essentially flip the stats screen, yet another left over from debugging where I would get teams on the wrong sides and wanted a quick way to fix it. If you've set everything up well enough, this should NOT be needed at all
### Add Game
This is the window where you are SUPPOSED to set up matches properly instead of the debug ways. Clicking thiss will open up a window where you can filter teams by their league, and also type in what time the game is supposed to be at (24 hour time), and then click Add Game to add it to the list of games being played. This will then also update the schedule file (a .html i forgot what name i actually gave it) to include all the games currently entered into the program. If you want to clear the schedule, and start fresh (may be needed if a game comes up between two other games), you will need to close and reopen the program and start re-entering games in the order they are going to be played, otherwise the schedule will be out of order (I haven't implemented a re-ordering system yet but that may come soonish)
### Set Game
This button opens another window in which you choose from the games you have added to switch to. This will change all assets used for streaming. Many features will not work if you do not use set game. This includes a majority of the other buttons, such as flip teams, prepare stats, and in some circumstances, fetch last period. 
### Open Config
The open config button will open the configuration menu in which you were able to change pretty much any setting that the program requires. This includes directories for asset output directory for Slapshot, OBS Studio ip, port, current season team data and current season player data. In this same menu, you can also configure what statistics will show up when you Choose the fetch last period button on the main application. 

# Usage and tips
This program is best utilized in advance in order to set up all of the different games that may be streamed in one night. It also attempts to manage all of the individual statistics and processing in a way that the streamer doesn't have to worry about actually computing or thinking about any of the additional details that may need to be thought of without this program. As such, for the most part, this program attempts to make everything a 1 click usage and as simple as possible. So that way you can commentate over high paced games. An additional thing that I can say that this program handles is the team lists. It automatically pulls the team lists from the slapshot player stat sheet that you put into the configuration menu. And as such, it should keep it 100% up to date. There currently is no easy way for manual team list entries into the program. So if this issue does arise, you will very likely need to create a text file or change the source in OBS manually.

If you run into any problems setting this up or testing this program out, please contact me. I will try and make sure to get back to you as quickly as possible.

# Logos and clubs.json
Below there will be a link to another repository managed by me, which contains the current up-to-date logos and clubs.json that will be used for this season. Once again, you can either download that repository manually every time that you want to update your logos and clubs file, Or you can clone the repository into the streaming assets folder and simply run a pull git command whenever you want to update your assets.

https://github.com/CowArmy33/StreamingAssets