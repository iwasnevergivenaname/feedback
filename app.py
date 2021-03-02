from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User, Feedback
from forms import RegisterUser, UserLogin, FeedbackForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "mamamiaspicymeatball"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flaskfeedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)
db.create_all()

@app.route('/')
def home():
	""" redirect to /register """
	return redirect("/register")


@app.route("/register", methods=["GET"])
def show_register_form():
	""" show form to register/create user """
	form = RegisterUser()
	return render_template('register.html', form=form)


@app.route("/register", methods=["POST"])
def process_user_registration():
	""" process the form and redirect to /secret"""
	form = RegisterUser()
	
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		email = form.email.data
		first_name = form.first_name.data
		last_name = form.last_name.data
		
		user = User.register(username, password, email, first_name, last_name)
		db.session.add(user)
		db.session.commit()
		
		session["username"] = user.username
		return redirect("/login")
	else:
		return render_template('register.html')


@app.route("/login", methods=["GET"])
def show_login_form():
	""" show a login form """
	form = UserLogin()
	return render_template('login.html', form=form)


@app.route("/login", methods=["POST"])
def process_login():
	""" process login and authenticate user redirect to /secret if logged in """
	form = UserLogin()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		
		user = User.authenticate(username, password)
		
		if user:
			session["username"] = user.username
			return redirect(f"/users/{username}")
		else:
			form.username.errors = ["login attempted failed"]
			return render_template('login.html', form=form)


@app.route("/users/<username>")
def user_secret_page(username):
	if "username" not in session or username != session['username']:
		return redirect("/")
	else:
		user = User.query.get(username)
		return render_template("user.html", user=user)

	
@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
	""" remove user from database LOGGED IN USER ONLY"""
	if "username" not in session or username != session['username']:
		print("ooop")
	user = User.query.get(username)
	db.session.delete(user)
	db.session.commit()
	session.pop("username")
	return redirect("/")
	
	
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def show_new_feedback(username):
	""" create new feedback LOGGED IN USER ONLY"""
	if "username" not in session or username != session['username']:
		return redirect("/")
	form = FeedbackForm()
	if form.validate_on_submit():
		title = form.title.data
		content = form.content.data
		
		feedback = Feedback(title=title, content=content, username=username)
		db.session.add(feedback)
		db.session.commit()
		return redirect(f"/users/{feedback.username}")
	else:
		return render_template("feedback_form.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def show_feedback_edit(feedback_id):
	""" show update form """
	feedback = Feedback.query.get(feedback_id)
	if "username" not in session or feedback.username != session['username']:
		print("oops")
	form = FeedbackForm(obj=feedback)
	if form.validate_on_submit():
		feedback.title = form.title.data
		feedback.content = form.content.data
		
		db.session.commit()
		return redirect(f"/users/{feedback.username}")
	return render_template("feedback_edit.html", form=form)
	

@app.route("/feedback/<int:feedback_id>/delete")
def delete_feedback(feedback_id):
	""" delete feedback """
	feedback = Feedback.query.get(feedback_id)
	if "username" not in session or feedback.username != session['username']:
		print("oops")
	db.session.delete(feedback)
	db.session.commit()
	return redirect(f"/users/{feedback.username}")


@app.route("/logout")
def log_user_out():
	if "username" not in session:
		return redirect("/")
	session.pop("username")
	return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404