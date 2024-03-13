#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving App Module

"""
from fastapi import HTTPException
import uvicorn

from handler import process_action
from utils.helpers import CustomLogger, make_app
from utils.variables import PORT_MODELSERVING

model_serving_app = make_app()
custom_logger = CustomLogger(service_name='MODELSERVING')


@model_serving_app.get("/test")
async def test():
    prediction = {"MODEL WORKING": "Sample prediction from model serving service"}
    return prediction


# New endpoint to handle the triggered action
@model_serving_app.post("/model-action")
async def handle_action(action: dict):
    if action is not None:
        try:
            response = await process_action(action)
            custom_logger.log("INFO",
                              "Model Server successfully processed action")
            return response
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"An error occurred: {e}")
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")


if __name__ == "__main__":
    uvicorn.run(model_serving_app, host="0.0.0.0", port=PORT_MODELSERVING)
