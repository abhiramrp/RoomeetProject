from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('roommeet', __name__)

@bp.route('/')
def index():
    if not session.get("user_id"):
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

        if not fname:
            error = 'First Name is required.'
        elif not lname:
            error = 'Last Name is required.'
        
        if not mname:
            mname = ""

        if error is None:
            db.execute(
                'INSERT INTO profile (user_id, first_name, middle_name, last_name) VALUES (?, ?, ?, ?)',
                (user_id, fname, mname, lname)
            )

            db.execute(
                'UPDATE user SET verified = ?'
                'WHERE id = ?', (1, user_id)
            )
            db.commit()

            return redirect(url_for('roommeet.index'))
        
        flash(error)

    return render_template('profile/createprofile.html')


def get_profile(id):

    profile = get_db().execute(
        'SELECT user_id, first_name, middle_name, last_name FROM profile WHERE user_id = ?', (id,)
    ).fetchone()

    if profile is None:
        abort(404, f"Profile doesn't exist. Create a profile.")

    return profile


@bp.route('/changeprofile', methods=('GET', 'POST'))
@login_required
def change_profile():
    user_id = session.get('user_id')

    profile = get_profile(user_id)

    db = get_db()

    error = None

    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']

        if not fname:
            error = 'Username is required.'
        elif not lname:
            error = 'Password is required.'
        
        if not mname:
            mname = ""

        if error is None:
            db.execute(
                'UPDATE profile SET first_name = ?, middle_name = ?, last_name = ?' 
                'WHERE user_id = ?', (fname, mname, lname, user_id)
            )

            db.commit()

            return redirect(url_for('roommeet.index'))

    return render_template('profile/changeprofile.html', profile=profile)


def get_housing(housing_id):

    housing = get_db().execute(
        'SELECT housing_id, poster_id, zipcode, rent FROM profile WHERE housing_id = ?', (housing_id,)
    ).fetchone()

    if housing is None:
        abort(404, f"Profile doesn't exist. Create a profile.")

    return housing


@bp.route('/createhousing', methods=('GET', 'POST'))
@login_required
def create_housing():
    user_id = session.get('user_id')

    db = get_db()

    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    error = None

    if request.method == 'POST':
        zipcode = request.form['zipcode']
        rent = request.form['rent']

        if not zipcode:
            error = "Please enter zipcode"
        
        if not rent:
            error = "Please enter rent"

        if user['verified'] == 0:
            error = "User not verified. Please create a profile"

        
        if error is None:
            db.execute(
                'INSERT INTO housing (poster_id, zipcode, rent) VALUES (?, ?, ?)',
                (user_id, zipcode, rent)
            )

            db.commit()

            return redirect(url_for('roommeet.index'))

        flash(error)
    
    return render_template('housing/createhousing.html')