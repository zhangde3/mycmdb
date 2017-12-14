import logging
from logging.config import fileConfig

fileConfig('logger_config.ini')
logger=logging.getLogger('infoLogger')

class ExtVC():

    def ext(self):
        logger.info("start extract vc")

    def to_json(self):
        logger.info("start dump to json")

    def ext_dump(self):
        self.ext()
        self.to_json()


