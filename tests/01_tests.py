import requests

URL_TEST_SERVICE = "http://127.0.0.1:8000/"


def test_get_updated():
    response = requests.get(URL_TEST_SERVICE + "posts")
    assert response.status_code == 200


def test_get_posts():
    response = requests.get(URL_TEST_SERVICE + "update")
    assert response.status_code == 200


def test_check_type_response_posts():
    response = requests.get(URL_TEST_SERVICE + "posts")
    assert isinstance(response.json(), list)


def test_check_limit_response_posts():
    response = requests.get(URL_TEST_SERVICE + "posts?limit=10")
    assert len(response.json()) == 10


def test_check_limit_invalid_value():
    response = requests.get(URL_TEST_SERVICE + "posts?limit=-4")
    assert len(response.json()) == 4
    response = requests.get(URL_TEST_SERVICE + "posts?limit=hdfh001")
    result = response.json()
    assert result.get("error") == 'Invalid parameter limit'
