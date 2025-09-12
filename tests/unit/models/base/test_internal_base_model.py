#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_internal_base_model

This module provides 

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12 
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import pytest
from logging import getLogger
from pydantic import ValidationError

from tests.fixtures.models.base.internal_base_model.fixtures import (
     string_test_model,
     strict_test_model,
     validate_assignment_test_model,
)
from tests.fixtures.models.base.internal_base_model.data import TestData

logger = getLogger(__name__)


class TestInternalBaseModel:
    """
    TestInternalBaseModel: Testing test case set of InternalBaseModel

    """

    class TestModelConfig:
        """
        TestModelConfig: Test set for testing the model_config configuration of InternalBaseModel

        """

        @pytest.mark.parametrize("input_text, expected", TestData.TEST_STR_STRIP_WHITESPACE)
        def test_str_strip_whitespace(self, input_text, expected, string_test_model):
            """
            Test that strings are stripped of whitespace
            """
            instance = string_test_model(text=input_text)
            assert instance.text == expected
            logger.info(f"Whitespace stripping: '{input_text}' -> '{instance.text}'")

        @pytest.mark.parametrize("input_text, expected_length", TestData.TEST_STR_MAX_LENGTH_VALID)
        def test_str_max_length_valid(self, input_text, expected_length, string_test_model):
            """
            Test that valid length strings are accepted\
            """
            instance = string_test_model(text=input_text)
            assert len(instance.text) == expected_length
            logger.info(f"Valid string length: {len(instance.text)} chars")

        @pytest.mark.parametrize("input_text, expected_length", TestData.TEST_STR_MAX_LENGTH_INVALID)
        def test_str_max_length_invalid(self, input_text, expected_length, string_test_model):
            """
            Test that invalid length strings are rejected
            """
            with pytest.raises(ValidationError) as exc_info:
                string_test_model(text=input_text)

            error_msg = str(exc_info.value)
            assert "String should have at most 100000 characters" in error_msg
            logger.info(f"Rejected string length: {expected_length} chars")

        @pytest.mark.parametrize("input_data, expected_extra_fields", TestData.TEST_EXTRA_FORBID)
        def test_extra_forbid_parametrized(self, input_data, expected_extra_fields, string_test_model):
            """
            Test that extra fields are forbidden with various inputs
            """
            with pytest.raises(ValidationError) as exc_info:
                string_test_model(**input_data)

            error = exc_info.value
            error_dict = error.errors()

            # Check that all expected extra fields are reported as errors
            extra_field_errors = [e for e in error_dict if e['type'] == 'extra_forbidden']
            reported_fields = [e['input'] for e in extra_field_errors]

            for field in expected_extra_fields:
                assert any(field in str(e) for e in error_dict), f"Expected error for extra field '{field}'"

            logger.info(f"Rejected extra fields: {expected_extra_fields}")

        @pytest.mark.parametrize("field_name, new_value", TestData.TEST_FROZEN_MODIFICATIONS)
        def test_frozen_parametrized(self, field_name, new_value, string_test_model):
            """
            Test that frozen instances cannot be modified with various values
            """
            # Create instance with initial value
            instance = string_test_model(text="Initial Value")
            original_value = getattr(instance, field_name)

            # Attempt to modify the field
            with pytest.raises(ValidationError) as exc_info:
                setattr(instance, field_name, new_value)

            error = exc_info.value
            assert "Instance is frozen" in str(error)

            # Verify the value hasn't changed
            assert getattr(instance, field_name) == original_value
            logger.info(f"Frozen field '{field_name}' modification rejected")

        @pytest.mark.parametrize("input_data, error_field, error_msg", TestData.TEST_STRICT_MODE_INVALID)
        def test_strict_mode_no_coercion(self, input_data, error_field, error_msg, strict_test_model):
            """
            Test that strict mode prevents type coercion
            """
            with pytest.raises(ValidationError) as exc_info:
                strict_test_model(**input_data)

            error = exc_info.value
            error_dict = error.errors()[0]

            assert error_dict['loc'] == (error_field,)
            assert error_msg in error_dict['msg']

            logger.info(f"Strict mode rejected type coercion for field '{error_field}': {error_dict['msg']}")

        @pytest.mark.parametrize("input_data", TestData.TEST_STRICT_MODE_VALID)
        def test_strict_mode_valid_types(self, input_data, strict_test_model):
            """
            Test that strict mode accepts correct types
            """
            instance = strict_test_model(**input_data)

            # Verify all values are correctly assigned
            for field, value in input_data.items():
                assert getattr(instance, field) == value
                assert type(getattr(instance, field)) == type(value)

            logger.info(f"Strict mode accepted valid types: {input_data}")

        @pytest.mark.parametrize("field_name, new_value, expected_value", TestData.TEST_VALIDATE_ASSIGNMENT_VALID)
        def test_validate_assignment_valid(self, field_name, new_value, expected_value, validate_assignment_test_model):
            """
            Test that validate_assignment properly validates valid assignments
            """
            # Create instance with initial values
            instance = validate_assignment_test_model(text="Initial", number=10)

            # Perform valid assignment
            setattr(instance, field_name, new_value)

            # Verify assignment succeeded and value is correct
            assert getattr(instance, field_name) == expected_value
            logger.info(f"Valid assignment: {field_name}={new_value} -> {expected_value}")

        @pytest.mark.parametrize("field_name, new_value, error_msg", TestData.TEST_VALIDATE_ASSIGNMENT_INVALID)
        def test_validate_assignment_invalid(self, field_name, new_value, error_msg, validate_assignment_test_model):
            """
            Test that validate_assignment properly rejects invalid assignments
            """
            # Create instance with initial values
            instance = validate_assignment_test_model(text="Initial", number=10)
            original_value = getattr(instance, field_name)

            # Attempt invalid assignment
            with pytest.raises(ValidationError) as exc_info:
                setattr(instance, field_name, new_value)

            error = exc_info.value
            assert error_msg in str(error)

            # Verify value unchanged
            assert getattr(instance, field_name) == original_value
            logger.info(f"Invalid assignment rejected: {field_name}={new_value}, error: {error_msg}")

        def test_validate_assignment_config_verification(self, validate_assignment_test_model):
            """
            Test that validate_assignment configuration is properly set and functional
            """
            # Verify configuration
            assert validate_assignment_test_model.model_config.get('validate_assignment') is True
            assert validate_assignment_test_model.model_config.get('frozen') is False

            # Verify it inherits other configurations from InternalBaseModel
            assert validate_assignment_test_model.model_config.get('strict') is True
            assert validate_assignment_test_model.model_config.get('str_strip_whitespace') is True

            logger.info("validate_assignment configuration verified and functional with frozen=False")
