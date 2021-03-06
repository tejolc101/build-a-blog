from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

@app.route('/main-blog', methods=['POST','GET'])
def index():
    
    #title_name = request.args.get('title')
    #body_name = request.args.get('body')
    
    blog_id = request.args.get('id')
    #id = request.form['id']
    
    
    blogs = Blog.query.all()
    if blog_id:
        
        blog = Blog.query.get(blog_id)
        return render_template("new-post.html",blog = blog)
    else:
        return render_template("blog-posts.html",blogs=blogs,title="Main-Blog")
    
        
        
@app.route('/new-post', methods=['POST','GET'])
def new_post():
    return render_template('todos.html',title="Build a Blog")

@app.route('/new-blog', methods=['POST','GET'])
def new_blog():
    error_title =""
    error_body=""
    
    if request.method == 'GET':
        
        
        title_name = request.args.get('title')
        body_name = request.args.get('body')
       
        
        

        if title_name == "":
            error_title ="Please fill in the title"
        if body_name == "":
            error_body = "Please fill int the content"

        if not error_title and not error_body:
            new_body = Blog(title_name, body_name)
            db.session.add(new_body)
            db.session.commit()
            new_title = Blog.query.filter_by(title=title_name).first() 
            blog_id = new_title.id
            return redirect('/main-blog?id={0}'.format(blog_id))
            #return render_template("new-post.html",blog=new_body)
        else:
            return render_template('todos.html',title="Build a Blog",error_title=error_title,error_body=error_body)

        
        

if __name__ == '__main__':
    app.run()