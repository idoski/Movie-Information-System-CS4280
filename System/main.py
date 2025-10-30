from flask import *
from markupsafe import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def movie_info():
    name = "Scary House"
    img_path = url_for("static", filename="QnZyuA8.png")
    print(img_path)
    description = "it's scary"
    rating = "5" + "/5"
    return render_template('movie.html', title = name, description = description, rating = rating, img_path = img_path)