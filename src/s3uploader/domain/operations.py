import logging
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from s3uploader.load_config import get_aws_config, LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def upload_file_to_s3(file_name: str, bucket: str, object_name: str):
    access_key_id, access_key, region_name = get_aws_config()
    s3_client = boto3.client('s3',
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=access_key,
                             region_name=region_name,)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def generate_object_name(file_name: str) -> str:
    return '/'.join(file_name.split('/')[-6:])


def check_dat_files_in_dir(directory: str) -> list:
    directory_path = Path(directory)
    return [str(x) for x in directory_path.glob('**/*.dat') if x.is_file()]


def delete_uploaded_dat_files_from_disk(uploaded_files: list):
    for file in uploaded_files:
        Path(file).unlink()
        logging.debug(f"{file} has been deleted from disk.")


def delete_empty_folders_in_dir(directory: str):
    for dir_path, dir_names, filenames in os.walk(directory, topdown=False):
        if not filenames:
            os.rmdir(dir_path)
