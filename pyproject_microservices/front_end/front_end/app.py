#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Front-End App Module

"""
import asyncio
import streamlit as st

from front_end.handler import fetch_model_results, trigger_action
from front_end.subpages.page_1 import page_1
from front_end.subpages.page_2 import page_2
from front_end.utils.helpers import CustomLogger

custom_logger = CustomLogger(service_name='front_end')


def home_page():
    """
    A function to display the home page content with a subheader and a message.
    """
    st.subheader("Welcome to the Home Page")
    st.write("This is the home page of the app.")


async def main():
    """
    Main function to display the microservice front_end and handle navigation.
    """
    st.title("pyproject_microservices Front-End")

    # Navigation
    page = st.sidebar.selectbox("Menu", ["Home", "Model 1", "Model 2"])

    if page == "Home":
        home_page()

    elif page == "Model 1":
        page_1()

    elif page == "Model 2":
        page_2()

    # Button to trigger action
    if st.sidebar.button("Trigger Action"):
        await asyncio.create_task(trigger_action())

        await asyncio.create_task(fetch_model_results())


if __name__ == "__main__":
    asyncio.run(main())
