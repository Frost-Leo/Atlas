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


class TestData:
    """
    Test data constants for InternalBaseModel tests

    Attributes:
        TEST_STR_STRIP_WHITESPACE (List[Tuple[str, str]]): Test data for string whitespace stripping
        TEST_STR_MAX_LENGTH_VALID (Tuple[str, int]): Test data for valid string length
        TEST_STR_MAX_LENGTH_INVALID (Tuple[str, int]): Test data for invalid string length
    """

    # Test data of test str_strip_whitespace configuration based on string test model construction
    TEST_STR_STRIP_WHITESPACE = [
        ("    Tom   ", "Tom"),
        ("Tom", "Tom"),
        ("", ""),
        ("   Hello World", "Hello World"),
        ("\n\tJohn\r\n", "John"),
        ("  Multiple   Spaces  ", "Multiple   Spaces"),
    ]

    # Test data of test str_max_length configuration for valid string length
    TEST_STR_MAX_LENGTH_VALID = [
        pytest.param("a" * 100000, 100000, id="max_length_100000"),
        pytest.param("a" * 99999, 99999, id="length_99999"),
        pytest.param("a" * 50000, 50000, id="length_50000"),
        pytest.param("", 0, id="empty_string"),
    ]

    # Test data of test str_max_length configuration for invalid string length
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