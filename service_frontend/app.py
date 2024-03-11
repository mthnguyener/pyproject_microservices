#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Frontend App Module

"""
import os

import streamlit as st

from handler import fetch_model_results, trigger_action
from subpages.page_1 \
    import page_1
from subpages.page_2 \
    import page_2


def home_page():
    st.subheader("Welcome to the Home Page")
    st.write("This is the home page of the app.")


def main():
    st.title("My Streamlit App")

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
        trigger_action()
        fetch_model_results()


if __name__ == "__main__":
    main()
