
import functools  # provide special functional tools which are required.

# importing Blueprint for grouping our app modules to ther repecting context and use.
# importing special object g 
# Importig redirect and render_template to process the template views.
# session will come handy when to get the info and credential of the admin user or test user.
from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
	)

# importing werkzeug security features for password protection.
#from werkzeug.security import check_password_hash, generate_password_hash

# importing db into the module
from student.student_db import get_db

'''
	creation of blueprint for the application url 
	comes in handy while navigating through ome specific urls.
	This needs to be register in factory method in __init__.py
'''
bp = Blueprint('auth',__name__, url_prefix='')  # this will set prefix before the views url path.


@bp.route('/adduser', methods=('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, password)
            )
            db.commit()
            return redirect(url_for('student.index'))

        flash(error)

    return render_template('auth/adduser.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


'''
	Now we will be creating the views for login of the user admin
'''
@bp.route('/', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		db = get_db()
		error = None

		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username, )
		).fetchone()

		if user is None:
			error = 'Invalid Username.'
		elif user['password'] != password:
			error = 'Invalid Password.'	

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('student.index'))

		flash(error)

	return render_template('auth/login.html')

'''
	logout for the User Admin
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# all of the CRUD applications are required the admin to be login
def login_required(view):
	# below code will check if the user is login. 
    @functools.wraps(view)

    def wrapped_view(**kwargs):

    	# if not login then will redirect to login

        if g.user is None: 
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
