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

    # read the score from this part of the string: " """Team 1 (score: 58.75 #players: 7): """
    # Extract the score from the match notes
    team1_scores_from_text = []
    team2_scores_from_text = []
    for input_string in input_strings:
        lines = input_string.strip().split('\n')
        lines = [line.strip() for line in lines]
        team1_score = float(lines[0].split(' ')[3].strip('):'))
        team2_score = float(lines[1].split(' ')[3].strip('):'))
        team1_scores_from_text.append(team1_score)
        team2_scores_from_text.append(team2_score)

    return unique_players, rounds_data, team1_scores_from_text, team2_scores_from_text



def get_player_tier(player_score):
    if player_score >= 10:
        return 'S'
    elif player_score >= 8:
        return 'A'
    elif player_score >= 6:
        return 'B'
    else:
        return 'C'

def append_to_csv(filename, unique_players, rounds_data, player_scores, team1_scores_from_text, team2_scores_from_text):
    # Open the file in append mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Check if the file exists and is empty to write the header
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))] + ['Player Score']
            writer.writerow(header)

        # Write rows for each unique player
        for player in sorted(unique_players):
            player_row = [player]
            for round_data in rounds_data:
                team1_players, team2_players, score_team1, score_team2, _ = round_data
                # Normalize player name by removing team identifiers and trailing dots
                normalized_player = player
                if len(normalized_player.split()) > 2 and normalized_player.split()[-1] in ['A', 'B']:
                    normalized_player = ' '.join(normalized_player.split()[:-1])
                normalized_player = normalized_player.rstrip('.')

                current_match_notes = round_data[4]
                # Check if the normalized player name is a substring of any player name in the teams
                if any(normalized_player in p for p in team1_players):
                    if 'wipeout' in current_match_notes:
                        player_row.append('BigWin' if score_team1 > score_team2 else 'BigLoss')
                    elif score_team1 == score_team2:
                        player_row.append('Tie as Team 1')
                    else:
                        player_row.append('Win' if score_team1 > score_team2 else 'Lose')
                elif any(normalized_player in p for p in team2_players):
                    if 'wipeout' in current_match_notes:
                        player_row.append('BigWin' if score_team2 > score_team1 else 'BigLoss')
                    elif score_team1 == score_team2:
                        player_row.append('Tie as Team 2')
                    else:
                        player_row.append('Win' if score_team2 > score_team1 else 'Lose')
                else:
                    player_row.append('N/A')  # Player did not participate in this round

            player_score = player_scores.get(player, 0)
            # Append the player's score to the row
            player_row.append(player_score)
            writer.writerow(player_row)

        match_notes = [round_data[4] for round_data in rounds_data]
        writer.writerow(['Match Notes'] + match_notes)

        # Write the input string scores as the final two rows
        input_team1_scores_row = ['Team 1 Score before match']
        input_team2_scores_row = ['Team 2 Score before match']
        for team1_score, team2_score in zip(team1_scores_from_text, team2_scores_from_text):
            input_team1_scores_row.append(team1_score)
            input_team2_scores_row.append(team2_score)
        writer.writerow(input_team1_scores_row)
        writer.writerow(input_team2_scores_row)

        # Calculate and write the sum of scores for each team in each round
        team1_scores_row = ['Team 1 Total Score']
        team2_scores_row = ['Team 2 Total Score']
        for team1_players, team2_players, _, _, _ in rounds_data:
            team1_scores = 0
            for player in team1_players:
                # Normalize player name by removing team identifiers and trailing dots
                normalized_player = player.strip("'")
                if len(normalized_player.split()) > 1 and normalized_player.split()[-1] in ['A', 'B']:
                    normalized_player = ' '.join(normalized_player.split()[:-1])
                normalized_player = normalized_player.rstrip('.')
                player_score = player_scores.get(normalized_player, None)
                if player_score is None:
                    raise Exception(f"Player {normalized_player} not found in player scores")
                team1_scores += player_score

            team1_scores_row.append(team1_scores)

            team2_scores = 0
            for player in team2_players:
                # Normalize player name by removing team identifiers and trailing dots
                normalized_player = player.strip("'")
                if len(normalized_player.split()) > 1 and normalized_player.split()[-1] in ['A', 'B']:
                    normalized_player = ' '.join(normalized_player.split()[:-1])
                normalized_player = normalized_player.rstrip('.')
                player_score = player_scores.get(normalized_player, None)
                if player_score is None:
                    raise Exception(f"Player {normalized_player} not found in player scores")
                team2_scores +=  player_score

            team2_scores_row.append(team2_scores)
        writer.writerow(team1_scores_row)
        writer.writerow(team2_scores_row)

        # Calculate and write the number of players in each tier for each team in each round
        team1_tiers_row = ['Team 1 Tier Counts']
        team2_tiers_row = ['Team 2 Tier Counts']
        for team1_players, team2_players, _, _, _ in rounds_data:
            team1_tier_counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}
            for player in team1_players:
                normalized_player = player.strip("'")
                if len(normalized_player.split()) > 1 and normalized_player.split()[-1] in ['A', 'B']:
                    normalized_player = ' '.join(normalized_player.split()[:-1])
                normalized_player = normalized_player.rstrip('.')
                player_score = player_scores.get(normalized_player, None)
                if player_score is None:
                    raise Exception(f"Player {normalized_player} not found in player scores")
                tier = get_player_tier(player_score)
                team1_tier_counts[tier] += 1
            team1_tiers_row.append(f"S:{team1_tier_counts['S']} A:{team1_tier_counts['A']} B:{team1_tier_counts['B']} C:{team1_tier_counts['C']}")

            team2_tier_counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}
            for player in team2_players:
                normalized_player = player.strip("'")
                if len(normalized_player.split()) > 1 and normalized_player.split()[-1] in ['A', 'B']:
                    normalized_player = ' '.join(normalized_player.split()[:-1])
                normalized_player = normalized_player.rstrip('.')
                player_score = player_scores.get(normalized_player, None)
                if player_score is None:
                    raise Exception(f"Player {normalized_player} not found in player scores")
                tier = get_player_tier(player_score)
                team2_tier_counts[tier] += 1
            team2_tiers_row.append(f"S:{team2_tier_counts['S']} A:{team2_tier_counts['A']} B:{team2_tier_counts['B']} C:{team2_tier_counts['C']}")

        writer.writerow(team1_tiers_row)
        writer.writerow(team2_tiers_row)






