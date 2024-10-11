from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.collections import find_collections
from datetime import datetime


bp = Blueprint('collectios',__name__,url_prefix="/collections")


@bp.get('/')
def index_collections():

    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_method = request.args.get('payment_method')
    name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    all_collections, max_pages = find_collections(start_date, end_date, payment_method, name, last_name, order_by, page)

    return render_template("collectios/show_collections.html", collections = all_collections, max_pages = max_pages, current_page = page)


@bp.get('/collection_register_form')
def collection_register_form():
    return render_template("collections/collection_register_form.html")


