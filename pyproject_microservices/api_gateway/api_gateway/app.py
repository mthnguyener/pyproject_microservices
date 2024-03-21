#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" API Gateway App Module

"""
from fastapi import HTTPException
import httpx
import uvicorn

from api_gateway.utils.helpers import launch_app
from api_gateway.utils.variables import HTTP_TIMEOUT, PORT_APIGATEWAY, \
    URL_MODELSERVING

service_name = 'api_gateway'
api_gateway_app, custom_logger = launch_app(service_name=service_name)

model_output = None


# Sample endpoint in the model serving service
@api_gateway_app.get("/test")
async def test():
    """
    A simple test function for the api gateway app.
    """
    output = {"API WORKING": "Sample output from api gateway"}

    return output


# New endpoint to trigger an action in the model serving container
@api_gateway_app.post('/trigger-action')
async def trigger_action(action: dict) -> dict:
    """
    Trigger a specific action by posting to the API Gateway endpoint.

    Parameters:
        action: Information for the action to be triggered

    Returns:
        A dictionary with a message indicating the API response
    """
    try:

        # Perform whatever action you need to trigger here
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:

            url = f"{URL_MODELSERVING}/model-action"

            response = await client.post(url, json=action)

        if response.status_code == 200:
            response_json = response.json()

            await custom_logger.log(
                "INFO", f"API Gateway posted to model server:\n"
                f"{response.headers}\n"
                f"{response.text}")

            return {"message": f"API Response: {response_json}"}

        else:

            raise HTTPException(status_code=response.status_code,
                                detail=response.text)

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP Error: {e}")

    except Exception as e:
        raise e


@api_gateway_app.get("/model-results")
async def get_model_results() -> dict:
    """
    A function to get model results from the API Gateway.

    Returns:
        A dictionary with the model output
    """
    global model_output

    if model_output is None:
        raise HTTPException(status_code=404,
                            detail="Model output not available")

    await custom_logger.log(
        "INFO", "Successfully retrieved model output from "
        "API Gateway")

    return {"Model Output": model_output}


@api_gateway_app.post("/model-results")
async def update_model_results(result: dict) -> dict:
    """
    Update the model results with the new result.

    Returns:
        A dictionary with the updated model output
    """
    global model_output

    try:

        # Process the model results (e.g., send database, update UI, etc.)
        # For now, just store the result
        model_output = result

        await custom_logger.log(
            "INFO", "API Gateway received output from "
            "model server")

        return {"message": f"Model Output: {model_output}"}

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(api_gateway_app,
                host="0.0.0.0",
                port=PORT_APIGATEWAY,
                reload=True)
