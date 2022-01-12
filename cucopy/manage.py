import argparse
import os
import urllib.request
import pathlib

DATASET_PATH = os.path.join(os.path.join(pathlib.Path(__file__).parent.resolve(), 'data'))

VPI_ALL = "A00000"
VPI_FOOD = "C2C011"
VPI_CONSUMER_GOOD_NO_ENERGY = "GOODS0MFXE"
VPI_ENERGY = "NRGY00"
VPI_SERVICE_NO_RENT = "VXR"
VPI_RENT = "C2C041"

_timeseries = {
                "all" : VPI_ALL, 
                "food" : VPI_FOOD, 
                "consumer_goods_no_energy" : VPI_CONSUMER_GOOD_NO_ENERGY, 
                "energy" : VPI_ENERGY, 
                "service_no_rent" : VPI_SERVICE_NO_RENT, 
                "rent" : VPI_RENT
                }

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
    file_name = f'BBDP1.M.DE.N.VPI.C.{timeseries_classification}.I15.A'
    download_link = f'https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId={file_name}&mode=its&its_csvFormat={language}&its_currency=default&its_dateFormat=default&its_from=&its_to='
    download_path = os.path.join(os.path.join(DATASET_PATH, language), file_name+'.csv')
        
    urllib.request.urlretrieve(download_link, download_path)

def main():
    args = parser.parse_args()

    if(args.classification.lower() not in _timeseries.keys()):
        raise ValueError("There is no classification by the name " + args.classification)

    ts_classification = _timeseries[args.classification.lower()]

    download_data(ts_classification, args.language)

main()
