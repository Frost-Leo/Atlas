#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : env_vars_md
# @Created Time  : 2025/8/27 13:06
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**env_vars_md: Environment variable model module**

This module defines a Pydantic model for managing environment variables
used throughout the Atlas project with the following features:
    - Automatic detection of machine information (hostname and ID)
    - Environment variable validation and default value handling
    - Centralized configuration for project directory structure
    - Runtime environment specification
"""

import os
from pydantic import Field

from atlas.lib.models import AtlasBaseModel
from atlas.utils.toolkit import MachineInfo


class EnvVarsModel(AtlasBaseModel):
    """
    **EnvVarsModel: Environment variables configuration model**

    Defines and validates all environment variables required by the Atlas project.
    Provides automatic machine detection and configurable project paths.

    Class Attributes:
        - MACHINE_HOSTNAME: Current machine's hostname (computer name)
        - MACHINE_ID: Unique identifier for the current machine
        - ATLAS_ROOT: Project root directory path
        - ATLAS_ETC_ROOT: Configuration files directory path
        - ATLAS_LOGS_ROOT: Log files directory path
        - ATLAS_DATA_ROOT: Data files directory path
        - ATLAS_ENV: Current runtime environment identifier
    """

    MACHINE_HOSTNAME: str = Field(
        default_factory=MachineInfo.get_machine_hostname,
        description='The hostname (computer name) of the machine currently running the application'
    )
    """Hostname (computer name) of the current machine, automatically detected at runtime"""

    MACHINE_ID: str = Field(
        default_factory=MachineInfo.get_machine_id,
        description='Unique identifier of the physical machine currently running the application'
    )
    """Unique machine identifier used for distributed system coordination and logging"""

    c: str = Field(
        default_factory=lambda: os.getenv('ATLAS_ROOT'),
        description='The root directory path of the Atlas project file structure'
    )
    """
    Project root directory path. This is the base path for all other project directories.
    Many components depend on this variable, and it cannot be empty during project runtime.
    Should be set as an environment variable before starting the application.
    """

    ATLAS_ETC_ROOT: str = Field(
        default_factory=lambda: os.getenv('ATLAS_ETC_ROOT'),
        description='Directory path for project configuration files'
    )
    """
    Configuration files directory path, typically used for storing TOML, JSON, YAML
    configuration files. Components use this path to locate their configuration files
    during instantiation. Defaults to {ATLAS_ROOT}/etc if not specified.
    """

    ATLAS_LOGS_ROOT: str = Field(
        default_factory=lambda: os.getenv('ATLAS_LOGS_ROOT'),
        description='Directory path for application log files'
    )
    """
    Log files directory path where all application logs are stored.
    Used by logging components to determine log file locations.
    Defaults to {ATLAS_ROOT}/logs if not specified.
    """

    ATLAS_DATA_ROOT: str = Field(
        default_factory=lambda: os.getenv('ATLAS_DATA_ROOT'),
        description='Directory path for application data files'
    )
    """
    Data files directory path for storing application-generated data,
    databases, cache files, and other persistent data.
    Defaults to {ATLAS_ROOT}/data if not specified.
    """

    ATLAS_ENV: str = Field(
        default_factory=lambda: os.getenv('ATLAS_ENV'),
        description='Current runtime environment identifier (e.g., development, staging, production)'
    )
    """
    Runtime environment identifier used to determine application behavior,
    configuration selection, and feature flags. Common values include:
    'development', 'testing', 'staging', 'production'.
    Defaults to 'development' if not specified.
    """


