from flask import Blueprint, render_template, redirect, url_for, request, current_app
from project.user.form import loginForm, registerForm, accountUpdate
from flask_login import login_required, login_user, logout_user, current_user
from project.modles import User, db, Post
import os
import secrets
from sqlalchemy import desc

userBlueprint = Blueprint('user', __name__, template_folder='templates/user')


@userBlueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.checkPassword(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('user.account')
                return redirect(next)

    return render_template('login.html', form=form)


@userBlueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        user = User(userName=form.userName.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@userBlueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def addPicture(picUpload):
    file = picUpload.filename
    extType = file.split('.')[-1]
    fName = secrets.token_hex(8)
    storeFile = fName + '.' + extType
    filePath = os.path.join(current_app.root_path, 'static/images', storeFile)
    picUpload.save(filePath)
    return storeFile


@userBlueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = accountUpdate()
    user = User.query.filter_by(userName=current_user.userName).first()
    post = Post.query.filter_by(user=user).order_by(desc(Post.date)).all()
    if form.validate_on_submit():
        if form.profilePic.data:
            profilePic = addPicture(form.profilePic.data)
            current_user.profilePic = profilePic
        if form.profileBg.data:
            profileBg = addPicture(form.profileBg.data)
            current_user.profileBg = profileBg

        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('user.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.profilePic.data = current_user.profilePic
        form.profileBg.data = current_user.profileBg
        form.bio.data = current_user.bio

    return render_template('account.html', form=form, post=post)


@userBlueprint.route('/viewAccount/<string:sno>')
def viewAccount(sno):
    user = User.query.filter_by(id=sno).first()
    if current_user == user :
        return redirect(url_for('user.account'))
    post = Post.query.filter_by(userId=sno).order_by(desc(Post.date)).all()
    return render_template('viewAccount.html', user=user, post=post)
