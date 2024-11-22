import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from src.core.riders_and_horsewomen import get_scolarship, get_no_scolarship
from src.core.collections import get_collection_per_year
from src.core.riders_and_horsewomen import get_disability_types
from datetime import datetime
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions


bp = Blueprint("graphics", __name__, url_prefix="/graphics")


@login_required
@check_permissions("graphic_index")
@bp.get("/")
def graphic_index():


    years = list(range(2010, datetime.now().year + 1))

    return render_template("graphics/graphics.html", years = years)

@login_required
@check_permissions("graphic_scolarship_percentage")
@bp.get("/scolarship_percentage")
def graphic_scolarship_percentage():

    jye_scorlaship = get_scolarship()

    jye_no_scolarship = get_no_scolarship()

    data = {
        "Category" : ["Becados", "No Becados"],
        "Values" : [jye_scorlaship, jye_no_scolarship]
    }

    fig = px.pie(
        data_frame = data,
        names = "Category",
        values = "Values",
        title ="Grafico de los JyA becados",
        color_discrete_sequence=px.colors.sequential.RdBu 
    )

    fig.update_traces(
        textinfo = "percent+label",
        pull =[0,0.1,0,0]
    )

    fig = fig.to_html(full_html=False)

    years = list(range(2010, datetime.now().year + 1))
    return render_template("graphics/graphics.html", fig = fig, years = years)


@login_required
@check_permissions("graphic_collection_per_year")
@bp.get("/collection_per_year")
def graphic_collection_per_year():

    year = request.args.get('year')

    collections = get_collection_per_year(year)

    years = list(range(2010, datetime.now().year + 1))

    if not collections or all(x == 0 for x in collections):
        fig = "No hay registro de cobros en el año seleccionado"

        return render_template("graphics/graphics.html", fig = fig, years = years)
    
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    data = pd.DataFrame({
    'Mes': months,
    'Ingresos': collections
    })

    fig = px.bar(
        data_frame = data,
        x='Mes', 
        y='Ingresos', 
        title=f'Ingresos por Mes en {year}',
        labels={'Mes': 'Mes', 'Ingresos': 'Ingresos ($)'}
        
    )
    
    fig = fig.to_html(full_html=False)

    return render_template("graphics/graphics.html", fig = fig, years = years)


@login_required
@check_permissions("graphic_disability_type")
@bp.get("/disability_type")
def graphic_disability_type():
    
    years = list(range(2010, datetime.now().year + 1))

    disabilitys = get_disability_types()

    data = {
        "tipo de discapacidad" : [d[0] for d in disabilitys],
        "valor" : [d[1] for d in disabilitys]
    }

    fig = px.pie(
        data_frame = data,
        names = "tipo de discapacidad",
        values = "valor",
        title ="Grafico de los tipos de discapacidad",
        color_discrete_sequence=px.colors.sequential.RdBu 
    )

    fig.update_traces(
        textinfo = "percent+label",
        pull =[0,0.1,0,0]
    )

    fig = fig.to_html(full_html=False)

    years = list(range(2010, datetime.now().year + 1))
    return render_template("graphics/graphics.html", fig = fig, years = years)




    

    
