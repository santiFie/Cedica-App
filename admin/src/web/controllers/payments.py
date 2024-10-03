from flask import Blueprint, render_template, request, url_for, redirect, session, flash

bp = Blueprint('payment',__name__,url_prefix="/payments")

@bp.get('/')
def index_payments():
    pass

