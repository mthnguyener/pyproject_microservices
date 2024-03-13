#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" API Gateway App Module

"""
from fastapi import HTTPException
import httpx
import uvicorn

from utils.helpers import CustomLogger, make_app
from utils.variables import HTTP_TIMEOUT, PORT_APIGATEWAY, PORT_MODELSERVING, \
    PROJECT_NAME

api_gateway_app = make_app()
custom_logger = CustomLogger(service_name='APIGATEWAY')
model_output = None


# Sample endpoint in the model serving service
@api_gateway_app.get("/test")
async def test():
    output = {"API WORKING": "Sample output from api gateway"}
    return output


# New endpoint to trigger an action in the modelserving container
@api_gateway_app.post('/trigger-action')
async def trigger_action(action: dict):
    try:
        # Perform whatever action you need to trigger here
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.post(f"http://{PROJECT_NAME}-modelserving:"
                                         f"{PORT_MODELSERVING}/model-action",
                                         json=action)
        if response.status_code == 200:
            response_json = response.json()
            custom_logger.log("INFO",
                              "API Gateway received action from frontend")
            return {"message": f"API Response: {response_json}"}
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=response.text)

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_gateway_app.get("/model-results")
async def get_model_results():
    if model_output is None:
        raise HTTPException(status_code=404,
                            detail="Model output not available")
    custom_logger.log("INFO",
                      "Successfully retrieved model output from API Gateway")
    return {"Model Output": model_output}


@api_gateway_app.post("/model-results")
async def update_model_results(result: dict):
    global model_output
    try:
        # Process the model results (e.g., store in a database, update UI, etc.)
        # For now, just store the result
        model_output = result
        custom_logger.log("INFO",
                          "API Gateway received output from model server")
        return {"message": f"Model Output: {model_output}"}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(api_gateway_app, host="0.0.0.0", port=PORT_APIGATEWAY)
