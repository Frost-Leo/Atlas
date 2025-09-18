#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_device_info

This module provides models for getting device information

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

from pydantic import Field
from typing import Optional

from atlas.models.base import InternalBaseModel
from atlas.models.domain._infra.device_info.methods._cpu_info import CPUInfoReturn
from atlas.models.domain._infra.device_info.methods._disk_info import DiskInfoReturn
from atlas.models.domain._infra.device_info.methods._memory_info import MemoryInfoReturn
from atlas.models.domain._infra.device_info.methods._network_info import NetworkInfoReturn
from atlas.models.domain._infra.device_info.methods._platform_info import PlatformInfoReturn


class GetDeviceInfoParams(InternalBaseModel):
    """
    GetDeviceInfoParams: Parameters for getting device information

    Attributes:
        include_platform (bool): Whether to include platform information
        include_cpu (bool): Whether to include CPU information
        include_memory (bool): Whether to include memory information
        include_disk (bool): Whether to include disk information
        include_network (bool): Whether to include network information
    """

    include_platform: bool = Field(
        default=True,
        description="Whether to include platform information",
    )

    include_cpu: bool = Field(
        default=True,
        description="Whether to include CPU information",
    )

    include_memory: bool = Field(
        default=True,
        description="Whether to include memory information",
    )

    include_disk: bool = Field(
        default=True,
        description="Whether to include disk information",
    )

    include_network: bool = Field(
        default=True,
        description="Whether to include network information",
    )


class GetDeviceInfoReturn(InternalBaseModel):
    """
    GetDeviceInfoReturn: Complete device information return model

    Attributes:
        platform (Optional[PlatformInfoReturn]): Platform basic information
        cpu (Optional[CPUInfoReturn]): CPU information
        memory (Optional[MemoryInfoReturn]): Memory information
        disk (Optional[DiskInfoReturn]): Disk information
        network (Optional[NetworkInfoReturn]): Network information
        timestamp (Optional[float]): Timestamp when the information was collected
    """

    platform: Optional[PlatformInfoReturn] = Field(
        default=None,
        description="Platform basic information including OS, hostname, machine ID",
    )

    cpu: Optional[CPUInfoReturn] = Field(
        default=None,
        description="CPU information including cores, frequency, usage",
    )

    memory: Optional[MemoryInfoReturn] = Field(
        default=None,
        description="Memory information including RAM and swap usage",
    )

    disk: Optional[DiskInfoReturn] = Field(
        default=None,
        description="Disk information including partitions and I/O stats",
    )

    network: Optional[NetworkInfoReturn] = Field(
        default=None,
        description="Network information including IP addresses and speeds",
    )

    timestamp: Optional[float] = Field(
        default=None,
        description="Timestamp when the information was collected",
        ge=0.0,
    )
