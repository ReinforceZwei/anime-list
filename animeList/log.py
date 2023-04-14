import logging

logger = logging.getLogger(name="app")
handler = logging.StreamHandler()
format = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')

handler.setFormatter(format)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)