

def get_all():
    """
    Get all health insurances
    """
    from src.core.models.health_insurance import HealthInsurance

    health_insurances = HealthInsurance.query.all()

    return health_insurances

def get_by_id(id):

    from src.core.models.health_insurance import HealthInsurance

    health_insurance = HealthInsurance.query.filter_by(id = id).first()

    return health_insurance