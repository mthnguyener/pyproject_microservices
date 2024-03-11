#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving Handler

"""
import httpx

from utils.variables import PORT_APIGATEWAY, PORT_MODELSERVING, PROJECT_NAME, \
    URL_APIGATEWAY, USERNAME


async def process_action(action: dict):
    action["action"] = "example2"
    output = action
    try:
        async with httpx.AsyncClient() as client:
            url = f"{URL_APIGATEWAY}/model-results"
            response = await client.post(url, json=output)
            if response.status_code == 200:
                response_json = response.json()
            else:
                response_json = "Failed to send response back to API Gateway"
    except httpx.HTTPError as e:
        response_json = f"HTTP Error: {e}"
    return {"message": f"Model Response: {response_json}"}


if __name__ == "__main__":
    pass
