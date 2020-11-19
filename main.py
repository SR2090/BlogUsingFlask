from flask import Flask, render_template, request
from datetime import datetime
# For adding data base
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
# Resource
# The home page of the blog application

# Database
# connected to SQL db
# This will connect to sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


# Server variable 
local_server = True;

# Reading the config file 
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Server configuration
if(local_server):
    # This will allow easy configuration change
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    pass

# We need to connect to mysql data base
# Adding the password and database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/selfreflection'
db = SQLAlchemy(app)

# This class will define the db table


class Contacts(db.Model):
    """
    sno, name, email, phone_num, msg, date
    """
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(10), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if(request.method == 'POST'):
        """ Add entry to db """
        # Getting data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        """
        sno, name, email, phone_num, msg, date
        """
        entry = Contacts(name=name, phone_num=phone, msg=message,
                         email=email, date=datetime.now())
        # session add and commit to db
        db.session.add(entry)
        # Commiting the values into the db
        db.session.commit()
    return render_template('contact.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
