from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from kanban.auth import login_required
from kanban.db import get_db

bp = Blueprint('task', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT *'
        ' FROM task t JOIN user ON t.author_id = user.id'
        ' ORDER BY created ASC',
    ).fetchall()

    return render_template('task/index.html', tasks=tasks)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        author_id = g.user['id']
        error = None

        if not title:
            error = 'Title is required.'

        if not status:
            error = 'Status is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, description, status, priority, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, description, status, priority, author_id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html')


def get_task(id):
    """
    Re 
    """
    task = get_db().execute(
        'SELECT *'
        ' FROM task t JOIN user ON t.author_id = user.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    if task['author_id'] != g.user['id']:
        abort(403)

    return task

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        author_id = g.user['id']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title = ?, description = ?, status = ?, priority = ?, author_id = ?, created = CURRENT_TIMESTAMP'
                ' WHERE id = ?',
                (title, description, status, priority, author_id, id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', task=task)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.index'))

@bp.route('/<int:id>/markdoing', methods=('POST',))
@login_required
def markdoing(id):
    get_task(id)
    db = get_db()
    db.execute(
        'UPDATE task SET status = ?, created = CURRENT_TIMESTAMP'
        ' WHERE id = ?',
        ("doing",id)
    )
    db.commit()
    return redirect(url_for('task.index'))

@bp.route('/<int:id>/markdone', methods=('POST',))
@login_required
def markdone(id):
    get_task(id)
    db = get_db()
    db.execute(
        'UPDATE task SET status = ?, created = CURRENT_TIMESTAMP'
        ' WHERE id = ?',
        ("done",id)
    )
    db.commit()
    return redirect(url_for('task.index'))