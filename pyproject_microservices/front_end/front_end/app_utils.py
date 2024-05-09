#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" App Utils Module

"""


def html_download_link(filename: str, b64_encoded_data: str, type: str) -> str:
    """ Download Link

    Parameters:
      filename (str): The name of the file to be downloaded
      b64_encoded_data (str): The base64 encoded data to be downloaded
      type (str): The type of file to be downloaded
    Returns:
      A string containing the HTML code for the download link
    """

    if type == "csv":
        link = f"""
        <a href="data:text/csv;base64,{b64_encoded_data}"
        download="{filename}_data.csv" style="font-size: 15px;
        padding: 10px 20px; background-color: #9C54B3;
        color: white; border: none; border-radius: 5px;">
        <b>Download Dataset</b></a>
        """
    else:
        link = f"""
        <a href="data:application/vnd.openxmlformats-officedocument.
        wordprocessingml.document;base64,{b64_encoded_data}"
        download="{filename}.docx" style="font-size: 15px;
        padding: 10px 20px; background-color: #9C54B3;
        color: white; border: none; border-radius: 5px;">
        <b>Download Scenario</b></a>
        """

    return link