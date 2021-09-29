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

    from_date, to_date = utils.validate_dates([from_date, to_date])
    if adjust_for_inflation:
        # Amount of money needed for same purchasing power...
        fnc = inflation.get_equivalent_worth
    else:
        # Remaining purchasing power...
        fnc = inflation.get_buying_power

        # Adjusted for inflation, (x) in (a) are worth (y) in (b)
        val = fnc(from_country_code, settings.WORLD_CPI, value, from_date, to_date)
        print("Adjusted for inflation, {0}{1} in {3} are worth {2}{1} in {4}.".format(value, from_country_code, val, from_date, to_date))
    
    if not to_country_code == None:
        # (x) in (a) are worth (y) in (b)
        val = exchange.get_exchanged_value(from_country_code, to_country_code, settings.WORLD_ER, val, to_date)
        print("This means: {0}{1} in {2} are worth {3}{4} in {5}.".format(value, from_country_code, from_date, val, to_country_code, to_date))

    return val