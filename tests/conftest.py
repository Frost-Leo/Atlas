#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conftest

This module provides 

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12 
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))
