import csv
import os


def parse_input(input_strings):
    # Initialize a set to store unique player names
    unique_players = set()

    # Initialize a list to store parsed data for each round
    rounds_data = []

    # Process each input string
    for input_string in input_strings:
        # Split the input string by lines
        lines = input_string.strip().split('\n')
        # .strip() all lines
        lines = [line.strip() for line in lines]

        # Extract team information and player names
        team1_info = lines[0].split(': ')[3]
        team2_info = lines[1].split(': ')[3]
        team1_players = team1_info.strip('[]').split(', ')
        team2_players = team2_info.strip('[]').split(', ')

        # Update the set of unique player names, removing team identifiers and trailing dots if necessary
        for player in team1_players + team2_players:
            # Normalize player name by removing team identifiers and trailing dots
            normalized_player = ' '.join(player.split()[:-1]).rstrip('.')
            unique_players.add(normalized_player)

        # Extract scores and match notes, ensuring scores are integers and handling potential errors
        score_notes = lines[2].split(' ', 2)
        try:
            # Split the score string by '-' to separate the scores
            scores = score_notes[0].split('-')
            score_team1 = int(scores[0])
            score_team2 = int(scores[1])
        except (ValueError, IndexError):
            # Handle the case where scores are not in the 'x-y' format or are missing
            print(f"Error parsing scores from input: {lines[2]}")
            continue  # Skip this round of data
        match_notes = score_notes[2] if len(score_notes) > 2 else ''

        # Append round data to the list
        rounds_data.append((team1_players, team2_players, score_team1, score_team2, match_notes))

    return unique_players, rounds_data



def append_to_csv(filename, unique_players, rounds_data, match_notes):
    # Open the file in append mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Check if the file is empty to write the header
        if os.stat(filename).st_size == 0:
            header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))] + ['Match Notes']
            writer.writerow(header)

        # Write rows for each unique player
        for player in sorted(unique_players):
            player_row = [player]
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                # Normalize player name by removing team identifiers and trailing dots
                normalized_player = ' '.join(player.split()[:-1]).rstrip('.')

                # Check if the normalized player name is in the teams
                if normalized_player in [p.rstrip('.') for p in team1_players]:
                    player_row.append('Win' if score_team1 > score_team2 else 'Lose')
                elif normalized_player in [p.rstrip('.') for p in team2_players]:
                    player_row.append('Win' if score_team2 > score_team1 else 'Lose')
                else:
                    player_row.append('N/A')  # Player did not participate in this round
            writer.writerow(player_row)

        # Write match notes as the final row
        writer.writerow(['Match Notes'] + match_notes)



def append_notes_to_csv(filename, rounds_data):
    # Open the file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(['Round', 'Match Notes'])

        # Write rows for each round's match notes
        for i, round_data in enumerate(rounds_data):
            _, _, _, _, match_notes = round_data
            writer.writerow([f'Round {i+1}', match_notes])


if __name__ == '__main__':
    input_strings = [
        """Team 1 (score: 64.75 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'Alex_Mark B', 'jack_shepherd', 'jack_rogers B', 'jake_leichtling B', 'liam_kinney', 'andrew_carmine']
        Team 2 (score: 65.0 #players: 8): ['craig_collins A', 'alex_b A', 'arthur_orchanian', 'michael_arbeed', 'steven_safreno A', 'Zach_Costa', 'moe_koelueker', 'jason_leung']
        2-0 craig got a huge flag capture""",
        """Team 1 (score: 65.5 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'arthur_orchanian', 'Alex_Mark B', 'jake_leichtling B', 'jack_rogers B', 'andrew_carmine', 'moe_koelueker']
Team 2 (score: 64.25 #players: 8): ['craig_collins A', 'alex_b A', 'michael_arbeed', 'jack_shepherd', 'steven_safreno A', 'Zach_Costa', 'liam_kinney', 'jason_leung']
0-1 jeff did well, wipeout!
"""
    ]

    # Read match notes from CSV
    def read_match_notes(filename):
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            match_notes = [row[1] for row in reader]
        return match_notes

    # Parse the input
    unique_players, rounds_data = parse_input(input_strings)
    match_notes = read_match_notes('match_notes.csv')

    # Append to CSV including match notes
    append_to_csv('player_results.csv', unique_players, rounds_data, match_notes)
