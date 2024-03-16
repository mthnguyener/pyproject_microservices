#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Global Variable Module

"""
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[1]

FONT_SIZE = {
    'axis': 18,
    'label': 14,
    'legend': 12,
    'super_title': 24,
    'title': 20,
}

FONT_FAMILY = 'Courier New, monospace'
PLOTLY_FONTS = {
    'axis_font': {
        'family': FONT_FAMILY,
        'size': FONT_SIZE['axis'],
        'color': 'gray',
    },
    'legend_font': {
        'family': FONT_FAMILY,
        'size': FONT_SIZE['label'],
        'color': 'black',
    },
    'title_font': {
        'family': FONT_FAMILY,
        'size': FONT_SIZE['super_title'],
        'color': 'black',
    },
}

TIME_FORMAT = '%Y_%m_%d_%H_%M_%S'

if __name__ == '__main__':
    pass
