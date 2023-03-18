

from appdata import appdata
from datamodels import Game_Modes, Possible_Actions, Teams, Matches
from appsecrets import sqlAConnectionString

def loadGame_Modes() -> int:
    """
    Returns the number of modes loaded (for testing)
    """
    modeList = [
        {"mode_name":"Auton"},
        {"mode_name":"Tele"},
        {"mode_name":"Any"}
    ]
    with appdata.getSQLSession() as dbsession:
        for mode in modeList:
            newmode = Game_Modes().fromDict(mode)
            dbsession.add(newmode)
            dbsession.commit()
        
    return len(modeList)


def loadTeams():
    teamList = [
        {'team_number':207, 'team_name':'METALCRAFTERS'},
        {'team_number':294, 'team_name':'Beach Cities Robotics'},
        {'team_number':597, 'team_name':'The Wolverines'},
        {'team_number':606, 'team_name':'Cyber Eagles'},
        {'team_number':687, 'team_name':'The Nerd Herd'},
        {'team_number':702, 'team_name':'Bagel Bytes'},
        {'team_number':846, 'team_name':'The Funky Monkeys'},
        {'team_number':980, 'team_name':'ThunderBots'},
        {'team_number':1148, 'team_name':'Harvard Westlake Robotics'},
        {'team_number':1159, 'team_name':'Ramona Rampage'},
        {'team_number':1197, 'team_name':'TorBots'},
        {'team_number':1452, 'team_name':'Omnicats'},
        {'team_number':1515, 'team_name':'MorTorq'},
        {'team_number':1661, 'team_name':'Griffitrons'},
        {'team_number':1759, 'team_name':'Potatoes'},
        {'team_number':2584, 'team_name':'Flame of The West'},
        {'team_number':2710, 'team_name':'JetStream 2710'},
        {'team_number':3408, 'team_name':'cyberCubs'},
        {'team_number':3473, 'team_name':'Team Sprocket'},
        {'team_number':3863, 'team_name':'Pantherbotics'},
        {'team_number':3952, 'team_name':'Troy Robotics'},
        {'team_number':4123, 'team_name':'Tribe Robotics'},
        {'team_number':4201, 'team_name':'The Vitruvian Bots'},
        {'team_number':4470, 'team_name':'TiGears'},
        {'team_number':4501, 'team_name':'Humans'},
        {'team_number':4964, 'team_name':'Roosevelt Robotics'},
        {'team_number':4999, 'team_name':'Momentum'},
        {'team_number':5089, 'team_name':'Robo-Nerds'},
        {'team_number':5124, 'team_name':'West Torrance Robotics'},
        {'team_number':5199, 'team_name':'Robot Dolphins From Outer Space'},
        {'team_number':5500, 'team_name':'Jaguars Robotics & ROVs'},
        {'team_number':5669, 'team_name':'Techmen'},
        {'team_number':5857, 'team_name':'Walnut Valley Robotics'},
        {'team_number':6000, 'team_name':'Firehawk Robotics'},
        {'team_number':6658, 'team_name':'Rockbotics'},
        {'team_number':6833, 'team_name':'Phoenix Robotics'},
        {'team_number':6904, 'team_name':'TeraWatts'},
        {'team_number':7185, 'team_name':'TartanBots'},
        {'team_number':7230, 'team_name':'Mythic Mechanix'},
        {'team_number':7611, 'team_name':'AMAL HAWKS'},
        {'team_number':8020, 'team_name':'CyberpunK'},
        {'team_number':8600, 'team_name':'Kernel Panic'},
        {'team_number':8898, 'team_name':'Royal Rebel Robotics'},
        {'team_number':9172, 'team_name':'Robo-sharks'},
    ]

    with appdata.getSQLSession() as dbsession:
        for team in teamList:
            newteam = Teams().fromDict(team)
            dbsession.add(newteam)
        dbsession.commit()
    return len(teamList)

