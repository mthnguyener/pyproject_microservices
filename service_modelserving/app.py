#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Model Serving App Module

"""
import os
from fastapi import FastAPI
import httpx
import uvicorn

from handler import process_action

app = FastAPI()


@app.get("/test")
async def test():
    prediction = {"MODEL WORKING": "Sample prediction from model serving service"}
    return prediction


# Function for processing actions posted to model-action.
# async def process_action(action: dict):
#     action["action"] = "example2"
#     output = action
#     try:
#         async with httpx.AsyncClient() as client:
#             url = f"{URL_APIGATEWAY}/model-results"
#             response = await client.post(url, json=output)
#             if response.status_code == 200:
#                 response_json = response.json()
#             else:
#                 response_json = "Failed to send response back to API Gateway"
#     except httpx.HTTPError as e:
#         response_json = f"HTTP Error: {e}"
#     return {"message": f"Model Response: {response_json}"}


# New endpoint to handle the triggered action
@app.post("/model-action")
async def handle_action(action: dict):
    if action is not None:
        try:
            response = await process_action(action)
            return response
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"An error occurred: {e}")
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT_MODELSERVING)
