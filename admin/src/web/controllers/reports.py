import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from src.core.team_member import get_ranking_jobs
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