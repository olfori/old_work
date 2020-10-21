'''all web page logic here'''
import csv

from os import path
from io import StringIO

from flask import render_template, json, request, redirect, url_for, make_response, flash

from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.models import User
from app.forms import LoginForm, ChangePassForm


@app.shell_context_processor
def make_shell_context():
    '''this can help when flask shell command will be tested'''
    return {'db': db, 'User': User}


@app.route('/')
@login_required
def index():
    '''Main page'''
    title = 'Quest management page'
    return render_template(
        'index.html',
        cont=app.config['CONTENT'],  # submit content to a web page
        js_script=1,                 # allow load js script
        title=title,                 #
        timer=app.game.timer.data,   #
        tech_box=app.game.master.tech_box,   # send tech_box state
        q_server='success',          #
        js_settings=app.config['JS_SETTINGS']
    )


@app.route('/ajax_data', methods=['POST'])
@login_required
def ajax_data():
    '''receive data from the client, and send in response'''
    data = json.loads(request.get_data(as_text=True))

    app.game.processing(data)

    return json.dumps(app.game.data)


@app.route('/download/')
@login_required
def post():
    '''Send .csv statistics file'''
    s_i = StringIO()
    c_w = csv.writer(s_i)
    csv_list = app.game.stat.get_global_stat()
    c_w.writerows(csv_list)
    output = make_response(s_i.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/change_pass', methods=['POST', 'GET'])
@login_required
def change_pass():
    '''Change user password'''
    ok_message = ''
    form = ChangePassForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        db.session.commit()
        u = User(username=current_user.username)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        ok_message = 'Password was updated successfully'
    return render_template('change_pass.html', title='Change password', message=ok_message, form=form)
