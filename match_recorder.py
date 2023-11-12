import csv
import os
import json  # Import json to read the player scores


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
            # Remove team identifier if present
            player = player.strip("'")
            if player.split()[-1] in ['A', 'B']:
                player = ' '.join(player.split()[:-1])
            # Remove trailing dots
            player = player.rstrip('.')
            unique_players.add(player)

        # Extract scores and match notes, ensuring scores are integers and handling potential errors
        score_notes = lines[2].split(' ', 1)
        try:
            # Split the score string by '-' to separate the scores
            scores = score_notes[0].split('-')
            score_team1 = int(scores[0])
            score_team2 = int(scores[1])
        except (ValueError, IndexError):
            # Handle the case where scores are not in the 'x-y' format or are missing
            print(f"Error parsing scores from input: {lines[2]}")
            continue  # Skip this round of data
        # match_notes = score_notes[1] if len(score_notes) > 1 else ''
        match_notes = lines[2]

        # Append round data to the list
        rounds_data.append((team1_players, team2_players, score_team1, score_team2, match_notes))

    return unique_players, rounds_data



def append_to_csv(filename, unique_players, rounds_data):
    # Open the file in append mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Check if the file exists and is empty to write the header
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))] + ['Score']
            writer.writerow(header)

        # Write rows for each unique player
        for player in sorted(unique_players):
            player_row = [player]
            # Append match results for each round
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                if player in team1_players:
                    result = 'Win' if score_team1 > score_team2 else 'Lose' if score_team1 < score_team2 else 'Tie'
                elif player in team2_players:
                    result = 'Win' if score_team2 > score_team1 else 'Lose' if score_team2 < score_team1 else 'Tie'
                else:
                    result = 'N/A'
                player_row.append(result)
            # Retrieve the player's score from the dictionary, default to 0 if not found
            player_score = player_scores.get(player, 0)
            # Append the player's score to the row
            player_row.append(player_score)
            writer.writerow(player_row)
        # Append the player's score to each row
        for player in sorted(unique_players):
            player_row = [player]
            # Retrieve the player's score from the dictionary, default to 0 if not found
            player_score = player_scores.get(player, 0)
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                # ... (rest of the existing code remains unchanged)
            # Append the player's score to the row
            player_row.append(player_score)
            writer.writerow(player_row)

        # Write match notes as the final row
        match_notes = [round_data[4] for round_data in rounds_data]
        writer.writerow(['Match Notes'] + match_notes)




if __name__ == '__main__':
    input_strings = [
        """Team 1 (score: 63.75 #players: 8): ['alex_b', 'craig_collins', 'clayton_schubiner', 'arthur_orchanian', 'jack_shepherd', 'david_strickland', 'trevor_assaf']
Team 2 (score: 63.75 #players: 8): ['michael_arbeed', 'jeff_grimes', 'alex_roe', 'jack_rogers', 'garrett_schubiner', 'liam_kinney', 'david_freed']
0-0 tie (score unknown)""",
        """Team 1 (score: 63.75 #players: 8): ['alex_b', 'craig_collins', 'clayton_schubiner', 'arthur_orchanian', 'jack_shepherd', 'david_strickland', 'trevor_assaf']
Team 2 (score: 63.75 #players: 8): ['michael_arbeed', 'jeff_grimes', 'alex_roe', 'jack_rogers', 'garrett_schubiner', 'liam_kinney', 'david_freed']
1-1 tie""",
"""Team 1 (score: 63.75 #players: 8): ['alex_b', 'craig_collins', 'clayton_schubiner', 'arthur_orchanian', 'jack_shepherd', 'david_strickland', 'trevor_assaf']
Team 2 (score: 63.75 #players: 8): ['michael_arbeed', 'jeff_grimes', 'alex_roe', 'jack_rogers', 'garrett_schubiner', 'liam_kinney', 'david_freed']
1-0 close win to team 1""",
        """Team 1 (score: 64.25 #players: 7): ['craig_collins B', 'jeff_grimes', 'clayton_schubiner', 'michael_arbeed', 'jack_rogers B', 'liam_kinney', 'david_freed']
Team 2 (score: 64.5 #players: 8): ['alex_b', 'arthur_orchanian A', 'alex_roe A', 'garrett_schubiner', 'jack_shepherd', 'david_strickland', 'andrew_carmine', 'trevor_assaf']
2-0 wipeout by team 1""",
        """Team 1 (score: 63.75 #players: 8): ['craig_collins B', 'jeff_grimes B', 'michael_arbeed', 'jack_shepherd', 'liam_kinney', 'david_freed', 'andrew_carmine B', 'trevor_assaf B']
Team 2 (score: 63.5 #players: 7): ['clayton_schubiner', 'arthur_orchanian A', 'alex_roe A', 'alex_b', 'garrett_schubiner', 'jack_rogers A', 'david_strickland']
1-1 tie""",
        """Team 1 (score: 63.75 #players: 8): ['craig_collins B', 'jeff_grimes B', 'michael_arbeed', 'jack_shepherd', 'liam_kinney', 'david_freed', 'andrew_carmine B', 'trevor_assaf B']
Team 2 (score: 63.5 #players: 7): ['clayton_schubiner', 'arthur_orchanian A', 'alex_roe A', 'alex_b', 'garrett_schubiner', 'jack_rogers A', 'david_strickland', 'jason_leung']
2-0 wipeout by team 2 after adding jason onto team 2""",
        """Team 1 (score: 64.25 #players: 8): ['jeff_grimes', 'arthur_orchanian B', 'alex_b B', 'garrett_schubiner', 'jack_rogers', 'david_strickland B', 'david_freed', 'trevor_assaf']
Team 2 (score: 64.5 #players: 8): ['craig_collins', 'clayton_schubiner', 'alex_roe A', 'michael_arbeed', 'jack_shepherd', 'liam_kinney', 'andrew_carmine', 'jason_leung']
0-0 tie""",
        """Team 1 (score: 64.25 #players: 8): ['jeff_grimes', 'arthur_orchanian B', 'alex_b B', 'garrett_schubiner', 'jack_rogers', 'david_strickland B', 'david_freed', 'trevor_assaf']
Team 2 (score: 64.5 #players: 8): ['craig_collins', 'clayton_schubiner', 'alex_roe A', 'michael_arbeed', 'jack_shepherd', 'liam_kinney', 'andrew_carmine', 'jason_leung']
0-1""",
        """Team 1 (score: 64.25 #players: 8): ['jeff_grimes', 'arthur_orchanian B', 'alex_b B', 'garrett_schubiner', 'jack_rogers', 'david_strickland B', 'david_freed', 'trevor_assaf']
Team 2 (score: 64.5 #players: 8): ['craig_collins', 'clayton_schubiner', 'alex_roe A', 'michael_arbeed', 'jack_shepherd', 'liam_kinney', 'andrew_carmine', 'jason_leung']
3-1""",
    ]

    # Parse the input
    unique_players, rounds_data = parse_input(input_strings)

    # Append to CSV including match notes
    append_to_csv('player_results.csv', unique_players, rounds_data)
