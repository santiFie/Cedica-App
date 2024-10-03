from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.payments import find_payments

bp = Blueprint('payments',__name__,url_prefix="/payments")

@bp.get('/')
def index_payments():
    # Obtener parámetros de búsqueda del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('payment_type')
    order_by = request.args.get('order_by', 'asc')
    page = request.args.get('page', 1, type=int)

    all_payments, max_pages = find_payments(start_date, end_date, payment_type, order_by, page)

    return render_template("payments/show_payments.html", payments = all_payments, max_pages = max_pages )

