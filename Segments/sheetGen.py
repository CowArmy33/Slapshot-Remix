from Segments.scheduledGame import Team
from Segments.statPuller import Stat, StatPuller
import os
import shutil

homeKeyframeGenTemp = "homeKeyframeGen(\"{}%\",\"{}%\")"
awayKeyframeGenTemp = "awayKeyframeGen(\"{}%\",\"{}%\")"

mappedDictionary = {
    "passes": "Passes",
    "possession_time_sec": "Pos. (Sec)",
    "possession_percentage": "Pos. (%)",
    "takeaways": "Takeaways",
    "turnovers": "Turnovers",
    "score": "Score",
    "goals": "Goals",
    "goal_succ_rate": "Goal %",
    "shots": "Shots",
    "faceoffs_won": "Faceoffs",
    "saves": "Saves",
    "blocks": "Blocks",
    "post_hits": "P. hits",
    "assists": "Assists",
    "secondary_assists": "T. Goals",
    'has_mercy_ruled' :'Mercy',
    'turnovers' :'Turnovers',
    'shutouts':'Shutouts',
    'assists':'Assists',
    'overtime_goals':'OT Goals',
    'blocks':'Blocks',
    'conceded_goals':'Conc. Goals',
    'games_played':'Played',
    'losses':'Loss',
    'score':'Score',
    'passes':'Passes',
    'goals':'Goals',
    'faceoffs_won':'Faceoffs',
    'wins':'Wins',
    'overtime_losses':'OT Loss',
    'takeaways':'Takeaway',
    'ties':'Tie',
    'secondary_assists':'T. Goals',
    'shutouts_against':'Shutouts A.',
    'post_hits':'P. Hits',
    'contributed_goals':'Cont. Goals',
    'faceoffs_lost':'Faceoffs Lost',
    'was_mercy_ruled':'Mercied',
    'overtime_wins':'OT Win',
    'saves':'Save',
    'game_winning_goals':'GWG',
    'shots':'Shots',
    'primary_assists':'Duo Plays',
    'possession_time_sec':'Pos. (S)',
}


styleCSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

.bghome {
    height: 100%;
    width: 100%;
    background-color: blue;
    transform: skew(0);
    clip-path: polygon(10% 0%, 100% 0%, 100% 100%, 0% 100%);
    box-shadow: 0px 10px rgba(0, 0, 0, 0.777);
    display: flex;
}

.bgMid {
    transform: skew(0);
    height: 100%;
    width: 100%;
    background-color: black;
    display: flex;
}

.bgaway {
    height: 100%;
    width: 100%;
    background-color: red;
    clip-path: polygon(0 0, 90% 0, 100% 100%, 0% 100%);
    transform: skew(0);
    box-shadow: 0px 10px rgba(0, 0, 0, 0.777);
    display: flex;
}

.container {
    padding-left: 30px;
    margin-right: 0px;
    width: fit-content;
    height: fit-content;
    display: inline-block;
}

p {
    margin: 0;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Bebas Neue', Verdana, Geneva, Tahoma, sans-serif;
    color: white;
    text-shadow: 3px 3px black;
}


.center {
    margin-left: 50%;
    width: fit-content;
    height: fit-content;
    transform: translate(-50%);
}

th {
    width: auto;
    height: auto;
    padding-bottom: 1.5%;
    padding-left: .5%;
    padding-right: .5%;
    filter: drop-shadow(10px 10px 0px rgba(0, 0, 0, 0.777))
}

td {
    position: relative;
    width: auto;
    height: auto;
    padding-bottom: 1.5%;
    padding-left: .5%;
    padding-right: .5%;
    filter: drop-shadow(10px 10px 0px rgba(0, 0, 0, 0.777))
}

.home {
    padding-bottom: 1.5%;
    padding-left: .5%;
    padding-right: .5%;
}

table {
    width: 100%;
    height: 100%;
    padding: 1vh;
}

