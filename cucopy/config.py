import os, pathlib

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