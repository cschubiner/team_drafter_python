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

        # Extract team information and player names
        team1_info = lines[0].split(': ')[1]
        team2_info = lines[1].split(': ')[1]
        team1_players = team1_info.strip('[]').split(', ')
        team2_players = team2_info.strip('[]').split(', ')

        # Update the set of unique player names
        unique_players.update(team1_players)
        unique_players.update(team2_players)

        # Extract scores and match notes, ensuring scores are integers
        score_notes = lines[2].split(' ', 2)
        score_team1 = int(score_notes[0])
        score_team2 = int(score_notes[1])
        match_notes = score_notes[2]

        # Append round data to the list
        rounds_data.append((team1_players, team2_players, score_team1, score_team2, match_notes))

    return unique_players, rounds_data

    # Initialize a set to store unique player names
    unique_players = set()

    # Initialize a list to store parsed data for each round
    rounds_data = []

    # Process each input string
    for input_string in input_strings:
        # Split the input string by lines
        lines = input_string.strip().split('\n')

        # Extract team information and player names
        team1_info = lines[0].split(': ')[1]
        team2_info = lines[1].split(': ')[1]
        team1_players = team1_info.strip('[]').split(', ')
        team2_players = team2_info.strip('[]').split(', ')

        # Update the set of unique player names
        unique_players.update(team1_players)
        unique_players.update(team2_players)

        # Extract scores and match notes
        score_notes = lines[2].split(' ')
        score_team1 = score_notes[0]
        score_team2 = score_notes[1]
        match_notes = ' '.join(score_notes[2:])

        # Append round data to the list
        rounds_data.append((team1_players, team2_players, score_team1, score_team2, match_notes))

    return unique_players, rounds_data


def append_to_csv(filename, unique_players, rounds_data):
    # Open the file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Check if the file is empty to write the header
        if os.stat(filename).st_size == 0:
            header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))]
            writer.writerow(header)

        # Write rows for each unique player
        for player in sorted(unique_players):
            player_row = [player]
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                if player in team1_players:
                    player_row.append('Win' if int(score_team1) > int(score_team2) else 'Lose')
                elif player in team2_players:
                    player_row.append('Win' if int(score_team2) > int(score_team1) else 'Lose')
                else:
                    player_row.append('N/A')  # Player did not participate in this round
            writer.writerow(player_row)

    # Open the file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header with player names and rounds
        header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))]
        writer.writerow(header)

        # Write rows for each unique player
        for player in unique_players:
            player_row = [player]
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                if player in team1_players:
                    player_row.append('Win' if score_team1 > score_team2 else 'Lose')
                elif player in team2_players:
                    player_row.append('Win' if score_team2 > score_team1 else 'Lose')
                else:
                    player_row.append('N/A')  # Player did not participate in this round
            writer.writerow(player_row)


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

    # Parse the input
    unique_players, rounds_data = parse_input(input_strings)

    # Append to CSV
    append_to_csv('player_results.csv', unique_players, rounds_data)

    # Append match notes to a separate CSV
    append_notes_to_csv('match_notes.csv', rounds_data)
