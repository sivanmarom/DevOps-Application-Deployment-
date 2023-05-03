import logging
import os
class BaseClass:
    def log_conf(self):
        logger = logging.getLogger(__name__)
        fileHandler = logging.FileHandler("logfile.log")
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(message)s : %(user)s:")
        formatter.user = os.environ['BUILD_USER']
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.setLevel(logging.DEBUG)
        return logger


