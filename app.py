from flask import render_template
from project import app
from project.modles import User, Post


@app.route('/')
@app.route('/home')
def home():
    user = User.query.all()
    post = Post.query.all()
    return render_template('home.html', user=user, post=post)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
