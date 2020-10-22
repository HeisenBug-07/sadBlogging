from flask import Blueprint, render_template, redirect, abort, url_for, current_app, request
from project.modles import Post, db
from project.post.form import addPost, updatePost
from flask_login import login_required, current_user
import os
import secrets
from sqlalchemy import desc


postBlueprint = Blueprint('post', __name__, template_folder='templates/post')


def addPicture(picUpload):
    file = picUpload.filename
    extType = file.split('.')[-1]
    fName = secrets.token_hex(8)
    storeFile = fName + '.' + extType
    filePath = os.path.join(current_app.root_path, 'static\\images', storeFile)
    picUpload.save(filePath)
    return storeFile


@postBlueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = addPost()
    if form.validate_on_submit():
        postImage = addPicture(form.postImage.data)
        post = Post(title=form.title.data, content=form.content.data, postImage=postImage, userId=current_user.id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('user.account'))

    return render_template('create.html', form=form)


@postBlueprint.route('/update/<string:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    form = updatePost()
    post = Post.query.filter_by(id=sno).first()
    if post.user != current_user:
        abort(403)
    if form.validate_on_submit():
        if form.postImage.data:
            postImage = addPicture(form.postImage.data)
            post.postImage = postImage

        post.content = form.content.data
        post.title = form.title.data
        db.session.commit()
        return redirect(url_for('user.account'))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.postImage.data = post.postImage

    return render_template('update.html', form=form)


@postBlueprint.route('/view/<string:sno>', methods=['GET', 'POST'])
def view(sno):
    post = Post.query.filter_by(id=sno).first()
    return render_template('view.html', post=post)


@postBlueprint.route('/delete/<string:sno>')
@login_required
def delete(sno):
    post = Post.query.filter_by(id=sno).first()
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user.account'))


@postBlueprint.route('/displayPosts')
def displayPosts():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(desc(Post.date)).paginate(page=page, per_page=4)
    return render_template('postDisplay.html', post=post)
