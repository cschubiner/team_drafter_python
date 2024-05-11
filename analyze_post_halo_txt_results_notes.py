import json
import re


def remove_final_chars_from_rosters(roster: list[str]) -> list[str]:
    # player names are sometimes already correct, e.g. "alex_b". However, sometimes they have a ' A" or ' B' at the end.
    # This function removes those characters.
    return [player[:-2] if player[-2] == ' ' else player for player in roster]


def parse_game_data(file_content):
    games_data = []
    game_pattern = re.compile(
        r"Team 1 \(score: ([0-9.]+) #players: (\d+)\): (\[[^\]]+\])\s*"
        r"Team 2 \(score: ([0-9.]+) #players: (\d+)\): (\[[^\]]+\])\s*"
        r"([^\n]+)\n?", re.MULTILINE)

    matches = game_pattern.findall(file_content)
    for match in matches:
        team1_score, team1_players, team1_roster, team2_score, team2_players, team2_roster, result = match
        team1_roster = team1_roster.replace("'", '"')
        team2_roster = team2_roster.replace("'", '"')
        game_info = {
            "team_1": {
                "score": float(team1_score),
                "num_players": int(team1_players),
                "roster": remove_final_chars_from_rosters(json.loads(team1_roster)),
            },
            "team_2": {
                "score": float(team2_score),
                "num_players": int(team2_players),
                "roster": remove_final_chars_from_rosters(json.loads(team2_roster)),
            },
            "result": result.strip()
        }
        games_data.append(game_info)

    return json.dumps(games_data, indent=4)


# Load the file content
with open("text_files/halonight_rawresults-5-11-2024.txt", "r") as file:
    file_content = file.read()

if __name__ == "__main__":
    # Parse the file content
    json_data = parse_game_data(file_content)
    print(json_data)
