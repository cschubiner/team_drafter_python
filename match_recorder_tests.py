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
        # Use os.linesep to ensure the line endings match the system's default
        # Use os.linesep to ensure the line endings match the system's default
        expected_csv_output = """Player Name,Round 1,Round 2,Round 3,Round 4,Player Score
Alex_Mark,Win,Tie as Team 1,Win,Tie as Team 1,5.1
Zach_Costa,Lose,Tie as Team 2,Lose,Tie as Team 2,5
alex_b,Lose,Tie as Team 2,Lose,Tie as Team 2,6
andrew_carmine,Win,Tie as Team 1,Lose,Tie as Team 1,6
arthur_orchanian,Lose,Tie as Team 1,Win,Tie as Team 2,11
clayton_schubiner,Win,Tie as Team 1,Win,Tie as Team 1,9
craig_collins,Lose,Tie as Team 2,Lose,Tie as Team 2,12
garrett_schubiner,N/A,N/A,N/A,Tie as Team 2,10
jack_rogers,Win,Tie as Team 1,Win,Tie as Team 1,5.1
jack_shepherd,Win,Tie as Team 2,Lose,Tie as Team 2,5
jake_leichtling,Win,Tie as Team 1,Win,Tie as Team 1,6
jason_leung,Lose,Tie as Team 2,Lose,Tie as Team 2,6
jeff_grimes,Win,Tie as Team 1,Win,Tie as Team 1,11
liam_kinney,Win,Tie as Team 2,Lose,Tie as Team 1,9
michael_arbeed,Lose,Tie as Team 2,Win,Tie as Team 1,12
moe_koelueker,Lose,Tie as Team 1,Lose,N/A,10
steven_safreno,Lose,Tie as Team 2,Lose,Tie as Team 2,5.1
Match Notes,2-0 craig got a huge flag capture,"1-1 jeff did well, wipeout!",3-2 close match -- tie!,1-1 tie tie
Team 1 Score before match,64.75,65.5,65.25,66.5
Team 2 Score before match,65.0,64.25,64.5,66.75
Team 1 Total Score,56.2,63.2,59.2,63.2
Team 2 Total Score,67.1,60.1,64.1,60.1
"""
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            unique_players, rounds_data, team1_scores_from_text, team2_scores_from_text = parse_input(input_strings)
            player_scores = {
                "Alex_Mark": 5.1,
                "Zach_Costa": 5,
                "alex_b": 6,
                "andrew_carmine": 6,
                "arthur_orchanian": 11,
                "clayton_schubiner": 9,
                "craig_collins": 12,
                "garrett_schubiner": 10,
                "jack_rogers": 5.1,
                "jack_shepherd": 5,
                "jake_leichtling": 6,
                "jason_leung": 6,
                "jeff_grimes": 11,
                "liam_kinney": 9,
                "michael_arbeed": 12,
                "moe_koelueker": 10,
                "steven_safreno": 5.1
            }
            append_to_csv('dummy_file.csv', unique_players, rounds_data, player_scores, team1_scores_from_text, team2_scores_from_text)
            # Ensure the expected output matches the actual output including the line endings
            expected_lines = [line + os.linesep for line in expected_csv_output.strip().splitlines()]

            # Print the expected and actual calls for debugging
            # print("Expected calls:")
            # for line in expected_lines:
            #     print(f"call('{line.strip()}')")

            # Get the actual calls to write
            actual_calls = mock_file().write.call_args_list
            # strip the trailing newline from each call
            actual_lines = [call[0][0].rstrip() for call in actual_calls]

            # print("\nActual calls:")
            # for line in actual_lines:
            #     print(f"call('{line}')")
            
            # Normalize line endings in the expected output to match the actual output
            expected_lines = [line for line in expected_csv_output.strip().splitlines()]

            # instead assert that the expected lines are == to the actual lines
            self.assertEqual(expected_lines, actual_lines), "Expected output did not match actual output"



if __name__ == '__main__':
    unittest.main()
