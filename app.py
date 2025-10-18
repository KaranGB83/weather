from flask import render_template, Flask, request, flash, session,redirect
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from weather import get_weather
from functools import wraps

app = Flask(__name__)
app.secret_key="ther"
app.config['DEBUG'] = True

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if "user_id" not in session:
            flash("Please log in first","error")
            return redirect("/")
        return f(*args, **kwds)
    return wrapper

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        city=request.form.get("name").strip()
        if not city:
            flash("Must Enter city for Weather!", 'error')
            return render_template("index.html")
        weather_info=get_weather(city)
        if "user_id" in session:
            if weather_info:
                #connecting db and creating object to interact with db
                with sqlite3.connect("weather.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO history (user_id,city) VALUES (?,?)",(session["user_id"],city))
                    conn.commit()
                return render_template("weather.html",name=weather_info,city=city)
            else:
                flash("Could not found information for the city. Try Again!!!", 'error')
                return render_template("index.html")
        else:
            if weather_info:
                return render_template("weather.html",name=weather_info,city=city)
            else:
                flash("Could not found information for the city. Try Again!!!", 'error')
                return render_template("index.html")
    return render_template("index.html")
    
@app.route("/login", methods=["GET","POST"])
def login():
    """Loging User"""
    #clear user id
    session.clear()

    if request.method=="POST":
        #ensuring username and password is entered
        if not request.form.get("username"):
            flash("Must provide Username","error")
            return render_template("login.html")
        elif not request.form.get("password"):
            flash("Must provide Password","error")
            return render_template("login.html")
        #connecting db and creating object to interact with db
        with sqlite3.connect("weather.db") as conn:
            cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM users WHERE username=?", (request.form.get("username"),)).fetchone()
        conn.commit()
        if row is None or not check_password_hash(row[2],request.form.get("password")):
            flash('Invalid Credential, Try Again!', 'error')
            return render_template("login.html")
        
        #remembering which user logged in
        session["user_id"]=row[0]

        flash(f'You are logged in {request.form.get("username")}','success')
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Loging Out"""
    session.clear()
    flash("You are logged out","info")
    return redirect("/login")

@app.route("/register",methods=["GET","POST"])
def register():
    """Registering"""
    if request.method=="POST":
        username=request.form.get("username")
        pw=request.form.get("password")
        rpw=request.form.get("rpassword")
        if not username:
            flash("Must Enter Username", "error")
            return render_template("register.html")
        elif not pw:
            flash("Must Enter Password", "error")
            return render_template("register.html")
        elif not rpw:
            flash("Must Enter Password Again", "error")
            return render_template("register.html")
        elif pw!=rpw:
            flash("Password Must Match", "error")
            return render_template("register.html")
        #connecting db and creating object to interact with db
        with sqlite3.connect("weather.db") as conn:
            cursor = conn.cursor()
        existing_user=cursor.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        if existing_user:
            flash("Username Already Exist, Try different One", "error")
            return render_template("register.html") 
        hash=generate_password_hash(pw)
        cursor.execute("INSERT INTO users (username,hash) VALUES (?,?)",(username,hash))
        conn.commit()
        #Fetching data
        rows=cursor.execute("SELECT id FROM users WHERE username=?",(username,)).fetchone()
        #remembering which user logged in
        session["user_id"]=rows[0]
        #redirecting user to homepage
        flash(f"Your Account Has Been Created {username}", "success")
        return redirect("/")
    return render_template("register.html")

@app.route("/history")
@login_required
def history():
    #connecting db and creating object to interact with db
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        x=cursor.execute("SELECT city, time FROM history WHERE user_id=?",(session["user_id"],))
        history=x.fetchall()
    return render_template("history.html",history=history)
        


    
    
