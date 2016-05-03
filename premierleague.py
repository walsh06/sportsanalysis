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

def getPointsDifference(seasons, writeToFile=False):
    year = 2015
    result = {}
    while year > 1992:
        currentSeason = []
        for team in seasons[str(year)]:
            name = team[1].replace('(Q)', '').replace('(C)', '').replace('(R)', '').replace('(X)', '').strip()
            for prevTeam in seasons[str(year - 1)]:
                prevName = prevTeam[1].replace('(Q)', '').replace('(C)', '').replace('(R)', '').replace('(X)', '').strip()
                if name == prevName:
                    currentSeason.append((name, str(int(prevTeam[0]) - int(team[0])), team[0], prevTeam[0]))
        result[str(year)] = currentSeason
        year -= 1
    allDiffs = []
    for season in result:
        for team in result[season]:
            allDiffs.append((season, team[0], team[1], team[2], team[3]))
    sortedDiffs = sorted(allDiffs,  reverse=True, key=lambda tup: int(tup[2]))
    printHeader("Position Difference between Seasons")
    for diff in sortedDiffs:
        print diff
    if writeToFile:
        with open("pointsDiff.csv", "w") as f:
            for diff in sortedDiffs:
                f.write("{}\n".format(",".join(diff)))
               
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
                f.write("{}".format(",".join(winner)))

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
                f.write("{}".format(",".join(losers)))

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
        with open("lowestSurvivingPoints.csv", "w") as f:
            for survivors in sortedSurvivors:
                f.write("{}".format(",".join(survivors)))

seasons = readCSV("premierleague.csv")
#getHighestPoints(seasons)
#getLowestPoints(seasons)
#getLowestSurvivingPoints(seasons)
getPointsDifference(seasons, True)