#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving Handler

"""
import httpx

from utils.helpers import CustomLogger
from utils.variables import URL_APIGATEWAY

custom_logger = CustomLogger(service_name='MODELSERVING')


async def process_action(action: dict):
    action["action"] = "example2"
    output = action
    try:
        async with httpx.AsyncClient() as client:
            url = f"{URL_APIGATEWAY}/model-results"
            response = await client.post(url, json=output)
            if response.status_code == 200:
                response_json = response.json()
                custom_logger.log("INFO",
                                  f"Successfully processed action: "
                                  f"{response_json}")
            else:
                response_json = "Failed to send response back to API Gateway"
    except httpx.HTTPError as e:
        response_json = f"HTTP Error: {e}"
        custom_logger.log("ERROR", response_json)
    return {"message": f"Model Response: {response_json}"}


if __name__ == "__main__":
    pass
