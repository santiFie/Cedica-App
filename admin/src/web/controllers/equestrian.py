from flask import Blueprint
from src.core import team_member as tm
from src.core.models.riders_and_horsewomen import proposal_enum
from src.core import equestrian as eq
from flask import render_template, request, flash, url_for, redirect
from src.core import utils

bp = Blueprint("equestrian", __name__, url_prefix="/equestrians")

@bp.get("/new")
def new():

    email_lists = tm.list_emails_from_trainers_and_handlers()
    proposal = proposal_enum.enums

    return render_template("equestrians/new.html", email_list=email_lists, job_list=proposal)

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

    proposals = proposal_enum.enums
    email_lists = tm.list_emails_from_trainers_and_handlers()
    selected_emails = [team_member.email for team_member in equestrian.team_members]

    if equestrian.proposals:
        selected_proposals = [proposal for proposal in equestrian.proposals]
    else:
        selected_proposals = []

    return render_template("equestrians/edit.html", equestrian=equestrian, proposals=proposals, email_list=email_lists, selected_emails = selected_emails, selected_proposals=selected_proposals)

@bp.post("/update<int:id>")
def update(id):
    eq.equestrian_update(id, request.form)
    return redirect(url_for("equestrian.edit", id=id))



@bp.get("/list")
def list():
    #obtengo nro de pagina o por defecto tomo el 1
    page = request.args.get('page', 1, type=int) 

    # obtengo los filtros del formulario
    name = request.args.get('name', None)
    proposal = request.args.get('proposal', None)
    date_of_birth = request.args.get('date_of_birth', None)
    date_of_entry = request.args.get('date_of_entry', None)
    sort_by = request.args.get('sort_by', None)

    all_proposals = proposal_enum.enums


    # find_users tambien me devuelve la cantidad maxima de paginas para que sea evaluado en el html
    all_users, max_pages = eq.list_equestrians(page=page, name=name, proposal=proposal, date_of_birth=date_of_birth, date_of_entry=date_of_entry, sort_by=sort_by)
        
    return render_template("equestrians/list.html",list = all_users, page=page, max_pages=max_pages,all_proposals=all_proposals)

@bp.post("/delete<int:id>")
def delete(id):
    eq.equestrian_delete(id)
    return redirect(url_for("equestrian.list"))