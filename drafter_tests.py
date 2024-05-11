import random
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
                                {"name": "player1"},  # One S tier player
                                {"name": "player3"},  # One A tier player
                                {"name": "player5"},  # One B tier player
                                {"name": "player6"},  # One C tier player
                                {"name": "player5"},
                                {"name": "player6"},
                            ]
                        },
                        {
                            "players": [
                                {"name": "player2"},  # One S tier player
                                {"name": "player4"},  # One A tier player
                                {"name": "player7"},  # One S tier player
                                {"name": "player8"},  # One A tier player
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

            self.assertTrue(abs(len(best_team1_s_tier) - len(best_team2_s_tier)) <= 1, "Difference in S tier players should be no more than 1")

            # If S tier players are evenly distributed, check for A tier distribution
            if len(best_team1_s_tier) == len(best_team2_s_tier):
                best_team1_a_tier = [p for p in best_team1_players if player_scores[p] == 9]
                best_team2_a_tier = [p for p in best_team2_players if player_scores[p] == 9]
                self.assertEqual(len(best_team1_a_tier), len(best_team2_a_tier), "A tier players should be evenly distributed if S tier is even")
    def test_modifyJson_with_large_player_pool(self):
        player_scores = {f"player{i}": random.randint(1, 12) for i in range(1, 21)}

        yaml_match_configuration = {
            "matches": [
                {
                    "_match number": 1,
                    "teams": [
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(1, 11)
                            ]
                        },
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(11, 21)
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

            # Check that the teams are balanced in size
            assert abs(len(eval(best_team1)) - len(eval(best_team2))) <= 1

    def test_modifyJson_with_multiple_matches(self):
        player_scores = {f"player{i}": random.randint(1, 12) for i in range(1, 13)}

        yaml_match_configuration = {
            "matches": [
                {
                    "_match number": 1,
                    "teams": [
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(1, 4)
                            ]
                        },
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(4, 7)
                            ]
                        }
                    ]
                },
                {
                    "_match number": 2,
                    "teams": [
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(7, 10)
                            ]
                        },
                        {
                            "players": [
                                {"name": f"player{i}"} for i in range(10, 13)
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
            
            for i in range(2):
                best_team1 = output[-4 + 2*i].split(': ')[-1]
                best_team2 = output[-3 + 2*i].split(': ')[-1]

                # Check that the teams are balanced in size for each match
                if best_team1 and best_team2:
                    assert abs(len(eval(best_team1)) - len(eval(best_team2))) <= 1
