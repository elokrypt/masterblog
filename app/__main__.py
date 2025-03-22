# -*- coding: utf-8 -*-
#
"""
An example Flask application, utilizing Jinja2 templates and
a JSON-file database to store Blog posts of a Blog-website.
"""

from os import getenv as getvar
from dotenv import load_dotenv as getvars
from flask import Flask
from flask import redirect, request, render_template as render
from flask import url_for

from json_storage import JsonStorage

getvars()

BLOG_DB_FILE = getvar("BLOG_DB_FILE", "blog_posts.json")
storage = JsonStorage(file_path=BLOG_DB_FILE)

app = Flask(__name__)
app.secret_key = getvar("SECRET_KEY", "my_super_secre7")


@app.route("/")
def index():
    blog_posts = storage.load_items()
    return render("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        post = storage.get_new_item()
        post["likes"] = 0
        post["author"] = request.form.get("author", type=str)
        post["title"] = request.form.get("title", type=str)
        post["content"] = request.form.get("content", type=str)
        storage.add_item(post)
        return redirect(url_for("index"))

    return render("add.html")


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id: int):
    # Fetch the blog posts from the JSON file
    post = storage.get_item(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form.get("author", type=str)
        post["title"] = request.form.get("title", type=str)
        post["content"] = request.form.get("content", type=str)
        storage.update_item(post_id, **post)
        return redirect(url_for("index"))
    # Else, it's a GET request
    # So display the update.html page
    return render("update.html", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id: int):
    post = storage.get_item(post_id)
    if post is None:
        return "Post not found", 404
    storage.delete_item(post["id"])

    return redirect(url_for("index"))


@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id: int):
    if request.method == "POST":
        post = storage.get_item(post_id)
        if post is None:
            return "Post not found", 404
        post["likes"] += 1

        storage.update_item(post["id"], **post)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
