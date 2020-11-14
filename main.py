from flask import Flask, render_template
app = Flask(__name__)

# The home page of the blog application


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/post')
def post():
    return render_template('post.html')


if __name__ == '__main__':
    app.run(debug=True)
