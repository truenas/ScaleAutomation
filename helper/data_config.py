import csv
from helper.global_config import get_test_data_path


def get_data_list(file_path: str) -> list:
    """
    This methode return the list of dictionary for pytest parametrize.

    :param file_path: the path to the file to use in test_data
    :return: the list of dictionary from the CSV file.
    """
    file = open(get_test_data_path(file_path), 'r')
    reader = csv.DictReader(file)
    return list(reader)


def get_data_and_name_list(file_name: str, object_name: str) -> list:
    """
    This methode return the list of tuple for pytest parametrize.
    :param file_name: The name of the file to use in test_data
    :param object_name: The name of the object to get from the list data
    :return: The list of tuple for pytest parametrize

    Usage:
        - @pytest.mark.parametrize('layout,data', get_data_and_name_list('create-data-pool', 'pool-layout'))
        - @pytest.mark.parametrize(['layout','data'], get_data_and_name_list('create-data-pool', 'pool-layout'))
    """
    data_list = get_data_list(file_name)
    object_list = [line[object_name] for line in data_list]
    return list(zip(object_list, data_list))
