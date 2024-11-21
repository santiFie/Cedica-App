import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request, flash
from src.core.team_member import get_ranking_jobs
from src.core.riders_and_horsewomen import get_debtors
from src.core.payments import get_payments_on_date
from src.web.forms import validate_date_not_in_future
from datetime import datetime

bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.get("/jobs_ranking")
def report_jobs_ranking():

    table = get_ranking_jobs()
    ranked_table = [
        {"rank": i + 1, "job_position": row.job_position, "cant": row.cant}
        for i, row in enumerate(table)
    ]

    return render_template("reports/ranking_job.html", table = ranked_table)

@bp.get("/report_debts")
def report_debtors():
    
    table = get_debtors()


    return render_template("reports/debtors.html", table = table)

@bp.get("/report_payments_date")
def report_payment_date():
    
    date = request.args.get("date")

    table = get_payments_on_date(date)

    return render_template("reports/payments_on_date.html", table = table)
