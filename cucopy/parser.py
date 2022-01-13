import pandas as pd
import os, pathlib
import datetime
import urllib.request
from locale import atof, setlocale, LC_NUMERIC

from .config import DATASET_PATH, _timeseries

class Parser(object):
    """
    Parser class

    The Parser class provides the following functionality:

    * It parses a csv file in its corresponding language and extracts the CPI value from a given date.
    
    The parameters stored in a Parser object refer to:

    * the language, in which the csv file was created (**language**; useful for choosing the correct delimiter)
    * the delimiter used for separating the values in the file (**delimiter**; if no language was provided)
    * the id of the csv file as outlined by the Deutsche Bundesbank (**classification**: https://www.bundesbank.de/dynamic/action/de/statistiken/zeitreihen-datenbanken/zeitreihen-datenbank/759778/759778?listId=www_s300_mb09_07)
    * the proper locale module, derived from the specified language (**locale_module**)
    """
    _supportedLang = {
        'en' : ',',
        'de' : ';'}

    def __init__(self, **kwargs):
        """
        Constructor for creating a Currency class instance

        **Default arguments:**
        :param language: the language of the .csv-files, important for parsing the file using pandas. Default is 'de'.
        :type language: string

        :param delimiter:  the delimiter used in a .csv-file, important for deducing the csv-file's location and parsing it using pandas, if no language is specified.
        :type delimiter: string 

        :param classification: the ID used to refer to the .csv-file.
        :type classification: string 
        """
        if 'language' in kwargs:
            if kwargs.get('language') in self._supportedLang.keys():
                _lang = kwargs.get('language')
                self.lang_delim_pair = (_lang, self._supportedLang[_lang])
                self.locale_module = 'de_DE.utf8' if (_lang == 'de') else 'en_US.utf8'
        elif 'delimiter' in kwargs:
            if kwargs.get('delimiter') == ',':
                self.lang_delim_pair = ('en', ',')
        else:
            self.lang_delim_pair = ('de', ';')
            self.locale_module = 'de_DE.utf8'

        if 'classification' in kwargs:
            if kwargs.get('classification') in _timeseries:
                self.data_classification = _timeseries[kwargs.get('classification')]
        else:
            self.data_classification = _timeseries['all']

        """ Path to where the default dataset will lie """
        default_path = os.path.join(DATASET_PATH, self.lang_delim_pair[0] ,(f"BBDP1.M.DE.N.VPI.C.{self.data_classification}.I15.A.csv"))

        self.df = pd.read_csv(default_path, delimiter=self.lang_delim_pair[1])

    @classmethod
    def specified_path(self, path : str, delimiter : str):
        """
        Decorator for creating a Parser class instance with a custom path to a csv file.

        **Required arguments:**
        :param path: the path to the custom .csv-file.
        :type path: string

        :param delimiter:  the delimiter used in a .csv-file, important for parsing the file using pandas.
        :type delimiter: string 
        """
        self.df = pd.read_csv(csv_path, delimiter=csv_delim)

    def get_cpi(self, date : datetime.datetime):
        """
        Function for extracting the cpi from the Parser object's dataframe (self.df).

        :param date_str: the target date, as a string
        :type date_str: string
        """
        setlocale(LC_NUMERIC, self.locale_module)

        month = str(date.month).zfill(2)

        date_index = f"{date.year}-{month}"
        date_col = self.df.columns[0]
        value_col = self.df.columns[1]

        value_str = self.df.loc[self.df[date_col] == date_index].iloc[0][value_col]

        return atof(value_str)