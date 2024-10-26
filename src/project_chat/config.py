from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import Type

import toml
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field

from .custom_argument_parser import CustomArgumentParser

load_dotenv()


class Config(BaseModel):
    _root: Path = Path(__file__).parent
    persistence: Path = _root / ".persistence"
    pos_args: list[str] = Field(default_factory=list)
    repo_path: Path
    model: str
    question: str
    config_file: Optional[Path] = None


def parse_arguments(config_class: Type[Config]):
    """
    Parses command-line arguments based on the fields defined in the provided
    configuration class.
    :param config_class: A class that defines the model fields for
    configuration.
    :return: Parsed command-line arguments object.
    """
    parser = CustomArgumentParser(
        description="Configure the application settings."
    )

    for name, value in config_class.model_fields.items():
        if name.startswith("_"):
            continue
        annotation = value.annotation
        if len(getattr(value.annotation, "__args__", [])) > 1:
            annotation = next(filter(None, value.annotation.__args__))
        parser.add_argument(
            f"--{name}" if name != "pos_args" else name,
            type=annotation,
            default=value.default,
            help=f"Default: {value}",
        )

    return parser.parse_args()


def create_config_with_args(config_class: Type[Config], args) -> Config:
    """
    Creates a configuration object from a specified configuration class and
    command-line arguments, optionally loading additional settings from a
    configuration file.
    :param config_class: The configuration class used to create the config
    object.
    :param args: Command-line arguments containing potential configuration
    values.
    :return: A configuration object of type Config.
    """
    arg_dict = {
        name: getattr(args, name)
        for name in config_class.model_fields
        if hasattr(args, name)
    }
    if arg_dict.get("config_file") and Path(arg_dict["config_file"]).exists():
        config = config_class(
            **{
                **arg_dict,
                **toml.load(arg_dict.get("config_file")),
            }
        )
    else:
        config = config_class(**arg_dict)
    for variable in config.model_fields:
        value = getattr(config, variable)
        if (
            isinstance(value, Path)
            and value.suffix == ""
            and not value.exists()
        ):
            value.mkdir(parents=True)
    return config
