#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Front-End Handler

"""
import asyncio
import httpx
import streamlit as st

from front_end.utils.helpers import CustomLogger
from front_end.utils.variables import URL_APIGATEWAY

custom_logger = CustomLogger(service_name='front_end')


async def fetch_model_results():
    """
    A function to fetch model results from a specified URL and displays them.
    """
    try:
        url = f"{URL_APIGATEWAY}/model-results"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                result = response.json()
                await custom_logger.log(
                    "INFO", f"Successfully fetched results:\n"
                    f"{response.headers}\n"
                    f"{response.text}")
                st.write("Model Results:", result)
            else:
                await custom_logger.log(
                    "ERROR", f"Status code: "
                    f"{response.status_code}\n"
                    f"Response: {response.text}")
                st.error(f"Failed to fetch model results. Status code: "
                         f"{response.status_code}")
                st.error(response.text)
    except httpx.TimeoutException as e:
        await custom_logger.log("ERROR", f"Timeout error: {e}")
        st.error(f"Timeout error: {e}")
    except httpx.HTTPStatusError as e:
        await custom_logger.log("ERROR", f"HTTP error: {e}")
        st.error(f"HTTP error: {e}")
    except Exception as e:
        await custom_logger.log("ERROR",
                                f"Error fetching model results: {str(e)}")
        st.error(f"Error fetching model results: {str(e)}")


async def trigger_action(action: str = "example") -> dict:
    """
    Triggers a specific action via an API call and retries the API call up to 3
     times in case of timeouts or errors.

    Parameters:
        action: The action to be triggered (default is "example").
    Returns:
        A dictionary with either a success message or an error message.
    """
    try:
        retries = 3
        for attempt in range(retries):
            try:
                url = f"{URL_APIGATEWAY}/trigger-action"
                async with httpx.AsyncClient() as client:
                    response = await client.post(url,
                                                 json={"action": action},
                                                 timeout=30)
                response.raise_for_status()
                if response.status_code == 200:
                    response_json = response.json()
                    await custom_logger.log(
                        "INFO", f"Successfully triggered action: "
                        f"{action}\n"
                        f"{response.headers}\n"
                        f"{response.text}")
                    st.sidebar.write("Action triggered successfully!")
                    st.sidebar.write("Frontend Response:", response_json)
                    return {"message": response_json["message"]}
                else:
                    st.sidebar.write("Failed to trigger action. Status Code:",
                                     response.status_code)
                    st.sidebar.write("Error:", response.json()["detail"])
                    await custom_logger.log(
                        "ERROR", f"Failed to trigger action: "
                        f"{action}\n"
                        f"Detail: "
                        f"{response.json()['detail']}")
                    return {
                        "error": "Failed to trigger action",
                        "detail": response.json()["detail"]
                    }
            except httpx.TimeoutException as e:
                await custom_logger.log("ERROR", f"Timeout error: {e}")
                st.sidebar.error(f"Timeout error: {e}")
                if attempt < retries - 1:
                    st.sidebar.info(f"Retrying... Attempt "
                                    f"{attempt + 1}/{retries}")
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                else:
                    await custom_logger.log(
                        "ERROR", f"Maximum retries exceeded: "
                        f"{str(e)}")
                    st.sidebar.error("Maximum retries exceeded. "
                                     "Please try again later.")
                    return {
                        "error": "Maximum retries exceeded",
                        "detail": str(e)
                    }
            except httpx.HTTPStatusError as e:
                await custom_logger.log("ERROR", f"HTTP error: {e}")
                st.sidebar.error(f"HTTP error: {e}")
                return {"error": "HTTP error", "detail": str(e)}
            except Exception as e:
                await custom_logger.log("ERROR",
                                        f"An unexpected error occurred: {e}")
                st.sidebar.error(f"An unexpected error occurred: {e}")
                return {"error": "Unexpected error", "detail": str(e)}

    except Exception as e:
        await custom_logger.log("ERROR", f"Error: {str(e)}")
        st.sidebar.error(f"Frontend Exception: {e}")
        return {"error": f"Error: {str(e)}"}


if __name__ == "__main__":
    pass
