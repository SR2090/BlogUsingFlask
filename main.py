from flask import Flask, render_template, request
from datetime import datetime
from flask_mail import Mail 
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




# Reading the config file 
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
# Server variable 
local_server = True;

# Sending Email Credential Configuration
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail_user"],
    MAIL_PASSWORD = params["gmail_passwd"]
)

# Host email config
mail = Mail(app)


# Server configuration
if(local_server):
    # This will allow easy configuration change
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

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
    return render_template('index.html', params = params)


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

        # # I want to send mail after commit
        # mail.send_message('Title of the mail'
        # ,msg = message, 
        # recipients= [params['gmail-user']],
        # body = message + '\n' + phone
        # # Whenever this runs the email will be sent
        # )
    return render_template('contact.html',params = params)


@app.route('/index')
def index():
    return render_template('index.html',params = params)


@app.route('/post')
def post():
    return render_template('post.html',params = params)


@app.route('/about')
def about():
    return render_template('about.html',params = params)


if __name__ == '__main__':
    app.run(debug=True)
