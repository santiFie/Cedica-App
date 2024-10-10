from flask import Blueprint
from src.core.models.team_member import TeamMember
from flask import render_template

bp = Blueprint("equestrian", __name__, url_prefix="/equestrian")

@bp.get("/new")
def new():

    email_lists = TeamMember.query.filter((TeamMember.job_position == 'ENTRENADOR') | (TeamMember.job_position == 'HANDLER')).all()

    return render_template("equestrian/new.html", email_lists=email_lists)