from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort, session, url_for, flash, abort
from datetime import datetime
import os
from werkzeug.utils import secure_filename

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
def index():
    print("Env: " + app.config['ENV'])
    print("Env: " + app.config['DB_NAME'])
    
    return render_template("public/index.html")

@app.route("/jinja")
def jinja():
    my_name = "Oleg"
    age = 30

    langs = ["Python", "Java", "Groovy"]

    friends = {
        "Tom": 30,
        "Amy": 26,
        "Tony": 32,
        "Clarissa": 36
    }

    colours = ("Red", "Green")

    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name=name
            self.description=description
            self.url=url
        
        def pull(self):
            return f"Pullin repo {self.name}"
        
        def clone(self):
            return f"Cloning into {self.url}"
    
    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template design tutorial",
        url="https://github.com/Aks1389/jinja.git"
    )

    def repeat(x, qty):
        return x* qty

    date = datetime.utcnow()

    my_html = "<h1>THIS IS SOME HTML</h1>"

    suspicious = "<script>alert('YOU GOT HACKED!')</script>"

    return render_template(
        "public/jinja.html", my_name=my_name, age=age,
        langs=langs, friends=friends, colours=colours,
        cool=cool, GitRemote=GitRemote, repeat=repeat,
        my_remote=my_remote, date=date, my_html=my_html,
        suspicious=suspicious
    )

@app.route("/about")
def about():
    return render_template("public/about.html")

""" @app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        req = request.form
        
        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)

        return redirect(request.url)
    return render_template("public/sign_up.html") """

""" users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):
    user = None
    if username in users:
        user = users[username]
    return render_template("public/profile.html", 
        username=username, user=user) """

@app.route("/multiple/<foo>/<bar>/<baz>")
def miltu(foo, bar, baz):
    return f"foo is {foo}; bar is {bar}; baz is {baz}"

@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": "JSON received!",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"message": "No JSON recevied"}), 400)
        return res
    
@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "JSON received"}), 200)
    #res = make_response(jsonify(req), 200)
    return res

@app.route("/query")
def query():
    if request.args:
        args = request.args

        serialized = ", ".join(f"{k}:{v}" for k,v in args.items())

        if "foo" in args:
            foo = args.get("foo")
            print(foo)
        
        print(request.query_string)

        return f"(Query) {serialized}", 200
    else:
        return "No query received", 200

app.config["IMAGE_UPLOADS"] = "C:\\Users\\aksnv\\Documents\\Programming\\Learn-Flask\\app\\static\\img\\upploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_image(filename):
    if not '.' in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:

            image = request.files["image"]
            
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extensions is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            filesize = request.cookies.get("filesize")
            if not allowed_image_filesize(filesize):
                print("File exceeded maximum size!")
                return redirect(request.url)
            print("Image saved")
            return redirect(request.url)
    return render_template("public/upload_image.html")


app.config["CLIENT_IMAGES"] = "/Users/oleg_aksenov/Documents/Learn Flask/Learn-Flask/app/static/client/img"
app.config["CLIENT_CSV"] = "/Users/oleg_aksenov/Documents/Learn Flask/Learn-Flask/app/static/client/csv"
app.config["CLIENT_REPORTS"] = "/Users/oleg_aksenov/Documents/Learn Flask/Learn-Flask/app/static/client/reports"

"""
converters:
string: - default
int:
float:
path:
uuid
"""
@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<filename>")
def get_csv(filename):
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(app.config["CLIENT_REPORTS"], filename=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


#Ls15
@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)

    cookies = request.cookies
    flavor = cookies.get("flavor")
    choc_type = cookies.get("chocolate type")
    chewy = cookies.get("chewy")

    print(flavor, choc_type, choc_type)
    
    res.set_cookie(
        "flavor", 
        value="chocolate chip",
        max_age=10,
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        samesite=None
        )

    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")
    return res

#Ls16
app.config["SECRET_KEY"] = "XdypQz5RKEzR3VgTrTb7UA"

users = {
    "julian": {
        "username": "julian",
        "email": "julian@gmail.com",
        "password": "example",
        "bio": "Some guy from the internet"
    },
    "clarissa": {
        "username": "clarissa",
        "email": "clarissa@icloud.com",
        "password": "sweetpotato22",
        "bio": "Sweet potato is life"
    }
}

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        
        if not username in users:
            print("username not found")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            print("Password incorrect")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            
            print("User added to session")
            return redirect(url_for("profile"))
    return render_template("public/sign_in.html")

@app.route("/profile")
def profile():
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("public/profile.html", user=user)
    else:
        print("Username not found in session")
        return redirect(url_for("sign_in"))

@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("sign_in"))

#Ls 17
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        req = request.form
        
        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        if not len(password) >= 10:
            flash("Password must be at least 10 characters in length", "warning")
            redirect(request.url)
        else:
            flash("Account created!", "success")
        return redirect(request.url)
    return render_template("public/sign_up.html")