def loadMatches():
    matchList = [
        'Qualification 1,1515,5669,4470,4999,3952,1759',
        'Qualification 2,597,2710,294,846,702,5857',
        'Qualification 3,5089,1159,7611,6833,1148,5500',
        'Qualification 4,6904,3863,4964,5124,207,6000',
        'Qualification 5,8600,7185,1197,606,687,2584',
        'Qualification 6,1661,8898,8020,6658,5199,4501',
        'Qualification 7,3408,7230,4201,4123,9172,1452',
        'Qualification 8,5500,7611,980,3473,4999,846',
        'Qualification 9,5089,6904,597,1515,1759,3863',
        'Qualification 10,4964,6833,606,2710,4470,687',
        'Qualification 11,5199,294,7185,4501,5669,5124',
        'Qualification 12,207,8600,5857,4201,1197,6658',
        'Qualification 13,1452,2584,1661,8898,1148,1159',
        'Qualification 14,7230,702,3952,3473,980,3408',
        'Qualification 15,6833,4123,8020,9172,6000,6904',
        'Qualification 16,5669,7185,597,4501,5089,2710',
        'Qualification 17,846,4201,207,7611,3863,606',
        'Qualification 18,5199,5124,5857,4470,2584,8898',
        'Qualification 19,4999,7230,1661,687,1452,3408',
        'Qualification 20,6658,980,8020,9172,1197,294',
        'Qualification 21,702,1515,3473,4123,1148,4964',
        'Qualification 22,5500,3952,6000,8600,1759,1159',
        'Qualification 23,5669,4201,8898,6833,846,5124',
        'Qualification 24,3863,5199,5089,3408,5857,4999',
        'Qualification 25,4470,7611,9172,597,2584,1197',
        'Qualification 26,1661,702,980,687,6904,1515',
        'Qualification 27,4964,6658,3473,1452,3952,1159',
        'Qualification 28,294,6000,4123,7185,5500,606',
        'Qualification 29,8020,4501,1148,2710,8600,7230',
        'Qualification 30,207,3408,9172,1759,5669,5857',
        'Qualification 31,6904,846,980,5199,1661,6833',
        'Qualification 32,4999,4470,5124,1159,6658,702',
        'Qualification 33,6000,3473,8898,687,5089,4201',
        'Qualification 34,3952,8600,294,7611,2584,7230',
        'Qualification 35,1197,1759,4964,4123,597,4501',
        'Qualification 36,1452,1515,5500,8020,7185,3863',
        'Qualification 37,606,207,4999,1148,2710,5124',
        'Qualification 38,8898,687,702,5669,9172,846',
        'Qualification 39,3408,1159,2584,6904,4201,294',
        'Qualification 40,6833,6658,8600,5857,4964,597',
        'Qualification 41,3863,4501,4470,7185,3473,7611',
        'Qualification 42,7230,1515,4123,1197,5500,207',
        'Qualification 43,2710,6000,1759,980,1452,5199',
        'Qualification 44,1148,1661,5089,3952,606,8020',
        'Qualification 45,294,3408,846,9172,4964,4999',
        'Qualification 46,3863,1159,6833,8600,702,5669',
        'Qualification 47,5857,687,7611,5500,5124,4123',
        'Qualification 48,6000,6658,1452,2584,4501,1515',
        'Qualification 49,3473,597,3952,8020,207,5199',
        'Qualification 50,4201,1148,606,7185,980,1759',
        'Qualification 51,6904,8898,2710,7230,1197,4470',
        'Qualification 52,5089,5124,9172,1661,4123,8600',
        'Qualification 53,702,6833,4501,3408,5500,6658',
        'Qualification 54,6000,8020,687,597,1452,207',
        'Qualification 55,1159,606,5669,7611,5199,1515',
        'Qualification 56,5857,7185,6904,980,8898,3952',
        'Qualification 57,1759,5089,2584,846,4964,7230',
        'Qualification 58,2710,4999,1197,3473,4201,1661',
        'Qualification 59,687,3863,1148,4470,294,6658',
        'Qualification 60,5124,7611,8600,1515,8020,3408',
        'Qualification 61,4501,5857,1452,606,6904,702',
        'Qualification 62,1159,597,846,8898,7230,7185',
        'Qualification 63,5199,3952,9172,4201,2710,5500',
        'Qualification 64,2584,3863,4123,5089,980,4999',
        'Qualification 65,1197,3473,1148,5669,6000,4964',
        'Qualification 66,1759,4470,6833,207,294,1661',
        'Qualification 67,4501,846,687,1515,5857,1159',
        'Qualification 68,6658,606,2710,7611,3408,6904',
        'Qualification 69,2584,4201,7185,702,8020,597',
        'Qualification 70,1148,4999,5199,8600,9172,3863',
        'Qualification 71,207,4123,3473,294,8898,1759',
        'Qualification 72,7230,5500,5669,4470,1661,6000',
        'Qualification 73,5124,1452,1197,3952,6833,5089',
        'Qualification 74,980,597,4201,4964,4501,7611',
    ]

    with appdata.getSQLSession() as dbsession:
        keys = ["match_name", "red_1", "red_2", "red_3", "blue_1", "blue_2", "blue_3"]    
        for m in matchList:
            values = m.split(",")
            match_dict = dict(zip(keys, values))
            newMatch = Matches().fromDict(match_dict)
            dbsession.add(newMatch)
        dbsession.commit()
    return len(matchList)

