import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('app_logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

class InfoLogger:

    def __init__(self, message):
        self.message = message

    def info_log(self):
        logger.info(self.message)

class ErrorLogger:

    def __init__(self, message):
        self.message = message

    def error_log(self):
        logger.exception(self.message)