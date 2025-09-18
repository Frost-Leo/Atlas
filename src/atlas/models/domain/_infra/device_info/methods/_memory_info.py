#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_memory_info

This module provides memory information models for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

from pydantic import Field
from typing import Optional

from atlas.models.base import InternalBaseModel


class MemoryInfoReturn(InternalBaseModel):
    """
    MemoryInfoReturn: DeviceInfo._memory_info parameter output model

    Attributes:
        total (Optional[int]): Total memory size in bytes
        available (Optional[int]): Available memory size in bytes
        percent (Optional[float]): Memory usage percentage (0-100)
        used (Optional[int]): Used memory size in bytes
        free (Optional[int]): Free memory size in bytes
        swap_total (Optional[int]): Total swap memory size in bytes
        swap_used (Optional[int]): Used swap memory size in bytes
        swap_free (Optional[int]): Free swap memory size in bytes
        swap_percent (Optional[float]): Swap memory usage percentage (0-100)
        buffers (Optional[int]): Buffer memory size in bytes (Linux/Unix)
        cached (Optional[int]): Cached memory size in bytes (Linux/Unix)
        shared (Optional[int]): Shared memory size in bytes (Linux/Unix)
    """

    total: Optional[int] = Field(
        default=None,
        description="Total memory size in bytes",
        ge=0,
    )

    available: Optional[int] = Field(
        default=None,
        description="Available memory size in bytes",
        ge=0,
    )

    percent: Optional[float] = Field(
        default=None,
        description="Memory usage percentage (0-100)",
        ge=0.0,
        le=100.0,
    )

    used: Optional[int] = Field(
        default=None,
        description="Used memory size in bytes",
        ge=0,
    )

    free: Optional[int] = Field(
        default=None,
        description="Free memory size in bytes",
        ge=0,
    )

    swap_total: Optional[int] = Field(
        default=None,
        description="Total swap memory size in bytes",
        ge=0,
    )

    swap_used: Optional[int] = Field(
        default=None,
        description="Used swap memory size in bytes",
        ge=0,
    )

    swap_free: Optional[int] = Field(
        default=None,
        description="Free swap memory size in bytes",
        ge=0,
    )

    swap_percent: Optional[float] = Field(
        default=None,
        description="Swap memory usage percentage (0-100)",
        ge=0.0,
        le=100.0,
    )

    buffers: Optional[int] = Field(
        default=None,
        description="Buffer memory size in bytes (Linux/Unix)",
        ge=0,
    )

    cached: Optional[int] = Field(
        default=None,
        description="Cached memory size in bytes (Linux/Unix)",
        ge=0,
    )

    shared: Optional[int] = Field(
        default=None,
        description="Shared memory size in bytes (Linux/Unix)",
        ge=0,
    )
