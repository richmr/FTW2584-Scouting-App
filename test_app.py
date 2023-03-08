import unittest

from dataload import initGame_Modes, initPossible_Actions, initTeams
from appdata import appdata
from datamodels import Game_Modes, Possible_Actions, Teams

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        # Setup the database
        appdata('sqlite://')

    def test_game_modes(self):
        # first load them
        loaded_modes = initGame_Modes()
        # check whats there
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Game_Modes).count()
            self.assertEqual(total, loaded_modes)

    def test_actions(self):
        loaded_actions = initPossible_Actions()
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Possible_Actions).count()
            self.assertEqual(total, loaded_actions)

    def test_teams(self):
        loaded_teams = initTeams()
        with appdata.getSQLSession() as dbsession:
            total = dbsession.query(Teams).count()
            self.assertEqual(total, loaded_teams)
    
if __name__ == '__main__':
    unittest.main()