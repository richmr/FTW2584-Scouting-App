import unittest
from pprint import pprint
import os

from dataload import initGame_Modes, initPossible_Actions, initTeams, initMatches
from appdata import appdata
from datamodels import Game_Modes, Possible_Actions, Teams, Matches, Observed_Actions
from appsecrets import sqlAConnectionString

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        # Setup the database 
        appdata(sqlAConnectionString)

    def test_1_game_modes(self):
        # first load them
        loaded_modes = initGame_Modes()
        # check whats there
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Game_Modes).count()
            self.assertEqual(total, loaded_modes)

    def test_2_actions(self):
        loaded_actions = initPossible_Actions()
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Possible_Actions).count()
            self.assertEqual(total, loaded_actions)

    def test_3_teams(self):
        loaded_teams = initTeams()
        self.loaded_team_count = loaded_teams
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Teams).count()
            self.assertEqual(total, loaded_teams)

            # specific check
            result = dbsession.query(Teams).filter_by(team_number = 2584).one()
            self.assertEqual(result.team_name, "Flame of The West")

    def test_4_persistence(self):
        with appdata.getSQLSession() as dbsession:
            team_count = dbsession.query(Teams).count()
            self.assertEqual(team_count, 44)

    def test_5_match(self):
        loaded_matches = initMatches()
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Matches).count()
            self.assertEqual(total, loaded_matches)

    def test_6_actions(self):
        obs_action = [
            {
                "matchID":2,
                "mode_name":"Auton",
                "team_number":2584,
                "action_label":"scored_cone",
                "count_seen": 1
            },
            {
                "matchID":2,
                "mode_name":"Tele",
                "team_number":2584,
                "action_label":"scored_cube",
                "count_seen":2
            },
            # {
            #     "matchID": 2,
            #     "mode_name": "Tele",
            #     "team_number": 2584,
            #     "action_label": "scored_cube"
            # },
            {
                "matchID": 2,
                "mode_name": "Tele",
                "team_number": 2584,
                "action_label": "balanced_charging_station"
            },
            {
                "matchID": 2,
                "mode_name": "Tele",
                "team_number": 6658,
                "action_label": "robot_broke"
            },
            {
                "matchID": 2,
                "mode_name": "Tele",
                "team_number": 8020,
                "action_label": "scored_cube",
                "count_seen":4
            },
            # {
            #     "matchID": 2,
            #     "mode_name": "Tele",
            #     "team_number": 8020,
            #     "action_label": "scored_cube"
            # },
            # {
            #     "matchID": 2,
            #     "mode_name": "Tele",
            #     "team_number": 8020,
            #     "action_label": "scored_cube"
            # },
            # {
            #     "matchID": 2,
            #     "mode_name": "Tele",
            #     "team_number": 8020,
            #     "action_label": "scored_cube"
            # },
            {
                "matchID": 3,
                "mode_name": "Auton",
                "team_number": 2584,
                "action_label": "scored_cone"
            },
            {
                "matchID": 3,
                "mode_name": "Tele",
                "team_number": 2584,
                "action_label": "scored_cube",
                "count_seen": 2
            },
            # {
            #     "matchID": 3,
            #     "mode_name": "Tele",
            #     "team_number": 2584,
            #     "action_label": "scored_cube"
            # },
            {
                "matchID": 1,
                "mode_name": "Tele",
                "team_number": 2584,
                "action_label": "balanced_charging_station"
            },
        ]
        with appdata.getSQLSession() as dbsession:
            for act in obs_action:
                dbsession.add(Observed_Actions().fromDict(act))
            dbsession.commit()
            # What do we have
            res = dbsession.query(Observed_Actions)
            headers = ["matchID", "mode_name", "team_number", "action_label", "action_timestamp"]
            datalist = []
            for row in res:
                thisdata = []
                for field in headers:
                    thisdata.append(getattr(row, field))
                datalist.append(thisdata)
            self.assertTrue(True)
            
    def test_7_team_game_actions(self):
        with appdata.getSQLSession() as dbsession:
            res = dbsession.query(Teams).filter_by(team_number = 2584).one()
            # for item in res.team_game_actions:
            #     pprint(item.__dict__)

        self.assertTrue(True)

if __name__ == '__main__':
    # delete old database
    try:
        os.remove('testdata.db')
    except:
        pass
    unittest.main()
