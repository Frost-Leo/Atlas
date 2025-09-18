#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_platform_info

This module provides platform information models for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/17
- Modified : 2025/9/17
- License  : GPL-3.0
"""

from pydantic import Field
from typing import Optional

from atlas.models.base import InternalBaseModel


class PlatformInfoReturn(InternalBaseModel):
    """
    PlatformInfoReturn: DeviceInfo._platform_info() return value model

    Attributes:
        hostname (Optional[str]): Hostname of the device
        machine_id (Optional[str]): Machine ID of the device
        os_name (Optional[str]): Operating system name
        os_version (Optional[str]): Operating system version
        python_version (Optional[str]): Python version
        platform (Optional[str]): Platform identifier
        architecture (Optional[str]): System architecture
        processor (Optional[str]): Processor type
        boot_time (Optional[float]): System boot time timestamp
        uptime (Optional[float]): System uptime in seconds
    """

    hostname: Optional[str] = Field(
        default=None,
        description="Hostname of the device",
    )

    machine_id: Optional[str] = Field(
        default=None,
        description="Machine ID of the device",
    )

    os_name: Optional[str] = Field(
        default=None,
        description="Operating system name",
    )

    os_version: Optional[str] = Field(
        default=None,
        description="Operating system version",
    )

    python_version: Optional[str] = Field(
        default=None,
        description="Python version",
    )

    platform: Optional[str] = Field(
        default=None,
        description="Platform identifier (e.g., Windows-10, Linux-5.4.0)",
    )

    architecture: Optional[str] = Field(
        default=None,
        description="System architecture (e.g., x86_64, ARM64)",
    )

    processor: Optional[str] = Field(
        default=None,
        description="Processor type",
    )

    boot_time: Optional[float] = Field(
        default=None,
        description="System boot time timestamp",
        ge=0.0,
    )

    uptime: Optional[float] = Field(
        default=None,
        description="System uptime in seconds",
        ge=0.0,
    )
