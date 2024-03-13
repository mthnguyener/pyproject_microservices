#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Variables

"""
import os
from pathlib import Path

HTTP_TIMEOUT = 30
PACKAGE_ROOT = Path(__file__).parents[1]
PORT_APIGATEWAY = os.getenv("PORT_APIGATEWAY")
PORT_MODELSERVING = os.getenv("PORT_MODELSERVING")
PROJECT_NAME = os.getenv("PROJECT_NAME")
URL_APIGATEWAY = f"http://{PROJECT_NAME}-apigateway:{PORT_APIGATEWAY}"
USERNAME = os.getenv("USER_NAME")