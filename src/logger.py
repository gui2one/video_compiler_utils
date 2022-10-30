import logging
FORMAT = '[ %(levelname)-s ] -> %(filename)s:%(lineno)s -- %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)