import re
from datetime import datetime

from .interface import LogParser


class PlaytimeParser(LogParser):
    def __init__(self):
        self.playtime = {}
        self.login_times = {}

    def process_line(self, line: str) -> None:
        login_match = re.search(
            r"\[.*\] \[Server thread/INFO\] \[.*\]: ([a-zA-Z0-9_]+) joined the game",
            line,
        )
        if login_match:
            player = login_match.group(1)
            self.login_times[player] = datetime.strptime(line[1:9], "%H:%M:%S")

        logout_match = re.search(
            r"\[.*\] \[Server thread/INFO\] \[.*\]: (.+) left the game", line
        )
        if logout_match:
            player = logout_match.group(1)
            logout_time = datetime.strptime(line[1:9], "%H:%M:%S")
            if player in self.login_times:
                session_time = (logout_time - self.login_times[player]).total_seconds()
                if player not in self.playtime:
                    self.playtime[player] = 0
                self.playtime[player] += session_time
                del self.login_times[player]

    def get_stats(self):
        return self.playtime
