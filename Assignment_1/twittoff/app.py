from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["CUSTOM_VAR"] = 5 # just an example of app config :-D
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twittoff.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

#
# ROUTING
#

@app.route("/")
def index():
    #return "Hello World!"
    return render_template("homepage.html")

@app.route("/about")
def about():
    return "About Me"

@app.route("/users")
@app.route("/users.json")
def users():
    #users = [
    #    {"id":1, "name": "First User"},
    #    {"id":2, "name": "Second User"},
    #    {"id":3, "name": "Third User"},
    #]
    #return jsonify(users)

    users = User.query.all() # returns a list of <class 'alchemy.User'>
    print(type(users))
    print(type(users[0]))
    #print(len(users))

    users_response = []
    for u in users:
        user_dict = u.__dict__
        del user_dict["_sa_instance_state"]
        users_response.append(user_dict)

    return jsonify(users_response)



@app.route("/users/create", methods=["POST"]) #POST makes requests to a server, in this case flask
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form)) #request (Flask function)
    # todo: create a new user
    #return jsonify({"message": "CREATED OK (TODO)"})
    if "name" in request.form:
        name = request.form["name"]
        print(name)
        db.session.add(User(name=name))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "name": name})
    else:
        return jsonify({"message": "OOPS PLEASE SPECIFY A NAME!"})




# GET /hello
# GET /hello?name=Polly
@app.route("/hello")
def hello(name=None):
    print("VISITING THE HELLO PAGE")
    print("REQUEST PARAMS:", dict(request.args))

    if "name" in request.args:
        name = request.args["name"]
        message = f"Hello, {name}"
    else:
        message = "Hello World"

    #return message
    return render_template("hello.html", message=message)


#__________________tweets route______________________
@app.route("/tweets")
@app.route("/tweets.json")
def tweet():
    tweets = Tweet.query.all() # returns a list of <class 'alchemy.Tweet'>
    print(type(tweets))
    print(type(tweets[0]))

    tweets_response = []
    for t in tweets:
        tweet_dict = t.__dict__
        del tweet_dict["_sa_instance_state"]
        tweets_response.append(tweet_dict)

    return jsonify(tweets_response)

@app.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("CREATING A NEW TWEET...")
    print("FORM DATA:", dict(request.form))
    if "tweet" in request.form:
        tweet = request.form["tweet"]
        print(tweet)
        db.session.add(Tweet(status=tweet))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "tweet": tweet})
    else:
        return jsonify({"message": "OOPS PLEASE SPECIFY A TWEET!"})