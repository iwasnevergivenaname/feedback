from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email

class RegisterUser(FlaskForm):
	""" form to register user """
	
	username = StringField("username", validators=[InputRequired(message="please enter a user unique username, "
	                                                                     "no longer than 20 characters")])
	password = PasswordField("password", validators=[InputRequired(message="please enter a password")])
	email = StringField("email", validators=[InputRequired(message="please enter your unique email address"),
	                                         Email(message="please enter a valid email address")])
	first_name = StringField("first name", validators=[InputRequired(message="please enter a name shorter than 50 characters")])
	last_name = StringField("last name", validators=[InputRequired(message="please enter a name shorter than 50 characters")])
	
	
class UserLogin(FlaskForm):
	""" form for user login """
	
	username = StringField("username", validators=[InputRequired(message="please enter your username")])
	password = PasswordField("password", validators=[InputRequired(message="please enter your password")])
	
	
class FeedbackForm(FlaskForm):
	""" form to create new feedback """
	
	title = StringField("title", validators=[InputRequired(message="please enter a title shorter than 100 characters")])
	content = TextAreaField("content", validators=[InputRequired(message="please enter your content")])