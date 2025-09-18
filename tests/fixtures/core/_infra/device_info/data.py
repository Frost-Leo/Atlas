#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data

This module provides test data for device information testing

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18 
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import platform
from typing import List, Tuple, Any, Dict, Optional


class DeviceInfoTestData:
    """
    DeviceInfoTestData: Test data for device information testing
    
    Attributes:
        TEST_PLATFORM_INFO_VALID: Valid platform information test cases
        TEST_CPU_INFO_VALID: Valid CPU information test cases
        TEST_MEMORY_INFO_VALID: Valid memory information test cases
        TEST_DISK_INFO_VALID: Valid disk information test cases
        TEST_NETWORK_INFO_VALID: Valid network information test cases
        TEST_GET_DEVICE_INFO_PARAMS: GetDeviceInfo parameter test cases
    """

    # Platform information test data
    TEST_PLATFORM_INFO_VALID: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (
            {
                "hostname": "test-machine",
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
            {
                "hostname": "test-machine",
                "machine_id": "12345678-1234-1234-1234-123456789012",
                "os_name": "windows",
                "os_version": "10.0.19045",
                "python_version": "3.13.0",
                "platform": "Windows-10-10.0.19045-SP0",
                "architecture": "AMD64",
                "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel",
                "boot_time": 1695000000.0,
                "uptime": 86400.0,
            }
        ),
        (
            {
                "hostname": "ubuntu-server",
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
            {
                "hostname": "ubuntu-server",
                "machine_id": "abcdef1234567890abcdef1234567890",
                "os_name": "linux",
                "os_version": "5.15.0-91-generic",
                "python_version": "3.13.0",
                "platform": "Linux-5.15.0-91-generic-x86_64-with-glibc2.35",
                "architecture": "x86_64",
                "processor": "x86_64",
                "boot_time": 1695100000.0,
                "uptime": 43200.0,
            }
        ),
    ]

    # CPU information test data
    TEST_CPU_INFO_VALID: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (
            {
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
            },
            {
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
        ),
        (
            {
                "brand_raw": "AMD Ryzen 7 5800X 8-Core Processor",
                "vendor_id_raw": "AuthenticAMD",
                "arch": "X86_64",
                "bits": 64,
                "physical_cores": 8,
                "logical_cores": 16,
                "current_freq": 3800.0,
                "min_freq": 2200.0,
                "max_freq": 4700.0,
                "base_freq": 3800.0,
                "cpu_usage": 15.2,
                "l_two_cache_size": 4194304,
                "l_three_cache_size": 33554432,
                "family": 25,
                "model": 33,
                "stepping": 0,
                "flags": ["fpu", "vme", "de", "pse", "tsc", "msr", "pae", "avx2"],
            },
            {
                "brand_raw": "AMD Ryzen 7 5800X 8-Core Processor",
                "vendor_id_raw": "AuthenticAMD",
                "arch": "X86_64",
                "bits": 64,
                "physical_cores": 8,
                "logical_cores": 16,
                "current_freq": 3800.0,
                "min_freq": 2200.0,
                "max_freq": 4700.0,
                "base_freq": 3800.0,
                "cpu_usage": 15.2,
                "l_two_cache_size": 4194304,
                "l_three_cache_size": 33554432,
                "family": 25,
                "model": 33,
                "stepping": 0,
                "flags": ["fpu", "vme", "de", "pse", "tsc", "msr", "pae", "avx2"],
            }
        ),
    ]

    # Memory information test data
    TEST_MEMORY_INFO_VALID: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (
            {
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
            },
            {
                "total": 17179869184,
                "available": 8589934592,
                "percent": 50.0,
                "used": 8589934592,
                "free": 8589934592,
                "swap_total": 4294967296,
                "swap_used": 1073741824,
                "swap_percent": 25.0,
                "swap_free": 3221225472,
                "buffers": 536870912,
                "cached": 1073741824,
                "shared": 268435456,
            }
        ),
        (
            {
                "total": 34359738368,  # 32 GB
                "available": 25769803776,  # 24 GB
                "percent": 25.0,
                "used": 8589934592,  # 8 GB
                "free": 25769803776,  # 24 GB
                "swap_total": 8589934592,  # 8 GB
                "swap_used": 0,
                "swap_percent": 0.0,
                "swap_free": 8589934592,  # 8 GB
                "buffers": None,
                "cached": None,
                "shared": None,
            },
            {
                "total": 34359738368,
                "available": 25769803776,
                "percent": 25.0,
                "used": 8589934592,
                "free": 25769803776,
                "swap_total": 8589934592,
                "swap_used": 0,
                "swap_percent": 0.0,
                "swap_free": 8589934592,
                "buffers": None,
                "cached": None,
                "shared": None,
            }
        ),
    ]

    # Disk information test data
    TEST_DISK_INFO_VALID: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (
            {
                "partitions": [
                    {
                        "device": "C:",
                        "mountpoint": "C:",
                        "fstype": "NTFS",
                        "total": 536870912000,  # 500 GB
                        "used": 268435456000,  # 250 GB
                        "free": 268435456000,  # 250 GB
                        "percent": 50.0,
                    },
                    {
                        "device": "D:",
                        "mountpoint": "D:",
                        "fstype": "NTFS",
                        "total": 1073741824000,  # 1 TB
                        "used": 214748364800,  # 200 GB
                        "free": 858993459200,  # 800 GB
                        "percent": 20.0,
                    }
                ],
                "total_disk_space": 1610612736000,  # 1.5 TB
                "total_used_space": 483183820800,  # 450 GB
                "total_free_space": 1127428915200,  # 1.05 TB
                "average_usage_percent": 35.0,
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
            },
            {
                "partitions": [
                    {
                        "device": "C:",
                        "mountpoint": "C:",
                        "fstype": "NTFS",
                        "total": 536870912000,
                        "used": 268435456000,
                        "free": 268435456000,
                        "percent": 50.0,
                    },
                    {
                        "device": "D:",
                        "mountpoint": "D:",
                        "fstype": "NTFS",
                        "total": 1073741824000,
                        "used": 214748364800,
                        "free": 858993459200,
                        "percent": 20.0,
                    }
                ],
                "total_disk_space": 1610612736000,
                "total_used_space": 483183820800,
                "total_free_space": 1127428915200,
                "average_usage_percent": 35.0,
                "io_stats": {
                    "read_count": 1000000,
                    "write_count": 500000,
                    "read_bytes": 10737418240,
                    "write_bytes": 5368709120,
                    "read_time": 5000,
                    "write_time": 3000,
                    "read_merged_count": 50000,
                    "write_merged_count": 25000,
                    "busy_time": 8000,
                },
            }
        ),
    ]

    # Network information test data
    TEST_NETWORK_INFO_VALID: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (
            {
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
            },
            {
                "public_ip": "203.0.113.42",
                "local_ip": "192.168.1.100",
                "mac_address": "00:11:22:33:44:55",
                "hostname": "test-machine",
                "interface_speed": 1000,
                "total_bytes_sent": 1073741824,
                "total_bytes_recv": 2147483648,
                "interface_name": "Ethernet",
                "download_speed": 50.5,
                "upload_speed": 25.2,
                "ping": 15.5,
            }
        ),
        (
            {
                "public_ip": "198.51.100.123",
                "local_ip": "10.0.0.50",
                "mac_address": "aa:bb:cc:dd:ee:ff",
                "hostname": "ubuntu-server",
                "interface_speed": 100,  # 100Mbps
                "total_bytes_sent": 536870912,  # 512 MB
                "total_bytes_recv": 1073741824,  # 1 GB
                "interface_name": "eth0",
                "download_speed": 12.3,  # Mbps
                "upload_speed": 5.8,  # Mbps
                "ping": 8.2,  # ms
            },
            {
                "public_ip": "198.51.100.123",
                "local_ip": "10.0.0.50",
                "mac_address": "aa:bb:cc:dd:ee:ff",
                "hostname": "ubuntu-server",
                "interface_speed": 100,
                "total_bytes_sent": 536870912,
                "total_bytes_recv": 1073741824,
                "interface_name": "eth0",
                "download_speed": 12.3,
                "upload_speed": 5.8,
                "ping": 8.2,
            }
        ),
    ]

    # GetDeviceInfo parameter test data
    TEST_GET_DEVICE_INFO_PARAMS: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        # Test all parameters True
        (
            {
                "include_platform": True,
                "include_cpu": True,
                "include_memory": True,
                "include_disk": True,
                "include_network": True,
            },
            {
                "include_platform": True,
                "include_cpu": True,
                "include_memory": True,
                "include_disk": True,
                "include_network": True,
            }
        ),
        # Test all parameters False
        (
            {
                "include_platform": False,
                "include_cpu": False,
                "include_memory": False,
                "include_disk": False,
                "include_network": False,
            },
            {
                "include_platform": False,
                "include_cpu": False,
                "include_memory": False,
                "include_disk": False,
                "include_network": False,
            }
        ),
        # Test selective parameters
        (
            {
                "include_platform": True,
                "include_cpu": True,
                "include_memory": False,
                "include_disk": False,
                "include_network": True,
            },
            {
                "include_platform": True,
                "include_cpu": True,
                "include_memory": False,
                "include_disk": False,
                "include_network": True,
            }
        ),
        # Test default parameters (all True by default)
        (
            {},
            {
                "include_platform": True,
                "include_cpu": True,
                "include_memory": True,
                "include_disk": True,
                "include_network": True,
            }
        ),
    ]

    # Mock data for mocking external dependencies
    MOCK_PLATFORM_DATA = {
        "windows": {
            "system": "Windows",
            "version": "10.0.19045",
            "platform": "Windows-10-10.0.19045-SP0",
            "machine": "AMD64",
            "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel",
            "python_version": "3.13.0",
        },
        "linux": {
            "system": "Linux",
            "version": "5.15.0-91-generic",
            "platform": "Linux-5.15.0-91-generic-x86_64-with-glibc2.35",
            "machine": "x86_64",
            "processor": "x86_64",
            "python_version": "3.13.0",
        },
        "darwin": {
            "system": "Darwin",
            "version": "22.6.0",
            "platform": "macOS-13.5.2-arm64-arm-64bit",
            "machine": "arm64",
            "processor": "arm",
            "python_version": "3.13.0",
        },
    }

    # Error test cases
    TEST_ERROR_SCENARIOS: List[Tuple[str, str, Any]] = [
        ("platform_error", "Failed to get platform info", RuntimeError("Mock platform error")),
        ("cpu_error", "Failed to obtain CPU information", RuntimeError("Mock CPU error")),
        ("memory_error", "Failed to get memory info", RuntimeError("Mock memory error")),
        ("disk_error", "Failed to get disk info", RuntimeError("Mock disk error")),
        ("network_error", "Failed to get network info", RuntimeError("Mock network error")),
    ]

    # Singleton test data
    TEST_SINGLETON_SCENARIOS: List[Tuple[str, int]] = [
        ("single_thread", 1),
        ("multi_thread_5", 5),
        ("multi_thread_10", 10),
        ("multi_thread_20", 20),
    ]
