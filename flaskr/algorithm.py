from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from datetime import datetime, date
import random

import os


from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.__init__ import create_app



bp = Blueprint('algorithm', __name__)

app = create_app()

app.config["PROFILE_UPLOADS"] = "flaskr/static/images/profiles"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS




def get_age(bdate):
    dt = datetime.strptime(bdate, '%Y-%m-%d')
    d = dt.date()
    today = date.today()

    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    if age >= 17:
        return age

    return -1


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_profile(id):

    profile = get_db().execute(
        'SELECT * FROM profile WHERE user_id = ?', (id,)
    ).fetchone()

    if profile is None:
        abort(404, f"Profile doesn't exist. Create a profile.")

    return profile

def get_user(id):

    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (id,)
    ).fetchone()

    if user is None:
        abort(404, f"User doesn't exist.")

    return user

def get_housing(id):

    housing = get_db().execute(
        'SELECT * FROM housing WHERE housing_id = ?', (id,)
    ).fetchone()

    if housing is None:
        abort(404, f"Housing doesn't exist.")

    return housing




def get_profile_ids():

    user_id = session.get('user_id')

    p = get_db().execute(
        'SELECT user_id FROM profile'
    ).fetchall()

    profilelist = []

    for profile in p:
        for i in profile:
            profilelist.append(i)


    profilelist.remove(user_id)

    m = get_db().execute(
        'SELECT match_id FROM matchpairing WHERE user_id = ?', (user_id,)
    ).fetchall()

    for match in m:
        for i in match:
            if i in profilelist:
                profilelist.remove(i)
    

    return profilelist



def get_housing_ids():

    user_id = session.get('user_id')

    h = get_db().execute(
        'SELECT housing_id FROM housing WHERE poster_id != ?', (user_id,)
    ).fetchall()

    houselist = []

    for house in h:
        for i in house:
            houselist.append(i)

    print(houselist)

    hm = get_db().execute(
        'SELECT house_id FROM housepairing WHERE user_id = ?', (user_id,)
    ).fetchall()

    for hmatch in hm:
        for i in hmatch:
            if i in houselist:
                houselist.remove(i)

    return houselist


@bp.route('/match/<int:id>/<int:liketype>')
@login_required
def matchlike(id, liketype):
    db = get_db()


    if liketype == 1: 
        user_id = session.get('user_id')


        db.execute('INSERT INTO matchpairing (user_id, match_id) VALUES (?,?)', (user_id, id))
        db.commit()



    profilelist = get_profile_ids()

    if (len(profilelist)==0):
        return render_template('roommeet/error.html', message="Out of profiles")


    id = random.choice(profilelist)

    rp = get_profile(id)

    photopath = 'images/profiles/'+rp['photo']
    age = get_age(rp['dob'])

    return render_template('algorithm/profile.html', profile=rp, photopath=photopath, age=age)



@bp.route('/hmatch/<int:id>/<int:liketype>')
@login_required
def houselike(id, liketype):
    db = get_db()


    if liketype == 1: 
        user_id = session.get('user_id')


        db.execute('INSERT INTO housepairing (user_id, house_id) VALUES (?,?)', (user_id, id))
        db.commit()


    houselist = get_housing_ids()

    if (len(houselist)==0):
        return render_template('roommeet/error.html', message="Out of houses")


    id = random.choice(houselist)

    rh = get_housing(id)

    photopath = 'images/houses/'+rh['photo']

    return render_template('algorithm/house.html', housing=rh, photopath=photopath)


@bp.route('/houseselectors/<int:id>')
def houseselectors(id):
    hm = get_db().execute(
        'SELECT user_id FROM housepairing WHERE house_id = ?', (id,)
    ).fetchall()

    profilelist = []

    housing = get_housing(id)

    for person in hm:
        for i in person:
            p = get_profile(i)
            profilelist.append(p)

    return render_template('algorithm/viewselectors.html', housing=housing, plist = profilelist)



@bp.route('/houseselections')
def houseselections():
    user_id = session.get('user_id')


    dh = get_db().execute(
        'SELECT house_id FROM housepairing WHERE user_id = ?', (user_id,)
    ).fetchall()

    houses = []

    for house in dh:
        for i in house:
            h = get_housing(i)
            houses.append(h)
    

    return render_template('algorithm/houseselections.html', hlist = houses)






@bp.route('/selections')
def selections():
    user_id = session.get('user_id')


    m = get_db().execute(
        'SELECT match_id FROM matchpairing WHERE user_id = ?', (user_id,)
    ).fetchall()

    profiles = []

    for match in m:
        for i in match:
            p = get_profile(i)
            profiles.append(p)
    

    return render_template('algorithm/viewselections.html', mlist = profiles)


@bp.route('/matches')
def matches():
    user_id = session.get('user_id')


    m = get_db().execute(
        'SELECT match_id FROM matchpairing WHERE user_id = ?', (user_id,)
    ).fetchall()

    profile_ids = []
    profiles = []

    for match in m:
        for i in match:
            profile_ids.append(i)

    for i in profile_ids:
        p = get_db().execute(
            'SELECT match_id FROM matchpairing WHERE user_id = ? AND match_id = ?', (i, user_id)
        ).fetchone()

        if p is not None:
            profiles.append(get_profile(i))



    return render_template('algorithm/viewmatches.html', mlist = profiles)

@bp.route('/matchprofile', defaults={'profid': None})
@bp.route('/matchprofile/<int:profid>')
@login_required
def match_profile(profid):
    profile = get_profile(profid)

    age = get_age(profile['dob'])

    photopath = 'images/profiles/'+profile['photo']

    u = get_user(profid)

    phone = u['phone']

    return render_template('algorithm/selectmatch.html', profile=profile, photopath=photopath, phone=phone, age=age)




    