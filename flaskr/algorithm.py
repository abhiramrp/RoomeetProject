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

app.config["PROFILE_UPLOADS"] = "/Users/abhiram/Documents/GitHub/RoomeetProject/flaskr/static/images/profiles"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

profilelist = []


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




def get_profile_ids():

    user_id = session.get('user_id')

    p = get_db().execute(
        'SELECT user_id FROM profile'
    ).fetchall()

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
    

    print(profilelist)

    return profilelist


@bp.route('/match/<int:id>/<int:liketype>')
@login_required
def matchlike(id, liketype):
    db = get_db()



    print(liketype, type(liketype))

    if liketype == 1: 
        user_id = session.get('user_id')

        print(id, type(id))

        db.execute('INSERT INTO matchpairing (user_id, match_id) VALUES (?,?)', (user_id, id))
        db.commit()

    print("Going to matchnext")

    matchnext(id)
    

@bp.route('/match/')
def matchrandom():
    profilelist = get_profile_ids()

    print(profilelist)

    id = random.choice(profilelist)

    rp = get_profile(id)

    photopath = 'images/profiles/'+rp['photo']
    age = get_age(rp['dob'])

    return render_template('algorithm/profile.html', profile=rp, photopath=photopath, age=age)



def matchnext(id):
    # profilelist = get_profile_ids()

    idloc = profilelist.index(id) + 1

    print(profilelist)

    if (idloc >= len(profilelist)):
        idloc = 0

    rp = get_profile(profilelist[idloc])

    photopath = 'images/profiles/'+rp['photo']
    age = get_age(rp['dob'])

    return render_template('algorithm/profile.html', profile=rp, photopath=photopath, age=age)




    