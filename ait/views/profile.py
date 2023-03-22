import os
import secrets
from flask import abort, redirect, render_template, Blueprint, request, url_for
from flask_login import current_user, login_required
from ait import db_fire, db

profile =Blueprint('profile',__name__)

def save_profile(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(profile.root_path, f'static\profile_pic' , picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@profile.route('/account')
@login_required
def account():
    user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
    return render_template('users-profile.html', user_data = user_data)

@profile.route('/account/edit/<string:username>', methods=['POST'])
@login_required
def edit_account(username):
    if username != current_user.username:
        abort()
    if request.method == "POST":
        name = request.form.get("fullName")
        about = request.form.get("about")
        address = request.form.get("address")
        phone = request.form.get("phone")
        twitter = request.form.get("twitter")
        facebook = request.form.get("facebook")
        instagram = request.form.get("instagram")
        linkedin = request.form.get("linkedin")
        cv_link = request.form.get("cv_link")
        data ={
            'name' : name,
            'about' : about,
            'add' : address,
            'phone' : phone,
            'twitter' : twitter,
            'facebook' : facebook,
            'instagram' : instagram,
            'linkedin' : linkedin,
            'cv_link' : cv_link,
        }
        
        picture_url = request.files["picture_url"]
        if picture_url.filename:
            final = save_profile(picture_url)
            current_user.profile_url = final
            data["profile_url"] = final
            db.session.commit()
        
        db_fire.collection(current_user.role).document(username).set(data, merge = True)

    return redirect(url_for('profile.account'))


@profile.route('/user/<string:role>/<string:username>')
@login_required
def user(username,role):
    if username == current_user.username:
        return redirect (url_for('profile.account'))
    else:
        posts = db_fire.collection('post').where('username','==',username).get()
        user_data = db_fire.collection(current_user.role).document(current_user.username).get().to_dict()
        profile_data = db_fire.collection(role).document(username).get().to_dict()
        type = db_fire.collection('connection').document(current_user.username).get()
        
        value = False
        
        if type.exists:
            if username in type.to_dict().keys():
                value = True 
        return render_template('user.html', profile_data = profile_data,user_data = user_data, posts = posts, value = value  )


@profile.route('/test')
def test():
    return "<h1>Hello, World</h1>"