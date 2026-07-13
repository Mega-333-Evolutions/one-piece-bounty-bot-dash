from pathlib import Path

# Command
STANDARD_SPLIT_CHAR = "|"

# Environment variables file path
ENV_FILE_PATH = "environment/.env"

# Root directory of the project, used to build paths that must not depend on the current working directory
ROOT_DIR = Path(__file__).resolve().parent

# Directory used to persist local runtime files, e.g. the Telethon session used by TgBot
DATA_DIR = ROOT_DIR / "data"

HIDE_ST_STYLE = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

