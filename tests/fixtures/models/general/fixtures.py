#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fixtures

This module provides 

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12 
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import pytest
from pydantic import Field

from atlas.models.base import InternalBaseModel


@pytest.fixture
def string_test_model():
    """
    Provide a test model specifically for testing string handling.

    Returns:
        Type[InternalBaseModel]
    """

    class StringTestModel(InternalBaseModel):
        """
        Provide a test model specifically for testing string handling.

        Attributes:
            text (str): string representation of the test model
        """

        text: str = Field(description="string type field for testing")

    return StringTestModel