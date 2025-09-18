#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fixtures

This module provides test fixtures for device information testing

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18 
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import pytest
import platform
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, Optional, Tuple

from atlas.core._infra.device_info import DeviceInfo
from atlas.models.domain._infra.device_info import models as device_info_models


@pytest.fixture
def device_info_instance():
    """
    Provide a fresh DeviceInfo instance for testing
    
    Note: Since DeviceInfo is a singleton, we need to reset it for each test
    """
    # Reset singleton instance
    DeviceInfo._instance = None
    return DeviceInfo()


@pytest.fixture
def mock_platform_info():
    """
    Provide mock platform information for testing
    """
    def _mock_platform_info(os_name: str = "windows") -> Dict[str, Any]:
        mock_data = {
            "windows": {
                "hostname": "test-windows",
                "machine_id": "12345678-1234-1234-1234-123456789012",
                "os_name": "windows",
                "os_version": "10.0.19045",
                "python_version": "3.13.0",
                "platform": "Windows-10-10.0.19045-SP0",
                "architecture": "AMD64",
                "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel",
                "boot_time": 1695000000.0,
                "uptime": 86400.0,
            },
            "linux": {
                "hostname": "test-linux",
                "machine_id": "abcdef1234567890abcdef1234567890",
                "os_name": "linux",
                "os_version": "5.15.0-91-generic",
                "python_version": "3.13.0",
                "platform": "Linux-5.15.0-91-generic-x86_64-with-glibc2.35",
                "architecture": "x86_64",
                "processor": "x86_64",
                "boot_time": 1695100000.0,
                "uptime": 43200.0,
            },
            "darwin": {
                "hostname": "test-macos",
                "machine_id": "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE",
                "os_name": "darwin",
                "os_version": "22.6.0",
                "python_version": "3.13.0",
                "platform": "macOS-13.5.2-arm64-arm-64bit",
                "architecture": "arm64",
                "processor": "arm",
                "boot_time": 1695200000.0,
                "uptime": 21600.0,
            }
        }
        return mock_data.get(os_name, mock_data["windows"])
    
    return _mock_platform_info


@pytest.fixture
def mock_cpu_info():
    """
    Provide mock CPU information for testing
    """
    return {
        "brand_raw": "Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz",
        "vendor_id_raw": "GenuineIntel",
        "arch": "X86_64",
        "bits": 64,
        "physical_cores": 4,
        "logical_cores": 8,
        "current_freq": 1800.0,
        "min_freq": 400.0,
        "max_freq": 4600.0,
        "base_freq": 1800.0,
        "cpu_usage": 25.5,
        "l_two_cache_size": 1048576,
        "l_three_cache_size": 8388608,
        "family": 6,
        "model": 142,
        "stepping": 12,
        "flags": ["fpu", "vme", "de", "pse", "tsc", "msr", "pae"],
    }


@pytest.fixture
def mock_memory_info():
    """
    Provide mock memory information for testing
    """
    return {
        "total": 17179869184,  # 16 GB
        "available": 8589934592,  # 8 GB
        "percent": 50.0,
        "used": 8589934592,  # 8 GB
        "free": 8589934592,  # 8 GB
        "swap_total": 4294967296,  # 4 GB
        "swap_used": 1073741824,  # 1 GB
        "swap_percent": 25.0,
        "swap_free": 3221225472,  # 3 GB
        "buffers": 536870912,  # 512 MB
        "cached": 1073741824,  # 1 GB
        "shared": 268435456,  # 256 MB
    }


@pytest.fixture
def mock_disk_info():
    """
    Provide mock disk information for testing
    """
    return {
        "partitions": [
            {
                "device": "C:",
                "mountpoint": "C:",
                "fstype": "NTFS",
                "total": 536870912000,  # 500 GB
                "used": 268435456000,  # 250 GB
                "free": 268435456000,  # 250 GB
                "percent": 50.0,
            }
        ],
        "total_disk_space": 536870912000,
        "total_used_space": 268435456000,
        "total_free_space": 268435456000,
        "average_usage_percent": 50.0,
        "io_stats": {
            "read_count": 1000000,
            "write_count": 500000,
            "read_bytes": 10737418240,  # 10 GB
            "write_bytes": 5368709120,  # 5 GB
            "read_time": 5000,
            "write_time": 3000,
            "read_merged_count": 50000,
            "write_merged_count": 25000,
            "busy_time": 8000,
        },
    }


