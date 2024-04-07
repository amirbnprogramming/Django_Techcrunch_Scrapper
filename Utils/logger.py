import logging


class CustomLogger():
    def __init__(self, name, level=logging.INFO, log_format='%(asctime)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(log_format)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.level = level

    def log(self, message):
        self.logger.log(self.level, message)


warning_log = CustomLogger(name='warning', level=logging.WARNING)
info_log = CustomLogger(name='info', level=logging.INFO)
star_log = CustomLogger(name='star', log_format='%(message)s')
