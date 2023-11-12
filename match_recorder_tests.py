import unittest
from unittest.mock import mock_open, patch
from match_recorder import parse_input, append_to_csv

class TestMatchRecorder(unittest.TestCase):

    def test_end_to_end_simple(self):
        input_strings = [
            # Add the input strings here, same as in match_recorder.py's __main__ block
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
