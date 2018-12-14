from flask import redirect, render_template, request, Flask, url_for
# from werkzeug.exception import BadReques, NotFound

import models

# app = Flask(__name__, template_folder="view")
app = Flask(__name__)

# flask quickstart
# @app.route("/")
# def index(): pass

@app.route("/hello/")
@app.route("/helo/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return "Post %d" % post_id

if __name__ == "__main__":
    app.run(debug=True)