.bar-home {
    position: absolute;
    top: 0;
    left: 0;
    width: 0%;
    opacity: 0%;
    /* Start with 0% width */
    height: 100%;
    background-color: blue;
    /* Adjust the color as needed */
    z-index: -1;
    /* Send the bars behind the content */
    /*animation: expandLeft 2s ease;*/
    /* Animation for left to right */
    animation-fill-mode: forwards;
    text-align: right;
}

.bar-away {
    position: absolute;
    top: 0;
    right: 0;
    opacity: 0%;
    width: 0%;
    /* Start with 0% width */
    height: 100%;
    background-color: red;
    /* Adjust the color as needed */
    z-index: -1;
    /* Send the bars behind the content */
    /*animation: expandRight 2s ease;*/
    /* Animation for right to left */
    animation-fill-mode: forwards;
}
.homeT {
    position:relative;
    padding-right: 50px;
}
.awayT {
    position:relative;
    padding-left: 50px;
}

@keyframes expandLeft {
    0% {
        width: 0%;
        left: 100%;
        /* Start from the right edge */
    }

    100% {
        width: 95%;
        left: 3%;
        /* Fill towards the left */
    }
}

@keyframes expandRight {
    0% {
        width: 0%;
        right: 100%;
    }

    100% {
        width: 95%;
        right: 3%;
    }
}


"""



firstPart = '''
<link rel="stylesheet" href="style.css">

<script>
    function homeKeyframeGen(x, y) {{
        return [{{ width: "0%", left: "100%", opacity: "0%" }}, {{ width: x, left: y, opacity: "100%" }}]
    }}
    function awayKeyframeGen(x, y) {{
        return [{{ width: "0%", right: "100%", opacity: "0%" }}, {{ width: x, right: y, opacity: "100%" }}]
    }}
    // Define a function to scale the font size
    function scaleFontSize() {{
        // Get a reference to the table element
        var table = document.getElementById("myTable");

        // Calculate the number of rows in the table
        var numRows = table.rows.length;

        // Define the base font size and scaling factor
        var baseFontSize = 87; // Change this to your desired base font size
        var scalingFactor = 5; // Adjust this as needed

        // Calculate the new font size based on the number of rows
        var newFontSize = baseFontSize - (numRows * scalingFactor);

        // Select all <p> elements and set their font size to the calculated value
        var paragraphs = document.getElementsByTagName("p");
        for (var i = 0; i < paragraphs.length; i++) {{
            paragraphs[i].style.fontSize = newFontSize + "px";
        }}
        var bgmid = document.getElementsByClassName("bgMid");
        bgmid[0].clientHeight
        var barsL = document.getElementsByClassName("bar-home");
        var barsR = document.getElementsByClassName("bar-away");
        var waitTime = 0;
        var shrinkWrapFactor = 0.2
        var animationsH = [{homeAnimations}]
        var animationsA = [{awayAnimations}]

        for (var i = 0; i < barsL.length; i++) {{
            // Calculate the delay for each element
            var delay = i * 100; // 200 milliseconds delay for each i

            // Use setTimeout to schedule the animation with the calculated delay
            setTimeout(function (index) {{
                return function () {{
                    barsL[index].style.height = bgmid[0].getBoundingClientRect().height - shrinkWrapFactor * bgmid[0].getBoundingClientRect().height;
                    barsL[index].style.top = shrinkWrapFactor / 2 * bgmid[0].getBoundingClientRect().height;
                    barsR[index].style.height = bgmid[0].getBoundingClientRect().height - shrinkWrapFactor * bgmid[0].getBoundingClientRect().height;
                    barsR[index].style.top = shrinkWrapFactor / 2 * bgmid[0].getBoundingClientRect().height;
                    var animationH = animationsH[index];
                    var animationA = animationsA[index];
                    barsL[index].animate(animationH, {{ duration: 2000, iterations: 1, fill: "both", easing: "ease" }});
                    barsR[index].animate(animationA, {{ duration: 2000, iterations: 1, fill: "both", easing: "ease" }});
                }};
            }}(i), delay);
        }}
    }}

    // Call the scaleFontSize function when the document is fully loaded
    window.onload = scaleFontSize;
</script>


<body>
<table id="myTable">
'''







tableRowTemplate = """
    <tr>
        <td>
            <!-- home bar -->
            <div class="bar-home" style="background-color: rgba({hC}, {hT});"><p class="homeT">{hS}</p></div>
        </td>
        <td>
            <div class="bgMid" style="background-color: rgba(0, 0, 0, 0.65);"><p>{statN}</p></div>
        </td>
        <td class = "away">
            <!-- away bar -->
            <div class="bar-away" style="background-color: rgba({aC}, {aT});"><p class="awayT">{aS}</p></div>
        </td>
    </tr>
