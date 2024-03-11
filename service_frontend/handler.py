#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Frontend Handler

"""
import httpx
import streamlit as st

from utils.variables import PORT_APIGATEWAY, PORT_MODELSERVING, PROJECT_NAME, \
    URL_APIGATEWAY, USERNAME


def fetch_model_results():
    try:
        url = f"{URL_APIGATEWAY}/model-results"
        response = httpx.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            result = response.json()
            st.write("Model Results:", result)
        else:
            st.error(f"Failed to fetch model results. Status code: "
                     f"{response.status_code}")
            st.error(response.text)
    except httpx.TimeoutException as e:
        st.error(f"Timeout error: {e}")
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"Error fetching model results: {str(e)}")


def trigger_action(action: str = "example"):
    try:
        url = f"{URL_APIGATEWAY}/trigger-action"

        retries = 3
        for attempt in range(retries):
            try:
                response = httpx.post(url, json={"action": action}, timeout=30)
                response.raise_for_status()
                if response.status_code == 200:
                    response_json = response.json()
                    st.sidebar.write("Action triggered successfully!")
                    st.sidebar.write("Frontend Response:", response_json)
                    return {"message": response_json["message"]}
                else:
                    st.sidebar.write("Failed to trigger action. Status Code:",
                             response.status_code)
                    st.sidebar.write("Error:", response.json()["detail"])
                    return {"error": "Failed to trigger action",
                            "detail": response.json()["detail"]}
            except httpx.TimeoutException as e:
                st.sidebar.error(f"Timeout error: {e}")
                if attempt < retries - 1:
                    st.sidebar.info(f"Retrying... Attempt {attempt + 1}/{retries}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    st.sidebar.error("Maximum retries exceeded. "
                             "Please try again later.")
                    return {"error": "Maximum retries exceeded",
                            "detail": str(e)}
            except httpx.HTTPStatusError as e:
                st.sidebar.error(f"HTTP error: {e}")
                return {"error": "HTTP error", "detail": str(e)}
            except Exception as e:
                st.sidebar.error(f"An unexpected error occurred: {e}")
                return {"error": "Unexpected error", "detail": str(e)}

    except Exception as e:
        st.sidebar.error(f"Frontend Exception: {e}")
        return {"error": f"Error: {str(e)}"}


if __name__ == "__main__":
    pass
