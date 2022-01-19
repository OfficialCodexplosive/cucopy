import datetime
import warnings
from .parser import Parser

class Currency(object):
    """
    Currency class

    The Currency class provides the following functionality:

    * It provides the basic structure of a value, meaning, it stores information about its dimension (i.e. the actual monetary value), its recording date and its unit.
    * In addition to the most common scientific number notations (K, M, B, T), it is also possible to store a currency with a custom notation and value.
    * It allows for easy adjustment for inflation of the provided value, in terms of taking a base value from date A and calculating its worth at date B.
    
    The parameters stored in a Currency object refer to:

    * the date, at which the value, which is to be adjusted for inflation, was recorded (**recording_date**)
    * the actual value to be adjusted (**value**)
    * the scientific notation of the value (**notation**; e.g. 'K' for 1.000, 'M' for 1.000.000, etc.)
    * the currency in which the value was recorded (**currency**; for now: EURO)

    When creating a Currency object with a custom notation, following parameters are added:

    * the scientific notation of the new unit (**notation_pow**; the value of a unit is determined as follows: 1E[notation_pow]).
    
    Following parameters are also stored in an instance of this class, but only after initialization:

    * the target date, meaning, the date, to which adjust the value to (**target_date**)
    * the parser, which handles the extraction of CPIs from a table (**parser**)
    """
    YYYY_MM_DD = '%Y-%m-%d'
    _allowed_date_formats = [YYYY_MM_DD]

    EUR = "eur"
    _allowed_currencies = [EUR]

    " dictionary of the most important scientific number notations and their value "
    _allowed_notations = {
        ""  : int(1e0),
        "K" : int(1e3),
        "M" : int(1e6),
        "B" : int(1e9),
        "T" : int(1e12)         
    }

    """specify currency and notation in kwargs.
       default is: 1, EUR, 10^0."""
    """value means [value] * notation"""
    def __init__(self, recording_date : str, value : float = 1, **kwargs):
        """
        Constructor for creating a Currency class instance

        **Required arguments:**
        :param recording_date: the date, at which a value was recorded
        :type recording_date: string

        **Default arguments:**
        :param value: the monetary value. The default value is 1
        :type value: float

        :param notation: the notation of the value. The default is '', meaning 1E0
        :type notation: string

        :param currency: the currency in which the value was recorded. The default is 'Eur'.
        :type currency: string
        """

        self.recording_date = self._validate_date(recording_date)
        self.value = value

        if('notation' in kwargs):
            _notation = kwargs.get('notation')
            if _notation in self._allowed_notations:
                self.notation = kwargs.get('notation')
            else:
                raise ValueError(f"Notation {_notation} not supported.\nSupported notations are: {self._allowed_notations}.")
        else:
            self.notation = ""
        
        if('currency' in kwargs):
            _currency = kwargs.get('currency')
            if _currency in self._allowed_currencies:
                self.currency = _currency
            else:
                raise ValueError(f"Currency {_currency} not supported.\nSupported currencies are: {self._allowed_currencies}.")
        else:
            self.currency = self.EUR

    @classmethod
    def unique_notation(cls, recording_date : str, notation : str, notation_pow : int, value : float = 1, **kwargs):
        """
        Decorator for creating a Currency class instance with a custom notation.

        **Required arguments:**
        :param recording_date: the date, at which a value was recorded
        :type recording_date: string

        :param notation: the new and unique symbol/ string, by which the notation should be referred to
        :type notation: string

        :param notation_pow: the scientific notation of the new unit. The value of a unit is determined as follows: 1E[notation_pow]
        :type notation_pow: int

        **Default arguments:**
        :param value: the monetary value. The default value is 1
        :type value: float

        :param currency: the currency in which the value was recorded. The default is 'Eur'.
        :type currency: string
        """
        
        if value == None:
            value = 1
        if notation not in cls._allowed_notations:
            cls._allowed_notations[notation] = 10**notation_pow
        else:
            raise ValueError(f"Notation {notation} already defined.")
        return cls(recording_date, value, notation=notation, kwargs=kwargs)

    def _validate_date(self, date_str):
        # TODO: COMPARE AGAINST DIFFERENT FORMATS AND RETURN AS YYYY-MM-DD
        try:
            return datetime.datetime.strptime(date_str, self.YYYY_MM_DD)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def set_target_date(self, date_str):
        """
        Function for setting the date, to which should be adjusted to.

        :param date_str: the target date, as a string
        :type date_str: string
        """
        self.target_date = self._validate_date(date_str)

    def set_parser(self, path=None, delim=';', language='de', classification='all'):
        """
        Function for setting the parser.

        :param path: the path at which the csv file containing the recorded cpi values is stored
        :type path: string

        :param delim: the csv delimiter, by which the values are separated
        :type delim: string

        :param language: the language, in which the csv file is stored. Only needed, when no custom csv file is provided via path.
        :type language: string
        """
        if path == None:
            self.parser = Parser(language=language, classification=classification)
        else:
            self.parser = Parser.specified_path(csv_path=path, csv_delim=delim, classification=classification)

    def get_equivalent_worth(self):
        """
        Function for getting the inflation-corrected value.

        :returns: the base value adjusted for inflation
        :rtype: float
        """
        try:
            recording_cpi = self.parser.get_cpi(self.recording_date)

            try:
                target_cpi = self.parser.get_cpi(self.target_date)
            except AttributeError:
                warnings.warn("No target date specified. Did you forget to call \'set_target_date(date_str)\'?", RuntimeWarning)
                return None

            return ((self.value * target_cpi)/recording_cpi)
        except AttributeError:
            warnings.warn("No parser assigned. Did you forget to call \'set_parser(...)\'?", RuntimeWarning)
            return None

    def get_purchasing_power(self):
        """
        Function for getting the purchasing power of a value.

        :returns: the base value's remaining purchasing power
        :rtype: float
        """
        try:
            recording_cpi = self.parser.get_cpi(self.recording_date)

            try:
                target_cpi = self.parser.get_cpi(self.target_date)
            except AttributeError:
                warnings.warn("No target date specified. Did you forget to call \'set_target_date(date_str)\'?", RuntimeWarning)
                return None

            return (recording_cpi/target_cpi)*self.value
        except AttributeError:
            warnings.warn("No parser assigned. Did you forget to call \'set_parser(...)\'?", RuntimeWarning)
            return None

"""Change in CPI:    TARGET_CPI / RECORDING_CPI
 Adjust EURO for inflation:
   A wind turbine had a recording price of 1.750.000€ in Dec, 2006.
   What would that be in Nov, 2021?

   CPI:
     Dec, 2006: 88.3
     Nov, 2021: 110.5

   88.3/110.5  =  1.750.000/X  => X = (1.750.000*110.5)/88.3"""

"""Calculate remaining purchasing power:
CPI:
     Dec, 2006: 88.3
     Nov, 2021: 110.5

(110.5/88.3) * X
"""

