#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Page 1 Module

"""
import streamlit as st


def page_1():
    """
    Function to display content for Model 1 and handle user input for prompt.
    """
    st.subheader("Model 1")
    st.write("This is content for Model 1.")

    prompt = st.text_input('Prompt', '')

    if prompt:
        st.write(f"Sending data to model\n"
                 f"data: {prompt}")
        st.write('Bot: Interesting...but this is just a template. '
                 'I have no idea what to say.')
