import logging
FORMAT = '[ %(levelname)-s ] -> %(message)s -- [ %(filename)s:%(lineno)s ]'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)