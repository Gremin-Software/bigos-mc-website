import gzip
import os
import zipfile
from typing import Iterable

import pandas as pd

from .interface import LogParser


def parse_log_file(file_path: str, parsers: Iterable[LogParser]) -> None:
    if file_path.endswith(".gz"):
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            for line in f:
                for parser in parsers:
                    parser.process_line(line)
    elif file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            for filename in zip_ref.namelist():
                with zip_ref.open(filename) as f:
                    for line in f:
                        line = line.decode("utf-8")
                        for parser in parsers:
                            parser.process_line(line)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                for parser in parsers:
                    parser.process_line(line)


def aggregate_logs(log_dir: str, parsers: Iterable[LogParser]) -> None:
    for root, _, files in os.walk(log_dir):
        for file in files:
            if "debug" in file:
                continue
            if (
                file.endswith(".log")
                or file.endswith(".log.gz")
                or file.endswith(".log.zip")
            ):
                file_path = os.path.join(root, file)
                parse_log_file(file_path, parsers)


def display_results(parsers: Iterable[LogParser]) -> None:
    for parser in parsers:
        stats = parser.get_stats()
        df = pd.DataFrame(
            stats.items(),
            columns=["Player", type(parser).__name__.replace("Parser", "")],
        )
        print(df)