@pytest.fixture
def mock_network_info():
    """
    Provide mock network information for testing
    """
    return {
        "public_ip": "203.0.113.42",
        "local_ip": "192.168.1.100",
        "mac_address": "00:11:22:33:44:55",
        "hostname": "test-machine",
        "interface_speed": 1000,  # 1Gbps
        "total_bytes_sent": 1073741824,  # 1 GB
        "total_bytes_recv": 2147483648,  # 2 GB
        "interface_name": "Ethernet",
        "download_speed": 50.5,  # Mbps
        "upload_speed": 25.2,  # Mbps
        "ping": 15.5,  # ms
    }


@pytest.fixture
def mock_psutil():
    """
    Provide mock psutil module for testing
    """
    mock_psutil = MagicMock()
    
    # Mock virtual memory
    mock_vm = MagicMock()
    mock_vm.total = 17179869184
    mock_vm.available = 8589934592
    mock_vm.percent = 50.0
    mock_vm.used = 8589934592
    mock_vm.free = 8589934592
    mock_vm.buffers = 536870912
    mock_vm.cached = 1073741824
    mock_vm.shared = 268435456
    mock_psutil.virtual_memory.return_value = mock_vm
    
    # Mock swap memory
    mock_swap = MagicMock()
    mock_swap.total = 4294967296
    mock_swap.used = 1073741824
    mock_swap.percent = 25.0
    mock_swap.free = 3221225472
    mock_psutil.swap_memory.return_value = mock_swap
    
    # Mock CPU info
    mock_freq = MagicMock()
    mock_freq.current = 1800.0
    mock_freq.min = 400.0
    mock_freq.max = 4600.0
    mock_psutil.cpu_freq.return_value = mock_freq
    mock_psutil.cpu_count.return_value = 8
    mock_psutil.cpu_percent.return_value = 25.5
    
    # Mock boot time
    mock_psutil.boot_time.return_value = 1695000000.0
    
    # Mock disk partitions
    mock_partition = MagicMock()
    mock_partition.device = "C:"
    mock_partition.mountpoint = "C:"
    mock_partition.fstype = "NTFS"
    mock_psutil.disk_partitions.return_value = [mock_partition]
    
    # Mock disk usage
    mock_usage = MagicMock()
    mock_usage.total = 536870912000
    mock_usage.used = 268435456000
    mock_usage.free = 268435456000
    mock_psutil.disk_usage.return_value = mock_usage
    
    # Mock disk I/O
    mock_io = MagicMock()
    mock_io.read_count = 1000000
    mock_io.write_count = 500000
    mock_io.read_bytes = 10737418240
    mock_io.write_bytes = 5368709120
    mock_io.read_time = 5000
    mock_io.write_time = 3000
    mock_io.read_merged_count = 50000
    mock_io.write_merged_count = 25000
    mock_io.busy_time = 8000
    mock_psutil.disk_io_counters.return_value = mock_io
    
    # Mock network interfaces
    mock_addr = MagicMock()
    mock_addr.family = 2  # AF_INET
    mock_addr.address = "192.168.1.100"
    
    mock_link_addr = MagicMock()
    mock_link_addr.family = -1  # AF_LINK (psutil.AF_LINK)
    mock_link_addr.address = "00:11:22:33:44:55"
    
    mock_psutil.net_if_addrs.return_value = {
        "Ethernet": [mock_addr, mock_link_addr]
    }
    
    # Mock network interface stats
    mock_stats = MagicMock()
    mock_stats.isup = True
    mock_stats.speed = 1000
    mock_psutil.net_if_stats.return_value = {"Ethernet": mock_stats}
    
    # Mock network I/O counters
    mock_net_io = MagicMock()
    mock_net_io.bytes_sent = 1073741824
    mock_net_io.bytes_recv = 2147483648
    mock_psutil.net_io_counters.return_value = mock_net_io
    
    # Set AF_LINK constant
    mock_psutil.AF_LINK = -1
    
    return mock_psutil


@pytest.fixture
def mock_cpuinfo():
    """
    Provide mock cpuinfo module for testing
    """
    return {
        "brand_raw": "Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz",
        "vendor_id_raw": "GenuineIntel",
        "arch": "X86_64",
        "bits": 64,
        "count": 8,
        "hz_advertised": [1800000000, "1.8000 GHz"],
        "l2_cache_size": 1048576,
        "l3_cache_size": 8388608,
        "family": 6,
        "model": 142,
        "stepping": 12,
        "flags": ["fpu", "vme", "de", "pse", "tsc", "msr", "pae"],
    }


