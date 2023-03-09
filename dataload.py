
from appdata import appdata
from datamodels import Game_Modes, Possible_Actions, Teams


def initGame_Modes() -> int:
    """
    Returns the number of modes loaded (for testing)
    """
    modeList = [
        {"mode_name":"Setup"},
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

def initPossible_Actions() -> int:
    """
    returns the count of loaded actions
    """
    actionList = [
        {
            "action_label":"took_position_1",
            "applicable_mode":"Setup",
            "count_limit":1,
            "action_description":"Robot was setup in position 1",
        },
        {
            "action_label":"took_position_2",
            "applicable_mode":"Setup",
            "count_limit":1,
            "action_description":"Robot was setup in position 2",
        },
        {
            "action_label":"took_position_3",
            "applicable_mode":"Setup",
            "count_limit":1,
            "action_description":"Robot was setup in position 3",
        },
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
        {
            "action_label":"dropped_cone",
            "applicable_mode":"Any",
            "action_description":"Team dropped a held cone",
        },
        {
            "action_label":"dropped_cube",
            "applicable_mode":"Any",
            "action_description":"Team dropped a held cube",
        },
        {
            "action_label":"picked_up_cone_ground",
            "applicable_mode":"Any",
            "action_description":"Team picked a cone up off the ground",
        },
        {
            "action_label":"picked_up_cube_ground",
            "applicable_mode":"Any",
            "action_description":"Team picked a cube up off the ground",
        },
        {
            "action_label":"picked_up_cone_loading",
            "applicable_mode":"Any",
            "action_description":"Team picked up a cone from the loading zone",
        },
        {
            "action_label":"entered_charging_station",
            "applicable_mode":"Any",
            "action_description":"Team drove onto charging station",
        },
        {
            "action_label":"balanced_charging_station",
            "applicable_mode":"Any",
            "action_description":"Team successfully balanced the charging station",
        },
        {
            "action_label": "robot_broke",
            "applicable_mode": "Any",
            "action_description": "The robot stopped working during match",
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
        
        
    ]
    with appdata.getSQLSession() as dbsession:
        for action in actionList:
            newaction = Possible_Actions().fromDict(action)
            dbsession.add(newaction)
            dbsession.commit()
    return len(actionList)

def initTeams() -> int:
    """
    returns count of loaded teams
    """
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
        {'team_number':4964, 'team_name':'Rough Riders Robotics'},
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
        {'team_number':8898, 'team_name':'Royal Rebels Robotics'},
        {'team_number':9172, 'team_name':'Robo-sharks'},
    ]
    with appdata.getSQLSession() as dbsession:
        for team in teamList:
            newteam = Teams().fromDict(team)
            dbsession.add(newteam)
        dbsession.commit()
    return len(teamList)
