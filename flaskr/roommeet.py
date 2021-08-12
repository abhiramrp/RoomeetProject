from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from datetime import datetime, date

import os

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.__init__ import create_app


bp = Blueprint('roommeet', __name__)

app = create_app()

app.config["PROFILE_UPLOADS"] = "/Users/abhiram/Documents/GitHub/RoomeetProject/flaskr/static/images/profiles"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    if (g.user == None):
        return render_template("roommeet/home.html")
    
    return render_template('roommeet/index.html')


@bp.route('/createprofile', methods=('GET', 'POST'))
@login_required
def create_profile():
    user_id = session.get('user_id')

    db = get_db()

    error = None

    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        dob = request.form['dob']
        occupation = request.form['occupation']
        description = request.form['description']
        gender = request.form['gender']
        genderPref = request.form['genderPref']

        minage = request.form['minage']
        maxage = request.form['maxage']

        minprice = request.form['minprice']
        maxprice = request.form['maxprice']

        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        pets = request.form['pets']
        looking = request.form['looking']

        if not fname:
            error = 'First Name is required.'
        elif not lname:
            error = 'Last Name is required.'
        
        if not mname:
            mname = ""

        if not occupation: 
            error = 'Occupation is required'

        if not description:
            description = ""
        
        if not dob:
            error = "Need date of birth"

        if get_age(dob) == -1:
            error = "You must be at least 17 years. "

        
        if ((not minage) or (not maxage)):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater'

        if ((int(minage) < 17) or (int(minage) >= int(maxage))):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater' 
        
        if ((not minprice) or (not maxprice)):
            error = 'Please enter price values. Maximum price should be greater'

        if (int(minprice) < 0) or (int(minprice) > int(maxprice)):
            error = 'Please enter price values. Maximum price should be greater' 

        if gender == "":
            error = 'Gender is required'
        
        if genderPref == "":
            error = 'Gender Preferences are required'

        if city is None:
            error = 'City is required'

        if state is None:
            error = 'State is required'
        
        if zipcode is None:
            error = 'Zipcode is required'

        if pets == "":
            error = 'Pet preference is required'

        if looking == "":
            error = 'Search preferences are required.'

        if 'photo' not in request.files:
            error = 'Missing Image'

        photo = request.files['photo']
        photoname = ''

        if photo.filename == '':

            error ='No selected file'


        if photo and allowed_file(photo.filename):
            photoname = secure_filename(photo.filename)

            photo.save(os.path.join(app.config['PROFILE_UPLOADS'], photoname))


            if error is None:
                db.execute(
                    'INSERT INTO profile (user_id, first_name, middle_name, last_name, photo, dob, occupation, description, gender,'
                    'genderPref, ageMin,ageMax,priceMin,priceMax, city, state, zipcode, pets, looking) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (user_id, fname, mname, lname, photoname, dob, occupation, description, gender, genderPref, int(minage), int(maxage), int(minprice), int(maxprice), city, state, int(zipcode), pets, looking)
                )

                db.execute(
                    'UPDATE user SET verified = ?'
                    'WHERE id = ?', (1, user_id)
                )
                db.commit()

                return redirect(url_for('roommeet.index'))
        
        flash(error)

    return render_template('profile/createprofile.html')


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


@bp.route('/changeprofile', methods=('GET', 'POST'))
@login_required
def change_profile():
    user_id = session.get('user_id')

    profile = get_profile(user_id)

    photopath = 'images/profiles/'+profile['photo']


    db = get_db()

    error = None

    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']

        dob = request.form['dob']
        occupation = request.form['occupation']
        description = request.form['description']
        gender = request.form['gender']
        genderPref = request.form['genderPref']

        minage = request.form['minage']
        maxage = request.form['maxage']

        minprice = request.form['minprice']
        maxprice = request.form['maxprice']

        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        pets = request.form['pets']
        looking = request.form['looking']

        if not fname:
            error = 'First Name is required.'
        elif not lname:
            error = 'Last Name is required.'
        
        if not mname:
            mname = ""

        if not occupation: 
            error = 'Occupation is required'

        if not description:
            description = ""

        if not dob:
            error = "Need date of birth"
        
        if get_age(dob) == -1:
            error = "You must be at least 17 years. "
        


        if ((not minage) or (not maxage) or (minage == ' ') or (maxage == ' ')):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater'



        if (int(minage) < 17) or (minage >= maxage):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater' 
        
        if ((not minprice) or (not maxprice)):
            error = 'Please enter price values. Maximum price should be greater'

        if (int(minprice) < 0) or (minprice > maxprice):
            error = 'Please enter price values. Maximum price should be greater' 

        if gender == "":
            error = 'Gender is required'
        
        if genderPref == "":
            error = 'Gender Preferences are required'

        if city is None:
            error = 'City is required'

        if state is None:
            error = 'State is required'
        
        if zipcode is None:
            error = 'Zipcode is required'

        if pets == "":
            error = 'Pet preference is required'

        if looking == "":
            error = 'Search preferences are required.'

        
        if 'photo' not in request.files:
            error = 'Missing Image'

        photo = request.files['photo']
        photoname = None

        if photo.filename is None:
            error = 'No selected file'


        if photo and allowed_file(photo.filename):
            photoname = secure_filename(photo.filename)

            photo.save(os.path.join(app.config['PROFILE_UPLOADS'], photoname))


            if error is None:

                db.execute(
                    'UPDATE profile SET first_name = ?, middle_name = ?, last_name = ?, dob = ?, photo=?, occupation= ?, description= ?, gender= ?, genderPref= ?, ageMin= ?,ageMax= ?,priceMin= ?,priceMax= ?, city= ?, state=?, zipcode=?, pets=?, looking=?' 
                    'WHERE user_id = ?', (fname, mname, lname, dob, photoname, occupation, description, gender, genderPref, int(minage), int(maxage), int(minprice), int(maxprice), city, state, int(zipcode), pets, looking, user_id)
                )

                db.commit()

                return redirect(url_for('roommeet.index'))

        error = 'upload the right file'
        
        flash(error)

    return render_template('profile/changeprofile.html', profile=profile, photopath=photopath)



@bp.route('/viewprofile', defaults={'profid': None})
@bp.route('/viewprofile/<int:profid>')
@login_required
def view_profile(profid):
    profile = get_profile(profid)

    age = get_age(profile['dob'])

    photopath = 'images/profiles/'+profile['photo']

    return render_template('profile/viewprofile.html', profile=profile, photopath=photopath, age=age)


