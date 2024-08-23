from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username="test", password="senha", email="mail@mail.com")

    session.add(user)

    session.commit()

    result = session.scalar(select(User).where(User.email == "mail@mail.com"))

    assert result.username == "test"
