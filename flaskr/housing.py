from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import os

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.__init__ import create_app



bp = Blueprint('housing', __name__)

app = create_app()

app.config["HOUSING_UPLOADS"] = "/Users/abhiram/Documents/GitHub/RoomeetProject/flaskr/static/images/houses"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

@bp.route('/createhousing', methods=('GET', 'POST'))
@login_required
def create_housing():
    user_id = session.get('user_id')

    db = get_db()

    error = None

    if request.method == 'POST':
        housing_number = request.form['housing_number']
        apt_number = request.form['apt_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        description = request.form['description']

        rent = request.form['rent']

        genderPref = request.form['genderPref']

        minage = request.form['minage']
        maxage = request.form['maxage']

        pets = request.form['pets']

        if housing_number is None:
            error = 'Housing number is required'
        
        if apt_number is None:
            apt_number = ""
        
        if street is None:
            error = 'Street is required'

        if city is None:
            error = 'City is required'

        if state is None:
            error = 'State is required'
        
        if zipcode is None:
            error = 'Zipcode is required'

        if not description:
            description = ""
        
        if ((not minage) or (not maxage)):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater'

        if ((int(minage) < 17) or (int(minage) >= int(maxage))):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater' 

        if genderPref == "":
            error = 'Gender Preferences are required'


        if (not rent):
            error = 'Rent is required and must be greater than 0'

        if (int(rent) <= 0):
            error = 'Rent is required and must be greater than 0'

        if pets == "":
            error = 'Pet preference is required'

        if 'photo' not in request.files:
            error = 'Missing Image'

        photo = request.files['photo']
        photoname = ''

        if photo.filename == '':

            error ='No selected file'


        if photo and allowed_file(photo.filename):
            photoname = secure_filename(photo.filename)

            photo.save(os.path.join(app.config['HOUSING_UPLOADS'], photoname))

            if error is None:
                db.execute(
                    'INSERT INTO housing (poster_id, rent, photo, description, genderPref, ageMin,ageMax, housing_number, apt_number, street, city, state, zipcode, pets) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (user_id, int(rent), photoname, description, genderPref, int(minage), int(maxage), housing_number, apt_number, street, city, state, int(zipcode), pets)
                )

                db.commit()

                return redirect(url_for('roommeet.index'))
            
        
        flash(error)

    return render_template('housing/createhousing.html')



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def get_housing(id):

    housing = get_db().execute(
        'SELECT * FROM housing WHERE housing_id = ?', (id,)
    ).fetchone()

    if housing is None:
        abort(404, f"Housing doesn't exist.")

    return housing

@bp.route('/viewhousing', defaults={'houseid': None})
@bp.route('/viewhousing/<int:houseid>')
@login_required
def view_housing(houseid):

    housing = get_housing(houseid)


    photopath = 'images/houses/'+housing['photo']

    return render_template('housing/viewhousing.html', housing=housing, photopath=photopath)


@bp.route('/changehousing', defaults={'houseid': None}, methods=('GET', 'POST'))
@bp.route('/changehousing/<int:houseid>', methods=('GET', 'POST'))
@login_required
def change_housing(houseid):
    housing = get_housing(houseid)
    photopath = 'images/houses/'+housing['photo']
    user_id = session.get('user_id')

    db = get_db()

    error = None

    if housing['poster_id'] != user_id:
        return redirect(url_for('roommeet.index'))


    if request.method == 'POST':
        housing_number = request.form['housing_number']
        apt_number = request.form['apt_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        description = request.form['description']

        rent = request.form['rent']

        genderPref = request.form['genderPref']

        minage = request.form['minage']
        maxage = request.form['maxage']

        pets = request.form['pets']

        if housing_number is None:
            error = 'Housing number is required'
        
        if apt_number is None:
            apt_number = ""
        
        if street is None:
            error = 'Street is required'

        if city is None:
            error = 'City is required'

        if state is None:
            error = 'State is required'
        
        if zipcode is None:
            error = 'Zipcode is required'

        if not description:
            description = ""
        
        if ((not minage) or (not maxage)):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater'

        if ((int(minage) < 17) or (int(minage) >= int(maxage))):
            error = 'Please enter age values. Must be more than 17 and Maximum Age should be greater' 

        if genderPref == "":
            error = 'Gender Preferences are required'


        if (not rent):
            error = 'Rent is required and must be greater than 0'

        if (int(rent) <= 0):
            error = 'Rent is required and must be greater than 0'

        if pets == "":
            error = 'Pet preference is required'

        if 'photo' not in request.files:
            error = 'Missing Image'

        photo = request.files['photo']
        photoname = ''

        if photo.filename == '':

            error ='No selected file'


        if photo and allowed_file(photo.filename):
            photoname = secure_filename(photo.filename)

            photo.save(os.path.join(app.config['HOUSING_UPLOADS'], photoname))

            if error is None:
                db.execute(
                    'UPDATE housing SET rent =?, photo=?, description=?, genderPref=?, ageMin=?, ageMax=?, housing_number=?, apt_number=?, street=?, city=?, state=?, zipcode=?, pets=?'
                    'WHERE housing_id = ?', (int(rent), photoname, description, genderPref, int(minage), int(maxage), housing_number, apt_number, street, city, state, int(zipcode), pets, houseid)
                )

                db.commit()

                return redirect(url_for('roommeet.index'))

            error = 'upload the right file'
            
        
        flash(error)

    return render_template('housing/changehousing.html', housing=housing, photopath=photopath)

@bp.route('/deletehousing', defaults={'houseid': None}, methods=('GET', 'POST'))
@bp.route('/deletehousing/<int:houseid>', methods=('GET', 'POST'))
@login_required
def delete_housing(houseid):
    housing = get_housing(houseid)
    user_id = session.get('user_id')

    db = get_db()

    error = None

    if housing['poster_id'] != user_id:
        return redirect(url_for('roommeet.index'))
    else:

        db.execute('DELETE FROM housing WHERE housing_id = ?', (houseid,))
    
        db.commit()


    return redirect(url_for('roommeet.index'))
    

@bp.route('/housings')
@login_required
def housings():
    user_id = session.get('user_id')



    housings = get_db().execute(
        'SELECT housing_id FROM housing WHERE poster_id = ?', (user_id,)
    ).fetchall()

    housinglist = []

    for h in housings:
        for i in h:
            housinglist.append(i)


    return render_template('housing/housings.html', hlist = housinglist)



