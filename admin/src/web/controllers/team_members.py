from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.core.models.team_member import ProfessionEnum, JobEnum, ConditionEnum
from src.core import team_member as tm
from src.core import health_insurance as hi

bp = Blueprint('team_members',__name__,url_prefix="/team_members")


@bp.get("/")
def team_members_list():

    page = request.args.get('page', 1, type=int) ##Obtengo el numero de pag

    team_members = tm.find_team_members(page) #Muestro los primeros 25 users

    if not team_members:
        flash("No hay miembros del equipo cargados en el sistema", "info")
        return render_template("home.html")
    
    return render_template("team_members/show_team_members.html", list = team_members)

@bp.get("/new")
def new():

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums

    health_insurances = hi.get_all()

    return render_template("team_members/new.html", professions=professions, conditions=conditions, job_positions=jobs, health_insurances=health_insurances)

@bp.post("/create")
def create():

    team_member = tm.check_team_member_by_email(request.form["email"])

    if team_member:
        flash("El miembro de equipo ya existe")
        return redirect(url_for("team_members.new"))
    
    tm.create(request.form)
    
    return redirect(url_for("team_members.new"))

@bp.get("show_team_member")
def show_team_member():
    team_member_email = request.args.get('team_member_email')   ##Deberia tomarlo por el id?

    

    team_member = tm.check_team_member_by_email(team_member_email)
    
    return render_template("team_members/view_team_member.html", team_member=team_member)

@bp.get("/edit")
def edit_team_member():

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums

    team_member_email = request.args.get('team_member_email')

    team_member = tm.check_team_member_by_email(team_member_email)

    health_insurances = hi.get_all()

    return render_template("team_members/edit_team_member.html", team_member = team_member, health_insurances = health_insurances, professions = professions, conditions = conditions, jobs = jobs)


@bp.post("/update")
def update_team_member():

    team_member_email = request.args.get('team_member_email')

    

    team_member = tm.edit(
        name = request.form['name'],
        last_name = request.form['last_name'],
        address = request.form['address'],
        email = team_member_email,
        locality = request.form['locality'],
        phone = request.form['phone'],
        end_date = request.form['end_date'],
        emergency_contact = request.form['emergency_contact'],
        emergency_phone = request.form['emergency_phone'],
        health_insurance = request.form['health_insurance'],
        condition = request.form['condition'],
        job_position = request.form['job_position'],
        profession = request.form['profession']
    )

    professions = ProfessionEnum.enums
    conditions = ConditionEnum.enums
    jobs = JobEnum.enums
    health_insurances = hi.get_all()

    flash("Usuario actualizado")
    return redirect(url_for('team_members.team_members_list'))

