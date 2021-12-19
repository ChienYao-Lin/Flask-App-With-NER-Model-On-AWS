# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from apps.home.models import getResultsByAPI
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.models import user_exist, ch_password
from apps.home.forms import ChangePassForm, TextInputForm
from apps.authentication.util import verify_pass


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/chpwd.html', methods=['GET', 'POST'])
@blueprint.route('/chpwd', methods=['GET', 'POST'])
@login_required
def chpwd():
    chpwd_form = ChangePassForm(request.form)
    if 'chpwd' in request.form:

        # read form data
        old_pass = request.form['old_pass']
        new_pass = request.form['new_pass']

        # Locate user
        user_details = user_exist(current_user.username)

        # Check the password
        if verify_pass(old_pass, user_details[0]["password"]):
            ch_password(current_user.username, new_pass)
            flash('Successfully Changed! Please Re-login')
            return redirect(url_for('authentication_blueprint.logout'))

        # Something (user or pass) is not ok
        return render_template('home/chpwd.html',
                               msg='Wrong password',
                               form=chpwd_form)

    return render_template('home/chpwd.html', segment='chpwd', form=chpwd_form)

@blueprint.route('/job_analysis.html', methods=['GET', 'POST'])
@blueprint.route('/job_analysis', methods=['GET', 'POST'])
@login_required
def job_analysis():
    text_form = TextInputForm(request.form)
    if 'job_analysis' in request.form:
        # read form data
        text = request.form['text_input']
        results = getResultsByAPI(text)
        return render_template('home/job_analysis.html', segment='job_analysis', form=text_form, results = results)

    return render_template('home/job_analysis.html', segment='job_analysis', form=text_form)




@blueprint.route('/<template>')
@login_required
def route_template(template):

    if not template.endswith('.html'):
        template += '.html'

    # Detect the current page
    segment = get_segment(request)

    # Serve the file (if exists) from app/templates/home/FILE.html
    return render_template("home/" + template, segment=segment)


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

