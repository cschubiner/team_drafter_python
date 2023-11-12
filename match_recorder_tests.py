import unittest
import os  # Import the os module
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
Alex_Mark,Win,Tie as Team 1,Win,Tie as Team 1
Zach_Costa,Lose,Tie as Team 2,Lose,Tie as Team 2
alex_b,Lose,Tie as Team 2,Lose,Tie as Team 2
andrew_carmine,Win,Tie as Team 1,Lose,Tie as Team 1
arthur_orchanian,Lose,Tie as Team 1,Win,Tie as Team 2
clayton_schubiner,Win,Tie as Team 1,Win,Tie as Team 1
craig_collins,Lose,Tie as Team 2,Lose,Tie as Team 2
garrett_schubiner,N/A,N/A,N/A,Tie as Team 2
jack_rogers,Win,Tie as Team 1,Win,Tie as Team 1
jack_shepherd,Win,Tie as Team 2,Lose,Tie as Team 2
jake_leichtling,Win,Tie as Team 1,Win,Tie as Team 1
jason_leung,Lose,Tie as Team 2,Lose,Tie as Team 2
jeff_grimes,Win,Tie as Team 1,Win,Tie as Team 1
liam_kinney,Win,Tie as Team 2,Lose,Tie as Team 1
michael_arbeed,Lose,Tie as Team 2,Win,Tie as Team 1
moe_koelueker,Lose,Tie as Team 1,Lose,N/A
steven_safreno,Lose,Tie as Team 2,Lose,Tie as Team 2
Match Notes,2-0 craig got a huge flag capture,"1-1 jeff did well, wipeout!",3-2 close match -- tie!,1-1 tie tie
"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            unique_players, rounds_data = parse_input(input_strings)
            append_to_csv('dummy_file.csv', unique_players, rounds_data)
            # Normalize line endings in the expected output to match the system's default
            expected_lines = [line + os.linesep for line in expected_csv_output.split('\n')]
            # Get the actual calls to write
            actual_calls = mock_file().write.call_args_list
            # Print the expected and actual calls for debugging
            print("Expected calls:")
            for line in expected_lines:
                print(f"call('{line.strip()}')")
            print("\nActual calls:")
            for call in actual_calls:
                print(call)
            
            # Check that write was called with each line of the expected output
            mock_file().write.assert_has_calls([unittest.mock.call(line) for line in expected_lines], any_order=True)


if __name__ == '__main__':
    unittest.main()
