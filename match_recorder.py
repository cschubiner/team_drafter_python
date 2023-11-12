import csv
import os


def parse_input(input_string):
    # Split the input string by lines
    lines = input_string.strip().split('\n')

    # Extract team information
    team1_info = lines[0].split(': ')[1]
    team2_info = lines[1].split(': ')[1]

    # Extract scores and match notes
    score_notes = lines[2].split(' ')
    score_team1 = score_notes[0]
    score_team2 = score_notes[1]
    match_notes = ' '.join(score_notes[2:])

    return team1_info, team2_info, score_team1, score_team2, match_notes


def append_to_csv(filename, data):
    # Check if file exists to write headers
    file_exists = os.path.isfile(filename)

    # Open the file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If file does not exist, write the header
        if not file_exists:
            writer.writerow(['Team 1', 'Team 2', 'Score Team 1', 'Score Team 2', 'Match Notes'])

        # Write the data
        writer.writerow(data)


if __name__ == '__main__':
    input_string = """Team 1 (score: 64.75 #players: 8): ['jeff_grimes B', 'clayton_schubiner B', 'Alex_Mark B', 'jack_shepherd', 'jack_rogers B', 'jake_leichtling B', 'liam_kinney', 'andrew_carmine']
    Team 2 (score: 65.0 #players: 8): ['craig_collins A', 'alex_b A', 'arthur_orchanian', 'michael_arbeed', 'steven_safreno A', 'Zach_Costa', 'moe_koelueker', 'jason_leung']
    2-0 craig got a huge flag capture"""

    # Parse the input
    team1_info, team2_info, score_team1, score_team2, match_notes = parse_input(input_string)

    # Append to CSV
    append_to_csv('match_results.csv', [team1_info, team2_info, score_team1, score_team2, match_notes])
