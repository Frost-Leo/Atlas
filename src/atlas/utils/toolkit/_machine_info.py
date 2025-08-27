#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _machine_info
# @Created Time  : 2025/8/27 14:25
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_machine_info: Get basic information about the physical machine**

This module provides utility functions to retrieve machine-specific information
such as hostname and unique machine identifiers across different operating systems.
"""

import os
import winreg
import platform
import subprocess


class MachineInfo:
    """
    **MachineInfo: Cross-platform machine information retrieval class**

    Provides static methods to obtain machine-specific information including
    hostname and unique machine identifiers for Windows, Linux, and macOS systems.

    Class Attributes:
        - WIN_MACHINE_ID_REGISTRY_PATH: Windows registry path for machine GUID
        - LINUX_MECHINE_ID_FILE_PATH: Primary Linux machine ID file location
        - LINUX_DBUS_ID_FILE_PATH: Alternative Linux machine ID file location
        - UNKNOWN_ID: Default identifier when retrieval fails

    Class Methods:
        - get_machine_hostname: Retrieve the machine's network hostname
        - get_machine_id: Get a unique machine identifier for the current OS
    """

    WIN_MACHINE_ID_REGISTRY_PATH = r'SOFTWARE\Microsoft\Cryptography'
    """Windows registry path containing the MachineGuid value"""

    LINUX_MECHINE_ID_FILE_PATH = '/etc/machine-id'
    """Standard location for machine ID file in modern Linux distributions"""

    LINUX_DBUS_ID_FILE_PATH = '/var/lib/dbus/machine-id'
    """Alternative machine ID location used by D-Bus system"""

    UNKNOWN_ID = 'UNKNOWN_MACHINE_ID'
    """Fallback identifier returned when machine ID cannot be determined"""

    @staticmethod
    def get_machine_hostname() -> str:
        """
        **get_machine_hostname: Retrieve the machine's network hostname**

        Attempts to get the hostname using platform.node(). Falls back to 'localhost'
        if the operation fails.

        Returns:
            str: The machine's hostname or 'localhost' as fallback

        Example:
            >>> MachineInfo.get_machine_hostname()
            'my-computer'
        """
        try:
            return platform.node()
        except:
            return 'localhost'

    @staticmethod
    def get_machine_id() -> str:
        """
        **get_machine_id: Get a unique machine identifier**

        Determines the current operating system and retrieves a unique machine
        identifier using OS-specific methods.

        Returns:
            str: Unique machine identifier or UNKNOWN_ID if retrieval fails

        Supported Systems:
            - Windows: Retrieves MachineGuid from registry
            - Linux: Reads from /etc/machine-id or D-Bus machine ID
            - macOS: Extracts Hardware UUID from system profiler

        Example:
            >>> MachineInfo.get_machine_id()
            '12345678-1234-1234-1234-123456789012'
        """
        machine_os = platform.system().lower()

        if machine_os == 'windows':
            return MachineInfo._get_windows_machine_id()
        elif machine_os == 'linux':
            return MachineInfo._get_linux_machine_id()
        elif machine_os == 'darwin':
            return MachineInfo._get_macos_machine_id()
        else:
            return MachineInfo.UNKNOWN_ID

    @staticmethod
    def _get_windows_machine_id() -> str:
        """
        **_get_windows_machine_id: Retrieve Windows machine GUID**

        Accesses the Windows registry to read the MachineGuid value from
        the Cryptography key.

        Returns:
            str: Windows MachineGuid or UNKNOWN_ID if retrieval fails

        Note:
            Requires appropriate permissions to read from HKEY_LOCAL_MACHINE
        """
        if winreg is None:
            return MachineInfo.UNKNOWN_ID

        try:
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, MachineInfo.WIN_MACHINE_ID_REGISTRY_PATH)
            v, _ = winreg.QueryValueEx(k, 'MachineGuid')
            winreg.CloseKey(k)

            return v

        except:
            return MachineInfo.UNKNOWN_ID

    @staticmethod
    def _get_linux_machine_id() -> str:
        """
        **_get_linux_machine_id: Retrieve Linux machine ID**

        Attempts to read the machine ID from standard Linux locations.
        First tries /etc/machine-id, then falls back to the D-Bus machine ID.

        Returns:
            str: Linux machine ID or UNKNOWN_ID if files don't exist or can't be read

        Note:
            The machine ID is typically a 32-character hexadecimal string
        """
        try:
            if os.path.exists(MachineInfo.LINUX_MECHINE_ID_FILE_PATH):
                with open(MachineInfo.LINUX_MECHINE_ID_FILE_PATH, 'r') as f:
                    return f.read().strip()
            elif os.path.exists(MachineInfo.LINUX_DBUS_ID_FILE_PATH):
                with open(MachineInfo.LINUX_DBUS_ID_FILE_PATH, 'r') as f:
                    return f.read().strip()
        except:
            return MachineInfo.UNKNOWN_ID

    @staticmethod
    def _get_macos_machine_id() -> str:
        """
        **_get_macos_machine_id: Retrieve macOS Hardware UUID**

        Uses the system_profiler command to extract the Hardware UUID
        from the system hardware information.

        Returns:
            str: macOS Hardware UUID or UNKNOWN_ID if retrieval fails

        Note:
            Executes system_profiler subprocess with a 10-second timeout
            to prevent hanging on slow systems
        """
        try:
            result = subprocess.run(
                ['system_profiler', 'SPHardwareDataType'],
                capture_output=True,
                text=True,
                timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'Hardware UUID' in line:
                    return line.split(':')[1].strip()
        except:
            pass
        return MachineInfo.UNKNOWN_ID