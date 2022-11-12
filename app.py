from flask import Flask, redirect, render_template, request, session, url_for, g
from database import connect_to_database, getDatabase
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'quizapp_db'):
        g.quizapp_db.close()


        #USER DATABASE
def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = getDatabase()
        user_cursor = db.execute("select * from users where name = ?", [user])
        user_result = user_cursor.fetchone()
    return user_result


@app.route('/')
def index():
    user = get_current_user()
    return render_template("home.html", user = user)

@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    if request.method == "POST":
        name = request.form['name']
        db = getDatabase()
        password = request.form['password']

    return render_template("login.html", user = user,  error = error)

@app.route('/register', methods = ["POST", "GET"])
def register():
    user = get_current_user()
    error = None
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        db = getDatabase()
        user_fetcing_cursor = db.execute("select * from users where name = ?", [name])
        existing_user = user_fetcing_cursor.fetchone()

        if existing_user:
            error = "Username already taken, please choose a different username." # NOTIFIKASI USER
            return render_template("register.html", error = error)

        hashed_password = generate_password_hash(password, method='sha256')
        db.execute("insert into users (name, password, teacher, admin) values (?,?,?,?)",
        [name, hashed_password, '0', '0'])
        db.commit()
        session['user'] = name
        return redirect(url_for('index'))
    return render_template("register.html", user = user)


@app.route('/allusers', methods =["POST", "GET"])
def allusers():
    user = get_current_user()
    db = getDatabase()
    user_cursor = db.execute("select * from users")
    allusers = user_cursor.fetchall()
    return render_template("allusers.html", user = user, allusers = allusers)










@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)