#!/usr/bin/python3
from flask import (
    redirect,
    render_template,
    request,
    session,
)
import re
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy import (
    Spotify
)
import webbrowser

from app import app

@app.route("/")
def index():
    """Display homepage w/login link"""
    return render_template("index.html", title="Home")


@app.route("/login/")
def login():
    """
    Routes user to unique authorization URL. Redirects back to app via redirect_uri
    """
    auth_manager = SpotifyOAuth(
        client_id=app.config["SPOTIPY_CLIENT_ID"],
        client_secret=app.config["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=app.config["SPOTIPY_REDIRECT_URI"],
        scope=app.config["SCOPE"]
    )
    url = auth_manager.get_authorize_url()

    # Code is the result of the redirect
    return redirect(url, code=302)


@app.route("/callback/")
def code_generation():
    """
    Authenticates app via response URL assigned to app (in Spotify), allowing access to code
    and giving user information.
    """
    sp = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=app.config["SPOTIPY_CLIENT_ID"],
            client_secret=app.config["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=app.config["SPOTIPY_REDIRECT_URI"],
            scope=app.config["SCOPE"]
        )
    )

    # Get some user information to display
    user_info = sp.current_user()

    return render_template(
        "callback.html",
        user_info=user_info
    )
