from flask import (
    redirect,
    render_template,
    request,
    session,
)
import re
from spotipy import (
    Credentials,
    scopes,
    Scope,
    Spotify
)
import webbrowser

from app import app

@app.route('/')
def index():
    """Display homepage w/login link"""
    return render_template('index.html', title='Home')


@app.route('/login/')
def login():
    """Log user into Spotify"""
    c = Credentials(
        app.config['CLIENT_ID'],
        app.config['CLIENT_SECRET'],
        app.config['REDIRECT_URI']
    )
    scope = Scope(*scopes)
    url = c.authorisation_url(scope)

    # Code is the result of the redirect
    return redirect(url, code=302)


@app.route('/callback/')
def code_generation():
    """Generates token from code in browser"""
    code = re.search(r'code=(.*)', request.environ['QUERY_STRING']).group(1)
    c = Credentials(
        app.config['CLIENT_ID'],
        app.config['CLIENT_SECRET'],
        app.config['REDIRECT_URI']
    )
    scope = Scope(*scopes)
    token = c.request_access_token(code, scope)

    s = Spotify(token.access_token)

    return render_template('callback.html')
