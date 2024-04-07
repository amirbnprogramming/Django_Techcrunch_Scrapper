import logging
from celery.signals import after_setup_logger

import logging
from celery.signals import after_setup_logger


def configure_celery_log(sender=None, **kwargs):
    # Get the Celery logger
    celery_logger = logging.getLogger('celery')

    # Remove existing handlers to prevent duplicates
    celery_logger.handlers = []

    # Set the desired log level (e.g., INFO, DEBUG, etc.)
    celery_logger.setLevel(logging.INFO)

    # Define the log format
    log_format = logging.Formatter('[%(asctime)s] : %(message)s')

    # Create a console handler and set its log level and format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # Add the console handler to the Celery logger
    celery_logger.addHandler(console_handler)


after_setup_logger.connect(configure_celery_log)
