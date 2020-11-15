import logging

import click
from boto3.exceptions import S3UploadFailedError
from s3uploader.load_config import load_config_file, LOG_LEVEL, LOG_FORMAT
from s3uploader.domain.operations import check_dat_files_in_dir, \
    upload_file_to_s3, generate_object_name, delete_uploaded_dat_files_from_disk

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


@click.command()
@click.argument('config_file')
def main(config_file: str):
    base_dir, bucket = load_config_file(config_file)
    new_files = check_dat_files_in_dir(base_dir)
    uploaded_files = list()

    for file_name in new_files:
        object_name = generate_object_name(file_name)
        try:
            upload_file_to_s3(file_name=file_name,
                              bucket=bucket,
                              object_name=object_name)
            uploaded_files.append(file_name)
            logging.info(f"{file_name} has been uploaded to {bucket}.")
        except S3UploadFailedError as e:
            logging.warning(e)

    delete_uploaded_dat_files_from_disk(uploaded_files)


if __name__ == '__main__':
    main()
