#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_disk_info

This module provides disk information models for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

from pydantic import Field
from typing import List, Optional

from atlas.models.base import InternalBaseModel


class DiskPartitionInfo(InternalBaseModel):
    """
    DiskPartitionInfo: Information model for a single partition

    Attributes:
        device (Optional[str]): Device name (e.g., C:, /dev/sda1)
        mountpoint (Optional[str]): Mount point path
        fstype (Optional[str]): File system type (NTFS, ext4, etc.)
        total (Optional[int]): Total disk space in bytes
        used (Optional[int]): Used disk space in bytes
        free (Optional[int]): Free disk space in bytes
        percent (Optional[float]): Disk usage percentage (0-100)
    """

    device: Optional[str] = Field(
        default=None,
        description="Device name (e.g., C:, /dev/sda1)",
    )

    mountpoint: Optional[str] = Field(
        default=None,
        description="Mount point path",
    )

    fstype: Optional[str] = Field(
        default=None,
        description="File system type (NTFS, ext4, etc.)",
    )

    total: Optional[int] = Field(
        default=None,
        description="Total disk space in bytes",
        ge=0,
    )

    used: Optional[int] = Field(
        default=None,
        description="Used disk space in bytes",
        ge=0,
    )

    free: Optional[int] = Field(
        default=None,
        description="Free disk space in bytes",
        ge=0,
    )

    percent: Optional[float] = Field(
        default=None,
        description="Disk usage percentage (0-100)",
        ge=0.0,
        le=100.0,
    )


class DiskIOInfo(InternalBaseModel):
    """
    DiskIOInfo: Disk I/O Statistical Information Model

    Attributes:
        read_count (Optional[int]): Number of read operations
        write_count (Optional[int]): Number of write operations
        read_bytes (Optional[int]): Number of bytes read
        write_bytes (Optional[int]): Number of bytes written
        read_time (Optional[int]): Time spent reading in milliseconds
        write_time (Optional[int]): Time spent writing in milliseconds
        read_merged_count (Optional[int]): Number of merged read operations
        write_merged_count (Optional[int]): Number of merged write operations
        busy_time (Optional[int]): Time spent doing I/Os in milliseconds
    """

    read_count: Optional[int] = Field(
        default=None,
        description="Number of read operations",
        ge=0,
    )

    write_count: Optional[int] = Field(
        default=None,
        description="Number of write operations",
        ge=0,
    )

    read_bytes: Optional[int] = Field(
        default=None,
        description="Number of bytes read",
        ge=0,
    )

    write_bytes: Optional[int] = Field(
        default=None,
        description="Number of bytes written",
        ge=0,
    )

    read_time: Optional[int] = Field(
        default=None,
        description="Time spent reading in milliseconds",
        ge=0,
    )

    write_time: Optional[int] = Field(
        default=None,
        description="Time spent writing in milliseconds",
        ge=0,
    )

    read_merged_count: Optional[int] = Field(
        default=None,
        description="Number of merged read operations",
        ge=0,
    )

    write_merged_count: Optional[int] = Field(
        default=None,
        description="Number of merged write operations",
        ge=0,
    )

    busy_time: Optional[int] = Field(
        default=None,
        description="Time spent doing I/Os in milliseconds",
        ge=0,
    )


class DiskInfoReturn(InternalBaseModel):
    """
    DiskInfoReturn: DeviceInfo._disk_info parameter output model

    Attributes:
        partitions (Optional[List[DiskPartitionInfo]]): List of disk partitions
        total_disk_space (Optional[int]): Total disk space across all partitions in bytes
        total_used_space (Optional[int]): Total used space across all partitions in bytes
        total_free_space (Optional[int]): Total free space across all partitions in bytes
        io_stats (Optional[DiskIOInfo]): Disk I/O statistics
        average_usage_percent (Optional[float]): Average disk usage percentage across all partitions
    """

    partitions: Optional[List[DiskPartitionInfo]] = Field(
        default=None,
        description="List of disk partitions",
    )

    total_disk_space: Optional[int] = Field(
        default=None,
        description="Total disk space across all partitions in bytes",
        ge=0,
    )

    total_used_space: Optional[int] = Field(
        default=None,
        description="Total used space across all partitions in bytes",
        ge=0,
    )

    total_free_space: Optional[int] = Field(
        default=None,
        description="Total free space across all partitions in bytes",
        ge=0,
    )

    io_stats: Optional[DiskIOInfo] = Field(
        default=None,
        description="Disk I/O statistics",
    )

    average_usage_percent: Optional[float] = Field(
        default=None,
        description="Average disk usage percentage across all partitions (0-100)",
        ge=0.0,
        le=100.0,
    )
