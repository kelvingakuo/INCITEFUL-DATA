import logging


form = logging.Formatter("%(asctime)s : %(levelname)-5.5s : %(message)s")
logger = logging.getLogger()

fileHandler = logging.FileHandler('logs.log')
fileHandler.setFormatter(form)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(form)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)
