from flask import render_template, Flask, request, flash
from weather import get_weather

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
    

