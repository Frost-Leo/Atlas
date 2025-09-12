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
from pydantic import ConfigDict, Field

from atlas.models.base import InternalBaseModel
from tests.fixtures.models.general.fixtures import string_test_model


@pytest.fixture
def strict_test_model():
    """
    Provide a test model for testing strict mode with various field types
    """

    class StrictTestModel(InternalBaseModel):
        """
        Test model with multiple field types for strict mode testing

        Attributes:
            text (str): String field
            number (int): Integer field
            decimal (int): Decimal field
            flag (bool): Flag field
        """

        text: str = Field(description="String field")
        number: int = Field(description="Integer field")
        decimal: float = Field(description="Float field")
        flag: bool = Field(description="Boolean field")

    return StrictTestModel


@pytest.fixture
def validate_assignment_test_model():
    """
    Provide a test model specifically for testing validate_assignment configuration.

    This model temporarily overrides frozen=False to allow testing of
    validate_assignment behavior.

    Returns:
        Type[InternalBaseModel]: A mutable model class for testing validate_assignment
    """

    # Create config outside the class to avoid Pydantic detection
    base_config = dict(InternalBaseModel.model_config)
    base_config['frozen'] = False

    class ValidateAssignmentTestModel(InternalBaseModel):
        """
        Test model with frozen=False to demonstrate validate_assignment functionality.

        Note: This is only for testing purposes. Production models should remain frozen.

        Attributes:
            text (str): String field with max length constraint
            number (int): Integer field with range constraint
        """

        model_config = ConfigDict(**base_config)

        text: str = Field(
            max_length=50,
            description="String field with max length validation"
        )
        number: int = Field(
            ge=0,
            le=100,
            description="Integer field with range validation (0-100)"
        )

    return ValidateAssignmentTestModel


__all__ = ["string_test_model", "strict_test_model", "validate_assignment_test_model"]