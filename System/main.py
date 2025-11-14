# Imports
from flask import *
from markupsafe import *
from pymongo import *
from bson.objectid import ObjectId
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Start Flask and connect to MongoDB
app = Flask(__name__)
client = MongoClient(os.getenv("DATABASE_URL"))
db = client[os.getenv("DATABASE_NAME")]

# Movie info page
@app.route("/m_<movieid>", methods=["GET"])
def movie_info(movieid):
    s_movie = db.Movies.find_one({"_id": ObjectId(str(movieid))})
    name = s_movie["Name"]
    if ":" in s_movie["Name"]:
        name = s_movie["Name"].replace(":", " -")
    img_path = url_for('static', filename=name + ".webp")
    summary = s_movie["Summary"]
    cast = ", ".join(s_movie["Cast"])
    director = s_movie["Director"]
    genre = ", ".join(s_movie["Genres"])
    runtime = s_movie["Runtime"]
    rating = s_movie["Rating"]
    release_date = s_movie["release_date"]
    return render_template('movie.html', name=name, img_path=img_path, rating=rating, release_date=release_date, director=director, cast=cast, genre=genre, runtime=runtime, summary=summary)

# Actor info page
@app.route ("/a_<actorid>", methods=["GET"])
def actor_info(actorid):
    s_actor = db.Actors.find_one({"_id": ObjectId(str(actorid))})
    name = s_actor["Name"]
    if "-" in s_actor["Name"]:
        name = s_actor["Name"].replace("-", " ")
    img_path = url_for('static', filename=name + ".webp")
    birthday = s_actor["Birthday"]
    height = s_actor["Height"]
    parents = s_actor["Parents"]
    parents = ", ".join(parents)
    return render_template('actor.html', name=name, img_path=img_path, birthday=birthday, height=height, parents=parents)

# Main page, includes a POST to handle search queries
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
        featured_actors = list(db.Actors.aggregate([{"$sample": {"size": 6}}]))
        return render_template('home.html', featured_movies=featured_movies, top_movies=top_movies, featured_actors=featured_actors)
    


# Alternative to /. Just here so the home button actually works.
@app.route("/home", methods=["GET"])
def home_redirect():
    return redirect(url_for('home'))

# About and Contact pages
@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET"])
def contact():
    return render_template('contact.html')

# Movie and Actor Lists
@app.route("/mlist", methods=["GET"])
def list_movies():
    db_movies = db.Movies.find().sort("Name", 1)
    movies = []
    for movie in db_movies:
        movies.append(movie)
    return render_template('list.html', movies=movies)

@app.route("/alist", methods=["GET"])
def list_actors():
    db_actors = db.Actors.find().sort("Name", 1)
    actors = []
    for actor in db_actors:
        actors.append(actor)
    return render_template('actor_list.html', actors=actors)