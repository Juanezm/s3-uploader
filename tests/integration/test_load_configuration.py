import os

from s3uploader.load_config import get_aws_config, load_config_file


def test_load_config_file(test_config_file, test_base_directory):
    config_file, exp_base_dir, exp_bucket = test_config_file
    base_dir, bucket = load_config_file(config_file)
    assert base_dir == exp_base_dir
    assert bucket == exp_bucket


def test_get_aws_config():
    # Save original values to restore after the test
    s3_key_id_value = os.environ.get('AWS_ACCESS_KEY_ID')
    s3_access_key_value = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_default_region_value = os.environ.get('AWS_DEFAULT_REGION')

    s3_key_id_test_value = 'test_key_id'
    s3_access_key_test_value = 'test_access_key'
    s3_default_region_test_value = 'test_default_region'

    os.environ['AWS_ACCESS_KEY_ID'] = s3_key_id_test_value
    os.environ['AWS_SECRET_ACCESS_KEY'] = s3_access_key_test_value
    os.environ['AWS_DEFAULT_REGION'] = s3_default_region_test_value

    s3_key_id, s3_access_key, s3_default_region = get_aws_config()

    # Restore original values
    if s3_key_id_value:
        os.environ['AWS_ACCESS_KEY_ID'] = s3_key_id_value
    else:
        del os.environ['AWS_ACCESS_KEY_ID']

    if s3_access_key_value:
        os.environ['AWS_SECRET_ACCESS_KEY'] = s3_access_key_value
    else:
        del os.environ['AWS_SECRET_ACCESS_KEY']

    if s3_default_region_value:
        os.environ['AWS_DEFAULT_REGION'] = s3_default_region_value
    else:
        del os.environ['AWS_DEFAULT_REGION']

    assert s3_key_id == s3_key_id_test_value
    assert s3_access_key == s3_access_key_test_value
    assert s3_default_region == s3_default_region_test_value
