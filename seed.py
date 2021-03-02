from models import db, User, Feedback
from app import app

db.drop_all()
db.create_all()

users = [
    User(username="user one", password="ilovepets", email="user.one@gmail.com", first_name="mariah", last_name="carey"),
    User(username="user two", password="ilovepets", email="user.two@gmail.com", first_name="jeff", last_name="winger"),
    User(username="user three", password="ilovepets", email="user.three@gmail.com", first_name="yo", last_name="gaba gaba"),
]

feedbacks = [
    Feedback(title="first post", content="this is my content", username="user one"),
    Feedback(title="second post", content="this is my content", username="user two"),
    Feedback(title="third post", content="this is my content", username="user three")
]

db.session.add_all(users, feedbacks)
db.session.commit()