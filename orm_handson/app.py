import logging
import sys

from orm_handson.database import session, Base, engine
from orm_handson.model import Result

"""
logging_fmt = '%(asctime)-15s %(levelname)-7s %(message)s'
log_level = logging.DEBUG
logger = logging.getLogger()
logger.setLevel(log_level)
formatter = logging.Formatter(logging_fmt)
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setFormatter(formatter)
logger.addHandler(stdoutHandler)
"""

Base.metadata.create_all(bind=engine)
#my_res = session.query(Result).filter_by(model='V2708M').all()[-1]
#print("my_res: {}".format(my_res))
res = Result(
    num=1, vender='다산', model='V2708M', serialnumber='whatthe', barcode='whatttte', date='2019-07-17',
    memory='PASS', cpu='PASS', traffic='-', port='-', final='개별', nos='-', config='PASS'
)
session.add(res)

session.commit()
my_res = session.query(Result).filter_by(num=2).first()
print(">>>>>>>>>>>> my_res {}".format(my_res))

session.add_all(
    [
        Result(num=2, vender='다산', model='V2708M', serialnumber='whatthe1', barcode='whatttte1', date='2019-07-17',
               memory='PASS', cpu='PASS', traffic='-', port='-', final='개별', nos='-', config='PASS'),
        Result(num=3, vender='다산', model='V2708M', serialnumber='whatthe2', barcode='whatttte2', date='2019-07-17',
               memory='PASS', cpu='PASS', traffic='PASS', port='PASS', final='PASS', nos='-', config='-')
    ]
)
session.commit()


result_list = session.query(Result).filter(Result.vender.in_(['다산'])).all()
print(">>>>>>>>>>>> result_list: {}".format(result_list))

my_res = session.query(Result).filter_by(model='V2708M').all()[-1]
print(">>>>>>>>>>>> my_res num: {}".format(my_res.num))

for result in result_list:
    session.delete(result)
session.commit()

result_list = session.query(Result).filter(Result.vender.in_(['다산'])).all()
print(">>>>>>>>>>>> result_list: {}".format(result_list))

import pdb
pdb.set_trace()