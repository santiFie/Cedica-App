from src.core.database import db
from src.core.models.collection import Collection, PaymentMethod
from src.core.models.team_member import TeamMember
from src.core.models.riders_and_horsewomen import RiderAndHorsewoman
from src.core.riders_and_horsewomen import find_rider
from datetime import datetime, timedelta
import locale
from sqlalchemy.orm import aliased
from sqlalchemy import extract
from sqlalchemy import func


def find_collections(
    start_date=None,
    end_date=None,
    payment_method=None,
    name=None,
    last_name=None,
    order_by="asc",
    page=1,
):
    """
    Search for all collections with the given parameters
    """

    per_page = 25

    # General query
    query = Collection.query

    # Filter by date range
    if start_date:
        query = query.filter(
            Collection.payment_date >= datetime.strptime(start_date, "%Y-%m-%d")
        )
    if end_date:
        query = query.filter(
            Collection.payment_date <= datetime.strptime(end_date, "%Y-%m-%d")
        )

    # Filter by payment method
    if payment_method:
        query = query.filter(Collection.payment_method == payment_method)

    # Create alias for the TeamMember table to avoid 'DuplicateAlias'
    if name or last_name:
        team_member_alias_name = aliased(TeamMember)
        team_member_alias_last_name = aliased(TeamMember)

    # Filter by payment receiver's name (team member)
    if name:
        query = query.join(
            team_member_alias_name,
            team_member_alias_name.email == Collection.team_member_id,
        ).filter(team_member_alias_name.name.ilike(f"%{name}%"))

    # Filter by payment receiver's last name (team member)
    if last_name:
        query = query.join(
            team_member_alias_last_name,
            team_member_alias_last_name.email == Collection.team_member_id,
        ).filter(team_member_alias_last_name.last_name.ilike(f"%{last_name}%"))

    # Order by payment date
    if order_by == "asc":
        query = query.order_by(Collection.payment_date.asc())
    else:
        query = query.order_by(Collection.payment_date.desc())

    total_collections = query.count()

    # Handle the case where there are no collections
    if total_collections == 0:
        return [], 0

    max_pages = (
        total_collections + per_page - 1
    ) // per_page  # Round up to calculate the number of pages

    # Ensure the requested page is not less than 1
    if page < 1:
        page = 1

    # Ensure the requested page is not greater than the maximum number of pages
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    collections = query.offset(offset).limit(per_page).all()

    return collections, max_pages


def create_collection(**kwargs):
    """
    Creates a collection with the given parameters
    """

    payment_type_str = kwargs["payment_method"]  # Captura el string del metodo de pago

    collection = Collection(
        amount=kwargs["amount"],
        payment_date=kwargs["payment_date"],
        payment_method=payment_type_str,
        observations=kwargs.get("observations", ""),
        team_member_id=kwargs["team_member_id"],
        rider_dni=kwargs["rider_dni"],
    )

    # Agregar el pago a la base de datos
    try:
        db.session.add(collection)
        db.session.flush()
    except:
        db.session.rollback()
        return None
    db.session.commit()

    # calcular si el rider es deudor, si no lo es le cambio debtor = False
    rider = find_rider(kwargs["rider_dni"])

    if rider:
        has_debt = check_debtor(rider)
        rider.debtor = has_debt
        db.session.commit()

    return collection


def find_collection(id):
    """
    Search for a collection with the given parameter
    """

    collection = Collection.query.get(id)

    return collection


def edit_a_collection(**kwargs):
    """
    Updates a collection with the given parameters
    """

    collection = find_collection(kwargs["collection_id"])

    if collection:

        collection.rider_dni = kwargs.get("rider_dni", collection.rider_dni)
        collection.team_member_id = kwargs.get(
            "team_member_id", collection.team_member_id
        )
        collection.amount = kwargs.get("amount", collection.amount)
        collection.payment_date = kwargs.get("payment_date")
        collection.payment_method = kwargs.get(
            "payment_method", collection.payment_method
        )
        collection.observations = kwargs.get("observations", collection.observations)

        db.session.commit()
        return collection
    return None


def delete_a_collection(collection):
    """
    Deletes the collection given by parameter
    """

    db.session.delete(collection)
    db.session.commit()

    return True


def create_enums_collection():
    """
    Creates the enums values for collections
    """
    # from src.core.models.payment import PaymentType

    PaymentMethod.create(db.engine, checkfirst=True)


