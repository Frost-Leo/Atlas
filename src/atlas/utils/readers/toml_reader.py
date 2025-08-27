#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : toml_reader
# @Created Time  : 2025/8/27 9:26
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**toml_reader: TOML file reading and parsing module**

This module provides a TOML file reader with the following features:
    - Read and parse TOML configuration files
    - Automatically replace environment variable placeholders (format: ${VAR_NAME} or ${VAR_NAME:default_value})
    - Convert specific null-like strings (e.g., 'none', 'null') to Python's None object
"""

import os
import re
import tomllib
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Any, Dict, Union


class TomlReader:
    """
    **TomlReader: TOML file parser class**

    Provides functionality to read and parse TOML files with support for
    environment variable substitution and null value conversion.

    Class Attributes:
        - _replacement_pattern: Regex pattern for matching environment variable placeholders
        - _replacement_null_set: Set of strings to be converted to None

    Class Methods:
        - read: Read and parse a TOML file
    """

    _replacement_pattern: re.Pattern[str] = re.compile(r'\$\{(?P<VAR_NAME>[a-zA-Z_][a-zA-Z0-9_]*?)(?::(?P<DEFAULT_VALUE>[^}]*))?\}')
    """Regex pattern to match environment variable placeholders in formats: ${VAR_NAME} or ${VAR_NAME:default_value}"""

    _replacement_null_set: set[str] = {'none', 'null', 'nil', '~'}
    """Set of string values that should be converted to Python None"""

    def read(self, path: Union[Path, str], replace: bool = True) -> Dict[str, Any]:
        """
        **read: Read and parse a TOML file**

        Args:
            path: Path to the TOML file (Path object or string)
            replace: Whether to perform environment variable substitution and null conversion (default: True)

        Returns:
            Dict[str, Any]: Parsed dictionary data from the TOML file

        Raises:
            RuntimeError: When file reading fails, parsing fails, or required environment variable is missing
        """
        try:
            with open(Path(path).resolve(), 'rb') as toml_file:
                raw_content = toml_file.read().decode(encoding='utf-8')

            if replace:
                raw_content = self._sub_env_var(raw_content)

            parsed_data = tomllib.loads(raw_content)

            if replace:
                parsed_data = self._sub_null_value(parsed_data)

            return parsed_data

        except Exception as e:
            raise RuntimeError(f"Failed to read and parse toml file '{path}': {e}") from e

    @classmethod
    def _sub_env_var(cls, raw_content: str) -> str:
        """
        **_sub_env_var: Replace environment variable placeholders in file content**

        Substitutes placeholders like ${VAR_NAME} or ${VAR_NAME:default_value} with actual environment variable values.

        Args:
            raw_content: Raw string content of the TOML file

        Returns:
            str: File content with environment variables substituted

        Raises:
            RuntimeError: When an environment variable doesn't exist and no default value is provided
        """

        def _var_replacer(match: re.Match[str]) -> str:
            """
            **_var_replacer: Internal function to perform individual variable replacement**

            Args:
                 match: Regular expression match object

            Returns:
                str: The environment variable value or default value

            Raises:
                RuntimeError: When environment variable is not found and no default is provided
            """
            var_name = match.group('VAR_NAME')
            default_value = match.group('DEFAULT_VALUE')

            env_value = os.getenv(var_name)

            if env_value is not None:
                return env_value
            elif default_value is not None:
                return default_value
            else:
                raise RuntimeError(f"Failed to find environment variable '{var_name}'")

        return cls._replacement_pattern.sub(_var_replacer, raw_content)

    @classmethod
    def _sub_null_value(cls, data: Any) -> Any:
        """
        **_sub_null_value: Recursively replace null-like strings in data structure**

        Traverses the parsed data structure and replaces specific strings (e.g., 'none', 'null') with Python None.

        Args:
            data: Data to process (can be dict, list, string, or other types)

        Returns:
            Any: Processed data with same structure but null-like strings replaced with None
        """
        if isinstance(data, dict):
            return {key: cls._sub_null_value(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [cls._sub_null_value(item) for item in data]
        elif isinstance(data, str):
            if data.strip().lower() in cls._replacement_null_set:
                return None
            return data
        else:
            return data