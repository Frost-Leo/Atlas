#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__init__.py

This module provides all the exports of atlas.

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/2
- Modified : 2025/9/2
- License  : GPL-3.0
"""

import os
from pathlib import Path


__version__ = "0.1.0"

# Environment variable acquisition
ATLAS_ROOT = os.getenv('ATLAS_ROOT', Path(__file__).resolve().parents[2])
