from flask import Blueprint
from src.core import team_member as tm
from src.core.models.team_member import JobEnum
from src.core import equestrian as eq
from flask import render_template, request, flash, url_for, redirect
from src.core import utils

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

@bp.get("/edit<int:id>")
def edit(id):

    equestrian = eq.find_equestrian_by_id(id)

    # Se pasan las fechas a string para que puedan ser mostradas en el formulario
    equestrian.date_of_birth = utils.date_to_string(equestrian.date_of_birth)
    equestrian.date_of_entry = utils.date_to_string(equestrian.date_of_entry)

    jobs = JobEnum.enums
    email_lists = tm.list_emails_from_trainers_and_handlers()
    selected_emails = [team_member.email for team_member in equestrian.team_members]

    if equestrian.jobs_in_institution:
        selected_jobs = [job for job in equestrian.jobs_in_institution]
    else:
        selected_jobs = []

    return render_template("equestrians/edit.html", equestrian=equestrian, job_list=jobs, email_list=email_lists, selected_emails = selected_emails, selected_jobs=selected_jobs)

@bp.post("/update<int:id>")
def update(id):
    eq.equestrian_update(id, request.form)
    return redirect(url_for("equestrian.edit", id=id))