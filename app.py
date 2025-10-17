from flask import render_template, Flask, request, flash, session
import pysqlite3 as sqlite3
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
    #ensuring username and password is entered
    if not request.form.get("username"):
        flash("Must provide Username")
        return render_template("login.html")
    elif not request.form.get("password"):
        flash("Must provide Password")
        return render_template("login.html")
    row = cursor.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))
    if not row !=0 or check_password_hash(row[0]["hash"],request.form.get("password")):
        flash('Invalid Credential, Try Again!', 'error')
    
    #remembering which user logged in
    session["user_id"]=row[0]["id"]
    
    
