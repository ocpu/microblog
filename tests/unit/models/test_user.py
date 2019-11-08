"""
Contains tests for app.models.User class
"""
# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta
from unittest import mock
import pytest
from app import db
from app.models import User, Post


@pytest.fixture
def user1():
    """
    User object
    """
    return User(
        username='john',
        email='john@example.com',
        about_me="Hello",
    )


@pytest.fixture
def user2():
    """
    User object
    """
    return User(
        username='alex',
        email='alex@example.com',
        about_me="Hello",
    )


@pytest.fixture
def user3():
    """
    User object
    """
    return User(
        username='mary',
        email='mary@example.com',
        about_me="Hello",
    )


@pytest.fixture
def user4():
    """
    User object
    """
    return User(
        username='david',
        email='david@example.com',
        about_me="Hello",
    )


def test_new_user(user1):
    """
    Test that user object contain correct values
    """
    assert user1.email == 'john@example.com'
    assert user1.username == "john"
    assert user1.about_me == 'Hello'
    assert str(user1) == "<User john, john@example.com>"


@mock.patch("app.models.current_app")
def test_password_hashing(_mock_current_app, user1):
    """
    Test setting password for user
    """
    user1.set_password('cat')
    assert user1.check_password('dog') is False
    assert user1.check_password('cat') is True


@mock.patch("app.models.current_app")
def test_avatar(_mock_current_app, user1):
    """
    Test creation of Gravatar URL
    """
    assert user1.avatar(128) == ('https://www.gravatar.com/avatar/'
                                 'd4c74594d841139328695756648b6bd6'
                                 '?d=retro&s=128')


def test_follow(test_app, user1, user2):
    """Test follow"""
    if test_app:
        pass
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    assert user1.followed.all() == []
    assert user1.followers.all() == []

    user1.follow(user2)
    db.session.commit()
    assert user1.is_following(user2)
    assert user1.followed.count()
    assert user1.followed.first().username == user2.username
    assert user2.followers.count() == 1
    assert user2.followers.first().username == user1.username

    user1.unfollow(user2)
    db.session.commit()
    assert not user1.is_following(user2)
    assert user1.followed.count() == 0
    assert user2.followers.count() == 0


def test_follow_posts(test_app):
    """Test follow posts"""
    if test_app:
        pass
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='susan', email='susan@example.com')
    u3 = User(username='mary', email='mary@example.com')
    u4 = User(username='david', email='david@example.com')
    # create four users
    db.session.add_all([u1, u2, u3, u4])

    # create four posts
    now = datetime.utcnow()
    p1 = Post(body="post from john", author=u1,
              timestamp=now + timedelta(seconds=1))
    p2 = Post(body="post from susan", author=u2,
              timestamp=now + timedelta(seconds=4))
    p3 = Post(body="post from mary", author=u3,
              timestamp=now + timedelta(seconds=3))
    p4 = Post(body="post from david", author=u4,
              timestamp=now + timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    # setup the followers
    u1.follow(u2)  # john follows susan
    u1.follow(u4)  # john follows david
    u2.follow(u3)  # susan follows mary
    u3.follow(u4)  # mary follows david
    db.session.commit()

    # check the followed posts of each user
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    assert f1 == [p2, p4, p1]
    assert f2 == [p2, p3]
    assert f3 == [p3, p4]
    assert f4 == [p4]
