import requests
import sys
from os import path
from Segments.scheduledGame import Team, Colour

teamPageFirstHalf = """
  <html>
    <head>
    <style>@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap')</style>
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript">
          var textColor = '#FFFFFF'
          var fontDef = 'Arial'
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawVisualization);

        function drawVisualization() {
          // Some raw data (not necessarily accurate)
  """
teamPageStats = """
            var goals = google.visualization.arrayToDataTable([

            ['Team','{teamL}', '{teamR}'],
            ['Goals', {}, {}],
          ]);
          var goaldif= google.visualization.arrayToDataTable([

            ['Team','{teamL}', '{teamR}'],
            ['Goals differential', {}, {}],
          ]);
          var shots= google.visualization.arrayToDataTable([

            ['Team','{teamL}', '{teamR}'],
            ['Shots', {}, {}],
          ]);
          var saves= google.visualization.arrayToDataTable([

            ['Team','{teamL}', '{teamR}'],
            ['Saves', {}, {}],
          ]);
          var passes= google.visualization.arrayToDataTable([

            ['Team','{teamL}', '{teamR}'],
            ['Passes', {}, {}]
          ]);
  """
teamPageSecondHalf = """
  var options = {{
            animation: {{
              duration: 3700,
              startup: true,
              easing: 'out'
            }},
            tooltip: {{
              trigger: 'selection',
              textStyle:{{
                fontName: fontDef,
                color: 'black',
                fontSize: 20,
            }}
            }},
            titleTextStyle: {{
                color: textColor,
                fontName: fontDef
            }},
            legend: {{
              position:'none',
              textStyle: {{
                  color: textColor,
                  fontName: fontDef
              }}
            }},
            bar: {{
              groupWidth: "80%"
            }},

            vAxis: {{title: '',
                  textStyle: {{
                      color: textColor,
                      fontName: fontDef
                  }},
                      titleTextStyle: {{
                      color: textColor,
                      fontName: fontDef,
                      fontSize: 40
                  }},
                  viewWindow: {{
                    min:0
                    }}

            }},

            hAxis: {{
                  textStyle: {{
                      color: textColor,
                      fontName: fontDef,
                      fontSize:28
                  }}
                  }},
                  viewWindow: {{
                    min: 0
                    }},


            seriesType: 'bars',
            backgroundColor: 'transparent',
            colors:['#{leftCol}', '#{rightCol}'],

                    fontName:'Times-Roaman',
                    fontSize: 18,


          }};

          var goalchart = new google.visualization.ComboChart(document.getElementById('goals'));
          var goaldifchart = new google.visualization.ComboChart(document.getElementById('goal-dif'));
          var shotschart = new google.visualization.ComboChart(document.getElementById('shots'));
          var saveschart = new google.visualization.ComboChart(document.getElementById('saves'));
          var passeschart = new google.visualization.ComboChart(document.getElementById('passes'));
          goalchart.draw(goals, options);
          shotschart.draw(shots, options);
          saveschart.draw(saves, options);
          passeschart.draw(passes, options);
          options.vAxis.viewWindow.min = {minScore} 
          options.vAxis.viewWindow.max = {maxScore}
          goaldifchart.draw(goaldif, options);
        }}
      </script>
    </head>
    <body style="background-color: rgba(0, 0, 0, 0);">
      <div style="position: relative; width: 100%;height: 100%;">
      <div id="goals" style="position:absolute; width: 20%; height: 100%; background-color: rgba(0, 0, 0, 0);"></div>
      <div id="goal-dif" style="position:absolute;left:20%; width: 20%; height: 100%; background-color: rgba(0, 0, 0, 0);"></div>
      <div id="shots" style="position:absolute;left:40%; width: 20%; height: 100%; background-color: rgba(0, 0, 0, 0);"></div>
      <div id="saves" style="position:absolute;left:60%; width: 20%; height: 100%; background-color: rgba(0, 0, 0, 0);"></div>
      <div id="passes" style="position:absolute;left:80%; width: 20%; height: 100%; background-color: rgba(0, 0, 0, 0);"></div></div>
      <div style="font-family: 'Bebas Neue';font-size: 48;color: white;top: 93%;position: absolute;text-align: center;width: 100%;"><span style="color: {leftCol};">{leftTeam} </span> Vs <span style="color: {rightCol};">{rightTeam}</span></div></div>
      </body>
  </html>

  """

