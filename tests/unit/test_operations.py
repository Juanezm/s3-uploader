from pathlib import Path

import boto3
from moto import mock_s3
from s3uploader.domain.operations import generate_object_name, check_dat_files_in_dir, \
    delete_uploaded_dat_files_from_disk, upload_file_to_s3, delete_empty_folders_in_dir
import random


@mock_s3
def test_upload_file_to_s3(test_file):
    bucket = 'testbucket'
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket=bucket)

    object_name = generate_object_name(test_file)
    upload_file_to_s3(file_name=test_file, bucket=bucket, object_name=object_name)

    uploaded_object = conn.Object(bucket, object_name)
    body = uploaded_object.get()['Body'].read().decode("utf-8")

    assert body == 'This is a test file info'


def test_generate_object_name():
    test_file_name = '/dir/dir/base_dir/location/YYYY/MM/DD/HH/mm-topic.dat'
    object_name = generate_object_name(test_file_name)
    assert object_name == 'location/YYYY/MM/DD/HH/mm-topic.dat'


def test_check_dat_files_in_dir(test_base_directory):
    base_directory, number_new_files = test_base_directory
    new_files = check_dat_files_in_dir(base_directory)
    assert len(new_files) == number_new_files


def test_delete_uploaded_dat_files_from_disk(test_base_directory):
    base_directory, number_new_files = test_base_directory
    files = [str(x) for x in Path(base_directory).glob('**/*.dat') if x.is_file()]
    uploaded_files = files[:random.randint(1, number_new_files)]
    delete_uploaded_dat_files_from_disk(uploaded_files)
    files_after_delete = [str(x) for x in Path(base_directory).glob('**/*.dat') if x.is_file()]
    assert sorted(list(set(files) - set(uploaded_files))) == sorted(files_after_delete)
