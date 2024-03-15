#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Helper Function Module

"""
import datetime
import os

import asyncio
from fastapi import FastAPI
from loguru import logger

from variables import PACKAGE_ROOT

NOW = datetime.datetime.now()
DATE_TIME = NOW.strftime("%Y-%m-%d")


class CustomLogger:
    """
    Initialize a custom logger with the provided service name and log level.

    Parameters:
        service_name: The name of the service.
        log_level: The log level to set (default is 'INFO').
            Can be one of 'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'.
    """

    def __init__(self, service_name, log_level='INFO'):
        self.service_name = service_name
        self.log_level = log_level
        self.log_dir = f"{PACKAGE_ROOT}/logs/apps"

        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Configure the logger
        logger.remove()  # Remove the default logger
        logger.add(f"{self.log_dir}/{DATE_TIME}.log", level=self.log_level)

    async def log(self, level, message):
        """
        A function that logs a message at a specified level.

        Parameters:
            level: The logging level (e.g., 'INFO', 'ERROR').
            message: The message to be logged.
        """
        log_message = f"[{self.service_name}] - {message}"
        await asyncio.to_thread(getattr(logger, level.lower()), log_message)


# Define the launch_app function
def launch_app(service_name: str) -> FastAPI:
    """
    Creates and returns a FastAPI application with the specified service name.

    Parameters:
        service_name: The name of the service.

    Returns:
        FastAPI App.
    """
    try:
        custom_logger = CustomLogger(service_name=service_name)

        app = FastAPI(title=service_name,
                      description=f"{service_name} API",
                      docs_url=f"/{service_name}/docs",
                      redoc_url=f"/{service_name}/redoc",
                      openapi_url=f"/{service_name}/openapi.json")

        # TODO: Add health checking
        # TODO: Add Middleware

        logger.info(f"Successfully started {service_name}.\n"
                    f"{app.openapi()}\n"
                    f"{app.docs_url} | {app.redoc_url}")
        return app, custom_logger
    except Exception as e:
        logger.error(f"Failed to start {service_name}: {e}")


if __name__ == "__main__":
    pass
