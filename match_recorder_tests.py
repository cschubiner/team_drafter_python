import unittest
from unittest.mock import mock_open, patch
from match_recorder import parse_input, append_to_csv

class TestMatchRecorder(unittest.TestCase):

    def test_parse_input_valid(self):
        input_strings = [
            "Team 1 (score: 64.75 #players: 8): ['jeff_grimes B', 'clayton_schubiner B']\n"
            "Team 2 (score: 65.0 #players: 8): ['craig_collins A', 'alex_b A']\n"
            "2-0 craig got a huge flag capture"
        ]
        expected_unique_players = {'jeff_grimes', 'clayton_schubiner', 'craig_collins', 'alex_b'}
        expected_rounds_data = [(['jeff_grimes', 'clayton_schubiner'], ['craig_collins', 'alex_b'], 2, 0, '2-0 craig got a huge flag capture')]
        unique_players, rounds_data = parse_input(input_strings)
        self.assertEqual(expected_unique_players, unique_players)
        self.assertEqual(expected_rounds_data, rounds_data)

    def test_append_to_csv(self):
        unique_players = {'jeff_grimes', 'clayton_schubiner', 'craig_collins', 'alex_b'}
        rounds_data = [(['jeff_grimes', 'clayton_schubiner'], ['craig_collins', 'alex_b'], 2, 0, '2-0 craig got a huge flag capture')]
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            append_to_csv('dummy_file.csv', unique_players, rounds_data)
        mock_file.assert_called_once_with('dummy_file.csv', mode='w', newline='')
        mock_file().write.assert_called()

if __name__ == '__main__':
    unittest.main()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
