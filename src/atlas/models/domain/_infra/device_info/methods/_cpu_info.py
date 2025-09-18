#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_cpu_info

This module provides CPU information models for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/17
- Modified : 2025/9/17
- License  : GPL-3.0
"""

from pydantic import Field
from typing import Optional, List

from atlas.models.base import InternalBaseModel


class CPUInfoReturn(InternalBaseModel):
    """
    CPUInfoReturn: DeviceInfo._cpu_info entry result model

    Attributes:
        brand_raw (Optional[str]): CPU brand name
        vendor_id_raw (Optional[str]): CPU vendor ID
        arch (Optional[str]): CPU architecture
        bits (Optional[int]): CPU bits (32 or 64)
        physical_cores (Optional[int]): Number of physical cores
        logical_cores (Optional[int]): Number of logical cores
        current_freq (Optional[float]): Current frequency in MHz
        min_freq (Optional[float]): Minimum frequency in MHz
        max_freq (Optional[float]): Maximum frequency in MHz
        base_freq (Optional[float]): Base/advertised frequency in MHz
        cpu_usage (Optional[float]): CPU usage percentage (0-100)
        l_two_cache_size (Optional[int]): L2 cache size in bytes
        l_three_cache_size (Optional[int]): L3 cache size in bytes
        family (Optional[int]): CPU family number
        model (Optional[int]): CPU model number
        stepping (Optional[int]): CPU stepping
        flags (Optional[List[str]]): Supported CPU instruction sets
    """

    brand_raw: Optional[str] = Field(
        default=None,
        description="CPU brand name",
    )

    vendor_id_raw: Optional[str] = Field(
        default=None,
        description="CPU vendor ID",
    )

    arch: Optional[str] = Field(
        default=None,
        description="CPU architecture",
    )

    bits: Optional[int] = Field(
        default=None,
        description="CPU bits (32 or 64)",
        ge=1,
    )

    physical_cores: Optional[int] = Field(
        default=None,
        description="Number of physical cores",
        ge=1,
    )

    logical_cores: Optional[int] = Field(
        default=None,
        description="Number of logical cores",
        ge=1,
    )

    current_freq: Optional[float] = Field(
        default=None,
        description="Current frequency in MHz",
        ge=0.0,
    )

    min_freq: Optional[float] = Field(
        default=None,
        description="Minimum frequency in MHz",
        ge=0.0,
    )

    max_freq: Optional[float] = Field(
        default=None,
        description="Maximum frequency in MHz",
        ge=0.0,
    )

    base_freq: Optional[float] = Field(
        default=None,
        description="Base/advertised frequency in MHz",
        ge=0.0,
    )

    cpu_usage: Optional[float] = Field(
        default=None,
        description="CPU usage percentage (0-100)",
        ge=0.0,
        le=100.0,
    )

    l_two_cache_size: Optional[int] = Field(
        default=None,
        description="L2 cache size in bytes",
        ge=0,
    )

    l_three_cache_size: Optional[int] = Field(
        default=None,
        description="L3 cache size in bytes",
        ge=0,
    )

    family: Optional[int] = Field(
        default=None,
        description="CPU family number",
        ge=0,
    )

    model: Optional[int] = Field(
        default=None,
        description="CPU model number",
        ge=0,
    )

    stepping: Optional[int] = Field(
        default=None,
        description="CPU stepping",
        ge=0,
    )

    flags: Optional[List[str]] = Field(
        default=None,
        description="Supported CPU instruction sets",
    )
