#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_internal_base_model

The base model of the internal data model of Atlas.

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/11 
- Modified : 2025/9/11
- License  : GPL-3.0
"""

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake

from atlas import __version__


class InternalBaseModel(BaseModel):
    """
    InternalBaseModel: Inheriting from pydantic's BaseModel, provides a basic model for data models between programs.

    Documentation Link: https://docs.pydantic.dev/latest/api/config/

    Attributes:
        model_config (ConfigDict): Global configuration of the model
        version (str): Version number of all models
        created_at (datetime): Timestamp when model instantiation
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,                      # Trim leading and trailing whitespace from string
        str_max_length=100000,                          # Limit string length to prevent DoS attacks
        extra="forbid",                                 # Prohibit adding additional fields to ensure model security
        frozen=False,                                   # After creating an instance, modifications are allowed
        strict=True,                                    # Strict mode validation
        validate_assignment=True,                       # Validation is also required when modifying model attributes
        validate_default=True,                          # Validate default values during validation
        validate_return=True,                           # Verify return value from validators
        revalidate_instances="always",                  # Maintain the refresh effect at all times to prevent data tampering
        use_enum_values=True,                           # Use enum values instead of enum objects
        arbitrary_types_allowed=True,                   # Allow non-Pydantic standard types for ORM compatibility
        allow_inf_nan=False,                            # Disallow infinity and NaN values
        coerce_numbers_to_str=False,                    # Prohibit implicit conversion from number to string
        from_attributes=True,                           # Allow model instances to be constructed from object properties
        alias_generator=to_snake,                       # Generate snake_case aliases for all fields
        validate_by_alias=True,                         # Allow validation using field aliases
        validate_by_name=False,                         # Disallow validation using original field names
        loc_by_alias=True,                              # Use aliases in error locations
        ser_json_bytes="base64",                        # Safe byte serialization format
        val_json_bytes="base64",                        # Matching byte deserialization format
        regex_engine='rust-regex',                      # Rust regex engine is more resistant to ReDoS attacks
        defer_build=True,                               # Enable delayed building to improve performance
        cache_strings='keys',                           # Cache dictionary keys for better performance
        hide_input_in_errors=False,                     # Show error details for debugging purposes
        validation_error_cause=True,                    # Display the original error cause
        use_attribute_docstrings=True,                  # Use attribute docstrings as field descriptions
    )
    """
    Configuration Field Descriptions:

    **str_strip_whitespace**: Automatically removes leading and trailing whitespace from all string fields.
    This helps sanitize user input and prevents issues with accidental spaces in data.

    **str_max_length**: Sets maximum length limit for all string fields to 100KB.
    This prevents DoS attacks through extremely long string inputs and controls memory usage.

    **extra**: Prohibits any additional fields beyond those defined in the model.
    This ensures data integrity and prevents injection of unexpected data fields.

    **frozen**: Makes model instances immutable after creation.
    Once created, attributes can be modified.

    **strict**: Enables strict type validation without automatic type coercion.
    Values must match the exact expected type, preventing subtle type-related bugs.

    **validate_assignment**: Validates data when model attributes are assigned new values.
    This ensures data integrity is maintained even after model creation (when not frozen).

    **validate_default**: Applies validation rules to default field values.
    Ensures that even default values meet the same validation criteria as user input.

    **validate_return**: Validates the return values from field validators.
    This ensures that custom validators return data in the expected format and type.

    **revalidate_instances**: Always revalidates model instances during validation.
    This prevents data tampering by ensuring all instances are validated, even when passed between functions.

    **use_enum_values**: Uses the actual enum values instead of enum objects.
    This simplifies serialization and database storage by using primitive values.

    **arbitrary_types_allowed**: Allows non-standard Pydantic types in model fields.
    Essential for ORM compatibility, enabling use of SQLAlchemy models and other custom types.

    **allow_inf_nan**: Disallows infinite and NaN (Not a Number) values in numeric fields.
    This prevents mathematical errors and ensures numeric data integrity.

    **coerce_numbers_to_str**: Prevents automatic conversion of numbers to strings.
    This maintains type safety and prevents unintended data type changes.

    **from_attributes**: Allows model creation from object attributes.
    Essential for ORM integration, enabling direct conversion from database models to Pydantic models.

    **alias_generator**: Automatically generates snake_case aliases for all fields.
    This ensures consistent naming convention throughout the system, converting camelCase to snake_case.

    **validate_by_alias**: Allows validation using field aliases.
    Enables input validation using the generated snake_case field names.

    **validate_by_name**: Disallows validation using original field names.
    Forces use of standardized aliases, ensuring consistent naming convention across the system.

    **loc_by_alias**: Uses field aliases in error messages and locations.
    This provides consistent error reporting using the standardized field names.

    **ser_json_bytes**: Serializes byte data using base64 encoding.
    This ensures safe and portable representation of binary data in JSON format.

    **val_json_bytes**: Deserializes byte data from base64 encoding.
    This matches the serialization format, ensuring round-trip compatibility.

    **regex_engine**: Uses Rust-based regex engine for pattern validation.
    This provides better protection against ReDoS (Regular Expression Denial of Service) attacks.

    **defer_build**: Delays model validation schema construction until first use.
    This improves application startup time by building validation schemas on-demand.

    **cache_strings**: Caches dictionary keys to reduce memory usage.
    This optimization reduces memory footprint when processing large amounts of similar data.

    **hide_input_in_errors**: Shows input values in validation error messages.
    This aids in debugging by providing complete error context, though it may expose sensitive data.

    **validation_error_cause**: Includes the original exception that caused validation errors.
    This provides detailed debugging information by showing the root cause of validation failures.

    **use_attribute_docstrings**: Uses attribute docstrings as field descriptions.
    This automatically generates field documentation from inline docstrings in the model definition.
    """

    version: str = Field(
        default=__version__,
        description="Version numbers of all models"
    )

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        description="Timestamp when model instantiation"
    )