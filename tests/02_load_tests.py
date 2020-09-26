import requests
import random

URL_TEST_SERVICE = "http://127.0.0.1:8000/"


def get_status(route: str):
    response = requests.get(URL_TEST_SERVICE + route)
    return response.status_code


def test_load():
    link = ['posts', 'update']
    for i in range(1, 20):
        assert get_status(link[random.randint(0, 1)]) == 200
