#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving Handler

"""
import httpx

from model_serving.utils.helpers import CustomLogger
from model_serving.utils.variables import URL_APIGATEWAY

custom_logger = CustomLogger(service_name='model_serving')


async def process_action(action: dict) -> dict:
    """
    Process the given action by sending it to the API gateway and
        returning the response message.

    Parameters:
        action (dict): The action to be processed.

    Returns:
        dict: A dictionary containing the message from the model response.
    """
    action["action"] = "example2"
    output = action
    try:
        async with httpx.AsyncClient() as client:
            url = f"{URL_APIGATEWAY}/model-results"
            response = await client.post(url, json=output)
            if response.status_code == 200:
                response_json = response.json()
                await custom_logger.log(
                    "INFO", f"Successfully processed data:\n"
                    f"{response.headers}\n"
                    f"{response.text}")
            else:
                response_json = "Failed to send response back to API Gateway"
    except httpx.HTTPError as e:
        response_json = f"HTTP Error: {e}"
        await custom_logger.log("ERROR", response_json)
    return {"message": f"Model Response: {response_json}"}


if __name__ == "__main__":
    pass
