import json
import os
from logging import INFO
from typing import Tuple

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


def get_aws_config() -> Tuple[str, str, str]:
    s3_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'AKIAIOSFODNN7EXAMPLE')
    s3_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')
    s3_default_region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
    return s3_key_id, s3_access_key, s3_default_region


def load_config_file(config_file: str) -> Tuple[str, str]:
    with open(config_file) as json_file:
        config = json.load(json_file)
    return config.get('base_dir'), config.get('s3_bucket')
