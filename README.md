# S3 Uploader

## Requirements

A program that uploads files from a local directory to an AWS S3 bucket, following these requirements:

- The program should run on Linux
- The program will be given a base directory path and target s3 bucket name as configuration.
- The environment will provide the AWS credentials and region.
- The program will be executed on a timer (e.g systemd or cron)
- The base directory given in the configuration follows this structure: base-dir/location/YYYY/MM/DD/HH/mm-topic.dat
- The dat files are generated by another service, and files will usually be finished writing within a few seconds of the timestamp of the data.
- The uploaded objects must be in the same directory structure as the base directory.
- dat files that have been successfully uploaded should be deleted from the base directory.

## Installation

### Installing Python

Python 3.5+ installed is required.

To install python

```
sudo apt update
sudo apt upgrade
sudo apt install software-properties-common
sudo apt-get install python3
```

To install pip

```
apt install python-pip
```

### Installing the tool

```
cd s3-uploader
pip install .
```

## Testing
Different unit, integration and e2e tests have been provided to ensure the tool meet the requirements listed above. 
To execute them (recommended use of virtual environment):
```
> python3 -m venv venv
> source venv/bin/activate
> pip install .
> python -m pytest tests -v
========================================================================================================================== test session starts ==========================================================================================================================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /Users/juanezm/Github/s3-uploader/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/juanezm/Github/s3-uploader/tests, configfile: pytest.ini
collected 7 items                                                                                                                                                                                                                                                       

tests/e2e/test_cli.py::test_main PASSED                                                                                                                                                                                                                           [ 14%]
tests/integration/test_load_configuration.py::test_load_config_file PASSED                                                                                                                                                                                        [ 28%]
tests/integration/test_load_configuration.py::test_get_aws_config PASSED                                                                                                                                                                                          [ 42%]
tests/unit/test_operations.py::test_upload_file_to_s3 PASSED                                                                                                                                                                                                      [ 57%]
tests/unit/test_operations.py::test_generate_object_name PASSED                                                                                                                                                                                                   [ 71%]
tests/unit/test_operations.py::test_check_dat_files_in_dir PASSED                                                                                                                                                                                                 [ 85%]
tests/unit/test_operations.py::test_delete_uploaded_dat_files_from_disk PASSED                                                                                                                                                                                    [100%]

========================================================================================================================== 7 passed in 16.54s ===========================================================================================================================
```


## Usage
The CLI tool can be invoked using ```s3-uploader-cli```:
```
> s3-uploader-cli --help
Usage: s3-uploader-cli [OPTIONS] CONFIG_FILE

Options:
  --help  Show this message and exit.

```

A configuration file is required with the following structure:
```
{
    "base_dir": "base_dir_path", 
    "s3_bucket": "bucket_name"
}
```

An execution example:
```
> s3-uploader-cli config.json
2020-11-15 20:31:40,717 -   INFO - /base_dir/bedroom/2020/13/29/20/46-topic.dat has been uploaded to bucket.
2020-11-15 20:31:40,981 -   INFO - /base_dir/bedroom/2020/13/29/21/41-topic.dat has been uploaded to bucket.
2020-11-15 20:31:41,096 -   INFO - /base_dir/bedroom/2020/13/29/12/50-topic.dat has been uploaded to bucket.
2020-11-15 20:31:41,208 -   INFO - /base_dir/bathroom/2020/13/29/10/21-topic.dat has been uploaded to bucket.
2020-11-15 20:31:41,322 -   INFO - /base_dir/bathroom/2020/13/29/10/38-topic.dat has been uploaded to bucket.
2020-11-15 20:31:41,428 -   INFO - /base_dir/kitchen/2020/13/29/6/54-topic.dat has been uploaded to bucket.

```

An execution example with incorrect credentials:
```
> s3-uploader-cli config.json
2020-11-15 20:24:05,642 - WARNING - Failed to upload /base_dir/bedroom/2020/13/29/20/46-topic.dat to bucket/bedroom/2020/13/29/20/46-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
2020-11-15 20:24:06,652 - WARNING - Failed to upload /base_dir/bedroom/2020/13/29/21/41-topic.dat to bucket/bedroom/2020/13/29/21/41-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
2020-11-15 20:24:07,660 - WARNING - Failed to upload /base_dir/bedroom/2020/13/29/12/50-topic.dat to bucket/bedroom/2020/13/29/12/50-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
2020-11-15 20:24:08,674 - WARNING - Failed to upload /base_dir/bathroom/2020/13/29/10/21-topic.dat to bucket/bathroom/2020/13/29/10/21-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
2020-11-15 20:24:09,690 - WARNING - Failed to upload /base_dir/bathroom/2020/13/29/10/38-topic.dat to bucket/bathroom/2020/13/29/10/38-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
2020-11-15 20:24:10,713 - WARNING - Failed to upload /base_dir/kitchen/2020/13/29/6/54-topic.dat to bucket/kitchen/2020/13/29/6/54-topic.dat: An error occurred (InvalidAccessKeyId) when calling the PutObject operation: The AWS Access Key Id you provided does not exist in our records.
```

## Deployment
If we want this tool to be executed every certain amount of time we can add it as a cron job.

To edit crontab file
```
> crontab -e
```

Insert the cron job below if you would like to run it every minute:
```
*/1 * * * * /usr/local/bin/s3-uploader-cli /path/to/config.json
```

## Further improvements
- [ ] Add persistence to store uploaded files, to list them if necessary without using AWS.
- [ ] Add a clean up function to delete tree of empty folders after deleting file from disk.