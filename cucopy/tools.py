from .components import exchange, inflation, utils, settings
from .components.update import download_and_extract

def update():
    download_and_extract(settings.DOWNLOAD_CPI, settings.WORLD_CPI)
    download_and_extract(settings.DOWNLOAD_ER, settings.WORLD_ER)

def adjust_currency(from_country_code : str,
        from_date : str,
        value : float = 1,
        adjust_for_inflation : bool = False, 
        to_country_code : str = None, 
        to_date : str = None):

    if to_country_code == None and to_date == None:
        raise ValueError("\'to_country_code\' and/or \'to_date\' must be specified.")

    if to_date == None:
        from_date = utils.get_valid_date(from_date)
        date = from_date
        val = value
    else:
        from_date, to_date = utils.validate_dates([from_date, to_date])
        date = to_date
        if adjust_for_inflation:
            fnc = inflation.get_equivalent_worth
            print("Amount of money needed for same purchasing power...")
        else:
            fnc = inflation.get_buying_power
            print("Remaining purchasing power...")

        val = fnc(from_country_code, settings.WORLD_CPI, value, from_date, to_date)
        print("Adjusted for inflation, {0}{1} in {3} are worth {2}{1} in {4}.".format(value, from_country_code, val, from_date, to_date))
    
    if not to_country_code == None:
        val = exchange.get_exchanged_value(from_country_code, to_country_code, settings.WORLD_ER, val, date)
        print("This means: {0}{1} in {2} are worth {3}{4} in {5}.".format(value, from_country_code, from_date, val, to_country_code, to_date))

    return val