#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _base_md
# @Created Time  : 2025/8/27 13:15
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_base_md: Internal pydantic base model module**

This module provides the base model class for all Pydantic models in the Atlas project,
establishing common configuration and behavior patterns.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Iterator


class AtlasBaseModel(BaseModel):
    """
    **AtlasBaseModel: Atlas project pydantic base model**

    Provides a base model class with standardized configuration for all derived models
    in the Atlas project. This ensures consistent behavior across all data models.

    Class Attributes:
        - model_config: Pydantic configuration settings for model behavior
        - version: Model version identifier for tracking schema evolution

    Class Methods:
        - keys: Return field names for mapping protocol
        - __getitem__: Enable dictionary-style field access
        - __iter__: Enable iteration over model fields as key-value pairs
    """

    model_config = ConfigDict(
        extra='forbid',
        frozen=False,
        strict=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
    )
    """
    Pydantic model configuration:
        - extra='forbid': Reject any extra fields not defined in the model
        - frozen=False: Allow model instances to be modified after creation
        - strict=True: Enable strict type checking without type coercion
        - str_strip_whitespace=True: Automatically strip whitespace from string fields
        - validate_assignment=True: Validate field values on assignment
        - validate_default=True: Validate default values during model definition
    """

    version: str = Field(default='1.0.0', description='Version number')
    """Model version identifier, useful for API versioning and schema migration tracking"""

    def keys(self) -> Iterator[str]:
        """
        **keys: Return model field names**

        Required for the mapping protocol to support ** unpacking.
        This method enables the model to be used with the ** operator.

        Returns:
            Iterator[str]: Iterator of field names

        Example:
            >>> model = AtlasBaseModel()
            >>> list(model.keys())
            ['version']
            >>> **model  # Can be used for unpacking
        """
        return iter(self.model_fields)

    def __getitem__(self, key: str) -> Any:
        """
        **__getitem__: Enable dictionary-style field access**

        Allows accessing model fields using dictionary syntax.
        Required for the mapping protocol to support ** unpacking.

        Args:
            key: Field name to access

        Returns:
            Any: The value of the requested field

        Raises:
            AttributeError: If the field does not exist

        Example:
            >>> model = AtlasBaseModel(version='2.0.0')
            >>> model['version']
            '2.0.0'
        """
        return getattr(self, key)

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        **__iter__: Enable iteration over model fields**

        Makes the model instance iterable, returning (field_name, field_value) pairs.
        This allows the model to be used with dict() constructor and tuple unpacking.

        Returns:
            Iterator[tuple[str, Any]]: Iterator of (field_name, field_value) pairs

        Example:
            >>> model = AtlasBaseModel()
            >>> dict(model)  # Convert to dictionary
            {'version': '1.0.0'}
            >>> for key, value in model:  # Iterate over fields
            ...     print(f"{key}: {value}")
            version: 1.0.0
        """
        return iter(self.model_dump().items())