#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
models

This module provides device information models and exports all related classes

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/17
- Modified : 2025/9/17
- License  : GPL-3.0
"""

from atlas.models.domain._infra.device_info.constants import Constants
from atlas.models.domain._infra.device_info.methods._cpu_info import CPUInfoReturn
from atlas.models.domain._infra.device_info.methods._platform_info import PlatformInfoReturn
from atlas.models.domain._infra.device_info.methods._memory_info import MemoryInfoReturn
from atlas.models.domain._infra.device_info.methods._disk_info import (
    DiskPartitionInfo,
    DiskIOInfo,
    DiskInfoReturn,
)
from atlas.models.domain._infra.device_info.methods._network_info import NetworkInfoReturn
from atlas.models.domain._infra.device_info.methods.get_device_info import (
    GetDeviceInfoParams,
    GetDeviceInfoReturn,
)

__all__ = [
    "Constants",
    "CPUInfoReturn",
    "PlatformInfoReturn",
    "MemoryInfoReturn",
    "DiskPartitionInfo",
    "DiskIOInfo",
    "DiskInfoReturn",
    "NetworkInfoReturn",
    "GetDeviceInfoParams",
    "GetDeviceInfoReturn",
]
