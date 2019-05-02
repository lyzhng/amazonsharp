import datetime
import flask
import functools
import passlib.hash


def no_cache(view):
    "Don't cache page defined by given view."
    cache_control_content = 'no-store, no-cache, must-revalidate, ' + \
        'post-check=0, pre-check=0, max-age=0'

    @functools.wraps(view)
    def nocache(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = cache_control_content
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = -1
        return response
    return functools.update_wrapper(nocache, view)


def redirect_back():
    "Redirect the user to the original page after login or to the homepage."
    homepage = flask.url_for('public_views.home')
    dest = flask.session.get('next')
    return flask.redirect(dest) if dest else flask.redirect(homepage)


def secure_hash_password(password: str) -> str:
    "Hash the given password using Argon."
    return passlib.hash.argon2.using(rounds=12).hash(password)
