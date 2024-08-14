import re

from .interface import LogParser


class DeathsParser(LogParser):
    def __init__(self):
        self.deaths = {}

    def process_line(self, line: str) -> None:
        patterns = [
            r"\[.*\] \[Server thread/INFO\] \[.*\]: ([a-zA-Z0-9_]+) was (slain by|shot by|blown up by|pummeled by|fireballed by|impaled by|squashed by|skewered by|struck by lightning while fighting|frozen to death by|burned to a crisp while fighting|killed while trying to hurt|obliterated by a sonically-charged shriek while trying to escape|was doomed to fall by) .+",
            r"\[.*\] \[Server thread/INFO\] \[.*\]: ([a-zA-Z0-9_]+) (hit the ground too hard|fell from a high place|fell off a ladder|fell off some vines|fell off some weeping vines|fell off some twisting vines|fell off scaffolding|fell while climbing|discovered the floor was lava|burned to death|tried to swim in lava|froze to death|starved to death|suffocated in a wall|fell out of the world|didn't want to live in the same world as|was killed by magic|was shot by a skull from|was poked to death by a sweet berry bush|went up in flames|died|was killed) while (trying to escape|fighting) .+",
            r"\[.*\] \[Server thread/INFO\] \[.*\]: ([a-zA-Z0-9_]+) (was pricked to death|drowned|blew up|hit the ground too hard|fell from a high place|fell off a ladder|fell off some vines|fell off some weeping vines|fell off some twisting vines|fell off scaffolding|fell while climbing|was squashed by a falling block|discovered the floor was lava|burned to death|tried to swim in lava|was struck by lightning|froze to death|starved to death|suffocated in a wall|fell out of the world|left the confines of this world|was poked to death by a sweet berry bush|went up in flames|was killed by magic|was slain by|was obliterated by a sonically-charged shriek|was squished too much|was impaled on a stalagmite|was squashed by a falling anvil|was skewered by a falling stalactite|was killed by even more magic)",
        ]

        for pattern in patterns:
            death_match = re.search(pattern, line)
            if death_match:
                player = death_match.group(1)
                if player not in self.deaths:
                    self.deaths[player] = 0
                self.deaths[player] += 1
                break

    def get_stats(self):
        return self.deaths