def loadPossible_Actions() -> int:
    """
    returns the count of loaded actions
    """
    actionList = [
        # Big ideas here..  didn't get them implemented..
        # {
        #     "action_label":"took_position_1",
        #     "applicable_mode":"Setup",
        #     "count_limit":1,
        #     "action_description":"Robot was setup in position 1",
        # },
        # {
        #     "action_label":"took_position_2",
        #     "applicable_mode":"Setup",
        #     "count_limit":1,
        #     "action_description":"Robot was setup in position 2",
        # },
        # {
        #     "action_label":"took_position_3",
        #     "applicable_mode":"Setup",
        #     "count_limit":1,
        #     "action_description":"Robot was setup in position 3",
        # },
        {
            "action_label":"scored_cone_top",
            "applicable_mode":"Any",
            "action_description":"Team scored a cone in a top position",
        },
        {
            "action_label":"scored_cone_middle",
            "applicable_mode":"Any",
            "action_description":"Team scored a cone in a middle position",
        },
        {
            "action_label":"scored_cone_hybrid",
            "applicable_mode":"Any",
            "action_description":"Team scored a cone in a hybrid position",
        },
        {
            "action_label":"scored_cube_top",
            "applicable_mode":"Any",
            "action_description":"Team scored a cube in a top position",
        },
        {
            "action_label":"scored_cone_middle",
            "applicable_mode":"Any",
            "action_description":"Team scored a cone in a middle position",
        },
        {
            "action_label":"scored_cone_hybrid",
            "applicable_mode":"Any",
            "action_description":"Team scored a cone in a hybrid position",
        },
        # {
        #     "action_label":"dropped_cone",
        #     "applicable_mode":"Any",
        #     "action_description":"Team dropped a held cone",
        # },
        # {
        #     "action_label":"dropped_cube",
        #     "applicable_mode":"Any",
        #     "action_description":"Team dropped a held cube",
        # },
        # {
        #     "action_label":"picked_up_cone_ground",
        #     "applicable_mode":"Any",
        #     "action_description":"Team picked a cone up off the ground",
        # },
        # {
        #     "action_label":"picked_up_cube_ground",
        #     "applicable_mode":"Any",
        #     "action_description":"Team picked a cube up off the ground",
        # },
        # {
        #     "action_label":"picked_up_cone_loading",
        #     "applicable_mode":"Any",
        #     "action_description":"Team picked up a cone from the loading zone",
        # },
        {
            "action_label":"entered_charging_station",
            "applicable_mode":"Any",
            "action_description":"Team drove onto charging station in attempt to balance",
        },
        {
            "action_label":"balanced_charging_station",
            "applicable_mode":"Any",
            "action_description":"Team successfully balanced the charging station",
        },
        {
            "action_label": "robot_broke",
            "applicable_mode": "Any",
            "action_description": "The robot stopped working during match (or didn't show)",
        },
        {
            "action_label": "scored_cone",
            "applicable_mode": "Any",
            "action_description": "Team scored a cone (any position)",
        },
        {
            "action_label": "scored_cube",
            "applicable_mode": "Any",
            "action_description": "Team scored a cube (any position)",
        },
        {
            "action_label": "team_competed",
            "applicable_mode": "Any",
            "action_description": "Team was part of this match",
        },
        {
            "action_label":"mobility",
            "applicable_mode":"Auton",
            "action_description": "Team scored mobility points during Auton"
        }
        
    ]
    with appdata.getSQLSession() as dbsession:
        for action in actionList:
            newaction = Possible_Actions().fromDict(action)
            dbsession.add(newaction)
            dbsession.commit()
    return len(actionList)


if __name__ == "__main__":
    appdata(sqlAConnectionString)
    loadGame_Modes()
    loadTeams()
    loadPossible_Actions()
    loadMatches()

