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
    for i, match in enumerate(yml["matches"]):
        match["_match number"] = i + 1
        for team in match["teams"]:
            team["team score"] = sum([int(player['name'].split(' ')[-1]) for player in team["players"]])
            team['team num_players'] = len(team['players'])
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
