import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc
from IPython.display import display

def flipY(y):
    return (422.5 - y) + 422.5
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()
        
    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    ohoop = Circle((0, flipY(0)), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
    obackboard = Rectangle((-30, flipY(-7.5)), 60, 1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    oouter_box = Rectangle((-80, flipY(-47.5)), 160, -190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)
    oinner_box = Rectangle((-60, flipY(-47.5)), 120, -190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    otop_free_throw = Arc((0, flipY(142.5)), 120, -120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    obottom_free_throw = Arc((0, flipY(142.5)), 120, -120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    orestricted = Arc((0, flipY(0)), 80, -80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    ocorner_three_a = Rectangle((-220, flipY(-47.5)), 0, -140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    ocorner_three_b = Rectangle((220, flipY(-47.5)), 0, -140, linewidth=lw, color=color)

    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    othree_arc = Arc((0, flipY(0)), 475, -475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    ocenter_outer_arc = Arc((0, flipY(422.5)), 120, -120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    ocenter_inner_arc = Arc((0, flipY(422.5)), 40, -40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc, ohoop, obackboard, oouter_box, oinner_box, otop_free_throw,
                      obottom_free_throw, orestricted, ocorner_three_a,
                      ocorner_three_b, othree_arc, ocenter_outer_arc,
                      ocenter_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        oouter_lines = Rectangle((-250, flipY(-47.5)), 500, -470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)
        court_elements.append(oouter_lines)


    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def combineHeadersAndData(headers, data):
    result = []
    for item in data:
        itemDict = {}
        for idx, value in enumerate(headers):
            itemDict[value] = item[idx]
        result.append(itemDict)
    return result

def getAllPlayers(season):
    playersDict = {}
    url = 'http://stats.nba.com/stats/commonallplayers?Season={}&isOnlyCurrentSeason=1&LeagueID=00'
    print "Querying {}".format(url.format(season))
    response = requests.get(url.format(season))
    headers = response.json()['resultSets'][0]['headers']
    players = response.json()['resultSets'][0]['rowSet']
    return combineHeadersAndData(headers, players)

def getPlayerByName(players, name):
    for player in players:
        if name.lower() == player['DISPLAY_FIRST_LAST'].lower():
            return player
    return []

def getShootingData(id,season):
    shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS={season}&ContextFilter='\
                    '&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID='\
                    '00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust='\
                    'N&PerMode=PerGame&Period=0&PlayerID={id}&PlusMinus=N&Position=&Rank='\
                    'N&RookieYear=&Season={season}&SeasonSegment=&SeasonType=Regular+Season&TeamID='\
                    '0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'
    print "Querying {}".format(shot_chart_url.format(id=id, season=season))
    response = requests.get(shot_chart_url.format(id=id, season=season), timeout=20)
    headers = response.json()['resultSets'][0]['headers']
    shots = response.json()['resultSets'][0]['rowSet']
    return headers, shots

def drawShotChart(shot_df):
    with pd.option_context('display.max_columns', None):
        display(shot_df.head())
    sns.set_style("white")
    sns.set_color_codes()

    plt.figure(figsize=(8,16))
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    draw_court(outer_lines=True)
    # Descending values along the axis from left to right
    plt.xlim(300,-300)
    plt.ylim(-100, 950)
    plt.show()


season = "2015-16"

players = getAllPlayers(season)
# for player in players:
#     print player['DISPLAY_FIRST_LAST']
#     headers, shots = getShootingData(player['PERSON_ID'], season)
id = getPlayerByName(players, "Klay Thompson")['PERSON_ID']
headers, shots = getShootingData(id, season)
threes = []
for shot in shots:
    if shot[-5] > 29:
        threes.append(shot)
drawShotChart(pd.DataFrame(threes, columns=headers))
print len(threes)