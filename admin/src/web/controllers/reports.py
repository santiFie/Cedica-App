from flask import Blueprint, render_template, request, flash
from src.core.team_member import get_ranking_jobs
from src.core.riders_and_horsewomen import get_debtors
from src.core.payments import get_payments_on_date
from src.core.collections import calculate_debt
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions


bp = Blueprint("reports", __name__, url_prefix="/reports")


@login_required
@check_permissions("report_jobs_ranking")
@bp.get("/jobs_ranking")
def report_jobs_ranking():

    table = get_ranking_jobs()
    ranked_table = [
        {"rank": i + 1, "job_position": row.job_position, "cant": row.cant}
        for i, row in enumerate(table)
    ]

    return render_template("reports/ranking_job.html", table = ranked_table)


@login_required
@check_permissions("report_debtors")
@bp.get("/report_debts")
def report_debtors():
    
    debtors = get_debtors()

    debtors_with_debt = [
        {
            "name": debtor.name,
            "last_name": debtor.last_name,
            "dni": debtor.dni,
            "address": debtor.address,
            "phone": debtor.phone,
            "debt": len(calculate_debt(debtor.dni)[0])
        }
        for debtor in debtors
    ]

    table = debtors_with_debt


    return render_template("reports/debtors.html", table = table)


@login_required
@check_permissions("report_payment_date")
@bp.get("/report_payments_date")
def report_payment_date():

    date = request.args.get("date")

    table = get_payments_on_date(date)

    return render_template("reports/payments_on_date.html", table = table)
