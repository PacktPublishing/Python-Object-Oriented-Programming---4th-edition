"""
Python 3 Object-Oriented Programming Case Study

Chapter 4, Expecting the Unexpected
"""
import base64
import csv
from pathlib import Path
from pytest import *
import classifier


@fixture(scope="module")
def app_client():
    test_users = [
        classifier.User(
                username='noriko',
                email='noriko@example.com',
                real_name='Noriko K. L.',
                role=classifier.Role.BOTANIST,
                password='md5$H5W30kno$10a2327b2fce08c1ad0f65a12d40552f'
            ),
        classifier.User(
            username='emma',
            email='emma@example.com',
            real_name='Emma K.',
            role=classifier.Role.RESEARCHER,
            password='md5$F8ZVxsuE$ebf71d15067ed7c887c0408550b671e2'
        )
    ]
    with classifier.app.app_context():
        classifier.app.config['TESTING'] = True
        classifier.app.config['USER_FILE'] = Path.cwd()/"test_data"
        for u in test_users:
            classifier.users.add_user(u)

    yield classifier.app.test_client()


def test_health_check(app_client):
    result = app_client.get("health")
    assert result.status_code == 200
    assert result.json == {
        "status": "OK",
        "user_count": 2,
        "users": [
            {
                'email': 'noriko@example.com',
                'role': 'botanist',
                'password': 'md5$H5W30kno$10a2327b2fce08c1ad0f65a12d40552f',
                'real_name': 'Noriko K. L.',
                'username': 'noriko'
             },
            {
                'email': 'emma@example.com',
                'role': 'researcher',
                'password': 'md5$F8ZVxsuE$ebf71d15067ed7c887c0408550b671e2',
                'real_name': 'Emma K.',
                'username': 'emma'

            },
        ]
    }


def test_whoami_good(app_client):
    credentials = base64.b64encode("noriko:Hunter2".encode("utf-8"))
    result = app_client.get(
        "whoami",
        headers={
            "Authorization": f"BASIC {credentials.decode('ASCII')}"
        }
    )
    assert result.status_code == 200
    print(result.json)
    assert result.json["status"] == "OK"


def test_whoami_bad(app_client):
    credentials = base64.b64encode("noriko:not my passowrd".encode("utf-8"))
    result = app_client.get(
        "whoami",
        headers={
            "Authorization": f"BASIC {credentials.decode('ASCII')}"
        }
    )
    assert result.status_code == 401
    print(result.json)
    assert result.json["message"] == "Unknown User"
