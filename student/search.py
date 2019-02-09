import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from student.auth import login_required
from student.student_db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')
    
@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
	pattern = ''
	students = []
	if request.method == 'POST':
	   pattern = request.form['search']
	   error = None

	   if not pattern:
		   error = 'Search field cannot be empty.'

	   if error is not None:
		   flash(error)
	   else:
	   	db = get_db()
	   	students = db.execute(
                     'SELECT id, "S0000" || CAST( id AS TEXT)  AS roll_number, name, age, gender, add_date FROM student'
                     ' FROM student WHERE name LIKE ?', (pattern,)
                     ).fetchall()
	return render_template('student/index.html', students=students)