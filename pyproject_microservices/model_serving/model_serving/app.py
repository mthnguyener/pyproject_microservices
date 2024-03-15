#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving App Module

"""
from fastapi import HTTPException
import uvicorn

from model_serving.handler import process_action
from model_serving.utils.helpers import launch_app
from model_serving.utils.variables import PORT_MODELSERVING

service_name = 'model_serving'
model_serving_app, custom_logger = launch_app(service_name=service_name)


@model_serving_app.get("/test")
async def test():
    """
    A simple test function for the model serving app.
    """
    pred = {"MODEL WORKING": "Sample prediction from model serving service"}
    return pred


# New endpoint to handle the triggered action
@model_serving_app.post("/model-action")
async def handle_action(action: dict) -> dict:
    """
    Handle the incoming action by processing it and returning the response.

    Parameters:
        action: The action to be processed.

    Returns:
        The response from processing the action.
    """
    if action is not None:
        try:
            response = await process_action(action)
            return response
        except Exception as e:
            await custom_logger.log("ERROR", e)
            raise HTTPException(status_code=500,
                                detail=f"An error occurred: {e}")
    else:
        await custom_logger.log("ERROR", f"Unknown action: {action}")
        raise HTTPException(status_code=400,
                            detail=f"Unknown action: {action}")


if __name__ == "__main__":
    uvicorn.run(model_serving_app,
                host="0.0.0.0",
                port=PORT_MODELSERVING,
                reload=True)
