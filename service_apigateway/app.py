#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" API Gateway App Module

"""
import os
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn

from utils.variables import HTTP_TIMEOUT,PORT_APIGATEWAY, PORT_MODELSERVING, \
    PROJECT_NAME, USERNAME

app = FastAPI()
model_output = None


# Sample endpoint in the model serving service
@app.get("/test")
async def test():
    output = {"API WORKING": "Sample output from api gateway"}
    return output


# New endpoint to trigger an action in the modelserving container
@app.post('/trigger-action')
async def trigger_action(action: dict):
    try:
        # Perform whatever action you need to trigger here
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.post(f"http://{PROJECT_NAME}-modelserving:"
                                         f"{PORT_MODELSERVING}/model-action",
                                         json=action)

        if response.status_code == 200:
            response_json = response.json()
            return {"message": f"API Response: {response_json}"}
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=response.text)

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-results")
async def get_model_results():
    if model_output is None:
        raise HTTPException(status_code=404,
                            detail="Model output not available")
    return {"Model Output": model_output}


@app.post("/model-results")
async def update_model_results(result: dict):
    global model_output
    try:
        # Process the model results (e.g., store in a database, update UI, etc.)
        # For now, just store the result
        model_output = result
        return {"message": f"Model Output: {model_output}"}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT_APIGATEWAY)
