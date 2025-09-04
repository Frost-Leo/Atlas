#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
models

This module provides device information models for the Atlas project.

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/4
- Modified : 2025/9/4
- License  : GPL-3.0
"""

from atlas.schemas.entities.cls_device_info.funcs.get_device_info_model import (
    CPUInfo,
    MemoryInfo,
    DiskInfo,
    NetworkInterfaceInfo,
    HardwareInfo,
    OSInfo,
    PythonInfo,
    ProcessInfo,
    SystemIdentifiers,
    SoftwareInfo,
    GetDeviceInfoParams,
    GetDeviceInfoReturn,
)

__all__ = [
    "CPUInfo",
    "MemoryInfo",
    "DiskInfo",
    "NetworkInterfaceInfo",
    "HardwareInfo",
    "OSInfo",
    "PythonInfo",
    "ProcessInfo",
    "SystemIdentifiers",
    "SoftwareInfo",
    "GetDeviceInfoParams",
    "GetDeviceInfoReturn"
]