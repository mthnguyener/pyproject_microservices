#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Style Variables

"""
# 4285F4, 4f88b1
button_style = """
<style>
div.stButton > button:first-child {
    background-color: #72A0C1;
    color:#FFFFFF;
}
div.stButton > button:hover {
    background-color: #4f88b1;
    color:#FFFFFF;
}
</style>"""

clicked_button_style = """
<style>
div.stButton > button:first-child {
    background-color: #1c313f;
    color: #FFFFFF;
}
</style>
"""

divider_style = """
<hr style="
height:5px;
border:none;
color:#8d95b7;
background-color:#8d95b7;
" />
"""

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''

hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""

# href_style = """<style>.css-znku1x a {color: #9d03fc;}</style>"""

sidebar_email_style = """
<style>
    .spacer {
        margin-bottom: 25px;
        }
    .centered-h3 {
      text-align: center;
      font-size: 1.15rem;
    }
</style>
<div class="spacer"></div>
<h3 class="centered-h3">
    EMAIL
    <a href="mailto:"></a>
</h3>
"""

spinner_style = """<style>.stSpinner > div > div 
{border-top-color: #72A0C1;}</style>"""

top_padding = """<style>div.block-container{padding-top: 0rem;}</style>"""