@pytest.fixture
def mock_socket():
    """
    Provide mock socket module for testing
    """
    mock_socket = MagicMock()
    mock_socket.gethostname.return_value = "test-machine"
    mock_socket.AF_INET = 2
    return mock_socket


@pytest.fixture
def mock_platform():
    """
    Provide mock platform module for testing
    """
    mock_platform = MagicMock()
    mock_platform.system.return_value = "Windows"
    mock_platform.version.return_value = "10.0.19045"
    mock_platform.python_version.return_value = "3.13.0"
    mock_platform.platform.return_value = "Windows-10-10.0.19045-SP0"
    mock_platform.machine.return_value = "AMD64"
    mock_platform.processor.return_value = "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel"
    return mock_platform


@pytest.fixture
def mock_time():
    """
    Provide mock time module for testing
    """
    mock_time = MagicMock()
    mock_time.time.return_value = 1695086400.0
    mock_time.sleep = MagicMock()  # Mock sleep to avoid actual delays
    return mock_time


@pytest.fixture
def mock_subprocess():
    """
    Provide mock subprocess module for testing
    """
    mock_subprocess = MagicMock()
    
    # Mock successful subprocess run
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "203.0.113.42"
    mock_subprocess.run.return_value = mock_result
    
    return mock_subprocess


@pytest.fixture
def mock_winreg():
    """
    Provide mock winreg module for testing Windows registry operations
    """
    mock_winreg = MagicMock()
    
    # Mock registry key context manager
    mock_key = MagicMock()
    mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key
    mock_winreg.OpenKey.return_value.__exit__.return_value = None
    
    # Mock registry query
    mock_winreg.QueryValueEx.return_value = ("12345678-1234-1234-1234-123456789012", 1)
    
    # Mock registry constants
    mock_winreg.HKEY_LOCAL_MACHINE = -2147483646
    
    return mock_winreg


@pytest.fixture
def mock_file_operations():
    """
    Provide mock file operations for testing Linux machine ID reading
    """
    def _mock_open(file_path: str, mode: str = "r"):
        mock_file = MagicMock()
        
        if "/etc/machine-id" in file_path:
            mock_file.read.return_value = "abcdef1234567890abcdef1234567890\n"
        elif "/var/lib/dbus/machine-id" in file_path:
            mock_file.read.return_value = "fedcba0987654321fedcba0987654321\n"
        else:
            raise FileNotFoundError(f"No such file: {file_path}")
        
        mock_file.strip = lambda: mock_file.read().strip()
        
        # Context manager support
        mock_file.__enter__ = lambda self: mock_file
        mock_file.__exit__ = lambda self, *args: None
        
        return mock_file
    
    return _mock_open


@pytest.fixture
def comprehensive_device_info_mock(
    mock_psutil,
    mock_cpuinfo,
    mock_socket,
    mock_platform,
    mock_time,
    mock_subprocess,
    mock_winreg,
    mock_file_operations
):
    """
    Provide comprehensive mocking for all DeviceInfo dependencies
    """
    patches = []
    
    # Apply all patches
    patches.append(patch('atlas.core._infra.device_info.psutil', mock_psutil))
    patches.append(patch('atlas.core._infra.device_info.cpuinfo.get_cpu_info', lambda: mock_cpuinfo))
    patches.append(patch('atlas.core._infra.device_info.socket', mock_socket))
    patches.append(patch('atlas.core._infra.device_info.platform', mock_platform))
    patches.append(patch('atlas.core._infra.device_info.time', mock_time))
    patches.append(patch('atlas.core._infra.device_info.subprocess', mock_subprocess))
    patches.append(patch('atlas.core._infra.device_info.winreg', mock_winreg))
    patches.append(patch('builtins.open', mock_file_operations))
    
    # Start all patches
    for patch_obj in patches:
        patch_obj.start()
    
    yield
    
    # Stop all patches
    for patch_obj in patches:
        patch_obj.stop()


__all__ = [
    "device_info_instance",
    "mock_platform_info",
    "mock_cpu_info",
    "mock_memory_info",
    "mock_disk_info",
    "mock_network_info",
    "mock_psutil",
    "mock_cpuinfo",
    "mock_socket",
    "mock_platform",
    "mock_time",
    "mock_subprocess",
    "mock_winreg",
    "mock_file_operations",
    "comprehensive_device_info_mock",
]