if __name__ == '__main__':
    # Load player scores from JSON file
    with open('player_scores.json', 'r') as f:
        player_scores = json.load(f)

    input_strings = ["""Team 1 (score: 40.75 #players: 5): ['clayton_schubiner A', 'alex_b', 'michael_arbeed', 'liam_kinney', 'moe_koelueker']
Team 2 (score: 40.75 #players: 5): ['jeff_grimes', 'jack_rogers', 'Alex_Mark', 'steven_safreno', 'andrew_carmine']
1-1 tie 5/10/24 team1 left early?""",

"""Team 1 (score: 52.25 #players: 6): ['clayton_schubiner A', 'jeff_grimes', 'michael_arbeed', 'steven_safreno', 'Zach_Costa', 'daniel_khasanov']
Team 2 (score: 52.25 #players: 7): ['arthur_orchanian B', 'alex_b', 'jack_rogers', 'Alex_Mark', 'liam_kinney', 'andrew_carmine', 'moe_koelueker']
2-0 team 1 wipeout""",

"""Team 1 (score: 52.5 #players: 6): ['clayton_schubiner A', 'arthur_orchanian A', 'alex_b A', 'jack_rogers', 'steven_safreno', 'moe_koelueker']
Team 2 (score: 52.5 #players: 7): ['jeff_grimes B', 'michael_arbeed', 'Alex_Mark B', 'Zach_Costa', 'daniel_khasanov', 'liam_kinney', 'andrew_carmine']
1-1 tie """,

"""Team 1 (score: 49.5 #players: 6): ['clayton_schubiner A', 'jeff_grimes A', 'alex_b A', 'Zach_Costa', 'liam_kinney', 'trevor_assaf A']
Team 2 (score: 49.5 #players: 7): ['arthur_orchanian', 'michael_arbeed B', 'steven_safreno', 'jack_rogers', 'daniel_khasanov', 'andrew_carmine', 'moe_koelueker']
2-3 team 2""",

"""Team 1 (score: 50.0 #players: 6): ['clayton_schubiner A', 'jeff_grimes A', 'alex_b A', 'Zach_Costa', 'daniel_khasanov', 'trevor_assaf A']
Team 2 (score: 49.75 #players: 7): ['arthur_orchanian', 'michael_arbeed B', 'jack_rogers', 'steven_safreno', 'liam_kinney', 'andrew_carmine', 'moe_koelueker']
1-2 team 2""",

"""Team 1 (score: 50.13 #players: 6): ['clayton_schubiner A', 'alex_b', 'michael_arbeed', 'jack_rogers', 'daniel_khasanov', 'trevor_assaf']
Team 2 (score: 50.25 #players: 7): ['jeff_grimes B', 'arthur_orchanian', 'steven_safreno', 'Zach_Costa', 'liam_kinney', 'andrew_carmine', 'moe_koelueker']
3-2 team 1""",

"""Team 1 (score: 50.13 #players: 6): ['clayton_schubiner A', 'alex_b', 'michael_arbeed', 'jack_rogers', 'daniel_khasanov', 'trevor_assaf']
Team 2 (score: 50.25 #players: 7): ['jeff_grimes B', 'arthur_orchanian', 'steven_safreno', 'Zach_Costa', 'liam_kinney', 'andrew_carmine', 'moe_koelueker']
1-1 tie game - same teams""",

"""Team 1 (score: 50.13 #players: 6): ['clayton_schubiner A', 'alex_b', 'michael_arbeed', 'jack_rogers', 'daniel_khasanov', 'trevor_assaf']
Team 2 (score: 50.25 #players: 7): ['jeff_grimes B', 'arthur_orchanian', 'steven_safreno', 'Zach_Costa', 'liam_kinney', 'andrew_carmine', 'moe_koelueker']
1-0 team 1 - same teams""",

"""Team 1 (score: 43.25 #players: 6): ['clayton_schubiner A', 'jeff_grimes', 'daniel_khasanov', 'liam_kinney', 'andrew_carmine A', 'trevor_assaf']
Team 2 (score: 43.38 #players: 5): ['arthur_orchanian', 'alex_b', 'jack_rogers', 'steven_safreno', 'Zach_Costa']
2-1 team 1""",

"""Team 1 (score: 39.0 #players: 5): ['jeff_grimes', 'arthur_orchanian', 'Zach_Costa', 'daniel_khasanov', 'trevor_assaf A']
Team 2 (score: 39.25 #players: 5): ['clayton_schubiner', 'alex_b', 'steven_safreno B', 'liam_kinney', 'andrew_carmine']
2-1 team 1""",
]
    # Parse the input
    unique_players, rounds_data, team1_scores_from_text, team2_scores_from_text = parse_input(input_strings)

    # Append to CSV including match notes
    append_to_csv('player_results.csv', unique_players, rounds_data, player_scores, team1_scores_from_text, team2_scores_from_text)
