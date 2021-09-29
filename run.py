from cucopy import tools
from cucopy.components import settings, exchange

from cucopy import tools
from cucopy.components import settings, exchange

# VALID: 1,2
# INVALID: 3-7

import datetime

configs = [
    ["USA", "CAN", settings.WORLD_ER, 1, "1997-09-23", 10],
    ["USA", "CAN", settings.WORLD_ER, 1, None, 10],
    ["ABC", "CAN", settings.WORLD_ER, 1, "2010-09-23", 10],
    ["USA", "ABC", settings.WORLD_ER, 1, "2010-09-23", 10],
    ["USA", "CAN", settings.WORLD_ER, 1, "2010-13-32", 10],
    ["USA", "CAN", settings.WORLD_ER, 1, "2032-09-12", 10],
    ["USA", "CAN", settings.WORLD_ER, -1, "2010-09-23", 10]
]

#from_country_code, to_country_code, filename_, value=1, date=None

def test_working_param():
    conf = configs[0]
    print(exchange.get_exchanged_value(
            from_country_code=conf[0], 
            to_country_code=conf[1], 
            filename_=conf[2],
            value=conf[3],
            date=datetime.datetime.strptime(conf[4], '%Y-%m-%d').date()))

test_working_param()
