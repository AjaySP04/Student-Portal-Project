from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from student.auth import login_required
from student.student_db import get_db

bp = Blueprint('student', __name__, url_prefix='/student')

@bp.route('/')
@login_required
def index():
    db = get_db()
    students = db.execute(
        'SELECT id, "S0000" || CAST( id AS TEXT)  AS roll_number, name, age, gender, add_date FROM student'
    ).fetchall()
    return render_template('student/index.html', students=students)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO student (name, age, gender)'
                ' VALUES (?, ?, ?)',
                (name, age, gender)
            )
            db.commit()
            return redirect(url_for('student.index'))

    return render_template('student/create.html')


def get_students(id):
    student = get_db().execute(
        'SELECT id, "S0000" || CAST( id AS TEXT)  AS roll_number, name, age, gender, add_date '
        ' FROM student WHERE id=?',
        (id,)
    ).fetchone()

    if student is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return student


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    student = get_students(id)

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        error = None

        if not name:
            error = 'Student Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE student SET name = ?, age = ?, gender=? WHERE id = ?', (name, age, gender, id, 	)
            )
            db.commit()
            return redirect(url_for('student.index'))

    return render_template('student/update.html', student=student)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_students(id)
    db = get_db()
    db.execute('DELETE FROM student WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('student.index'))


			