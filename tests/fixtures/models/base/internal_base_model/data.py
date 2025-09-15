#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data

This module provides test data constants for InternalBaseModel tests

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import pytest
import base64


class TestData:
    """
    Test data constants for InternalBaseModel tests

    Attributes:
        TEST_STR_STRIP_WHITESPACE (List[Tuple[str, str]]): Test data for string whitespace stripping
        TEST_STR_MAX_LENGTH_VALID (List[pytest.param]): Test data for valid string length
        TEST_STR_MAX_LENGTH_INVALID (List[pytest.param]): Test data for invalid string length
        TEST_EXTRA_FORBID (List[pytest.param]): Test data for extra="forbid" configuration
        TEST_FROZEN_MODIFICATIONS (List[pytest.param]): Test data for frozen=True configuration
        TEST_STRICT_MODE_INVALID (List[pytest.param]): Test data for strict mode invalid inputs
        TEST_STRICT_MODE_VALID (List[pytest.param]): Test data for strict mode valid inputs
        TEST_VALIDATE_ASSIGNMENT_VALID (List[pytest.param]): Test data for valid assignments
        TEST_VALIDATE_ASSIGNMENT_INVALID (List[pytest.param]): Test data for invalid assignments
        TEST_VALIDATE_DEFAULT (List[pytest.param]): Test data for validate_default configuration
        TEST_VALIDATE_RETURN (List[pytest.param]): Test data for validate_return configuration
        TEST_REVALIDATE_INSTANCES (List[pytest.param]): Test data for revalidate_instances configuration
        TEST_USE_ENUM_VALUES (List[pytest.param]): Test data for use_enum_values configuration
        TEST_ARBITRARY_TYPES (List[pytest.param]): Test data for arbitrary_types_allowed configuration
        TEST_ALLOW_INF_NAN_INVALID (List[pytest.param]): Test data for allow_inf_nan=False configuration
        TEST_ALLOW_INF_NAN_VALID (List[pytest.param]): Test data for valid numeric values
        TEST_COERCE_NUMBERS_TO_STR (List[pytest.param]): Test data for coerce_numbers_to_str=False
        TEST_FROM_ATTRIBUTES (List[pytest.param]): Test data for from_attributes configuration
        TEST_ALIAS_GENERATOR (List[pytest.param]): Test data for alias_generator configuration
        TEST_VALIDATE_BY_ALIAS (List[pytest.param]): Test data for validate_by_alias configuration
        TEST_VALIDATE_BY_NAME (List[pytest.param]): Test data for validate_by_name=False configuration
        TEST_BYTES_SERIALIZATION (List[pytest.param]): Test data for bytes serialization
        TEST_REGEX_VALIDATION (List[pytest.param]): Test data for regex validation
        TEST_COMPLEX_VALIDATION (List[pytest.param]): Test data for complex validation scenarios
    """

    # Test data for str_strip_whitespace configuration based on string test model construction
    TEST_STR_STRIP_WHITESPACE = [
        ("    Tom   ", "Tom"),
        ("Tom", "Tom"),
        ("", ""),
        ("   Hello World", "Hello World"),
        ("\n\tJohn\r\n", "John"),
        ("  Multiple   Spaces  ", "Multiple   Spaces"),
    ]

    # Test data for str_max_length configuration for valid string length
    TEST_STR_MAX_LENGTH_VALID = [
        pytest.param("a" * 100000, 100000, id="max_length_100000"),
        pytest.param("a" * 99999, 99999, id="length_99999"),
        pytest.param("a" * 50000, 50000, id="length_50000"),
        pytest.param("", 0, id="empty_string"),
    ]

    # Test data for str_max_length configuration for invalid string length
    TEST_STR_MAX_LENGTH_INVALID = [
        pytest.param("a" * 100001, 100001, id="over_limit_1"),
        pytest.param("a" * 150000, 150000, id="over_limit_50000"),
    ]

    # Test data for extra="forbid" configuration
    TEST_EXTRA_FORBID = [
        pytest.param(
            {"text": "Hello", "extra_field": "Not allowed"},
            ["extra_field"],
            id="single_extra_field"
        ),
        pytest.param(
            {"text": "Hello", "field1": "Extra1", "field2": "Extra2"},
            ["field1", "field2"],
            id="multiple_extra_fields"
        ),
        pytest.param(
            {"text": "Hello", "nested": {"key": "value"}},
            ["nested"],
            id="nested_extra_field"
        ),
    ]

    # Test data for frozen=True configuration
    TEST_FROZEN_MODIFICATIONS = [
        pytest.param(
            "text",
            "Modified Value",
            id="modify_text_field"
        ),
        pytest.param(
            "text",
            "",
            id="modify_to_empty_string"
        ),
        pytest.param(
            "text",
            "A" * 100,
            id="modify_with_long_string"
        ),
    ]

    # Test data for strict=True configuration
    TEST_STRICT_MODE_INVALID = [
        pytest.param(
            {"text": "hello", "number": "123", "decimal": 1.5, "flag": True},
            "number",
            "Input should be a valid integer",
            id="string_to_int"
        ),
        pytest.param(
            {"text": "hello", "number": 123.5, "decimal": 1.5, "flag": True},
            "number",
            "Input should be a valid integer",
            id="float_to_int"
        ),
        pytest.param(
            {"text": "hello", "number": 123, "decimal": 1.5, "flag": "true"},
            "flag",
            "Input should be a valid boolean",
            id="string_to_bool"
        ),
        pytest.param(
            {"text": "hello", "number": 123, "decimal": 1.5, "flag": 1},
            "flag",
            "Input should be a valid boolean",
            id="int_to_bool"
        ),
        pytest.param(
            {"text": "hello", "number": 123, "decimal": "1.5", "flag": True},
            "decimal",
            "Input should be a valid number",
            id="string_to_float"
        ),
    ]

    TEST_STRICT_MODE_VALID = [
        pytest.param(
            {"text": "hello", "number": 123, "decimal": 1.5, "flag": True},
            id="all_correct_types"
        ),
        pytest.param(
            {"text": "", "number": 0, "decimal": 0.0, "flag": False},
            id="zero_and_empty_values"
        ),
        pytest.param(
            {"text": "test", "number": -123, "decimal": -1.5, "flag": False},
            id="negative_values"
        ),
    ]

    # Test data for validate_assignment configuration
    TEST_VALIDATE_ASSIGNMENT_VALID = [
        pytest.param(
            "text", "New valid text", "New valid text",
            id="valid_text_assignment"
        ),
        pytest.param(
            "text", "   Spaces   ", "Spaces",
            id="text_with_whitespace_stripped"
        ),
        pytest.param(
            "number", 50, 50,
            id="valid_number_assignment"
        ),
        pytest.param(
            "number", 0, 0,
            id="min_boundary_number"
        ),
        pytest.param(
            "number", 100, 100,
            id="max_boundary_number"
        ),
    ]

    TEST_VALIDATE_ASSIGNMENT_INVALID = [
        pytest.param(
            "text", "A" * 51, "String should have at most 50 characters",
            id="text_exceeds_max_length"
        ),
        pytest.param(
            "number", -1, "Input should be greater than or equal to 0",
            id="number_below_min"
        ),
        pytest.param(
            "number", 101, "Input should be less than or equal to 100",
            id="number_above_max"
        ),
        pytest.param(
            "number", "50", "Input should be a valid integer",
            id="string_to_number_strict"
        ),
        pytest.param(
            "text", 123, "Input should be a valid string",
            id="number_to_text_strict"
        ),
    ]

    # Test data for validate_default configuration
    TEST_VALIDATE_DEFAULT = [
        pytest.param(
            {},  # Empty input to use defaults
            {
                "text": "default text",  # Whitespace should be stripped
                "number": 50,
                "computed": "computed"  # Factory result should be stripped
            },
            id="all_defaults_validated"
        ),
        pytest.param(
            {"text": "custom"},
            {
                "text": "custom",
                "number": 50,
                "computed": "computed"
            },
            id="partial_defaults_validated"
        ),
    ]

    # Test data for validate_return configuration
    TEST_VALIDATE_RETURN = [
        pytest.param(
            {
                "text": "hello",
                "number": 50,
                "transformed": "test"
            },
            {
                "text": "   hello   ",  # Whitespace added by validator is preserved
                "number": 50,
                "transformed": "TRANSFORMED_TEST"
            },
            id="validator_returns_with_whitespace"
        ),
        pytest.param(
            {
                "text": "world",
                "number": -10,  # Should be clamped to 0
                "transformed": "input"
            },
            {
                "text": "   world   ",  # Whitespace added by validator is preserved
                "number": 0,
                "transformed": "TRANSFORMED_INPUT"
            },
            id="validator_clamps_and_transforms"
        ),
        pytest.param(
            {
                "text": "test",
                "number": 150,  # Should be clamped to 100
                "transformed": "value"
            },
            {
                "text": "   test   ",  # Whitespace added by validator is preserved
                "number": 100,
                "transformed": "TRANSFORMED_VALUE"
            },
            id="validator_clamps_maximum"
        ),
    ]

    # Test data for revalidate_instances configuration
    TEST_REVALIDATE_INSTANCES = [
        pytest.param(
            {"value": "test", "count": 50},
            {"value": "test", "count": 50},
            id="valid_instance_revalidation"
        ),
        pytest.param(
            {"value": "ab", "count": 50},
            "String should have at least 3 characters",
            id="invalid_string_length_revalidation"
        ),
        pytest.param(
            {"value": "test", "count": 101},
            "Input should be less than or equal to 100",
            id="invalid_count_revalidation"
        ),
    ]

    # Test data for use_enum_values configuration
    TEST_USE_ENUM_VALUES = [
        pytest.param(
            {"color": "red", "status": 1},
            {"color": "red", "status": 1, "optional_color": None},
            id="enum_values_direct"
        ),
        pytest.param(
            {"color": "green", "status": 0, "optional_color": "blue"},
            {"color": "green", "status": 0, "optional_color": "blue"},
            id="all_enum_fields_set"
        ),
        pytest.param(
            {"color": "blue", "status": 2},
            {"color": "blue", "status": 2, "optional_color": None},
            id="enum_values_with_default"
        ),
    ]

    # Test data for arbitrary_types_allowed configuration
    TEST_ARBITRARY_TYPES = [
        pytest.param(
            "test_value",
            "standard_text",
            id="custom_type_instance"
        ),
        pytest.param(
            "another_value",
            "another_standard",
            id="different_custom_instance"
        ),
    ]

    # Test data for allow_inf_nan=False configuration
    TEST_ALLOW_INF_NAN_INVALID = [
        pytest.param(
            {"value": float('inf')},
            "Input should be a finite number",
            id="positive_infinity"
        ),
        pytest.param(
            {"value": float('-inf')},
            "Input should be a finite number",
            id="negative_infinity"
        ),
        pytest.param(
            {"value": float('nan')},
            "Input should be a finite number",
            id="not_a_number"
        ),
        pytest.param(
            {"value": 1.0, "optional_value": float('inf')},
            "Input should be a finite number",
            id="infinity_in_optional"
        ),
    ]

    TEST_ALLOW_INF_NAN_VALID = [
        pytest.param(
            {"value": 1.5},
            {"value": 1.5, "optional_value": None},
            id="valid_float"
        ),
        pytest.param(
            {"value": -999.999, "optional_value": 0.0},
            {"value": -999.999, "optional_value": 0.0},
            id="valid_floats_with_optional"
        ),
        pytest.param(
            {"value": 0.0},
            {"value": 0.0, "optional_value": None},
            id="zero_float"
        ),
    ]

    # Test data for coerce_numbers_to_str=False configuration
    TEST_COERCE_NUMBERS_TO_STR = [
        pytest.param(
            {"text": "hello", "code": 123},
            "Input should be a valid string",
            id="number_to_string_rejected"
        ),
        pytest.param(
            {"text": "hello", "code": 45.67},
            "Input should be a valid string",
            id="float_to_string_rejected"
        ),
        pytest.param(
            {"text": 123, "code": "ABC"},
            "Input should be a valid string",
            id="number_in_text_field"
        ),
    ]

    # Test data for from_attributes configuration
    TEST_FROM_ATTRIBUTES = [
        pytest.param(
            {"name": "John", "age": 30},
            {"name": "John", "age": 30, "active": True},
            id="basic_attributes"
        ),
        pytest.param(
            {"name": "Jane", "age": 25, "active": False},
            {"name": "Jane", "age": 25, "active": False},
            id="all_attributes"
        ),
        pytest.param(
            {"name": "   Bob   ", "age": 40},
            {"name": "Bob", "age": 40, "active": True},
            id="attributes_with_whitespace"
        ),
    ]

    # Test data for alias_generator configuration
    TEST_ALIAS_GENERATOR = [
        pytest.param(
            {"first_name": "John", "last_name": "Doe", "email_address": "john@example.com"},
            {"firstName": "John", "lastName": "Doe", "emailAddress": "john@example.com"},
            id="snake_case_input"
        ),
        pytest.param(
            {"first_name": "   Jane   ", "last_name": "   Smith   ", "email_address": "jane@test.com"},
            {"firstName": "Jane", "lastName": "Smith", "emailAddress": "jane@test.com"},
            id="snake_case_with_whitespace"
        ),
    ]

    # Test data for validate_by_alias configuration
    TEST_VALIDATE_BY_ALIAS = [
        pytest.param(
            {"first_name": "Alice", "last_name": "Brown", "email_address": "alice@example.com"},
            {"firstName": "Alice", "lastName": "Brown", "emailAddress": "alice@example.com"},
            id="validate_using_aliases"
        ),
    ]

    # Test data for validate_by_name=False configuration
    TEST_VALIDATE_BY_NAME = [
        pytest.param(
            {"firstName": "Bob", "lastName": "Wilson", "emailAddress": "bob@test.com"},
            "firstName",
            id="camelCase_names_rejected"
        ),
    ]

    # Test data for bytes serialization
    TEST_BYTES_SERIALIZATION = [
        pytest.param(
            b"Hello, World!",
            base64.b64encode(b"Hello, World!").decode('ascii'),
            id="basic_bytes"
        ),
        pytest.param(
            b"\x00\x01\x02\x03\x04",
            base64.b64encode(b"\x00\x01\x02\x03\x04").decode('ascii'),
            id="binary_data"
        ),
        pytest.param(
            b"",
            base64.b64encode(b"").decode('ascii'),
            id="empty_bytes"
        ),
    ]

    # Test data for regex validation
    TEST_REGEX_VALIDATION = [
        pytest.param(
            {"email": "test@example.com", "phone": "+1234567890"},
            {"email": "test@example.com", "phone": "+1234567890"},
            True,
            id="valid_regex_patterns"
        ),
        pytest.param(
            {"email": "invalid-email", "phone": "+1234567890"},
            {"email": "invalid-email", "phone": "+1234567890"},
            False,
            id="invalid_email_pattern"
        ),
        pytest.param(
            {"email": "test@example.com", "phone": "invalid-phone"},
            {"email": "test@example.com", "phone": "invalid-phone"},
            False,
            id="invalid_phone_pattern"
        ),
        pytest.param(
            {"email": "user.name+tag@example.co.uk", "phone": "123456789"},
            {"email": "user.name+tag@example.co.uk", "phone": "123456789"},
            True,
            id="complex_valid_patterns"
        ),
    ]

    # Test data for complex validation scenarios
    TEST_COMPLEX_VALIDATION = [
        pytest.param(
            {"name": "John Doe", "age": 25, "tags": ["Python", "CODING", "  Tech  "]},
            {"name": "John Doe", "age": 25, "tags": ["python", "coding", "tech"]},
            True,
            id="valid_complex_model"
        ),
        pytest.param(
            {"name": "J", "age": 25, "tags": []},
            None,
            False,
            id="name_too_short"
        ),
        pytest.param(
            {"name": "John123", "age": 25, "tags": []},
            None,
            False,
            id="name_with_numbers"
        ),
        pytest.param(
            {"name": "John Doe", "age": 16, "tags": ["adult", "mature"]},
            None,
            False,
            id="minor_with_adult_tag"
        ),
        pytest.param(
            {"name": "Jane Smith", "age": 30, "tags": ["adult", "professional"]},
            {"name": "Jane Smith", "age": 30, "tags": ["adult", "professional"]},
            True,
            id="adult_with_adult_tag"
        ),
    ]