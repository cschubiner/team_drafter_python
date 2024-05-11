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

    def test_modifyJson_with_uneven_players(self):
        player_scores = {
            "player1": 5,
            "player2": 5,
            "player3": 6,
            "player4": 6,
            "player5": 11,
            "player6": 9
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
                                {"name": "player5"},
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

            # Expected that the teams will still be balanced
            assert len(eval(best_team1)) in [2, 3]
            assert len(eval(best_team2)) in [2, 3]

    def test_modifyJson_with_equal_scores(self):
        player_scores = {
            "player1": 5,
            "player2": 5,
            "player3": 5,
            "player4": 5,
            "player5": 5,
            "player6": 5
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
                                {"name": "player5"},
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

            # Even though the scores are equal, the script should still try to balance player numbers
            assert len(eval(best_team1)) in [2, 3]
            assert len(eval(best_team2)) in [2, 3]
    def test_arthur_algorithm_tiebreaker(self):
        player_scores = {
            "player1": 10,  # S tier
            "player2": 10,  # S tier
            "player3": 9,   # A tier
            "player4": 8,   # A tier
            "player5": 7,   # B tier
            "player6": 5,   # C tier
            "player7": 10,  # S tier
            "player8": 9    # A tier
        }

        yaml_match_configuration = {
            "matches": [
                {
                    "_match number": 1,
                    "teams": [
                        {
                            "players": [
                                {"name": "player1"},
                                {"name": "player2"},
                                {"name": "player5"},
                                {"name": "player6"},
                            ]
                        },
                        {
                            "players": [
                                {"name": "player3"},
                                {"name": "player4"},
                                {"name": "player7"},
                                {"name": "player8"},
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

            # Check if the S tier players are evenly distributed
            best_team1_players = eval(best_team1)
            best_team2_players = eval(best_team2)
            best_team1_s_tier = [p for p in best_team1_players if player_scores[p] == 10]
            best_team2_s_tier = [p for p in best_team2_players if player_scores[p] == 10]

            self.assertEqual(len(best_team1_s_tier), len(best_team2_s_tier), "S tier players should be evenly distributed")

            # If S tier players are evenly distributed, check for A tier distribution
            if len(best_team1_s_tier) == len(best_team2_s_tier):
                best_team1_a_tier = [p for p in best_team1_players if player_scores[p] == 9]
                best_team2_a_tier = [p for p in best_team2_players if player_scores[p] == 9]
                self.assertEqual(len(best_team1_a_tier), len(best_team2_a_tier), "A tier players should be evenly distributed if S tier is even")
