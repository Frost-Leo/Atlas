#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants

This module provides constants for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/17
- Modified : 2025/9/17
- License  : GPL-3.0
"""

from pydantic import Field
from typing import List

from atlas.models.base import InternalBaseModel


class Constants(InternalBaseModel):
    """
    Constants: DeviceInfo's constant model

    Attributes:
        WINDOWS_MACHINE_GUID_REGISTRY_PATH (str): MachineGuid registry path in windows os
        WINDOWS_MACHINE_GUID_KEY_NAME (str): MachineGuid key name in registry
        LINUX_MACHINE_ID_FILE_PATH (str): Linux machine id file path
        LINUX_DBUS_MACHINE_ID_FILE_PATH (str): Linux dbus machine id file path
        MACOS_IOREG_COMMAND (List[str]): macOS ioreg command to get platform UUID
        MACOS_UUID_PATTERN (str): Regex pattern to extract IOPlatformUUID
    """

    WINDOWS_MACHINE_GUID_REGISTRY_PATH: str = Field(
        default=r"SOFTWARE\Microsoft\Cryptography",
        description="MachineGuid registry path in windows os",
    )

    WINDOWS_MACHINE_GUID_KEY_NAME: str = Field(
        default="MachineGuid",
        description="MachineGuid key name in registry",
    )

    LINUX_MACHINE_ID_FILE_PATH: str = Field(
        default="/etc/machine-id",
        description="Linux machine id file path",
    )

    LINUX_DBUS_MACHINE_ID_FILE_PATH: str = Field(
        default="/var/lib/dbus/machine-id",
        description="Linux DBus machine id file path",
    )

    MACOS_IOREG_COMMAND: List[str] = Field(
        default=["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
        description="macOS ioreg command to get platform UUID",
    )

    MACOS_UUID_PATTERN: str = Field(
        default=r'"IOPlatformUUID"\s*=\s*"([^"]+)"',
        description="Regex pattern to extract IOPlatformUUID",
    )
