import requests
import json
from helper.global_config import private_config

HEADER = {'Content-Type': 'application/json', 'Vary': 'accept'}
Response = requests.Response


def GET(api_path: str, payload=None) -> Response:
    """
    This Method sends a GET REST API call

    :param api_path: it is the path for the REST API call
    :param payload: is optional and is the payload to send with the call

    :return: REST API call response which can return status_code, json, text and more.
    """
    get_it = requests.get(
        f'http://{private_config["API_IP"]}/api/v2.0{api_path}',
        headers=HEADER,
        auth=(private_config['API_USER'], private_config["API_PASSWORD"]),
        data=json.dumps(payload) if payload else None
    )
    return get_it


def POST(api_path: str,  payload=None) -> Response:
    """
    This Method sends a POST REST API call

    :param api_path: it is the path for the REST API call
    :param payload: is optional and is the payload to send with the call

    :return: REST API call response which can return status_code, json, text and more.
    """
    post_it = requests.post(
        f'http://{private_config["API_IP"]}/api/v2.0{api_path}',
        headers=HEADER,
        auth=(private_config['API_USER'],private_config["API_PASSWORD"]),
        data=json.dumps(payload) if payload else None
    )
    return post_it


def PUT(api_path: str, payload=None) -> Response:
    """
    This Method sends a PUT REST API call

    :param api_path: it is the path for the REST API call
    :param payload: is optional and is the payload to send with the call

    :return: REST API call response which can return status_code, json, text and more.
    """
    put_it = requests.put(
        f'http://{private_config["API_IP"]}/api/v2.0{api_path}',
        headers=HEADER,
        auth=(private_config['API_USER'],private_config["API_PASSWORD"]),
        data=json.dumps(payload) if payload else None
    )
    return put_it


def DELETE(api_path: str, payload=None) -> Response:
    """
    This Method sends a DELETE REST API call

    :param api_path: it is the path for the REST API call
    :param payload: is optional and is the payload to send with the call

    :return: REST API call response which can return status_code, json, text and more.
    """
    delete_it = requests.delete(
        f'http://{private_config["API_IP"]}/api/v2.0{api_path}',
        headers=HEADER,
        auth=(private_config['API_USER'],private_config["API_PASSWORD"]),
        data=json.dumps(payload) if payload else None
    )
    return delete_it
