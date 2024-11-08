from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.web.forms import AuthForm as af
from src.web.handlers.auth import login_required
from src.core import auth

from src.web.oauth import oauth

bp = Blueprint('auth', __name__, url_prefix="/auth")

# google = oauth.remote_app(
#     'google',
#     consumer_key=environ.get('GOOGLE_CLIENT_ID'),
#     consumer_secret= environ.get('GOOGLE_CLIENT_SECRET'),
#     request_token_params={'scope': 'email profile'},
#     base_url='https://accounts.google.com/',
#     request_token_url=None,
#     access_token_url='https://oauth2.googleapis.com/token',
#     authorize_url='https://accounts.google.com/o/oauth2/auth'
# )

@bp.route("/login")
def login():
    """
    Renders the login page
    """
    redirect_uri = url_for('auth.verification', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
    


@bp.route("/google/callback")
def verification():
    """
    Verifies the user credentials
    """
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token, nonce=None)

    if user_info:
        session['user'] = user_info["email"]
        flash('Inicio de sesión exitoso', 'success')
        return render_template('home.html')
    else:
        flash('Error al iniciar sesión', 'error')
        return redirect(url_for('auth.login'))
    

@bp.get("/logout")
@login_required
def logout():
    """
    Logs out the logged-in user and clears the session
    """
    if (session.get('user')):
        del session['user']
        session.clear()
    return redirect(url_for('auth.login'))
