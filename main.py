from __future__ import annotations

from src.project_chat.config import Config
from src.project_chat.config import create_config_with_args
from src.project_chat.config import parse_arguments
from src.project_chat.retrieve import retrieve
from src.project_chat.vectorize import vectorize


def main():
    """
    The `main` function parses command-line arguments using a specified
    configuration, creates a configuration object based on those arguments, and
    then prints the resulting configuration.
    :return: A configuration object created from parsed command-line arguments.
    """
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    db = vectorize(config)
    qa = retrieve(db, config)
    print(qa.invoke({"role": "user", "content": config.question})["answer"])


if __name__ == "__main__":
    exit(main())
