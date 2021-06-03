"""
Python 3 Object-Oriented Programming Case Study

Chapter 9. Strings and Serialization
"""
from __future__ import annotations
import base64
import csv
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from typing import (
    cast,
    Optional,
    Callable,
    Any,
    Type,
    Mapping,
    overload,
    Iterable,
    Union,
    Iterator,
)
import werkzeug.security
from flask import Flask, current_app, jsonify, request, abort, g, Response


class Role(str, Enum):
    UNDEFINED = ""
    BOTANIST = "botanist"
    RESEARCHER = "researcher"


class User:
    """
    A user. Has a Role: Botanist or Researcher.
    The password must be of the form: ``method$salt$hexdigest``.
    For example: ``"md5$ZD8agylg$90c2494aa8a4965b20410e4cdb9e823d"``
    """

    headers = ["username", "email", "real_name", "role", "password"]

    def __init__(
        self,
        username: str,
        email: str,
        real_name: str,
        role: Role,
        password: Optional[str] = None,
    ) -> None:
        self.username = username
        self.email = email
        self.real_name = real_name
        self.role = role
        self.password = password

    @staticmethod
    def from_dict(csv_row: dict[str, str]) -> "User":
        return User(
            username=csv_row["username"],
            email=csv_row["email"],
            real_name=csv_row["real_name"],
            role=Role(csv_row["role"]),
            password=csv_row["password"],
        )

    def __eq__(self, other: Any) -> bool:
        other = cast(User, other)
        return all(
            [
                self.username == other.username,
                self.email == other.email,
                self.real_name == other.real_name,
                self.role == other.role,
            ]
        )

    def set_password(self, plain_text: str) -> None:
        self.password = werkzeug.security.generate_password_hash(plain_text)

    def valid_password(self, plain_text: str) -> bool:
        return werkzeug.security.check_password_hash(
            self.password or "md5$$", plain_text
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"real_name={self.real_name!r}, "
            f"role={self.role.value!r}, "
            f"password={self.password!r})"
        )

    def asdict(self) -> dict[str, Optional[str]]:
        return {
            "username": self.username,
            "email": self.email,
            "real_name": self.real_name,
            "role": self.role.value,
            "password": self.password,
        }


class Users:
    def __init__(self, init: Optional[dict[str, User]] = None) -> None:
        self.users = init or {}
        self.anonymous = User("", "", "", Role.UNDEFINED)
        self.app: Optional[Flask] = None

    def init_app(self, app: Flask) -> None:
        self.app = app
        self.app.config.setdefault("USER_FILE", Path("users.csv"))

    def get_user(self, name: str, default: Optional[User] = None) -> User:
        if not self.app:
            raise RuntimeError("Users not bound to an app")
        if not self.users:
            # Load file when needed.
            with self.app.config["USER_FILE"].open() as user_file:
                row_iter = csv.DictReader(user_file)
                user_iter = (User.from_dict(row) for row in row_iter if row)
                self.users = {user.username: user for user in user_iter}
        return self.users.get(name, default or self.anonymous)

    def add_user(self, user: User) -> None:
        if user.username in self.users:
            raise ValueError("Duplicate Username")
        self.users[user.username] = user

    def save(self) -> None:
        if not self.app:
            raise RuntimeError("Users not bound to an app")
        with self.app.config["USER_FILE"].open("w", newline="") as user_file:
            writer = csv.DictWriter(user_file, User.headers)
            writer.writeheader()
            writer.writerows(u.asdict() for u in self.users.values())

    def __len__(self) -> int:
        return len(self.users)

    def values(self) -> Iterator[User]:
        return iter(self.users.values())


class NotAuthorized(Exception):
    status_code = 401

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict[str, Any]:
        rv: dict[str, Any] = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def authenticate(view_function: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(view_function)
    def decorated_function(*args: str) -> Response:
        auth_header = request.headers.get("Authorization", "")
        if auth_header:
            auth_body = auth_header.split(" ")
        else:
            auth_body = [""]
        auth_type, credentials = auth_body if len(auth_body) == 2 else ("", ":")
        username, _, password = (
            base64.b64decode(credentials).decode("utf-8").partition(":")
        )
        g.user = users.get_user(username)  # type: ignore[attr-defined]
        conditions = [
            auth_type.upper() == "BASIC",
            g.user.valid_password(password),  # type: ignore[attr-defined]
        ]
        if not all(conditions):
            raise NotAuthorized("Unknown User")
        return view_function(*args)

    return decorated_function


class Config:
    USER_FILE = Path("data/users.csv")


class Demo(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True


app = Flask(__name__)
app.config.from_object(Demo)  # os.environ["CLASSIFIER_CONFIG"]
users = Users()
users.init_app(app)


@app.errorhandler(NotAuthorized)  # type: ignore[misc]
def handle_unauthorized(error: NotAuthorized) -> Response:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/health")
def user_list() -> Response:
    # Be sure the users database gets loaded.
    users.get_user("")
    response = {"status": "OK", "user_count": len(users)}
    if app.config["TESTING"]:
        response["users"] = [u.asdict() for u in users.values()]
    return jsonify(response)


@app.route("/whoami")
@authenticate
def who_am_i() -> Response:
    app.logger.info(
        f"whoami with {request.headers}: User {g.user}"  # type: ignore[attr-defined]
    )
    return jsonify(
        {
            "status": "OK",
            "user": g.user.asdict(),  # type: ignore[attr-defined]
        }
    )


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