def find_debtors(start_date=None, end_date=None, dni=None, order_by="asc", page=1):
    """
    Search for all debtors with the given parameters
    """
    per_page = 25

    # Get all riders who are debtors
    query = RiderAndHorsewoman.query.filter(RiderAndHorsewoman.debtor == True)

    # Filter by date range (optional)
    if start_date:
        query = query.filter(
            RiderAndHorsewoman.inserted_at >= datetime.strptime(start_date, "%Y-%m-%d")
        )
    if end_date:
        query = query.filter(
            RiderAndHorsewoman.inserted_at <= datetime.strptime(end_date, "%Y-%m-%d")
        )

    # Filter by DNI (optional)
    if dni:
        query = query.filter(RiderAndHorsewoman.dni.ilike(f"%{dni}%"))

    # Order by payment date
    if order_by == "asc":
        query = query.order_by(RiderAndHorsewoman.inserted_at.asc())
    else:
        query = query.order_by(RiderAndHorsewoman.inserted_at.desc())

    # Count the total number of debtors that meet the filters
    total_debtors = query.count()

    # If there are no results, return an empty list and 0 pages
    if total_debtors == 0:
        return [], 0

    max_pages = (
        total_debtors + per_page - 1
    ) // per_page  # Round up to calculate the number of pages

    # Ensure the requested page is within the valid range
    if page < 1:
        page = 1

    if page > max_pages:
        page = max_pages

    # Pagination: calculate the offset and limit the results
    offset = (page - 1) * per_page
    debtors = query.offset(offset).limit(per_page).all()

    return debtors, max_pages


def check_debtor(rider):
    """
    Checks if the rider given by parameter is a debtor
    """
    # Get the current date
    current_date = datetime.now()

    # If there is no insertion date, move to the next rider
    if not rider.inserted_at:
        return False

    # Calculate the difference in months from the insertion date to the current month
    months_diff = (
        (current_date.year - rider.inserted_at.year) * 12
        + current_date.month
        - rider.inserted_at.month
    )

    # Check if there is a missing payment for each elapsed month
    for month_offset in range(months_diff):
        # Get the first day of the elapsed month
        first_day_of_month = rider.inserted_at.replace(
            year=current_date.year, month=current_date.month, day=1
        )

        # Get the first and last day of the month in full date format
        start_of_month = first_day_of_month
        end_of_month = (first_day_of_month + timedelta(days=32)).replace(
            day=1
        ) - timedelta(days=1)

        # Check if there is a payment for that month
        existing_payment = (
            Collection.query.filter_by(rider_dni=rider.dni)
            .filter(
                Collection.payment_date >= start_of_month,
                Collection.payment_date <= end_of_month,
            )
            .first()
        )

        # If there is no payment for that month, the rider has debt
        if not existing_payment:
            return True

    return False


def calculate_debt(debtor_dni):
    """
    Calculate all debts of the given parameter
    """

    # Array of months in Spanish
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    # Get the rider's insertion date
    rider = find_rider(debtor_dni)
    insertion_date = rider.inserted_at
    current_date = datetime.now()

    # List of missing payments
    missing_payments = []

    # Iterate through each month from the insertion date to the current date
    # From the year and month of insertion to the current year and month
    current_year = current_date.year
    current_month = current_date.month
    start_year = insertion_date.year
    start_month = insertion_date.month

    # Iterate through the months between the insertion date and the current date
    for year in range(start_year, current_year + 1):
        # Calculate the range of months to iterate for each year
        start = start_month if year == start_year else 1
        end = current_month if year == current_year else 12

        for month in range(start, end + 1):
            # Check if there is a payment for that month and year
            payment = (
                db.session.query(Collection)
                .filter_by(rider_dni=rider.dni)
                .filter(extract("month", Collection.payment_date) == month)
                .filter(extract("year", Collection.payment_date) == year)
                .first()
            )

            if not payment:
                # Get the name of the month
                month_name = meses[
                    month - 1
                ]  # Subtract 1 because the array starts at 0
                missing_payments.append(f"{month_name} de {year}")

    return missing_payments, rider

def get_collection_per_year(year):

    
    collections = (
        db.session.query(
            extract("month", Collection.payment_date).label("mes"),
            func.sum(Collection.amount).label("total_monto")
        )
        .filter(extract("year", Collection.payment_date) == year)
        .group_by(extract("month", Collection.payment_date))
        .order_by(extract("month", Collection.payment_date))
        .all()
    )

    month_to_amount = {int(mes): total_monto for mes, total_monto in collections}

    month_collections = [month_to_amount.get(month, 0) for month in range(1, 13)]
    
    return month_collections

