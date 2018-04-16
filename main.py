from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'thiskeyissecret'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
    def empty(self):
        if self.title and self.body:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('entry.html', entry=entry)
    
    blog_post = Blog.query.all()
    return render_template('main_page.html', posts=blog_post)
   
@app.route('/newpost', methods=['POST', 'GET'])
def add_a_post():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        
        if new_blog.empty():
            db.session.add(new_blog)
            db.session.commit()
            post_url = "/blog?id=" + str(new_blog.id)
            return redirect(post_url)
        else:
            flash("Please enter a title and content for your blog.")
            return redirect('/newpost')        
    else:
        return render_template('add_new_post.html')

if __name__=='__main__':
    app.run()
