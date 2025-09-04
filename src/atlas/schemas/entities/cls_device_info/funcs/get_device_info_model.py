#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_device_info_model

This module provides Pydantic models for device information retrieval,
including hardware and software specifications.

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/4
- Modified : 2025/9/4
- License  : GPL-3.0
"""

from pydantic import Field
from datetime import datetime
from typing import List, Optional

from atlas.schemas.base import BaseSchema


class GetDeviceInfoParams(BaseSchema):
    """
    GetDeviceInfoParams: The input parameter model for the get_device_info() function.

    Attributes:
        include_hardware (bool): Whether to include hardware information. Defaults to True.
        include_software (bool): Whether to include software information. Defaults to True.
    """

    include_hardware: bool = Field(default=True, description="Whether to include hardware information")
    include_software: bool = Field(default=True, description="Whether to include software information")


class CPUInfo(BaseSchema):
    """
    CPUInfo: The CPU information model.

    Attributes:
        brand (Optional[str]): CPU brand and model.
        architecture (Optional[str]): CPU architecture type.
        physical_cores (Optional[int]): Number of physical CPU cores.
        logical_cores (Optional[int]): Number of logical CPU cores including hyperthreading.
        count (Optional[int]): Total number of CPU processors.
        max_frequency (Optional[float]): Maximum frequency in MHz.
        min_frequency (Optional[float]): Minimum frequency in MHz.
        cpu_percent (Optional[float]): Current CPU usage percentage.
    """

    brand: Optional[str] = Field(default="Unknown brand", description="CPU brand and model")
    architecture: Optional[str] = Field(default="Unknown architecture", description="CPU architecture (x86_64, ARM64, etc.)")
    physical_cores: Optional[int] = Field(default=None, description="Number of physical CPU cores")
    logical_cores: Optional[int] = Field(default=None, description="Number of logical CPU cores (including hyperthreading)")
    count: Optional[int] = Field(default=None, description="Total number of CPU processors")
    max_frequency: Optional[float] = Field(default=None, description="Maximum CPU frequency in MHz")
    min_frequency: Optional[float] = Field(default=None, description="Minimum CPU frequency in MHz")
    cpu_percent: Optional[float] = Field(default=None, description="Current CPU usage percentage (0-100)")


class MemoryInfo(BaseSchema):
    """
    MemoryInfo: The memory information model.

    Attributes:
        total (Optional[float]): Total physical memory in GB.
        available (Optional[float]): Available physical memory in GB.
        used (Optional[float]): Used physical memory in GB.
        percent (Optional[float]): Memory usage percentage.
        swap_total (Optional[float]): Total swap space in GB.
        swap_used (Optional[float]): Used swap space in GB.
        swap_percent (Optional[float]): Swap usage percentage.
        process_memory_rss (Optional[float]): Current process resident memory in MB.
        process_memory_percent (Optional[float]): Current process memory usage percentage.
    """

    total: Optional[float] = Field(default=None, description="Total physical memory in GB")
    available: Optional[float] = Field(default=None, description="Available physical memory in GB")
    used: Optional[float] = Field(default=None, description="Used physical memory in GB")
    percent: Optional[float] = Field(default=None, description="Memory usage percentage (0-100)")
    swap_total: Optional[float] = Field(default=None, description="Total swap space in GB")
    swap_used: Optional[float] = Field(default=None, description="Used swap space in GB")
    swap_percent: Optional[float] = Field(default=None, description="Swap usage percentage (0-100)")
    process_memory_rss: Optional[float] = Field(default=None, description="Current process resident memory in MB")
    process_memory_percent: Optional[float] = Field(default=None, description="Current process memory usage percentage (0-100)")


class DiskInfo(BaseSchema):
    """
    DiskInfo: The disk information model.

    Attributes:
        device (Optional[str]): Device name (e.g., "/dev/sda1", "C:\\").
        mountpoint (Optional[str]): Mount point (e.g., "/", "/home", "C:\\").
        fstype (Optional[str]): File system type (e.g., "ext4", "NTFS", "APFS").
        total (Optional[float]): Total disk capacity in GB.
        used (Optional[float]): Used disk capacity in GB.
        free (Optional[float]): Free disk capacity in GB.
        percent (Optional[float]): Disk usage percentage.
    """

    device: Optional[str] = Field(default=None, description="Device name (e.g., '/dev/sda1', 'C:\\')")
    mountpoint: Optional[str] = Field(default=None, description="Mount point (e.g., '/', '/home', 'C:\\')")
    fstype: Optional[str] = Field(default=None, description="File system type (e.g., 'ext4', 'NTFS', 'APFS')")
    total: Optional[float] = Field(default=None, description="Total disk capacity in GB")
    used: Optional[float] = Field(default=None, description="Used disk capacity in GB")
    free: Optional[float] = Field(default=None, description="Free disk capacity in GB")
    percent: Optional[float] = Field(default=None, description="Disk usage percentage (0-100)")


class NetworkInterfaceInfo(BaseSchema):
    """
    NetworkInterfaceInfo: The network interface information model.

    Attributes:
        name (Optional[str]): Network interface name.
        ip_addresses (Optional[List[str]]): List of IP addresses (local).
        mac_address (Optional[str]): MAC address of the interface.
        speed (Optional[int]): Interface speed in Mbps.
        is_up (Optional[bool]): Whether the interface is up and running.
        public_ip (Optional[str]): Public IP address (if available).
    """

    name: Optional[str] = Field(default=None, description="Network interface name (e.g., 'eth0', 'Wi-Fi')")
    ip_addresses: Optional[List[str]] = Field(default_factory=list, description="List of local IP addresses")
    mac_address: Optional[str] = Field(default=None, description="MAC address of the interface")
    speed: Optional[int] = Field(default=None, description="Interface speed in Mbps")
    is_up: Optional[bool] = Field(default=None, description="Whether the interface is up and running")
    public_ip: Optional[str] = Field(default=None, description="Public IP address (if detectable)")


class HardwareInfo(BaseSchema):
    """
    HardwareInfo: The complete hardware information model.

    Attributes:
        cpu (Optional[CPUInfo]): CPU information.
        memory (Optional[MemoryInfo]): Memory information.
        disks (Optional[List[DiskInfo]]): List of disk information.
        network_interfaces (Optional[List[NetworkInterfaceInfo]]): List of network interfaces.
    """

    cpu: Optional[CPUInfo] = Field(default=None, description="CPU information")
    memory: Optional[MemoryInfo] = Field(default=None, description="Memory information")
    disks: Optional[List[DiskInfo]] = Field(default_factory=list, description="List of disk information")
    network_interfaces: Optional[List[NetworkInterfaceInfo]] = Field(default_factory=list, description="List of network interfaces")


class OSInfo(BaseSchema):
    """
    OSInfo: The operating system information model.

    Attributes:
        system (Optional[str]): System type (Windows, Linux, Darwin).
        release (Optional[str]): System release version.
        platform (Optional[str]): Complete platform description.
        hostname (Optional[str]): System hostname.
        uptime (Optional[int]): System uptime in seconds.
        machine (Optional[str]): Machine type (AMD64, x86_64, etc.).
        bit_architecture (Optional[str]): System architecture (32-bit/64-bit).
    """

    system: Optional[str] = Field(default=None, description="System type (Windows, Linux, Darwin)")
    release: Optional[str] = Field(default=None, description="System release version")
    platform: Optional[str] = Field(default=None, description="Complete platform description")
    hostname: Optional[str] = Field(default=None, description="System hostname")
    uptime: Optional[int] = Field(default=None, description="System uptime in seconds")
    machine: Optional[str] = Field(default=None, description="Machine type (AMD64, x86_64, etc.)")
    bit_architecture: Optional[str] = Field(default=None, description="System architecture (32-bit/64-bit)")


class PythonInfo(BaseSchema):
    """
    PythonInfo: The Python environment information model.

    Attributes:
        version (Optional[str]): Python version.
        implementation (Optional[str]): Python implementation (CPython, PyPy, etc.).
        executable (Optional[str]): Python executable file path.
        compiler (Optional[str]): Compiler information.
    """

    version: Optional[str] = Field(default=None, description="Python version (e.g., '3.9.7')")
    implementation: Optional[str] = Field(default=None, description="Python implementation (CPython, PyPy, Jython, etc.)")
    executable: Optional[str] = Field(default=None, description="Python executable file path")
    compiler: Optional[str] = Field(default=None, description="Compiler information used to build Python")


class ProcessInfo(BaseSchema):
    """
    ProcessInfo: The current process information model.

    Attributes:
        pid (Optional[int]): Process ID.
        name (Optional[str]): Process name.
        create_time (Optional[str]): Process creation time.
        memory_usage (Optional[int]): Memory usage in bytes (RSS).
        memory_percent (Optional[float]): Memory usage percentage.
        cpu_percent (Optional[float]): CPU usage percentage.
        num_threads (Optional[int]): Number of threads.
        num_handles (Optional[int]): Number of handles (Windows) or file descriptors (Unix).
        connections (Optional[int]): Number of network connections.
    """

    pid: Optional[int] = Field(default=None, description="Process ID")
    name: Optional[str] = Field(default=None, description="Process name")
    create_time: Optional[str] = Field(default=None, description="Process creation time (ISO format)")
    memory_usage: Optional[int] = Field(default=None, description="Memory usage in bytes (RSS)")
    memory_percent: Optional[float] = Field(default=None, description="Memory usage percentage (0-100)")
    cpu_percent: Optional[float] = Field(default=None, description="CPU usage percentage (0-100)")
    num_threads: Optional[int] = Field(default=None, description="Number of threads")
    num_handles: Optional[int] = Field(default=None, description="Number of handles (Windows) or file descriptors (Unix)")
    connections: Optional[int] = Field(default=None, description="Number of network connections")


class SystemIdentifiers(BaseSchema):
    """
    SystemIdentifiers: The system identifiers information model.

    Attributes:
        machine_id (Optional[str]): Machine unique ID.
        hostname (Optional[str]): System hostname.
        uuid (Optional[str]): Hardware UUID.
        mac_address (Optional[str]): Primary network interface MAC address.
    """

    machine_id: Optional[str] = Field(default=None, description="Machine unique ID")
    hostname: Optional[str] = Field(default=None, description="System hostname")
    uuid: Optional[str] = Field(default=None, description="Hardware UUID (from DMI/SMBIOS)")
    mac_address: Optional[str] = Field(default=None, description="Primary network interface MAC address")


class SoftwareInfo(BaseSchema):
    """
    SoftwareInfo: The complete software information model.

    Attributes:
        os (Optional[OSInfo]): Operating system information.
        python (Optional[PythonInfo]): Python environment information.
        process (Optional[ProcessInfo]): Current process information.
        identifiers (Optional[SystemIdentifiers]): System unique identifiers.
    """

    os: Optional[OSInfo] = Field(default=None, description="Operating system information")
    python: Optional[PythonInfo] = Field(default=None, description="Python environment information")
    process: Optional[ProcessInfo] = Field(default=None, description="Current process information")
    identifiers: Optional[SystemIdentifiers] = Field(default=None, description="System unique identifiers")


class GetDeviceInfoReturn(BaseSchema):
    """
    GetDeviceInfoReturn: The return value for the get_device_info() function.

    Attributes:
        hardware_info (Optional[HardwareInfo]): Hardware information (optional based on request).
        software_info (Optional[SoftwareInfo]): Software information (optional based on request).
        timestamp (datetime): Timestamp when the information was collected.
        collection_duration (float): Time taken to collect the information in seconds.
        service_name (Optional[str]): Name of the service (optional).
        service_version (Optional[str]): Version of the service (optional).
    """

    service_name: Optional[str] = Field(default=None, description="Service name")
    service_version: Optional[str] = Field(default=None, description="Service version")
    hardware_info: Optional[HardwareInfo] = Field(default=None, description="Hardware information")
    software_info: Optional[SoftwareInfo] = Field(default=None, description="Software information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Information collection timestamp")
    collection_duration: float = Field(default=0.0, description="Collection duration in seconds")
