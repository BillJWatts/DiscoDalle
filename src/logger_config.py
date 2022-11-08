"""Module containing logging configuration details"""
import logging

FILENAME = "bot.log"
FORMAT = "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
LEVEL = logging.DEBUG


def set_logging_config():
    """Sets up basic loggin configuration"""
    logging.basicConfig(
        filename=FILENAME,
        filemode="w",
        encoding="utf-8",
        format=FORMAT,
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.DEBUG,
    )
