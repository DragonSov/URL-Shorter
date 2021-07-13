from flask import Blueprint, request, render_template, abort, url_for, redirect,\
    flash
from flask_login import current_user
from blueprints import db
from .models import Url
import string
from random import choices

shorter = Blueprint(
    "shorter", __name__, template_folder="templates", static_folder="static")


@shorter.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Forms
        url = request.form['url']
        if url:
            # URL Template
            if not url.startswith('https://') or not url.startswith('http://'):
                url = 'http://' + url
            if not current_user.is_authenticated:
                creator = ""
            else:
                creator = current_user.username
            short_url = ''.join(choices(string.ascii_letters + string.digits,
                                        k=6))

            new_url = Url(
                original_url=url,
                short_url=short_url,
                creator=creator
            )

            # Add URL
            db.session.add(new_url)
            db.session.commit()

            return render_template('index.html', short_url=url_for(f"shorter.redirect_url", short_url=short_url, _external=True))
    else:
        return render_template('index.html')


@shorter.route('/<string:short_url>')
def redirect_url(short_url):
    # Find original URL
    url = Url.query.filter(Url.short_url == short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        return abort(404)


@shorter.route('/delete_url', methods=['POST'])
def delete_url():
    # Form
    url = request.form['del-url']
    if url:
        # Find URL and delete it
        db.session.delete(Url.query.filter(Url.short_url == url).first())
        db.session.commit()

        return redirect('/profile')
    else:
        flash('Вы не выбрали ссылку для удаления.')
        return redirect('/profile')
