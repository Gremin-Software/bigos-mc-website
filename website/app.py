import logging

import pandas as pd
from flask import Flask, render_template, request

from log_parser import DeathsParser, PlaytimeParser, aggregate_logs

MC_LOG_DIR = "./logs"

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)


@app.route("/")
def home():
    logging.info("Home page accessed from %s", request.remote_addr)
    return render_template("homepage.html")


@app.route("/stats")
def stats():
    logging.info("Stats page accessed from %s", request.remote_addr)

    try:
        deaths_parser = DeathsParser()
        playtime_parser = PlaytimeParser()

        logging.debug("Starting to aggregate logs from directory: %s", MC_LOG_DIR)
        aggregate_logs(MC_LOG_DIR, [deaths_parser, playtime_parser])

        deaths_data = {
            "Player": deaths_parser.get_stats().keys(),
            "Deaths": deaths_parser.get_stats().values(),
        }

        playtime_data = {
            "Player": playtime_parser.get_stats().keys(),
            "Playtime": playtime_parser.get_stats().values(),
        }

        logging.debug("Creating DataFrames for deaths and playtime data")
        df_deaths = pd.DataFrame(deaths_data)
        df_playtime = pd.DataFrame(playtime_data)

        df_combined = pd.merge(df_deaths, df_playtime, on="Player", how="outer")

        def seconds_to_hms(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        logging.debug("Formatting playtime data")
        df_combined["Formatted_Playtime"] = df_combined["Playtime"].apply(
            seconds_to_hms
        )
        df_combined = df_combined.fillna(
            {"Deaths": 0, "Playtime": 0, "Formatted_Playtime": "00:00:00"}
        )

        df_combined = df_combined[
            ["Player", "Deaths", "Playtime", "Formatted_Playtime"]
        ]
        df_combined["Deaths"] = df_combined["Deaths"].astype(int)

        columns = df_combined.columns.tolist()
        data = df_combined.to_dict(orient="records")

        logging.info("Successfully generated stats data for rendering")
        return render_template("stats.html", columns=columns, data=data)

    except Exception as e:
        logging.error("Error occurred in /stats route: %s", str(e))
        return "An error occurred while processing the stats.", 500


if __name__ == "__main__":
    logging.info("Starting Flask application")
    app.run(debug=True)
