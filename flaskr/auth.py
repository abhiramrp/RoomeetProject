import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        cpassword = request.form['cpassword']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not phone:
            error = 'Phone is required.'
        elif password != cpassword:
            error != 'Passwords not matching'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered." 
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = f"Email {email} is already registered."
        elif db.execute(
            'SELECT id FROM user WHERE phone = ?', (phone,)
        ).fetchone() is not None:
            error = f"Phone number {phone} is already registered."


        if error is None:
            db.execute(
                'INSERT INTO user (username, email, phone, password) VALUES (?, ?, ?, ?)',
                (username, email, phone, generate_password_hash(password))
            )
            db.commit()

            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('roommeet.index'))

            # return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('roommeet.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/changeaccount', methods=('GET', 'POST'))
def change_account():
    user_id = session.get('user_id')

    db = get_db()

    error = None

    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not phone:
            error = 'Phone is required.'

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            if user['username'] != username:
                error = f"User {username} is already registered." 
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            if user['email'] != email:
                error = f"Email {email} is already registered."
        elif db.execute(
            'SELECT id FROM user WHERE phone = ?', (phone,)
        ).fetchone() is not None:
            if user['phone'] != phone:
                error = f"Phone number {phone} is already registered."
        
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            db.execute(
                'UPDATE user SET username = ?, email = ?, phone = ?, password = ?'
                'WHERE id = ?',
                (username, email, phone, generate_password_hash(password), user_id)
            )
            db.commit()
            return redirect(url_for('roommeet.index'))

        flash(error)

    return render_template('auth/changeaccount.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/changepassword', methods=('GET', 'POST'))
def change_password():
    user_id = session.get('user_id')

    db = get_db()

    error = None

    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if request.method == 'POST':
        oldpass = request.form['oldpass']
        newpass = request.form['newpass']
        newpassc = request.form['newpassc']

        if newpass != newpassc:
            error = 'Passwords not matching'
    
        if not check_password_hash(user['password'], oldpass):
            error = 'Incorrect password.'

        if error is None:
            db.execute('UPDATE user SET password = ?'
                'WHERE id = ?',
                (generate_password_hash(newpass), user_id))

            db.commit()


            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('roommeet.index'))

        flash(error)
    
    return render_template('auth/changepassword.html')


@bp.route('/deleteaccount', methods=('GET', 'POST'))
def delete_account():
    user_id = session.get('user_id')

    db = get_db()

    error = None

    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if request.method == 'POST':
        password = request.form['password']
        cpassword = request.form['cpassword']

        if password != cpassword:
            error = 'Passwords not matching'
    
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            db.execute('DELETE FROM user WHERE id = ?', (user_id)) 
            db.commit()
            session.clear()
            return redirect(url_for('roommeet.index'))

        flash(error)
    
    return render_template('auth/deleteaccount.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('roommeet.index'))


