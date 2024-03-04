import os
import toml
from pathlib import Path

test_cases = str(Path('/test_cases'))
keywords = str(Path('/keywords'))
workdir = os.getcwd().partition(test_cases)[0].partition(keywords)[0]
screenshots = str(Path(f'{workdir}/screenshots'))
home = str(Path.home())
downloads = home + str(Path('/Downloads'))

shared = str(Path('/profiles/shared.toml'))
shared_file = open(workdir + shared, 'r')
shared_config = toml.load(shared_file)

private = str(Path('/profiles/private.toml'))
private_file = open(workdir + private, 'r')
private_config = toml.load(private_file)


def get_test_data_path(file_path: str) -> str:
    """
    This method return the path of the data file compatible with POSIX and Windows

    :param file_path: the path to the test data file.
    :return: the full path of the test data file compatible with POSIX and Windows
    """
    data_test_file = str(Path(f'/test_data/{file_path}.csv'))
    return workdir + data_test_file
