#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_network_info

This module provides network information models for device information collection

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

from pydantic import Field
from typing import Optional

from atlas.models.base import InternalBaseModel


class NetworkInfoReturn(InternalBaseModel):
    """
    NetworkInfoReturn: DeviceInfo._network_info parameter output model

    Attributes:
        public_ip (Optional[str]): Public IP address
        local_ip (Optional[str]): Local/Private IP address
        mac_address (Optional[str]): Primary network interface MAC address
        hostname (Optional[str]): System hostname
        interface_speed (Optional[int]): Network interface speed in Mbps (e.g., 1000 for gigabit)
        total_bytes_sent (Optional[int]): Total bytes sent since boot
        total_bytes_recv (Optional[int]): Total bytes received since boot
        interface_name (Optional[str]): Primary network interface name
        download_speed (Optional[float]): Actual download speed in Mbps from speed test
        upload_speed (Optional[float]): Actual upload speed in Mbps from speed test
        ping (Optional[float]): Network latency in milliseconds
    """

    public_ip: Optional[str] = Field(
        default=None,
        description="Public IP address",
    )

    local_ip: Optional[str] = Field(
        default=None,
        description="Local/Private IP address",
    )

    mac_address: Optional[str] = Field(
        default=None,
        description="Primary network interface MAC address",
    )

    hostname: Optional[str] = Field(
        default=None,
        description="System hostname",
    )

    interface_speed: Optional[int] = Field(
        default=None,
        description="Network interface speed in Mbps (e.g., 1000 for gigabit)",
        ge=0,
    )

    total_bytes_sent: Optional[int] = Field(
        default=None,
        description="Total bytes sent since boot",
        ge=0,
    )

    total_bytes_recv: Optional[int] = Field(
        default=None,
        description="Total bytes received since boot",
        ge=0,
    )

    interface_name: Optional[str] = Field(
        default=None,
        description="Primary network interface name",
    )

    download_speed: Optional[float] = Field(
        default=None,
        description="Actual download speed in Mbps from speed test",
        ge=0.0,
    )

    upload_speed: Optional[float] = Field(
        default=None,
        description="Actual upload speed in Mbps from speed test",
        ge=0.0,
    )

    ping: Optional[float] = Field(
        default=None,
        description="Network latency in milliseconds",
        ge=0.0,
    )
