from scheduledGame import Team
from statPuller import Stat, StatPuller

homeKeyframeGenTemp = "homeKeyframeGen(\"{}%\",\"{}%\")"
awayKeyframeGenTemp = "awayKeyframeGen(\"{}%\",\"{}%\")"

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




s = StatPuller(
    r"G:\Program Files\Steam\steamapps\common\SlapshotRebound\Slapshot_Data\\").getStats(["shots", "saves", "goal_succ_rate", "passes", "post_hits", "possession_time_sec"])



def makeStats(stats: dict, homeTeam: Team, awayTeam: Team, dest: str):
    "Takes the stats made by a statPuller, the home team, and away team, followed by the destination, where an HTML file will be output containing the statistics needed"
    firstRow = f"""
            <tr>
            <th>
                <div class="bghome" style="background-color: rgba({homeTeam.colour[0]},{homeTeam.colour[1]},{homeTeam.colour[2]});">
                    <p>{homeTeam.teamName}</p>
                </div>
            </th>
            <th style="width: 15%;">
                <div class="bgMid">
                    <p>Stat</p>
                </div>
            </th>
            <th>
                <div class="bgaway" style="background-color: rgba({awayTeam.colour[0]},{awayTeam.colour[1]},{awayTeam.colour[2]});">
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
        hS = s.statHomeScore/biggest
        aS = s.statAwayScore/biggest
        print(hS,aS)
        hAnims.append(hk(hS))
        aAnims.append(ak(aS))
        tableRows.append(tableRowTemplate.format(
            hS=s.statHomeScore, aS=s.statAwayScore, statN=s.statName, hC=f"{homeTeam.colour[0]},{homeTeam.colour[1]},{homeTeam.colour[2]}", hT=trans(hS), aC=f"{awayTeam.colour[0]},{awayTeam.colour[1]},{awayTeam.colour[2]}", aT=trans(aS)))
        
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

    with open(dest, "w") as f:
        f.write(firstPart.format(homeAnimations = hAnimsStr, awayAnimations = aAnimsStr))
        for row in tableRows:
            f.write(row)
        f.write(lastPart)

hT = Team("Homelanders", 111, (255, 100, 0))
aT = Team("Away Squad", 111, (0, 100, 255))

makeStats(s, hT, aT, r"H:\!Personal Projects\Slap Streaming Toll Python Port\HTML Templates\export.html")
