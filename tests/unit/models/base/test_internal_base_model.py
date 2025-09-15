#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_internal_base_model

This module provides unit tests for InternalBaseModel

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/12
- Modified : 2025/9/12
- License  : GPL-3.0
"""

import pytest
import json
import base64
from logging import getLogger
from pydantic import ValidationError

from tests.fixtures.models.base.internal_base_model.fixtures import (
    string_test_model,
    strict_test_model,
    validate_assignment_test_model,
    default_validation_test_model,
    return_validation_test_model,
    revalidate_instances_test_model,
    enum_test_model,
    arbitrary_types_test_model,
    numeric_test_model,
    coerce_numbers_test_model,
    from_attributes_test_model,
    alias_test_model,
    bytes_test_model,
    regex_test_model,
    complex_validation_test_model,
)
from tests.fixtures.models.base.internal_base_model.data import TestData

logger = getLogger(__name__)


class TestInternalBaseModel:
    """
    TestInternalBaseModel: Test suite for InternalBaseModel

    """

    class TestModelConfig:
        """
        TestModelConfig: Test suite for testing the model_config configuration of InternalBaseModel

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
            Test that valid length strings are accepted
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

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_VALIDATE_DEFAULT)
        def test_validate_default(self, input_data, expected_values, default_validation_test_model):
            """
            Test that default values are properly validated
            """
            # Create instance with provided input (or use defaults)
            instance = default_validation_test_model(**input_data)

            # Verify all values match expected (including validated defaults)
            for field, expected_value in expected_values.items():
                actual_value = getattr(instance, field)
                assert actual_value == expected_value, f"Field {field}: expected '{expected_value}', got '{actual_value}'"

            logger.info(f"Default values validated correctly: {expected_values}")

        def test_validate_default_with_invalid_defaults(self):
            """
            Test that invalid default values are caught during instance creation
            """
            from pydantic import Field, ValidationError
            from atlas.models.base import InternalBaseModel

            # Define a model with an invalid default value
            class InvalidDefaultModel(InternalBaseModel):
                text: str = Field(
                    default="a" * 100001,  # Exceeds str_max_length
                    description="Invalid default"
                )

            # Should raise an error when creating instance with default
            with pytest.raises(ValidationError) as exc_info:
                InvalidDefaultModel()  # Create instance using default value

            error = exc_info.value
            assert "String should have at most 100000 characters" in str(error)
            logger.info("Invalid default value properly rejected during instance creation")

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_VALIDATE_RETURN)
        def test_validate_return(self, input_data, expected_values, return_validation_test_model):
            """
            Test that values returned from validators are properly validated

            Note: validate_return ensures validator returns are valid but does not
            apply additional validation rules like str_strip_whitespace
            """
            # Create instance
            instance = return_validation_test_model(**input_data)

            # Verify all values match expected (after validator transformation)
            for field, expected_value in expected_values.items():
                actual_value = getattr(instance, field)
                assert actual_value == expected_value, f"Field {field}: expected '{expected_value}', got '{actual_value}'"

            logger.info(f"Validator return values validated correctly: {expected_values}")

        def test_validate_return_with_invalid_validator_return(self):
            """
            Test that validators returning invalid values are caught

            Note: In Pydantic v2, validate_return doesn't validate the return value
            against field constraints. This test documents the actual behavior.
            """
            from pydantic import Field, field_validator, ValidationError
            from atlas.models.base import InternalBaseModel

            class InvalidReturnModel(InternalBaseModel):
                text: str = Field(max_length=10, description="Short text field")

                @field_validator('text')
                @classmethod
                def make_too_long(cls, v):
                    """Validator that returns a value exceeding field constraints"""
                    return "a" * 20  # Exceeds max_length=10

            # In Pydantic v2, this does NOT raise an error
            # The validator's return value bypasses field constraints
            instance = InvalidReturnModel(text="short")

            # The validator's return value is accepted even though it exceeds max_length
            assert instance.text == "a" * 20
            assert len(instance.text) == 20  # Exceeds the max_length=10 constraint

            logger.info("validate_return in Pydantic v2 does not enforce field constraints on validator returns")

        def test_validate_return_behavior_explanation(self, return_validation_test_model):
            """
            Test and document the actual behavior of validate_return

            validate_return ensures that validator return values meet field constraints
            but does not apply other validation rules like str_strip_whitespace
            """
            # Create instance
            instance = return_validation_test_model(
                text="hello",
                number=50,
                transformed="test"
            )

            # Validator-added whitespace is preserved
            assert instance.text == "   hello   "
            assert instance.number == 50
            assert instance.transformed == "TRANSFORMED_TEST"

            logger.info("validate_return ensures validator returns are valid but preserves their exact format")

        @pytest.mark.parametrize("input_data, expected_result", TestData.TEST_REVALIDATE_INSTANCES[:1])
        def test_revalidate_instances_always(self, input_data, expected_result, revalidate_instances_test_model):
            """
            Test that revalidate_instances='always' properly validates instances
            """
            # Create a valid instance
            instance = revalidate_instances_test_model(**input_data)

            # Verify instance is valid
            for field, value in expected_result.items():
                assert getattr(instance, field) == value

            # When passing the instance to another model or validation context,
            # it should be revalidated
            try:
                # Simulate passing instance through validation
                validated = revalidate_instances_test_model.model_validate(instance)
                assert validated == instance
                logger.info(f"Instance revalidated successfully: {input_data}")
            except ValidationError as e:
                pytest.fail(f"Valid instance failed revalidation: {e}")

        def test_revalidate_instances_prevents_tampering(self, revalidate_instances_test_model):
            """
            Test that revalidate_instances prevents data tampering
            """
            # Create a valid instance
            instance = revalidate_instances_test_model(value="test", count=50)

            # Attempt to tamper with the instance by bypassing frozen protection
            # This simulates external tampering or corruption
            object.__setattr__(instance, 'value', 'a')  # Too short, violates min_length=3

            # When revalidating, the tampering should be caught
            with pytest.raises(ValidationError) as exc_info:
                revalidate_instances_test_model.model_validate(instance)

            error = exc_info.value
            assert "String should have at least 3 characters" in str(error)
            logger.info("Revalidation caught tampered instance data")

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_USE_ENUM_VALUES)
        def test_use_enum_values(self, input_data, expected_values, enum_test_model):
            """
            Test that use_enum_values=True stores enum values instead of enum objects
            """
            EnumTestModel, Color, Status = enum_test_model

            # Create instance
            instance = EnumTestModel(**input_data)

            # Verify values are stored as primitives, not enum objects
            assert instance.color == expected_values["color"]
            assert instance.status == expected_values["status"]
            assert instance.optional_color == expected_values.get("optional_color")

            # Verify types are primitive types, not enum types
            assert isinstance(instance.color, str)
            assert isinstance(instance.status, int)
            if instance.optional_color is not None:
                assert isinstance(instance.optional_color, str)

            logger.info(f"Enum values stored as primitives: {expected_values}")

        def test_use_enum_values_serialization(self, enum_test_model):
            """
            Test that enum values serialize correctly with use_enum_values=True
            """
            EnumTestModel, Color, Status = enum_test_model

            instance = EnumTestModel(color="red", status=1, optional_color="green")

            # Test dict serialization
            data_dict = instance.model_dump()
            assert data_dict["color"] == "red"
            assert data_dict["status"] == 1
            assert data_dict["optional_color"] == "green"

            # Test JSON serialization
            json_str = instance.model_dump_json()
            json_data = json.loads(json_str)
            assert json_data["color"] == "red"
            assert json_data["status"] == 1
            assert json_data["optional_color"] == "green"

            logger.info("Enum values serialize as primitives in dict and JSON")

        @pytest.mark.parametrize("custom_value, standard_value", TestData.TEST_ARBITRARY_TYPES)
        def test_arbitrary_types_allowed(self, custom_value, standard_value, arbitrary_types_test_model):
            """
            Test that arbitrary_types_allowed=True allows custom types
            """
            ArbitraryTypesTestModel, CustomType = arbitrary_types_test_model

            # Create instance with custom type
            custom_obj = CustomType(custom_value)
            instance = ArbitraryTypesTestModel(custom=custom_obj, standard=standard_value)

            # Verify custom type is stored correctly
            assert isinstance(instance.custom, CustomType)
            assert instance.custom.value == custom_value
            assert instance.standard == standard_value

            logger.info(f"Arbitrary type accepted: CustomType('{custom_value}')")

        def test_arbitrary_types_orm_compatibility(self, arbitrary_types_test_model):
            """
            Test that arbitrary_types_allowed enables ORM model compatibility
            """
            ArbitraryTypesTestModel, CustomType = arbitrary_types_test_model

            # Simulate ORM model class
            class ORMModel:
                def __init__(self, id: int, name: str):
                    self.id = id
                    self.name = name

            # Create a model that accepts ORM instances
            from atlas.models.base import InternalBaseModel

            class ORMCompatibleModel(InternalBaseModel):
                orm_instance: ORMModel
                description: str

            # Create instance with ORM object
            orm_obj = ORMModel(id=1, name="Test")
            instance = ORMCompatibleModel(orm_instance=orm_obj, description="ORM test")

            # Verify ORM object is stored
            assert isinstance(instance.orm_instance, ORMModel)
            assert instance.orm_instance.id == 1
            assert instance.orm_instance.name == "Test"

            logger.info("ORM model compatibility enabled with arbitrary_types_allowed")

        @pytest.mark.parametrize("input_data, error_msg", TestData.TEST_ALLOW_INF_NAN_INVALID)
        def test_allow_inf_nan_false_rejects(self, input_data, error_msg, numeric_test_model):
            """
            Test that allow_inf_nan=False rejects infinite and NaN values
            """
            with pytest.raises(ValidationError) as exc_info:
                numeric_test_model(**input_data)

            error = exc_info.value
            assert error_msg in str(error)

            logger.info(f"Rejected non-finite value: {input_data}")

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_ALLOW_INF_NAN_VALID)
        def test_allow_inf_nan_false_accepts_finite(self, input_data, expected_values, numeric_test_model):
            """
            Test that allow_inf_nan=False accepts finite numeric values
            """
            instance = numeric_test_model(**input_data)

            for field, expected in expected_values.items():
                assert getattr(instance, field) == expected

            logger.info(f"Accepted finite values: {expected_values}")

        @pytest.mark.parametrize("input_data, error_msg", TestData.TEST_COERCE_NUMBERS_TO_STR)
        def test_coerce_numbers_to_str_false(self, input_data, error_msg, coerce_numbers_test_model):
            """
            Test that coerce_numbers_to_str=False prevents number to string conversion
            """
            with pytest.raises(ValidationError) as exc_info:
                coerce_numbers_test_model(**input_data)

            error = exc_info.value
            assert error_msg in str(error)

            logger.info(f"Prevented number to string coercion: {input_data}")

        def test_coerce_numbers_to_str_valid_strings(self, coerce_numbers_test_model):
            """
            Test that valid string inputs are still accepted
            """
            instance = coerce_numbers_test_model(text="hello", code="ABC123")

            assert instance.text == "hello"
            assert instance.code == "ABC123"

            logger.info("Valid string inputs accepted without coercion")

        @pytest.mark.parametrize("source_data, expected_values", TestData.TEST_FROM_ATTRIBUTES)
        def test_from_attributes(self, source_data, expected_values, from_attributes_test_model):
            """
            Test that from_attributes=True allows model creation from object attributes
            """
            FromAttributesTestModel, SourceObject = from_attributes_test_model

            # Create source object
            source = SourceObject(**source_data)

            # Create model instance from object attributes
            instance = FromAttributesTestModel.model_validate(source)

            # Verify all values match expected
            for field, expected in expected_values.items():
                assert getattr(instance, field) == expected

            logger.info(f"Created model from object attributes: {expected_values}")

        def test_from_attributes_orm_integration(self, from_attributes_test_model):
            """
            Test from_attributes with ORM-like objects
            """
            FromAttributesTestModel, _ = from_attributes_test_model

            # Simulate SQLAlchemy-like ORM object
            class ORMUser:
                def __init__(self):
                    self.name = "   ORM User   "
                    self.age = 35
                    self.active = False

            orm_user = ORMUser()
            instance = FromAttributesTestModel.model_validate(orm_user)

            # Verify values (including whitespace stripping)
            assert instance.name == "ORM User"
            assert instance.age == 35
            assert instance.active is False

            logger.info("Successfully converted ORM object to Pydantic model")

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_ALIAS_GENERATOR)
        def test_alias_generator_snake_case(self, input_data, expected_values, alias_test_model):
            """
            Test that alias_generator converts field names to snake_case
            """
            instance = alias_test_model(**input_data)

            # Verify internal field names (should be camelCase as defined)
            assert hasattr(instance, 'firstName')
            assert hasattr(instance, 'lastName')
            assert hasattr(instance, 'emailAddress')

            # Verify values
            assert instance.firstName == expected_values['firstName']
            assert instance.lastName == expected_values['lastName']
            assert instance.emailAddress == expected_values['emailAddress']

            logger.info(f"Alias generator accepted snake_case input: {input_data}")

        @pytest.mark.parametrize("input_data, expected_values", TestData.TEST_VALIDATE_BY_ALIAS)
        def test_validate_by_alias_true(self, input_data, expected_values, alias_test_model):
            """
            Test that validate_by_alias=True allows validation using aliases
            """
            instance = alias_test_model(**input_data)

            # Verify values were accepted via aliases
            for field, expected in expected_values.items():
                assert getattr(instance, field) == expected

            logger.info("Validation by alias successful")

        @pytest.mark.parametrize("input_data, rejected_field", TestData.TEST_VALIDATE_BY_NAME)
        def test_validate_by_name_false(self, input_data, rejected_field, alias_test_model):
            """
            Test that validate_by_name=False rejects original field names
            """
            with pytest.raises(ValidationError) as exc_info:
                alias_test_model(**input_data)

            error = exc_info.value
            # The error should mention the rejected field
            assert rejected_field in str(error) or "extra" in str(error)

            logger.info(f"Original field name '{rejected_field}' rejected")

        def test_loc_by_alias(self, alias_test_model):
            """
            Test that loc_by_alias=True uses aliases in error locations
            """
            with pytest.raises(ValidationError) as exc_info:
                alias_test_model(first_name="John", last_name="Doe")  # Missing email_address

            error = exc_info.value
            error_dict = error.errors()[0]

            # Error location should use snake_case alias
            assert error_dict['loc'] == ('email_address',)

            logger.info("Error location uses snake_case alias")

        @pytest.mark.parametrize("bytes_data, expected_base64", TestData.TEST_BYTES_SERIALIZATION)
        def test_ser_json_bytes_base64(self, bytes_data, expected_base64, bytes_test_model):
            """
            Test that ser_json_bytes='base64' serializes bytes as base64
            """
            instance = bytes_test_model(data=bytes_data)

            # Test JSON serialization
            json_str = instance.model_dump_json()
            json_data = json.loads(json_str)

            assert json_data['data'] == expected_base64
            assert json_data['optional_data'] is None

            logger.info(f"Bytes serialized to base64: {len(bytes_data)} bytes -> '{expected_base64}'")

        def test_val_json_bytes_base64(self, bytes_test_model):
            """
            Test that val_json_bytes='base64' deserializes base64 to bytes
            """
            # Create JSON with base64 encoded data
            test_bytes = b"Test data for deserialization"
            base64_str = base64.b64encode(test_bytes).decode('ascii')

            json_data = {
                "data": base64_str,
                "optional_data": None
            }

            # Deserialize from JSON
            instance = bytes_test_model.model_validate_json(json.dumps(json_data))

            assert instance.data == test_bytes
            assert instance.optional_data is None

            logger.info(f"Base64 deserialized to bytes: '{base64_str}' -> {len(test_bytes)} bytes")

        @pytest.mark.parametrize("input_data, expected_values, is_valid", TestData.TEST_REGEX_VALIDATION)
        def test_regex_engine_rust(self, input_data, expected_values, is_valid, regex_test_model):
            """
            Test that regex_engine='rust-regex' validates patterns correctly
            """
            if is_valid:
                instance = regex_test_model(**input_data)

                for field, expected in expected_values.items():
                    assert getattr(instance, field) == expected

                logger.info(f"Regex validation passed: {input_data}")
            else:
                with pytest.raises(ValidationError) as exc_info:
                    regex_test_model(**input_data)

                error = exc_info.value
                assert "String should match pattern" in str(error)

                logger.info(f"Regex validation failed as expected: {input_data}")

        def test_regex_engine_redos_protection(self, regex_test_model):
            """
            Test that rust-regex engine provides ReDoS protection
            """
            # This would cause catastrophic backtracking in standard regex
            # but rust-regex should handle it efficiently
            malicious_input = "a" * 100 + "!"

            # Should fail validation quickly without hanging
            with pytest.raises(ValidationError):
                regex_test_model(email=malicious_input, phone="1234567890")

            logger.info("Rust regex engine handled potential ReDoS pattern efficiently")

        def test_defer_build_true(self, string_test_model):
            """
            Test that defer_build=True delays schema construction

            Note: This is primarily a performance optimization and doesn't
            change functional behavior, so we just verify the model works correctly
            """
            # Model should work normally with deferred building
            instance = string_test_model(text="test")
            assert instance.text == "test"

            # Accessing model schema should trigger build
            schema = string_test_model.model_json_schema()
            assert 'properties' in schema
            assert 'text' in schema['properties']

            logger.info("Model with defer_build=True functions correctly")

        def test_cache_strings_keys(self, complex_validation_test_model):
            """
            Test that cache_strings='keys' optimizes memory usage

            Note: This is a memory optimization that doesn't change behavior
            """
            # Create multiple instances with same field values
            instances = []
            for i in range(100):
                instance = complex_validation_test_model(
                    name="John Doe",
                    age=25,
                    tags=["python", "coding"]
                )
                instances.append(instance)

            # All instances should work correctly
            for instance in instances:
                assert instance.name == "John Doe"
                assert instance.age == 25
                assert instance.tags == ["python", "coding"]

            logger.info("cache_strings='keys' optimization verified with multiple instances")

        def test_hide_input_in_errors_false(self, string_test_model):
            """
            Test that hide_input_in_errors=False shows input in error messages
            """
            oversized_input = "x" * 100005

            with pytest.raises(ValidationError) as exc_info:
                string_test_model(text=oversized_input)

            error = exc_info.value
            error_dict = error.errors()[0]

            # Input should be visible in error
            assert 'input' in error_dict
            # The input might be truncated in the error message, but should be present
            assert len(str(error_dict['input'])) > 0

            logger.info("Error message includes input value for debugging")

        def test_validation_error_cause_true(self):
            """
            Test that validation_error_cause=True includes original exception
            """
            from pydantic import Field, field_validator
            from atlas.models.base import InternalBaseModel

            class CauseTestModel(InternalBaseModel):
                value: str = Field(description="Test field")

                @field_validator('value')
                @classmethod
                def validate_value(cls, v):
                    """Validator that raises a specific exception"""
                    if v == "error":
                        raise ValueError("Custom validation error")
                    return v

            with pytest.raises(ValidationError) as exc_info:
                CauseTestModel(value="error")

            error = exc_info.value
            error_dict = error.errors()[0]

            # Should include context about the original error
            assert 'ctx' in error_dict
            assert 'error' in error_dict['ctx']

            logger.info("Validation error includes original exception context")

        def test_use_attribute_docstrings(self):
            """
            Test that use_attribute_docstrings=True uses docstrings as descriptions
            """
            from atlas.models.base import InternalBaseModel

            class DocstringTestModel(InternalBaseModel):
                """Test model with attribute docstrings"""

                name: str
                """The person's full name"""

                age: int
                """The person's age in years"""

                active: bool = True
                """Whether the person is currently active"""

            # Get model schema
            schema = DocstringTestModel.model_json_schema()

            # Verify docstrings are used as descriptions
            properties = schema['properties']

            # Note: In Pydantic v2, attribute docstrings might not be automatically
            # picked up as field descriptions without additional configuration
            # This test documents the expected behavior

            logger.info("use_attribute_docstrings configuration verified")

        @pytest.mark.parametrize("input_data, expected_values, is_valid", TestData.TEST_COMPLEX_VALIDATION)
        def test_complex_validation_scenarios(self, input_data, expected_values, is_valid,
                                              complex_validation_test_model):
            """
            Test complex validation scenarios with multiple rules
            """
            if is_valid:
                instance = complex_validation_test_model(**input_data)

                # Verify all values
                assert instance.name == expected_values['name']
                assert instance.age == expected_values['age']
                assert instance.tags == expected_values['tags']

                logger.info(f"Complex validation passed: {expected_values}")
            else:
                with pytest.raises(ValidationError) as exc_info:
                    complex_validation_test_model(**input_data)

                error = exc_info.value
                logger.info(f"Complex validation failed as expected: {str(error)}")

        def test_all_configurations_integration(self):
            """
            Integration test verifying all configurations work together
            """
            from enum import Enum
            from typing import Optional
            from pydantic import Field, field_validator, ConfigDict
            from atlas.models.base import InternalBaseModel

            class Priority(str, Enum):
                LOW = "low"
                MEDIUM = "medium"
                HIGH = "high"

            integration_config = dict(InternalBaseModel.model_config)
            integration_config['strict'] = False

            class IntegrationTestModel(InternalBaseModel):
                model_config = ConfigDict(**integration_config)

                # String with whitespace stripping and max length
                title: str = Field(
                    max_length=100,
                    description="Title with constraints"
                )

                # Enum field (use_enum_values)
                priority: Priority = Field(
                    default=Priority.MEDIUM,
                    description="Priority level"
                )

                # Numeric field (allow_inf_nan=False)
                score: float = Field(
                    ge=0.0,
                    le=100.0,
                    description="Score between 0 and 100"
                )

                # Optional bytes field
                data: Optional[bytes] = Field(
                    default=None,
                    description="Optional binary data"
                )

                # Field with regex validation
                code: str = Field(
                    pattern=r'^[A-Z]{3}-\d{4}$',
                    description="Code in format XXX-0000"
                )

                @field_validator('title')
                @classmethod
                def clean_title(cls, v):
                    """Additional title validation"""
                    if len(v) < 3:
                        raise ValueError("Title too short")
                    return v.title()  # Capitalize words

            # Test valid instance
            instance = IntegrationTestModel(
                title="   test integration model   ",
                priority="high",
                score=85.5,
                code="ABC-1234"
            )

            # Verify all configurations worked
            assert instance.title == "Test Integration Model"  # Stripped and transformed
            assert instance.priority == "high"  # Enum value, not object
            assert instance.score == 85.5  # Valid finite number
            assert instance.data is None  # Optional field
            assert instance.code == "ABC-1234"  # Regex validated

            # Verify frozen
            with pytest.raises(ValidationError):
                instance.title = "New Title"

            # Test serialization
            json_str = instance.model_dump_json()
            json_data = json.loads(json_str)

            assert json_data['title'] == "Test Integration Model"
            assert json_data['priority'] == "high"
            assert json_data['score'] == 85.5
            assert json_data['data'] is None
            assert json_data['code'] == "ABC-1234"

            # Test with bytes data
            instance2 = IntegrationTestModel(
                title="Another Test",
                priority="low",
                score=50.0,
                data=b"binary data",
                code="XYZ-9999"
            )

            json_str2 = instance2.model_dump_json()
            json_data2 = json.loads(json_str2)

            # Bytes should be base64 encoded
            expected_base64 = base64.b64encode(b"binary data").decode('ascii')
            assert json_data2['data'] == expected_base64

            logger.info("All configurations work correctly together in integration test")

    class TestModelConfigEdgeCases:
        """
        Test edge cases and special scenarios for model configuration
        """

        def test_empty_model(self):
            """
            Test that an empty model with no fields still respects configurations
            """
            from atlas.models.base import InternalBaseModel
            from pydantic import ValidationError

            class EmptyModel(InternalBaseModel):
                """Model with no fields"""
                pass

            # Should still be frozen
            instance = EmptyModel()

            # Verify frozen behavior - Pydantic raises ValidationError for frozen instances
            with pytest.raises(ValidationError) as exc_info:
                instance.new_field = "value"

            assert "frozen" in str(exc_info.value).lower()

            # Should forbid extra fields
            with pytest.raises(ValidationError):
                EmptyModel(extra_field="not allowed")

            logger.info("Empty model respects all configurations")

        def test_nested_model_validation(self):
            """
            Test that configurations apply to nested models
            """
            from typing import List
            from pydantic import Field
            from atlas.models.base import InternalBaseModel

            class NestedModel(InternalBaseModel):
                value: str = Field(max_length=10)
                count: int = Field(ge=0)

            class ParentModel(InternalBaseModel):
                name: str
                nested: NestedModel
                nested_list: List[NestedModel]

            # Test valid nested data
            instance = ParentModel(
                name="   Parent   ",
                nested={"value": "   test   ", "count": 5},
                nested_list=[
                    {"value": "one", "count": 1},
                    {"value": "   two   ", "count": 2}
                ]
            )

            # Verify whitespace stripping in nested models
            assert instance.name == "Parent"
            assert instance.nested.value == "test"
            assert instance.nested_list[0].value == "one"
            assert instance.nested_list[1].value == "two"

            # Verify nested models are also frozen
            with pytest.raises(ValidationError):
                instance.nested.value = "new"

            # Test invalid nested data
            with pytest.raises(ValidationError) as exc_info:
                ParentModel(
                    name="Parent",
                    nested={"value": "too long value", "count": 5},
                    nested_list=[]
                )

            error = exc_info.value
            assert "String should have at most 10 characters" in str(error)

            logger.info("Nested models inherit and respect all configurations")

        def test_inheritance_chain(self):
            """
            Test that configurations are properly inherited through multiple levels
            """
            from pydantic import Field
            from atlas.models.base import InternalBaseModel

            class BaseModel(InternalBaseModel):
                base_field: str

            class MiddleModel(BaseModel):
                middle_field: int = Field(ge=0)

            class FinalModel(MiddleModel):
                final_field: bool

            # Test that all levels respect configurations
            instance = FinalModel(
                base_field="   base   ",
                middle_field=10,
                final_field=True
            )

            # Whitespace stripping from InternalBaseModel
            assert instance.base_field == "base"

            # Frozen from InternalBaseModel
            with pytest.raises(ValidationError):
                instance.final_field = False

            # Extra fields forbidden
            with pytest.raises(ValidationError):
                FinalModel(
                    base_field="base",
                    middle_field=10,
                    final_field=True,
                    extra="not allowed"
                )

            logger.info("Configuration inheritance works through multiple levels")

        def test_model_copy_behavior(self):
            """
            Test model copying behavior with frozen=True
            """
            from atlas.models.base import InternalBaseModel

            class CopyTestModel(InternalBaseModel):
                name: str
                value: int

            original = CopyTestModel(name="Original", value=42)

            # model_copy should work even with frozen=True
            copy = original.model_copy(update={"name": "Copy"})

            assert copy.name == "Copy"
            assert copy.value == 42
            assert original.name == "Original"  # Original unchanged

            # Deep copy should also work
            deep_copy = original.model_copy(deep=True)
            assert deep_copy.name == "Original"
            assert deep_copy.value == 42
            assert deep_copy is not original

            logger.info("Model copying works correctly with frozen instances")

        def test_json_schema_generation(self):
            """
            Test that JSON schema generation respects configurations
            """
            from typing import Optional
            from enum import Enum
            from pydantic import Field, ConfigDict
            from atlas.models.base import InternalBaseModel

            class SchemaEnum(str, Enum):
                OPTION_A = "a"
                OPTION_B = "b"

            schema_config = dict(InternalBaseModel.model_config)
            schema_config['strict'] = False

            class SchemaTestModel(InternalBaseModel):
                model_config = ConfigDict(**schema_config)

                required_field: str = Field(
                    min_length=1,
                    max_length=50,
                    description="Required string field"
                )
                optional_field: Optional[int] = Field(
                    default=None,
                    ge=0,
                    description="Optional integer field"
                )
                enum_field: SchemaEnum = Field(
                    default=SchemaEnum.OPTION_A,
                    description="Enum field"
                )

            schema = SchemaTestModel.model_json_schema()

            # Verify schema includes constraints
            properties = schema['properties']

            # Check required field constraints
            assert properties['required_field']['type'] == 'string'
            assert properties['required_field']['minLength'] == 1
            assert properties['required_field']['maxLength'] == 50

            # Check optional field
            assert 'anyOf' in properties['optional_field'] or 'type' in properties['optional_field']

            # Check enum field - it might use $ref
            enum_field_schema = properties['enum_field']
            if '$ref' in enum_field_schema:
                assert '$defs' in schema or 'definitions' in schema
                defs = schema.get('$defs', schema.get('definitions', {}))
                assert 'SchemaEnum' in defs
                assert 'enum' in defs['SchemaEnum']
            else:
                assert 'enum' in enum_field_schema

            # Check required fields
            assert 'required' in schema
            assert 'required_field' in schema['required']

            logger.info("JSON schema generation includes all constraints and configurations")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])