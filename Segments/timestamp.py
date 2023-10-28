from datetime import datetime
def getTime(hour, minute): 
    now = datetime.now()
    a = datetime(now.year, now.month, now.day, hour, minute, 0)
    return int(a.timestamp())
def getRelative(hour, minute):
    "Will return timestamp in relative format aka :R"
    return f"<t:{getTime(hour, minute)}:R>"
def getStamp(hour, minute):
    "Will return timestamp in normal format aka :f"
    return f"<t:{getTime(hour, minute)}:t>"