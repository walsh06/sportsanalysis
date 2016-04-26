headers = ['Pos','Team', 'Pld', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']

def printHeader(heading):
    print "============================"
    print heading
    print "============================"
def readCSV(filename):
    with open(filename) as f:
        contents = f.readlines()
    seasons = {}
    reading = False
    year = None
    currentSeason = []
    
    for line in contents:
        if "Year" in line:
            if currentSeason:
                seasons[year] = currentSeason
            year = line.split(",")[1]
            currentSeason = []
        else:
            currentSeason.append(line.split(','))
    seasons[year] = currentSeason
    return seasons
            
def getHighestPoints(seasons, writeToFile=False):
    idx = headers.index('Pts')
    winners = []
    for season in seasons:
        winners.append((season, seasons[season][0][1], seasons[season][0][idx]))
    sortedWinders = sorted(winners,  reverse=True, key=lambda tup: tup[2])
    printHeader("Highest Points")
    for winner in sortedWinders:
        print winner
    if writeToFile:
        with open("highestPoints.csv", "w") as f:
            for winner in sortedWinders:
                f.write("{}\n".format(",".join(winner)))

def getLowestPoints(seasons, writeToFile=False):
    idx = headers.index('Pts')
    losers = []
    for season in seasons:
        losers.append((season, seasons[season][19][1], seasons[season][19][idx]))
    sortedLosers = sorted(losers, key=lambda tup: tup[2])
    printHeader("Lowest Points")
    for loser in sortedLosers:
        print loser
    if writeToFile:
        with open("lowestPoints.csv", "w") as f:
            for losers in sortedLosers:
                f.write("{}\n".format(",".join(losers)))

def getLowestSurvivingPoints(seasons, writeToFile=False):
    idx = headers.index('Pts')
    survivors = []
    for season in seasons:
        surviveIdx = -5 if season == '1994' else -4
        survivors.append((season, seasons[season][surviveIdx][1], seasons[season][surviveIdx][idx]))
    sortedSurvivors = sorted(survivors, key=lambda tup: tup[2])
    printHeader("Lowest Surviving Points")
    for loser in sortedSurvivors:
        print loser
    if writeToFile:
        with open("lowestPoints.csv", "w") as f:
            for survivors in sortedSurvivors:
                f.write("{}\n".format(",".join(survivors)))

seasons = readCSV("premierleague.csv")
getHighestPoints(seasons)
getLowestPoints(seasons)
getLowestSurvivingPoints(seasons)