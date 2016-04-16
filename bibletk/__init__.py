#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import versioneer

__author__ = 'Chia-Jung, Yang'
__email__ = 'jeroyang@gmail.com'
__version__ = versioneer.get_version()

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
