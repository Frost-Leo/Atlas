#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fixtures

This module provides test fixtures for InternalBaseModel testing

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import pytest
from typing import Optional
from pydantic import ConfigDict, Field, field_validator, model_validator

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
            decimal (float): Decimal field
            flag (bool): Flag field
        """

        text: str = Field(description="String field")
        number: int = Field(description="Integer field")
        decimal: float = Field(description="Decimal field")
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


@pytest.fixture
def default_validation_test_model():
    """
    Provide a test model for testing validate_default configuration
    """

    class DefaultValidationTestModel(InternalBaseModel):
        """
        Test model with default values that require validation

        Attributes:
            text (str): String field with validated default
            number (int): Integer field with range validation and default
            computed (str): Field with default factory
        """

        text: str = Field(
            default="   default text   ",  # This should be stripped
            description="String field with whitespace in default"
        )
        number: int = Field(
            default=50,
            ge=0,
            le=100,
            description="Integer field with validated default"
        )
        computed: str = Field(
            default_factory=lambda: "   computed   ",  # This should also be stripped
            description="Field with default factory"
        )

    return DefaultValidationTestModel


@pytest.fixture
def return_validation_test_model():
    """
    Provide a test model for testing validate_return configuration
    """

    class ReturnValidationTestModel(InternalBaseModel):
        """
        Test model with validators that return values requiring validation

        Attributes:
            text (str): String field with validator that returns value with whitespace
            number (int): Integer field with validator that ensures range
            transformed (str): Field with validator that transforms the value
        """

        text: str = Field(description="String field with return validation")
        number: int = Field(description="Integer field with range validation")
        transformed: str = Field(description="Field that gets transformed")

        @field_validator('text')
        @classmethod
        def add_whitespace(cls, v):
            """Validator that adds whitespace - will NOT be stripped by validate_return"""
            return f"   {v}   "

        @field_validator('number')
        @classmethod
        def ensure_range(cls, v):
            """Validator that ensures number is in range"""
            if v < 0:
                return 0  # Clamp to minimum
            elif v > 100:
                return 100  # Clamp to maximum
            return v

        @field_validator('transformed')
        @classmethod
        def transform_value(cls, v):
            """Validator that transforms the value"""
            return f"TRANSFORMED_{v.upper()}"

    return ReturnValidationTestModel


@pytest.fixture
def revalidate_instances_test_model():
    """
    Provide a test model for testing revalidate_instances configuration
    """

    class RevalidateInstancesTestModel(InternalBaseModel):
        """
        Test model for revalidate_instances testing

        Attributes:
            value (str): String field with validation
            count (int): Integer field with range validation
        """

        value: str = Field(min_length=3, max_length=10, description="Validated string")
        count: int = Field(ge=0, le=100, description="Count with range")

    return RevalidateInstancesTestModel


@pytest.fixture
def enum_test_model():
    """
    Provide a test model for testing use_enum_values configuration
    """
    from enum import Enum
    from typing import Optional
    from pydantic import ConfigDict, Field
    from atlas.models.base import InternalBaseModel

    class Color(str, Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    class Status(int, Enum):
        PENDING = 0
        ACTIVE = 1
        COMPLETED = 2

    # Create a custom config that allows enum value conversion
    # by temporarily disabling strict mode for this specific test
    enum_config = dict(InternalBaseModel.model_config)
    enum_config['strict'] = False  # Allow automatic conversion of values to enums

    class EnumTestModel(InternalBaseModel):
        """
        Test model with enum fields

        Attributes:
            color (Color): Color enum field
            status (Status): Status enum field
            optional_color (Optional[Color]): Optional color enum
        """
        model_config = ConfigDict(**enum_config)

        color: Color = Field(description="Color enum")
        status: Status = Field(description="Status enum")
        optional_color: Optional[Color] = Field(default=None, description="Optional color")

    return EnumTestModel, Color, Status


@pytest.fixture
def arbitrary_types_test_model():
    """
    Provide a test model for testing arbitrary_types_allowed configuration
    """

    class CustomType:
        """Custom type that's not a standard Pydantic type"""

        def __init__(self, value: str):
            self.value = value

        def __eq__(self, other):
            return isinstance(other, CustomType) and self.value == other.value

    class ArbitraryTypesTestModel(InternalBaseModel):
        """
        Test model with arbitrary types

        Attributes:
            custom (CustomType): Custom type field
            standard (str): Standard string field
        """

        custom: CustomType = Field(description="Custom type field")
        standard: str = Field(description="Standard field")

    return ArbitraryTypesTestModel, CustomType


