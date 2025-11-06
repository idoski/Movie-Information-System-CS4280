from flask import *
from markupsafe import *

app = Flask(__name__)

@app.route("/<int:movieid>", methods=["GET"])
def movie_info(movieid):
    name = "Scary House"
    img_path = url_for('static', filename='uiconcept.png')
    description = "it's scary"
    rating = "5" + "/5"
    return render_template('movie.html', title = name, description = description, rating = rating, img_path = img_path)

@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/home", methods=["GET"])
def home_redirect():
    return redirect(url_for('home'))

@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET"])
def contact():
    return render_template('contact.html')

@app.route("/list", methods=["GET"])
def list_movies():
    return render_template('list.html')