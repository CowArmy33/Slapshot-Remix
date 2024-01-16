import os
import shutil
from Segments.scheduledGame import Colour, Team
from PIL import Image


def generate_gradient(
        colour1: tuple[int, int, int], colour2: tuple[int, int, int], width: int, height: int) -> Image:
    """Generate a vertical gradient."""
    base = Image.new('RGB', (width, height), colour1)
    top = Image.new('RGB', (width, height), colour2)
    mask = Image.new('L', (width, height))
    mask_data = []

    one_line = []
    for x in range(width):
        level = int((x /width) * 255)
        one_line.append(level)
    for x in range(height):
        mask_data.extend(one_line)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def setTeam(team: Team, path: str, colour, gamedir):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    img = Image.new("RGB", (1, 1), colour)
    logo = os.path.normpath(os.path.join(gamedir,"StreamingAssets",team.image))
    print("===============",logo)
    players = team.players
    print(f'{path}\\logo{path[-4:]}.png')
    if os.path.exists(logo):
        print(1)
        shutil.copyfile(logo, f'{path}\\logo{path[-4:]}.png')
    elif os.path.exists(f'{path}\\logo{path[-4:]}.png'):
        print(2)
        os.remove(f'{path}\\logo{path[-4:]}.png')
    if players != None:
        with open(f'{path}\\players{path[-4:]}.txt', 'w') as file:
            for x in players[:-1]:
                file.write(x + "\n")
            file.write(players[-1])
    else:
        with open(f'{path}\\players{path[-4:]}.txt', 'w') as file:
            file.write("")
    img.save(f'{path}\\colour{path[-4:]}.png', "png")
    with open(f'{path}\\name{path[-4:]}.txt', 'w') as file:
        file.write(team.teamName)
    with open(f'{path}\\accro{path[-4:]}.txt', 'w') as file:
        file.write(team.accronym)
    

def setTeams(team1: Team, team2: Team, basePath: str, gamedir:str):
    homePath = basePath + "\\Home"
    awayPath = basePath + "\\Away"
    gradientPath = basePath + "\\NonTeam"
    c1, c2 = team1.colour.getRGB(), team2.colour.getRGB()
    if not os.path.exists(gradientPath):
        os.makedirs(gradientPath, exist_ok=True)
    setTeam(team1, homePath, c1, gamedir)
    setTeam(team2, awayPath, c2, gamedir)

    baseImg = generate_gradient(c1, c2, 1920, 1080)
    baseImg.save(gradientPath + "\\gradient.png", "png")
