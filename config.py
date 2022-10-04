from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class GeneralConfig:
    secret_key: str


@dataclass
class DatabaseConfig:
    name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class Config:
    general: GeneralConfig
    database: DatabaseConfig


def init_config(config_path: Path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config(
        general=GeneralConfig(
            raw_config['general']['secret-key']
        ),
        database=DatabaseConfig(
            name=raw_config['database']['name'],
            user=raw_config['database']['user'],
            password=raw_config['database']['password'],
            host=raw_config['database']['host'],
            port=raw_config['database']['port']
        )
    )
    return config
