

def get_all():
    """
    Get all health insurances
    """
    from src.core.models.health_insurance import HealthInsurance

    health_insurances = HealthInsurance.query.all()

    return health_insurances