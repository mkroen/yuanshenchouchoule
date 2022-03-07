import os
from app.helpers.config_helper import load_env_from_yaml_file, StrConfigKey
from pathlib import Path

env_file_name = os.getenv("ENV_FILE_NAME", "env.yaml")
PROJECT_HOME = Path(__file__).absolute().parent.parent
load_env_from_yaml_file(PROJECT_HOME.joinpath(env_file_name))

REDIS_URL = StrConfigKey(env_key="REDIS_URL", require=True).to_value()
SQLALCHEMY_DATABASE_URI = StrConfigKey(env_key="SQLALCHEMY_DATABASE_URI", require=True).to_value()
