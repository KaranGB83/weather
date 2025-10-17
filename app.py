from flask import render_template, Flask, request, flash, session,redirect
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from weather import get_weather

conn=sqlite3.connect("weather.db") #connecting db
cursor = conn.cursor() #creating object to interact with db

app = Flask(__name__)
app.secret_key="ther"
app.config['DEBUG'] = True

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        city=request.form.get("name").strip()
        if not city:
            flash("Must Enter city for Weather!", 'error')
            return render_template("index.html")
        weather_info=get_weather(city)
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
        row = cursor.execute("SELECT * FROM users WHERE username=?", (request.form.get("username"),)).fetchone()
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
    flash("You are logged out")
    return redirect("login.html")

app.route("/register",methods=["GET","POST"])
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
        existing_user=cursor.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        if existing_user:
            flash("Username Already Exist, Try different One", "error")
            return render_template("register.html") 
        hash=generate_password_hash(pw)
        cursor.execute("INSERT INTO users (username,hash) VALUES (?,?)",(username,hash))

        #Fetching data
        rows=cursor.execute("SELECT id FROM users WHERE username=?",(username,)).fetchone()
        conn.commit()
        #remembering which user logged in
        session["user_id"]=rows[0]
        #redirecting user to homepage
        flash(f"Your Account Has Been Created {username}", "success")
        return redirect("/")
    else:
        flash("Registration Failed!","success")
        return render_template("register.html")

    
    
