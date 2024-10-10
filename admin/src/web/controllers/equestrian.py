from flask import Blueprint
from src.core import team_member as tm
from src.core.models.team_member import JobEnum
from src.core import equestrian as eq
from flask import render_template, request, flash, url_for, redirect

bp = Blueprint("equestrian", __name__, url_prefix="/equestrians")

@bp.get("/new")
def new():

    email_lists = tm.list_emails_from_trainers_and_handlers()
    jobs = JobEnum.enums

    return render_template("equestrians/new.html", email_list=email_lists, job_list=jobs)

@bp.post("/create")
def create():

    equestrian = eq.find_equestrian_by_name(request.form["name"])
    
    if equestrian:
        flash("El equestre ya existe")
        return redirect(url_for("equestrian.new"))
    
    eq.equestrian_create(request.form)

    return redirect(url_for("equestrian.new"))
