from flask import *
from markupsafe import *
from pymongo import *
from bson.objectid import ObjectId
import random
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("DATABASE_URL"))
db = client[os.getenv("DATABASE_NAME")]

@app.route("/<movieid>", methods=["GET"])
def movie_info(movieid):
    s_movie = db.Movies.find_one({"_id": ObjectId(str(movieid))})
    name = s_movie["Name"]
    if ":" in s_movie["Name"]:
        name = s_movie["Name"].replace(":", " -")
    img_path = url_for('static', filename=name + ".webp")
    cast = ", ".join(s_movie["Cast"])
    director = s_movie["Director"]
    genre = ", ".join(s_movie["Genres"])
    runtime = s_movie["Runtime"]
    rating = s_movie["Rating"]
    release_date = s_movie["release_date"]
    return render_template('movie.html', name=name, img_path=img_path, rating=rating, release_date=release_date, director=director, cast=cast, genre=genre, runtime=runtime)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        q = request.form.get('query').__str__()
        query = db.Movies.find_one({"Name": {"$regex": q, "$options": "i"}})
        if query is None:
            return redirect(url_for('home'))
        objID = query["_id"].__str__()
        return redirect(url_for('movie_info', movieid=objID))
    else:
        top_movies = list(db.Movies.find().sort("Rating", -1).limit(8))
        featured_movies = list(db.Movies.aggregate([{"$sample": {"size": 8}}]))
        return render_template('home.html', featured_movies=featured_movies, top_movies=top_movies)
    
    

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
    db_movies = db.Movies.find()
    movies = []
    for movie in db_movies:
        movies.append(movie)
    return render_template('list.html', movies=movies)