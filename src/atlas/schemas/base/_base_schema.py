#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_base_schema

This module provides the foundational base schema class for all Pydantic models
in the Atlas project. It establishes strict validation rules, security measures,
and consistent behavior patterns that all derived schemas inherit.

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/2 
- Modified : 2025/9/2
- License  : GPL-3.0
"""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    BaseSchema: A standardized base class for all data model schemas.

    Inherits from pydantic's BaseModel and provides strict validation
    and security measures for all derived schemas.

    Attributes:
        model_config (ConfigDict): Configuration dictionary that enforces strict validation,
            immutability, and security measures for all derived schemas.
    """

    model_config = ConfigDict(
        allow_inf_nan=False,                                         # Disallow infinity and NaN values
        arbitrary_types_allowed=False,                               # Disallow arbitrary types
        defer_build=False,                                           # Build immediately for instant validation
        extra='forbid',                                              # Forbid extra fields
        frozen=True,                                                 # Immutable after creation
        hide_input_in_errors=True,                                   # Hide input values in errors (security)
        loc_by_alias=True,                                           # Use aliases for error locations
        protected_namespaces=('model_', 'schema_', 'config_', '_'),  # Protected namespace prefixes
        revalidate_instances='always',                               # Always revalidate instances
        ser_json_bytes='base64',                                     # Serialize bytes as base64
        ser_json_inf_nan='null',                                     # Serialize inf/nan as null
        ser_json_timedelta='iso8601',                                # Serialize timedelta as ISO8601
        str_strip_whitespace=True,                                   # Strip leading/trailing whitespace
        str_to_lower=False,                                          # Preserve original case
        str_to_upper=False,                                          # Preserve original case
        strict=True,                                                 # Strict mode: no type coercion (allows None)
        validate_assignment=True,                                    # Validate on assignment
        validate_default=True,                                       # Validate default values
        validate_return=True,                                        # Validate return values
    )
    """
    Model Configuration Settings:

    **allow_inf_nan** : False
        Disallows infinity and NaN values in float fields.
        Ensures numerical data integrity and prevents invalid calculations.

    **arbitrary_types_allowed** : False
        Restricts field types to standard pydantic-supported types.
        Prevents use of arbitrary Python classes as field types, ensuring
        type safety and validation consistency.

    **defer_build** : False
        Builds model validators immediately upon class definition.
        Ensures immediate validation capability and early error detection
        during development.

    **extra** : 'forbid'
        Forbids any extra attributes during model initialization.
        Prevents injection of undefined fields and maintains strict
        schema compliance.

    **frozen** : True
        Makes model instances immutable after creation.
        Ensures data integrity by preventing accidental modifications
        and maintaining object consistency.

    **hide_input_in_errors** : True
        Hides input values in validation error messages.
        Prevents potential exposure of sensitive data in logs and
        error reports for security purposes.

    **loc_by_alias** : True
        Uses field aliases in error locations when available.
        Provides clearer error messages when field aliases are defined,
        improving debugging experience.

    **protected_namespaces** : ('model_', 'schema_', 'config_', '_')
        Prevents fields from using protected namespace prefixes.
        Avoids naming conflicts with internal pydantic methods and
        maintains framework stability.

    **revalidate_instances** : 'always'
        Always revalidates model instances during validation.
        Ensures data consistency across nested models and prevents
        stale data from bypassing validation.

    **ser_json_bytes** : 'base64'
        Serializes bytes to base64-encoded strings in JSON output.
        Ensures safe transmission and storage of binary data in
        JSON-compatible format.

    **ser_json_inf_nan** : 'null'
        Serializes infinity and NaN float values as null in JSON.
        Maintains JSON standard compliance since JSON doesn't support
        these special float values.

    **ser_json_timedelta** : 'iso8601'
        Serializes timedelta objects to ISO 8601 duration format.
        Ensures standard, interoperable time duration representation
        across different systems.

    **str_strip_whitespace** : True
        Automatically strips leading and trailing whitespace from strings.
        Ensures consistent string data and prevents common input errors
        from affecting data quality.

    **str_to_lower** : False
        Preserves original string case without conversion to lowercase.
        Maintains data as provided by the user, preserving original
        formatting and case sensitivity.

    **str_to_upper** : False
        Preserves original string case without conversion to uppercase.
        Maintains data as provided by the user, preserving original
        formatting and case sensitivity.

    **strict** : True
        Enables strict type checking without automatic type coercion.
        Prevents unexpected type conversions while still allowing None
        values for optional fields.

    **validate_assignment** : True
        Validates data when attributes are assigned after initialization.
        Ensures data integrity throughout the entire object lifecycle,
        not just during creation.

    **validate_default** : True
        Validates default field values during model creation.
        Ensures that default values meet the same validation requirements
        as user-provided values.

    **validate_return** : True
        Validates return values from custom validator functions.
        Ensures that custom validators produce data that meets field
        requirements and maintains data consistency.
    """