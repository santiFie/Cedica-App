from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum
from src.core import team_member as tm
from src.core import health_insurance as hi

bp = Blueprint('team_members',__name__,url_prefix="/team_members")

@bp.get("/new")
def new():

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums
    print(jobs)

    health_insurances = hi.get_all()

    return render_template("team_members/new.html", professions=professions, conditions=conditions, job_positions=jobs, health_insurances=health_insurances)

@bp.post("/create")
def create():

    team_member = tm.check_team_member_by_email(request.form["email"])

    if team_member:
        flash("El miembro de equipo ya existe")
        return redirect(url_for("team_members.new"))
    


    return redirect(url_for("team_members.new"))