from abc import ABC, abstractmethod


class LogParser(ABC):
    @abstractmethod
    def process_line(self, line: str) -> None:
        raise NotImplementedError()
