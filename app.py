from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    db = sqlite3.connect("posts.db")
    db.row_factory = sqlite3.Row  # カラム名でアクセスできるようにする
    return db

# 一覧表示（Read）
@app.route("/")
def index():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template("index.html", posts=posts)

# 新規作成フォーム表示
@app.route("/create")
def create_form():
    return render_template("create.html")

# 新規作成（Create）
@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    body = request.form["body"]
    db = get_db()
    db.execute("INSERT INTO posts (title, body) VALUES (?, ?)", (title, body))
    db.commit()
    db.close()
    return redirect(url_for("index"))

# 編集フォーム表示
@app.route("/edit/<int:id>")
def edit_form(id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    db.close()
    return render_template("edit.html", post=post)

# 更新（Update）
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    title = request.form["title"]
    body = request.form["body"]
    db = get_db()
    db.execute("UPDATE posts SET title = ?, body = ? WHERE id = ?", (title, body, id))
    db.commit()
    db.close()
    return redirect(url_for("index"))

# 削除（Delete）
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

