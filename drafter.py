#!/usr/bin/env python3

import yaml
import sys
import time
import logging
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from watchdog.events import LoggingEventHandler

CURRENT_TEAM_FILENAME = "current_teams.yml"

def modifyYaml(yml):

class MyHandler(PatternMatchingEventHandler):
   patterns = ["*" + CURRENT_TEAM_FILENAME]

   def on_modified(self, event):
       # print(event.src_path, event.event_type)
       with open(event.src_path, 'r') as stream:
           try:
                parsed = yaml.safe_load(stream)
                newYaml = modifyYaml(parsed)

           except yaml.YAMLError as exc:
               print(exc)
               print("NOT YAML")


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=sys.argv[1] if len(sys.argv) > 1 else 'text_files')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
