import json
from pathlib import Path
import shutil
import pytest

from random_files import generate_random_files_tree


@pytest.fixture
def test_file():
    test_dir_parent_path = Path(__file__).parent / 'office'
    test_dir_path = test_dir_parent_path / '2020' / '11' / '15' / '23'
    test_dir_path.mkdir(parents=True, exist_ok=True)
    test_file = test_dir_path / "30-topic.dat"
    with open(test_file, "w") as file:
        file.write("This is a test file info")
    yield str(test_file)
    test_file.unlink()
    shutil.rmtree(test_dir_parent_path)


@pytest.fixture
def test_base_directory():
    base_dir = Path(__file__).parent / 'base_dir'
    new_files = generate_random_files_tree(str(base_dir))
    yield str(base_dir), len(new_files)
    shutil.rmtree(base_dir)


@pytest.fixture
def test_config_file():
    test_config_file = Path(__file__).parent / "test_config_file.json"
    base_dir = str(Path(__file__).parent)
    bucket = 'bucket'
    config = {
        'base_dir': base_dir,
        's3_bucket': bucket
    }
    with open(test_config_file, "w") as json_file:
        json.dump(config, json_file)
    yield str(test_config_file), base_dir, bucket
    test_config_file.unlink()
