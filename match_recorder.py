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

        # Check if the file is empty to write the header
        if os.stat(filename).st_size == 0:
            header = ['Player Name'] + [f'Round {i+1}' for i in range(len(rounds_data))]
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

                # Check if the normalized player name is in the teams
                # Check if the normalized player name is a substring of any player name in the teams
                if any(normalized_player in p for p in team1_players):
                    if score_team1 == score_team2:
                        player_row.append('Tie as Team 1')
                    else:
                        player_row.append('Win' if score_team1 > score_team2 else 'Lose')
                elif any(normalized_player in p for p in team2_players):
                    if score_team1 == score_team2:
                        player_row.append('Tie as Team 2')
                    else:
                        player_row.append('Win' if score_team2 > score_team1 else 'Lose')
                else:
                    player_row.append('N/A')  # Player did not participate in this round
            writer.writerow(player_row)

        # Write match notes as the final row
        match_notes = [round_data[4] for round_data in rounds_data]
        writer.writerow(['Match Notes'] + match_notes)




if __name__ == '__main__':
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

    # Parse the input
    unique_players, rounds_data = parse_input(input_strings)

    # Append to CSV including match notes
    append_to_csv('player_results.csv', unique_players, rounds_data)
