#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Helper Function Module

"""
import datetime
import os

from fastapi import FastAPI
from loguru import logger

from utils.variables import PACKAGE_ROOT

NOW = datetime.datetime.now()
DATE_TIME = NOW.strftime("%Y-%m-%d_%H-%M")


class CustomLogger:
    def __init__(self, service_name, log_level='INFO'):
        self.service_name = service_name
        # log_level = 'INFO' | 'DEBUG' | 'WARNING' | 'ERROR' | 'CRITICAL'
        self.log_level = log_level
        self.log_dir = f"{PACKAGE_ROOT}/logs"

        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Configure the logger
        logger.remove()  # Remove the default logger
        logger.add(f"{self.log_dir}/{DATE_TIME}.log", level=self.log_level)

    def log(self, level, message):
        log_message = f"[{self.service_name}] - {message}"
        getattr(logger, level.lower())(log_message)


# Define the make_app function
def make_app() -> FastAPI:
    app = FastAPI()

    # TODO: Add health checking
    # TODO: Add Middleware

    return app


if __name__ == "__main__":
    pass
