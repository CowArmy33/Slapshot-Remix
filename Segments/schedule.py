from Segments.scheduledGame import Game
import os
def createSchedule(games: list, dir: str, rootdir):
    websiteFirstHalf = """
    <html>

    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
            tr {
                opacity: 0;
                /* Set initial opacity to 0 */
                transform: translateX(-100%);
                /* Move the elements off-screen to the left */
                transition: opacity 1s ease, transform 1s ease;
                /* Define the transition properties */
                background-color: black;
            }

            td {
                font-family: 'Century Gothic';
                font-size: 60;
                color: white;
                margin: 0px;
                text-align: center;
                padding: 15px;
            }
            img {
                max-width: 0;
                max-height: 0;
            }
            table {
                width: 100%;
                height: 100%;
                border-collapse: collapse;
            }
        </style>
    </head>

    <body>
        <table id="table">
    """


    websiteSecondHalf = """
       </table>

        <script>

            function main() {
                calculateAverageRowHeight()
                slideIn()

            }

            function slideIn() {
                var rows = document.querySelectorAll('#table tr');

                rows.forEach(function (row, index) {
                    // Set a delay for each row
                    setTimeout(function () {
                        row.style.backgroundColor = index % 2 === 0 ? 'rgba(0, 0, 0, 0.85)' : 'rgba(0, 0, 0, 0.8)'; // Alternating opacity
                        row.style.opacity = 1; // Animating Opacity
                        row.style.transform = 'translateX(0)';
                    }, index * 200);
                });
            }

            function calculateAverageRowHeight() {
                    var table = document.getElementById('table');
                    var rows = table.getElementsByTagName('td');

                    var height = rows[0].getBoundingClientRect().height;
                    var totalWidth = 0;
                    var fontSize = Math.min(height / 3, 70); // Adjust as needed

                    for (var i = 0; i < rows.length; i++) {
                        rows[i].style.fontSize = fontSize + 'px';
                    }

                    maxSize = height * .7
                var images = table.getElementsByTagName("img");
                for (let index = 0; index < images.length; index++) {
                    images[index].style.maxHeight = maxSize + "px";
                    images[index].style.maxWidth = maxSize + "px";
                }
                }

            // Call the slideIn function after the page loads
            window.onload = main;
        </script>
    </body>

    </html>
    """

    tableRowTemplate = """
            <tr>
                <td>{league}</td>
                <td><img src="{hLogo}" ></td>
                <td>{hName}</td>
                <td>-</td>
                <td>{aName}</td>
                <td><img src="{aLogo}" ></td>
                <td>{time}</td>
            </tr>
    """

    schedule = websiteFirstHalf
    for g in games:
        g: Game
        
        leg = g.homeTeam.league
        if leg == "Intermediate":
            leg = "IM"
        
        leg = leg.upper()

        line = tableRowTemplate.format(
            league= leg,
            hLogo= "http://absolute/" +os.path.normpath(os.path.join(rootdir,"StreamingAssets" ,g.homeTeam.image)),
            aLogo= "http://absolute/" +os.path.normpath(os.path.join(rootdir,"StreamingAssets",g.awayTeam.image)),
            aName= g.awayTeam.teamName,
            hName= g.homeTeam.teamName,
            time= g.getTime()
        )
        schedule += line
    schedule += websiteSecondHalf
    with open(os.path.join(dir, "schedule.html"), "w") as f :
        f.write(schedule)