"""
Python 3 Object-Oriented Programming Case Study

Chapter 5, When to Use Object-Oriented Programming
"""

from textwrap import dedent
import classifier
from classifier import User, Users, Role
from flask import current_app
from pytest import *

@fixture
def user_noriko():
    u = User(
        username="noriko",
        email="noriko@example.com",
        real_name="Noriko K. L.",
        role=Role.BOTANIST,
        password='pbkdf2:sha256:150000$mofx2fJU$a008dc0974620e5848709e022981f74abeb62eaa665d272eff5511e8c57dca3a'
    )
    return u

def test_user(user_noriko):
    assert user_noriko.is_valid_password("sesame")

    user_noriko.set_password("new_password")
    assert not user_noriko.is_valid_password("sesame")
    assert user_noriko.is_valid_password("new_password")

    assert user_noriko.role == Role.BOTANIST
    assert user_noriko.role != Role.RESEARCHER


@fixture
def user_database(tmp_path, user_noriko):
    with classifier.app.app_context():
        user_file = tmp_path / "users.csv"
        classifier.app.config['TESTING'] = True
        classifier.app.config['USER_FILE'] = user_file

        seed_users = classifier.Users()
        seed_users.init_app(current_app)
        seed_users.add_user(
            User(
                username='xander',
                email='xander@example.com',
                real_name='Xander L.',
                role=Role.RESEARCHER,
                password='sha1$oSzv7O8N$aaa6407c35aad7c2f8ee874e1b583d40be708758'
            )
        )
        seed_users.add_user(
            User(
                username='jen',
                email='jen@example.com',
                real_name='Jen K.',
                role=Role.RESEARCHER,
                password='sha1$AM471O9b$fde97e0ca99644f1271a1c3e69cf97d83bf0165c'
            )
        )
        seed_users.add_user(user_noriko)
        seed_users.save()

        users = classifier.Users()
        users.init_app(current_app)
        yield users

def test_users(user_database, user_noriko):
    assert user_database.get_user("noriko") == user_noriko
    assert user_database.get_user("noriko").is_valid_password("sesame")
    assert len(user_database) == 3
