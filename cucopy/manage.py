import argparse
import os
import urllib.request
import pathlib

from .config import DATASET_PATH, _timeseries

parser = argparse.ArgumentParser()

parser.add_argument('-c',
                    '--classification',
                    metavar='string',
                    type=str,
                    required=True,
                    help='consumer price index id; allowed ids: '+''.join(id+', ' for id in list(_timeseries.keys())))
parser.add_argument('-l',
                    '--language',
                    default='de',
                    metavar='string',
                    type=str,
                    help='language for table format')

def download_data(timeseries_classification, language='de'):
    """
        Function for downloading a timeseries containing the most recent cpi data from the Deutsche Bundesbank in either german ('de') or english ('en') formatting.

        :param timeseries_classification: the timeseries' statistics classification id.
        :type timeseries_classification: string

        :param language: the language the timeseries should be formatted in.
        :type language: string
        """
    file_name = f'BBDP1.M.DE.N.VPI.C.{timeseries_classification}.I15.A'
    download_link = f'https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId={file_name}&mode=its&its_csvFormat={language}&its_currency=default&its_dateFormat=default&its_from=&its_to='
    download_path = os.path.join(os.path.join(DATASET_PATH, language), file_name+'.csv')
        
    pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)

    urllib.request.urlretrieve(download_link, download_path)

def main():
    args = parser.parse_args()

    if(args.classification.lower() not in _timeseries.keys()):
        raise ValueError("There is no classification by the name " + args.classification)

    ts_classification = _timeseries[args.classification.lower()]

    download_data(ts_classification, args.language)

if __name__ == "__main__":
    main()
