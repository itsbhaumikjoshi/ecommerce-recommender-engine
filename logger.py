import logging

class Logger():

    def __init__(
        self,
        name: str,
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    ):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(format)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)

        self.logger.addHandler(sh)

    def get_logger(self):
        return self.logger
