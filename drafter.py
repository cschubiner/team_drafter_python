#!/usr/bin/env python3
import json
from collections import defaultdict
from collections import Counter
from typing import Dict, Any

import yaml
import sys
import time
import logging
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from yaml import load, dump
from watchdog.events import LoggingEventHandler

CURRENT_TEAM_FILENAME: str = "current_teams.yml"


def modifyJson(yml):
    forced_team_to_player_names, player_to_score = read_yml(yml)
    players_and_scores = sorted(player_to_score.items(), key=lambda x: x[1], reverse=True)

    # Also, add in "proposed_team_1" and "proposed_team_2" to each match
    # Create the proposed teams by enumerating all possible combinations of players
    # in which the team size is equal or +1/-1 of each other
    # Then, for each match, add in the proposed teams

    possible_teams = []
    total_players = len(player_to_score)
    # now shuffle it
    import random

    best_min_score_delta = 999
    already_seen_teams = set()
    already_seen_teams = set()
    printed_team_combinations = set()
    best_team1_tiers = Counter()
    best_team2_tiers = Counter()

    # Choose 100 random teams
    for i in range(30250):
        random.shuffle(players_and_scores)
        team1 = []
        team2 = []
        # first, assert that there are only up to 2 forced teams
        assert len(forced_team_to_player_names) <= 2
        forced_teams = list(forced_team_to_player_names.values())
        # assign the first forced team to team1
        if len(forced_teams) > 0:
            team1 = [x for x in players_and_scores if x[0] in forced_teams[0]]
        # assign the second forced team to team2
        if len(forced_teams) > 1:
            team2 = [x for x in players_and_scores if x[0] in forced_teams[1]]


        # First put half of the players on team 1
        # num_players_on_team_1 = total_players // 2
        # Choose a random number of players on team 1 which is +- 1 of the other team
        num_players_on_team_1 = random.randint(total_players // 2 - 1, total_players // 2 + 1)

        while len(team1) < num_players_on_team_1:
            # make sure we don't add a player that is already on team 1
            for player in players_and_scores:
                if player not in team1 and player not in team2:
                    team1.append(player)
                    break

        # Now, put the rest of the players on team 2
        team2 = [x for x in players_and_scores if x not in team1]

        # Add team1 to the already seen teams
        # First sort the team by score
        # already_seen_key = tuple(sorted(team1, key=lambda x: x[1], reverse=True))
        # First sort the team by score first, name second
        already_seen_key = tuple(sorted(team1, key=lambda x: (x[1], x[0]), reverse=True))
        if already_seen_key in already_seen_teams:
            continue
        already_seen_teams.add(already_seen_key)

        # Now, calculate the score delta
        team1_score = sum([x[1] for x in team1])
        team2_score = sum([x[1] for x in team2])
        score_delta = abs(team1_score - team2_score)


        team_size_tiny_delta = abs(len(team1) - len(team2)) * 0.0001
        if score_delta + team_size_tiny_delta < best_min_score_delta:
            best_min_score_delta = score_delta + team_size_tiny_delta
            best_team1 = team1
            best_team2 = team2
            best_team1_tiers = Counter(get_player_tier(x[1]) for x in best_team1)
            best_team2_tiers = Counter(get_player_tier(x[1]) for x in best_team2)
        elif score_delta + team_size_tiny_delta == best_min_score_delta:
            # Tiebreak using the Arthur method
            team1_tiers = Counter(get_player_tier(x[1]) for x in team1)
            team2_tiers = Counter(get_player_tier(x[1]) for x in team2)

            if abs(team1_tiers["S"] - team2_tiers["S"]) < abs(best_team1_tiers["S"] - best_team2_tiers["S"]):
                best_team1 = team1
                best_team2 = team2
                best_team1_tiers = team1_tiers
                best_team2_tiers = team2_tiers
            elif abs(team1_tiers["S"] - team2_tiers["S"]) == abs(best_team1_tiers["S"] - best_team2_tiers["S"]):
                if abs(team1_tiers["A"] - team2_tiers["A"]) < abs(best_team1_tiers["A"] - best_team2_tiers["A"]):
                    best_team1 = team1 
                    best_team2 = team2
                    best_team1_tiers = team1_tiers
                    best_team2_tiers = team2_tiers

        # Create a string representation of the teams
        team1_str = ' '.join(sorted([x[0] for x in best_team1]))
        team2_str = ' '.join(sorted([x[0] for x in best_team2]))
        teams_str = team1_str + ' vs ' + team2_str
        # Check if we have already printed these teams
        if teams_str not in printed_team_combinations:
            printed_team_combinations.add(teams_str)
            print("Current best team found with score delta of {}".format(best_min_score_delta))
            print("Team 1 (score: {} #players: {}): {}".format(sum(x[1] for x in best_team1), len(best_team1), [x[0] for x in sorted(best_team1, key=lambda x: x[1], reverse=True)]))
            print("Team 1 Tiers - S:{} A:{} B:{} C:{}".format(best_team1_tiers["S"], best_team1_tiers["A"], best_team1_tiers["B"], best_team1_tiers["C"]))
            print("Team 2 (score: {} #players: {}): {}".format(sum(x[1] for x in best_team2), len(best_team2), [x[0] for x in sorted(best_team2, key=lambda x: x[1], reverse=True)]))  
            print("Team 2 Tiers - S:{} A:{} B:{} C:{}".format(best_team2_tiers["S"], best_team2_tiers["A"], best_team2_tiers["B"], best_team2_tiers["C"]))
            # print a message of congratulations

    # for match in yml["matches"]:
    #     match["proposed_team_1"] = [x[0] for x in sorted(best_team1, key=lambda x: x[1], reverse=True)]
    #     match["proposed_team_2"] = [x[0] for x in sorted(best_team2, key=lambda x: x[1], reverse=True)]
    #     match["proposed_team_1_score"] = sum([x[1] for x in best_team1])
    #     match["proposed_team_2_score"] = sum([x[1] for x in best_team2])

    return yml


def read_yml(yml):
    # Load player scores from json
    with open('player_scores.json', 'r') as f:
        player_scores = json.load(f)

    player_to_score: dict[str, float] = {}
    forced_team_to_player_names = defaultdict(list)

    for i, match in enumerate(yml["matches"]):
        match["_match number"] = i + 1
        for team in match["teams"]:
            for player in team["players"]:
                name_split = player['name'].split(' ')
                # remove any empty strings from the split
                name_split = [x for x in name_split if x]
                player_to_score[player['name']] = float(player_scores[name_split[0]])
                if len(name_split) == 2:
                    # this is the forced team name
                    forced_team_to_player_names[name_split[1]].append(player['name'])

        for i, team in enumerate(match["teams"]):
            team["team score"] = sum(
                player_to_score[player['name']] for player in team["players"]
            )
            team['team num_players'] = len(team['players'])
            team['team number'] = i + 1

    return forced_team_to_player_names, player_to_score

def get_player_tier(player_score):
    if player_score >= 10:
        return "S"
    elif player_score >= 8:
        return "A" 
    elif player_score >= 6:
        return "B"
    else:
        return "C"


def modifyFile(path):
    yaml_dump = None
    with open(path, 'r') as stream:
        try:
            parsed = yaml.safe_load(stream)
            newYaml = modifyJson(parsed)
            yaml_dump = yaml.dump(newYaml)
            # print(yaml_dump)
        except yaml.YAMLError as exc:
            print(exc)
            print("NOT YAML")
        with open(path, 'w') as stream:
            try:
                stream.write(yaml_dump)
            except yaml.YAMLError as exc:
                print("could not write")


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*" + CURRENT_TEAM_FILENAME]

    def on_modified(self, event):
        # print(event.src_path, event.event_type)
        modifyFile(event.src_path)


if __name__ == "__main__" or __name__ == "builtins":
    modifyFile("text_files/" + CURRENT_TEAM_FILENAME)

# if __name__ == "__main__":
if __name__ == "__main__" and False:
    observer = Observer()
    observer.schedule(MyHandler(), path=sys.argv[1] if len(sys.argv) > 1 else 'text_files')
    observer.start()

    try:
        while True:
            time.sleep(4)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
