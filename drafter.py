#!/usr/bin/env python3

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
    player_to_score = {}
    for i, match in enumerate(yml["matches"]):
        match["_match number"] = i + 1
        for team in match["teams"]:
            # team["team score"] = sum([int(player['name'].split(' ')[-1]) for player in team["players"]])
            # team['team num_players'] = len(team['players'])
            for player in team["players"]:
                player_to_score[player['name']] = int(player['name'].split(' ')[-1])
        for i, team in enumerate(match["teams"]):
            team["team score"] = sum([player_to_score[player['name']] for player in team["players"]])
            team['team num_players'] = len(team['players'])
            team['team number'] = i + 1

    # Also, add in "proposed_team_1" and "proposed_team_2" to each match
    # Create the proposed teams by enumerating all possible combinations of players
    # in which the team size is equal or +1/-1 of each other
    # Then, for each match, add in the proposed teams

    possible_teams = []
    total_players = len(player_to_score)
    players_and_scores = sorted(player_to_score.items(), key=lambda x: x[1], reverse=True)
    # now shuffle it
    import random

    best_min_score_delta = 999
    already_seen_teams = set()

    # Choose 100 random teams
    for i in range(100):
        random.shuffle(players_and_scores)
        team1 = []
        team2 = []
        # First put half of the players on team 1
        # num_players_on_team_1 = total_players // 2
        # Choose a random number of players on team 1 which is +- 1 of the other team
        num_players_on_team_1 = random.randint(total_players // 2 - 1, total_players // 2 + 1)

        for j in range(num_players_on_team_1):
            team1.append(players_and_scores[j])
        # Then put the remaining on team 2
        for j in range(num_players_on_team_1, total_players):
            team2.append(players_and_scores[j])

        # Add team1 to the already seen teams
        # First sort the team by score
        already_seen_key = tuple(sorted(team1, key=lambda x: x[1], reverse=True))
        if already_seen_key in already_seen_teams:
            continue
        already_seen_teams.add(already_seen_key)

        # Now, calculate the score delta
        team1_score = sum([x[1] for x in team1])
        team2_score = sum([x[1] for x in team2])
        score_delta = abs(team1_score - team2_score)
        if score_delta <= best_min_score_delta:
            best_min_score_delta = score_delta
            best_team1 = team1
            best_team2 = team2
            print("New best team found with score delta of {}".format(score_delta))
            # Print with teams sorted by score
            print("Team 1 (score: {} #players: {}): {}".format(team1_score, len(team1), sorted(team1, key=lambda x: x[1], reverse=True)))
            print("Team 2 (score: {} #players: {}): {}".format(team2_score, len(team2), sorted(team2, key=lambda x: x[1], reverse=True)))

    for match in yml["matches"]:
        match["proposed_team_1"] = [x[0] for x in sorted(best_team1, key=lambda x: x[1], reverse=True)]
        match["proposed_team_2"] = [x[0] for x in sorted(best_team2, key=lambda x: x[1], reverse=True)]
        match["proposed_team_1_score"] = sum([x[1] for x in best_team1])
        match["proposed_team_2_score"] = sum([x[1] for x in best_team2])

    return yml


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
