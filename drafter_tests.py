import unittest
import unittest.mock as mock
from contextlib import redirect_stdout
from io import StringIO

from drafter import modifyJson


class TestModifyJson(unittest.TestCase):

    def test_modifyJson(self):
        player_scores = {
            "player1": 5.1,
            "player2": 5,
            "player3": 6,
            "player4": 6,
            "player5": 11,
            "player6": 9,
            "player7": 12,
            "player8": 10
        }

        yaml_match_configuration = {
            "matches": [
                {
                    "_match number": 1,
                    "teams": [
                        {
                            "players": [
                                {"name": "player1 A"},
                                {"name": "player2"},
                            ]
                        },
                        {
                            "players": [
                                {"name": "player3"},
                                {"name": "player4 B"},
                            ]
                        }
                    ]
                }
            ]
        }

        with mock.patch('json.load', return_value=player_scores):
            f = StringIO()
            with redirect_stdout(f):
                modifyJson(yaml_match_configuration)

            output = f.getvalue().strip().split('\n')
            best_team1 = output[-2].split(': ')[-1]
            best_team2 = output[-1].split(': ')[-1]

            assert best_team1 == "['player3', 'player1 A']"
            assert best_team2 == "['player4 B', 'player2']"


    def test_modifyJson_with_forced_teams(self):
        player_scores = {
            "player1": 5,
            "player2": 5,
            "player3": 6,
            "player4": 6,
            "player5": 11,
            "player6": 9,
            "player7": 12,
            "player8": 10
        }

        yaml_match_configuration = {
            "matches": [
                {
                    "_match number": 1,
                    "teams": [
                        {
                            "players": [
                                {"name": "player1 A"},
                                {"name": "player2 A"},
                            ]
                        },
                        {
                            "players": [
                                {"name": "player3"},
                                {"name": "player4 B"},
                            ]
                        }
                    ]
                }
            ]
        }

        with mock.patch('json.load', return_value=player_scores):
            f = StringIO()
            with redirect_stdout(f):
                modifyJson(yaml_match_configuration)

            output = f.getvalue().strip().split('\n')
            best_team1 = output[-2].split(': ')[-1]
            best_team2 = output[-1].split(': ')[-1]

            assert best_team1 in [
                "['player2 A', 'player1 A']",
                "['player1 A', 'player2 A']",
            ]
            assert best_team2 in ["['player4 B', 'player3']", "['player3', 'player4 B']"]
