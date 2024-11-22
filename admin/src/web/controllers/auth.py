from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.web.forms.AuthForm import AuthForm as af
from src.web.handlers.auth import login_required
from src.core import auth
import requests
from src.web.oauth import oauth

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.get("/login")
def login_google():
    """
    Renders the login page
    """
    redirect_uri = url_for('auth.verification_with_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp.get("/")
def login():
    """
    Renders the login page
    """
    return render_template("auth/login.html")


    

@bp.post("/authenticate")
def verification():
    """
    Verifies the user credentials
    """

    form = af(request.form)
    if form.validate():
        params = request.form
        user = auth.check_user(params["email"], params["password"])
        if not user:
            flash("Usuario o contraseña inválidos", "info")
            return redirect(url_for("auth.login"))

        if auth.user_is_active(user):
            session["user"] = user.email
            return redirect(url_for('home'))
        else:
            flash(
                "Tu cuenta ha sido desactivada. Por favor, contacta a un administrador", "info")
    else:
        flash("Faltan campos por completar", "info")

    return redirect(url_for("auth.login"))

    

@bp.route("/google/callback")
def verification_with_google():
    """
    Verifies the user credentials
    """
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token, nonce=None)

    if user_info:
        if auth.find_user_by_email(user_info["email"]) is None:
            flash('No tienes permisos para acceder', 'error')
            revoke_google_token(token['access_token']) # To have the chance to choose another account
            return redirect(url_for('auth.login'))
        session['user'] = user_info["email"]
        session["google_token"] = token['access_token']
        flash('Inicio de sesión exitoso')
        return render_template('home.html')
    else:
        flash('Error al iniciar sesión', 'error')
        return redirect(url_for('auth.login'))

def revoke_google_token(token):

    try:
        revoke_url = f'https://accounts.google.com/o/oauth2/revoke?token={token}'
        response = requests.get(revoke_url)
        
        # Check if revocation was successful
        if response.status_code == 200:
            return True
        else:
            return False
    
    except Exception as e:
        flash("Error al revocar el token", "error")

@bp.get("/logout")
@login_required
def logout():
    """
    Logs out the logged-in user and clears the session
    """
    if (session.get('google_token')):
        revoke_google_token(session['google_token'])
    if (session.get('user')):
        del session['user']
        session.clear()
    return redirect(url_for('auth.login'))
