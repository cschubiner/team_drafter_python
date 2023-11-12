import unittest
from unittest.mock import mock_open, patch
from match_recorder import parse_input, append_to_csv

class TestMatchRecorder(unittest.TestCase):

    def test_end_to_end_simple(self):
        input_strings = [
        """Team 1 (score: 64.75 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'Alex_Mark B', 'jack_shepherd', 'jack_rogers B', 'jake_leichtling B', 'liam_kinney', 'andrew_carmine']
        Team 2 (score: 65.0 #players: 8): ['craig_collins A', 'alex_b A', 'arthur_orchanian', 'michael_arbeed', 'steven_safreno A', 'Zach_Costa', 'moe_koelueker', 'jason_leung']
        2-0 craig got a huge flag capture""",
        """Team 1 (score: 65.5 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'arthur_orchanian', 'Alex_Mark B', 'jake_leichtling B', 'jack_rogers B', 'andrew_carmine', 'moe_koelueker']
Team 2 (score: 64.25 #players: 8): ['craig_collins A', 'alex_b A', 'michael_arbeed', 'jack_shepherd', 'steven_safreno A', 'Zach_Costa', 'liam_kinney', 'jason_leung']
1-1 jeff did well, wipeout!
""",
        """
        Team 1 (score: 65.25 #players: 7): ['jeff_grimes B', 'clayton_schubiner B', 'arthur_orchanian', 'michael_arbeed', 'Alex_Mark B', 'jake_leichtling B', 'jack_rogers B']
Team 2 (score: 64.5 #players: 9): ['craig_collins A', 'alex_b A', 'jack_shepherd', 'steven_safreno A', 'Zach_Costa', 'liam_kinney', 'andrew_carmine', 'moe_koelueker', 'jason_leung']
3-2 close match -- tie! 
""",
        """Team 1 (score: 66.5 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'michael_arbeed', 'Alex_Mark B', 'jack_rogers B', 'jake_leichtling B', 'liam_kinney', 'andrew_carmine']
Team 2 (score: 66.75 #players: 8): ['craig_collins A', 'alex_b A', 'arthur_orchanian', 'jack_shepherd', 'garrett_schubiner', 'steven_safreno A', 'Zach_Costa', 'jason_leung']
1-1 tie tie
"""
    ]
        expected_csv_output = """Player Name,Round 1,Round 2,Round 3,Round 4
# Add the expected CSV output here, formatted as a string
"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            unique_players, rounds_data = parse_input(input_strings)
            append_to_csv('dummy_file.csv', unique_players, rounds_data)
            mock_file().write.assert_called_with(expected_csv_output)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
