import json
import unittest

import pytest
import unittest.mock as mock
from io import StringIO
from contextlib import redirect_stdout

from drafter import modifyJson


class TestModifyJson(unittest.TestCase):

    def test_modifyJson(self):
        player_scores = {
            "player1": 10,
            "player2": 8,
            "player3": 12,
            "player4": 9,
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
                                {"name": "player3 B"},
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
            best_team1 = output[-3].split(': ')[-1]
            best_team2 = output[-2].split(': ')[-1]

            assert best_team1 == "['player1', 'player3']"
            assert best_team2 == "['player2', 'player4']"