@pytest.fixture
def numeric_test_model():
    """
    Provide a test model for testing allow_inf_nan configuration
    """

    class NumericTestModel(InternalBaseModel):
        """
        Test model with numeric fields

        Attributes:
            value (float): Float field
            optional_value (Optional[float]): Optional float field
        """

        value: float = Field(description="Float value")
        optional_value: Optional[float] = Field(default=None, description="Optional float")

    return NumericTestModel


@pytest.fixture
def coerce_numbers_test_model():
    """
    Provide a test model for testing coerce_numbers_to_str configuration
    """

    class CoerceNumbersTestModel(InternalBaseModel):
        """
        Test model for number to string coercion testing

        Attributes:
            text (str): String field
            code (str): String field that might receive numbers
        """

        text: str = Field(description="Text field")
        code: str = Field(description="Code field")

    return CoerceNumbersTestModel


@pytest.fixture
def from_attributes_test_model():
    """
    Provide a test model for testing from_attributes configuration
    """

    class SourceObject:
        """Source object with attributes"""

        def __init__(self, name: str, age: int, active: bool = True):
            self.name = name
            self.age = age
            self.active = active

    class FromAttributesTestModel(InternalBaseModel):
        """
        Test model for from_attributes testing

        Attributes:
            name (str): Name field
            age (int): Age field
            active (bool): Active status
        """

        name: str = Field(description="Name")
        age: int = Field(description="Age")
        active: bool = Field(default=True, description="Active status")

    return FromAttributesTestModel, SourceObject


@pytest.fixture
def alias_test_model():
    """
    Provide a test model for testing alias_generator and related configurations
    """

    class AliasTestModel(InternalBaseModel):
        """
        Test model with camelCase field names for alias testing

        Attributes:
            firstName (str): First name field
            lastName (str): Last name field
            emailAddress (str): Email address field
        """

        firstName: str = Field(description="First name")
        lastName: str = Field(description="Last name")
        emailAddress: str = Field(description="Email address")

    return AliasTestModel


@pytest.fixture
def bytes_test_model():
    """
    Provide a test model for testing ser_json_bytes and val_json_bytes configuration
    """

    class BytesTestModel(InternalBaseModel):
        """
        Test model with bytes fields

        Attributes:
            data (bytes): Binary data field
            optional_data (Optional[bytes]): Optional binary data
        """

        data: bytes = Field(description="Binary data")
        optional_data: Optional[bytes] = Field(default=None, description="Optional binary data")

    return BytesTestModel


@pytest.fixture
def regex_test_model():
    """
    Provide a test model for testing regex_engine configuration
    """

    class RegexTestModel(InternalBaseModel):
        """
        Test model with regex-validated fields

        Attributes:
            email (str): Email field with regex validation
            phone (str): Phone field with regex validation
        """

        email: str = Field(
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            description="Email with regex validation"
        )
        phone: str = Field(
            pattern=r'^\+?1?\d{9,15}$',
            description="Phone with regex validation"
        )

    return RegexTestModel


@pytest.fixture
def complex_validation_test_model():
    """
    Provide a complex test model for testing multiple configurations together
    """

    class ComplexValidationTestModel(InternalBaseModel):
        """
        Complex test model with multiple validation rules

        Attributes:
            name (str): Name with multiple constraints
            age (int): Age with range validation
            tags (list[str]): List of tags
        """

        name: str = Field(
            min_length=2,
            max_length=50,
            pattern=r'^[a-zA-Z\s]+$',
            description="Name with constraints"
        )
        age: int = Field(
            ge=0,
            le=150,
            description="Age with range"
        )
        tags: list[str] = Field(
            default_factory=list,
            description="List of tags"
        )

        @field_validator('tags')
        @classmethod
        def validate_tags(cls, v):
            """Ensure all tags are lowercase"""
            return [tag.lower().strip() for tag in v]

        @model_validator(mode='after')
        def validate_model(self):
            """Cross-field validation"""
            if self.age < 18 and 'adult' in self.tags:
                raise ValueError("Cannot have 'adult' tag for minors")
            return self

    return ComplexValidationTestModel


__all__ = [
    "string_test_model", "strict_test_model", "validate_assignment_test_model",
    "default_validation_test_model", "return_validation_test_model",
    "revalidate_instances_test_model", "enum_test_model", "arbitrary_types_test_model",
    "numeric_test_model", "coerce_numbers_test_model", "from_attributes_test_model",
    "alias_test_model", "bytes_test_model", "regex_test_model",
    "complex_validation_test_model"
]