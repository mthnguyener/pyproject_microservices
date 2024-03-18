#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from pkg_resources import get_distribution, DistributionNotFound
import sys

from api_gateway.pkg_globals import PACKAGE_ROOT

__version__ = '0.1.0'

try:
    _dist = get_distribution('api_gateway')
    dist_loc = path.normcase(_dist.location)
    here = path.normcase(__file__)
    if not here.startswith(path.join(dist_loc, 'api_gateway')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

sys.path.append(str(PACKAGE_ROOT / 'api_gateway/utils'))
