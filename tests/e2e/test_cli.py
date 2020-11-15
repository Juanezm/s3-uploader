from click.testing import CliRunner
from s3uploader.entrypoints.cli import main


def test_main(test_config_file, test_base_directory):
    config_file = test_config_file[0]
    runner = CliRunner()
    result = runner.invoke(main, [config_file])
    assert result.exit_code == 0
