#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conftest

This module provides pytest configuration and fixture imports

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12 
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

# Import all fixtures to make them available to pytest
from tests.fixtures.core._infra.device_info.fixtures import *
