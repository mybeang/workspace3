import colorlog
import logging

chdr = colorlog.StreamHandler()
fhdr = logging.FileHandler("test_log.log")
logger = colorlog.getLogger()
logging_fmt = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)-15s %(levelname)-7s {%(module)s:%(lineno)d} %(message)s'
)
f_l_fmt = logging.Formatter('%(asctime)-15s %(levelname)-7s {%(module)s:%(lineno)d} %(message)s')

logger.setLevel(logging.DEBUG)
chdr.setFormatter(logging_fmt)
fhdr.setFormatter(f_l_fmt)
logger.addHandler(chdr)
logger.addHandler(fhdr)


logging.critical("Hello this is critical log")
logging.error("Hello this is error log")
logging.warning("Hello this is warning log")
logging.info("Hello this is info log")
logging.debug("Hello this is debug log")