"""

lastPart = """
</table>
</body>
"""


def predY(x):
    return (x*-1) + .98
def filtX(x):
    x = x*.95
    if x < .20:
        x = .20
    return x

def hk(x):
    x = filtX(x)
    y = predY(x)
    return homeKeyframeGenTemp.format(x*100, y*100)
def ak(x):
    x = filtX(x)
    y = predY(x)
    return awayKeyframeGenTemp.format(x*100, y*100)
def trans(x):
    max =.85
    min = .4
    return x*(max - min) + min





def makeStats(stats: dict, homeTeam: Team, awayTeam: Team, dest: str):
    "Takes the stats made by a statPuller, the home team, and away team, followed by the destination, where an HTML file will be output containing the statistics needed"
    firstRow = f"""
            <tr>
            <th>
                <div class="bghome" style="background-color: rgba({homeTeam.colour.R},{homeTeam.colour.G},{homeTeam.colour.B});">
                    <p>{homeTeam.teamName}</p>
                </div>
            </th>
            <th style="width: 15%;">
                <div class="bgMid">
                    <p>Stat</p>
                </div>
            </th>
            <th>
                <div class="bgaway" style="background-color: rgba({awayTeam.colour.R},{awayTeam.colour.G},{awayTeam.colour.B});">
                    <p>{awayTeam.teamName}</p>
                </div>
            </th>
        </tr>
        """
    
    hAnims = []
    aAnims = []
    tableRows = [firstRow]
    def addStat(s: Stat):
        biggest = max(s.statHomeScore, s.statAwayScore)
        if biggest != 0:
            hS = s.statHomeScore/biggest
            aS = s.statAwayScore/biggest
            print(hS,aS)
            hAnims.append(hk(hS))
            aAnims.append(ak(aS))
            tableRows.append(tableRowTemplate.format(
                hS=s.statHomeScore, aS=s.statAwayScore, statN=mappedDictionary[s.statName], hC=f"{homeTeam.colour.R},{homeTeam.colour.G},{homeTeam.colour.B}", hT=trans(hS), aC=f"{awayTeam.colour.R},{awayTeam.colour.G},{awayTeam.colour.B}", aT=trans(aS)))
        
    for stat in stats.values():
        addStat(stat)
    
    hAnimsStr = ""
    for x in hAnims[:-1]:
        hAnimsStr += f"{x},"
    hAnimsStr += hAnims[-1]
    
    aAnimsStr = ""
    for x in aAnims[:-1]:
        aAnimsStr += f"{x},"
    aAnimsStr += aAnims[-1]

    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
    if not os.path.exists(f"{dest}\\style.css"):
        with open(f"{dest}\\style.css", "w") as f:
            f.write(styleCSS)

    with open(f"{dest}\\board.html", "w") as f:
        f.write(firstPart.format(homeAnimations = hAnimsStr, awayAnimations = aAnimsStr))
        for row in tableRows:
            f.write(row)
        f.write(lastPart)