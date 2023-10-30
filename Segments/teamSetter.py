import os
import shutil
from scheduledGame import Colour, Team, getValidColours
from PIL import Image, ImageDraw


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


def setTeam(team: Team, path: str, colour):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    img = Image.new("RGB", (1, 1), colour)
    logo = team.image
    players = team.players
    shutil.copyfile(logo, f'{path}\\logo{path[-4:]}.png')
    with open(f'{path}\\players{path[-4:]}.txt', 'w') as file:
        for x in players[:-1]:
            file.write(x + "\n")
        file.write(players[-1])
    img.save(f'{path}\\colour{path[-4:]}.png', "png")
    with open(f'{path}\\name{path[-4:]}.txt', 'w') as file:
        file.write(team.teamName)
    with open(f'{path}\\accro{path[-4:]}.txt', 'w') as file:
        file.write(team.accronym)
    

def setTeams(team1: Team, team2: Team, basePath: str):
    homePath = basePath + "\\Home"
    awayPath = basePath + "\\Away"
    gradientPath = basePath + "\\NonTeam"
    c1,c2 = team1.colour, team2.colour
    c1,c2 = getValidColours(c1,c2)
    c1,c2 = c1.getRGB(), c2.getRGB()
    if not os.path.exists(gradientPath):
        os.makedirs(gradientPath, exist_ok=True)
    setTeam(team1, homePath, c1)
    setTeam(team2, awayPath, c2)

    baseImg = generate_gradient(c1, c2, 1920, 1080)
    baseImg.save(gradientPath + "\\gradient.png", "png")