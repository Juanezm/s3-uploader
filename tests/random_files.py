import random
from pathlib import Path


def generate_random_files_tree(base_dir: str):
    year = 2020
    month = random.randint(1, 13)
    day = random.randint(1, 31)
    new_files = list()
    for x in range(1, random.randint(1, 20) + 1):
        location = random.choice(('office', 'bedroom', 'kitchen', 'bathroom'))
        hour = random.randint(1, 24)
        minute = random.randint(1, 60)
        test_dir_path = Path(base_dir) / f"{location}/{year}/{month}/{day}/{hour}"
        test_dir_path.mkdir(parents=True, exist_ok=True)
        test_file = test_dir_path / f"{minute}-topic.dat"
        with open(test_file, "w") as file:
            file.write("This is a test file info")
        new_files.append(test_file)
    return new_files
