from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'thiskeyissecret'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(120))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        new_post = Post(post_title, post_content)
        db.session.add(new_post)
        db.session.commit()
    post_title = Post.query.all()
    post_content = Post.query.all()
    return render_template('add_new_post.html', post_title=post_title, post_content=post_content)

if __name__=='__main__':
    app.run()
