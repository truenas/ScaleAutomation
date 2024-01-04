import csv
from helper.global_config import get_test_data_path


def get_data_list(file_name: str) -> list:
    """
    This methode return the list of dictionary for pytest parametrize.

    :param file_name: the name of the file to use in test_data
    :return: the list of dictionary from the CSV file.
    """
    file = open(get_test_data_path(file_name), 'r')
    reader = csv.DictReader(file)
    return list(reader)