# Batch call to the program is made to select teams, made to cooperate with my java program
def genBoard(t1: Team, t2: Team, allteams: list[Team], teamStatsURL: str, out: str, slapdir: str):

  teamStatsURL = teamStatsURL.replace("/edit#", "/export?format=csv&")

  leftTeamImport= t1
  rightTeamImport= t2
  LeagueRequested = t1.league

  class ladderTeam:
    def __init__(self, team):
      self.team: Team = team
      self.Wins = 0
      self.otWins = 0
      self.Losses = 0
      self.otLosses = 0
      self.points = 0
      self.goalDiff = 0
      self.goalFor = 0
      self.league = ""


  teamClassList: list[ladderTeam] = []
  for x in allteams:
    teamClassList.append(ladderTeam(x))

  

  teamStats = requests.get(teamStatsURL)

  teamStatLines = teamStats.content.decode().strip().splitlines()
  for index, x in enumerate(teamStatLines):
      teamStatLines[index] = x.split(",")
  print(teamStatLines)

  t: ladderTeam
  for t in teamClassList:
    for a in teamStatLines:
      if t.team.teamName == a[0]:
        print(t.team.teamName, "is setting Wins to", int(a[4]))
        t.Wins = int(a[4])
        print(t.team.teamName, "is setting otWins to",int(a[5]))
        t.otWins = int(a[5])
        print(t.team.teamName, "is setting Losses to",int(a[6]))
        t.Losses = int(a[6])
        print(t.team.teamName, "is setting otLosses to",int(a[7]))
        t.otLosses = int(a[7])
        print(t.team.teamName, "is setting points to", t.Wins*3 + t.otWins*2 + t.otLosses)
        t.points = t.Wins*3 + t.otWins*2 + t.otLosses
        t.goalDiff = (int(a[11]) - int(a[12]))
        t.goalFor = int(11)
        t.league = a[2]

  teamNames = [a.team.teamName for a in teamClassList]

  for a in teamStatLines:
    if a[0] not in teamNames:
      bru = Team(a, None, None, Colour.Hex("#ffffff"), None, None, None)
      bru = ladderTeam(bru)
      bru.league = a[2]
      teamClassList.append(bru)

  teamClassList.sort(key=lambda a: (a.points, a.goalDiff, a.goalFor), reverse=True)

  leftTeamIndex = 1
  rightTeamIndex = 2
  for index, a in enumerate(teamStatLines):
    if a[0] == leftTeamImport.teamName:
      leftTeamIndex = index
    elif a[0] == rightTeamImport.teamName:
      rightTeamIndex = index



  teamPageStatsF = teamPageStats.format(

                       teamStatLines[leftTeamIndex][15], teamStatLines[rightTeamIndex][15],
                       int(teamStatLines[leftTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]), int(teamStatLines[rightTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]),
                       teamStatLines[leftTeamIndex][16], teamStatLines[rightTeamIndex][16],
                       teamStatLines[leftTeamIndex][18], teamStatLines[rightTeamIndex][18],
                       teamStatLines[leftTeamIndex][21], teamStatLines[rightTeamIndex][21], teamL=teamStatLines[leftTeamIndex][0], teamR=teamStatLines[rightTeamIndex][0],
                       )


  firstTeamCol: str
  secondTeamCol: str

  for x in teamClassList:
    if teamStatLines[leftTeamIndex][0] == x.team.teamName:
      firstTeamCol = x.team.colour.getHex()
    elif teamStatLines[rightTeamIndex][0] == x.team.teamName:
      secondTeamCol = x.team.colour.getHex()

  minimumScore:int
  minimumScore = min(
      int(teamStatLines[leftTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]), int(
          teamStatLines[rightTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]))
  maximumScore:int
  maximumScore = max(
      int(teamStatLines[leftTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]), int(
          teamStatLines[rightTeamIndex][15])-int(teamStatLines[leftTeamIndex][12]))
  if maximumScore < 0:
    maximumScore = 0
  if minimumScore > 0:
    minimumScore = 0
  finalpage = teamPageFirstHalf + teamPageStatsF + teamPageSecondHalf.format(leftCol=firstTeamCol, rightCol=secondTeamCol, minScore=minimumScore, maxScore=maximumScore, leftTeam=teamStatLines[leftTeamIndex][0], rightTeam=teamStatLines[rightTeamIndex][0])

  anotherPage = """
  <style>
      @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

          img {
          height: 60px;
          width: auto;
          max-width: 120px;
      }

      table {
          border-collapse: collapse;
          border-radius: 20px;
          position:absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 80%;
      }
      th{
        background-color:white;
      }
      td,
      th {
          border-top: 2px solid red;
          border-bottom: 2px solid red;
          border-color: black;
          font-size: xx-large;
          font-family: 'Bebas Neue', Verdana, Geneva, Tahoma, sans-serif;
          text-align: center;
          height: 70px;
          padding: 10px;



      }
      th {
        height: 70px
      }

      td:not(:first-child),
      th:not(:first-child) {
          border-right: 2px solid grey;
      }

      td:first-child,
      th:first-child {
          border-left: 2px solid black
      }

      td:last-child,
      th:last-child {
          border-right: 2px solid black
      }


      td:not(:nth-child(1), :nth-child(2)){
          background-color: rgba(212, 212, 212, 0.5);
      }
      td:not(:nth-child(1), :nth-child(2), :nth-child(odd)){
          background-color: rgba(176, 176, 176, 0.5);
      }

      div {
          position: fixed;
          height: 100%;
          width: 100%;
      }
  </style>
  <hmtl><body><table>"""
  anotherPage += "<tr><th></th><th>Team</th><th>Points</th><th>Games Won</th><th>OT Wins</th><th>Losses</th><th>OT Losses</th></tr>"
  x:ladderTeam
  for x in teamClassList:
    if  x.league == LeagueRequested:
        anotherPage += "<tr><td style=\"background-color: {}88;\"><img src=\"http://absolute/{}\"></td><td style=\"background-color: {}88;\">{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            f"#{x.team.colour.getHex()}",path.join(slapdir,"StreamingAssets",x.team.image.replace("/", "\\")), f"#{x.team.colour.getHex()}", x.team.teamName, x.points, x.Wins, x.otWins, x.Losses, x.otLosses)
  anotherPage += "</table></body></html>"

  writer = open(f"{out}\ladder.html", "w")
  writer.write(anotherPage)

  finap = open(f"{out}\general-stats.html", "w")
  finap.write(finalpage)