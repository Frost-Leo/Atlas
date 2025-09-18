#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
device_info

This module provides information about the running physical machine

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/17
- Modified : 2025/9/17
- License  : GPL-3.0
"""

import re
import time
import winreg
import socket
import psutil
import cpuinfo
import platform
import threading
import subprocess
import shutil
from typing import Optional

from atlas.models.domain._infra.device_info import models as device_info_models


class DeviceInfo:
    """
    DeviceInfo: Equipment basic information provision category

    Attributes:
        _lock (threading.Lock()): Thread lock
        _instance (Optional[DeviceInfo]): DeviceInfo instance, default is None
        _constants (device_info_models.Constants()): DeviceInfo constants
    """

    _lock = threading.Lock()
    _instance: Optional["DeviceInfo"] = None
    _constants = device_info_models.Constants()

    def __new__(cls, *args, **kwargs) -> "DeviceInfo":
        """
        __new__: Singleton implementation method
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_device_info(
        self,
        params: Optional[device_info_models.GetDeviceInfoParams] = None
    ) -> device_info_models.GetDeviceInfoReturn:
        """
        get_device_info: Get device information based on parameters

        Args:
            params: Parameters specifying which information to include

        Returns:
            device_info_models.GetDeviceInfoReturn: Requested device information

        Raises:
            RuntimeError: If failed to get device information
        """
        if params is None:
            params = device_info_models.GetDeviceInfoParams()

        result = device_info_models.GetDeviceInfoReturn()
        result.timestamp = time.time()

        try:
            if params.include_platform:
                result.platform = self._platform_info()

            if params.include_cpu:
                result.cpu = self._cpu_info()

            if params.include_memory:
                result.memory = self._memory_info()

            if params.include_disk:
                result.disk = self._disk_info()

            if params.include_network:
                result.network = self._network_info()

            return result

        except Exception as e:
            raise RuntimeError(f"Failed to get device information: {e}") from e

    def _platform_info(self) -> device_info_models.PlatformInfoReturn:
        """
        _platform_info: Get some basic information about the physical machine

        Returns:
            device_info_models.PlatformInfoReturn: Platform basic information model

        Raises:
            RuntimeError: If the information is failed
        """
        try:
            hostname = socket.gethostname()
            os_name = platform.system().lower()
            os_version = platform.version()
            python_version = platform.python_version()
            machine_id = None

            if os_name == "windows":
                try:
                    with winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        self._constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH
                    ) as key:
                        machine_id = winreg.QueryValueEx(
                            key,
                            self._constants.WINDOWS_MACHINE_GUID_KEY_NAME
                        )[0]
                except Exception:
                    pass

            elif os_name == "linux":
                try:
                    with open(self._constants.LINUX_MACHINE_ID_FILE_PATH, "r") as file:
                        machine_id = file.read().strip()
                except FileNotFoundError:
                    try:
                        with open(self._constants.LINUX_DBUS_MACHINE_ID_FILE_PATH, "r") as file:
                            machine_id = file.read().strip()
                    except Exception:
                        pass

            elif os_name == "darwin":
                try:
                    result = subprocess.run(
                        self._constants.MACOS_IOREG_COMMAND,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    match = re.search(self._constants.MACOS_UUID_PATTERN, result.stdout)
                    if match:
                        machine_id = match.group(1)

                except Exception:
                    pass

            return device_info_models.PlatformInfoReturn(
                hostname=hostname,
                machine_id=machine_id,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                platform=platform.platform(),
                architecture=platform.machine(),
                processor=platform.processor(),
                boot_time=psutil.boot_time(),
                uptime=time.time() - psutil.boot_time(),
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get platform info: {e}")

    def _cpu_info(self) -> device_info_models.CPUInfoReturn:
        """
        _cpu_info: Function to obtain the CPU information of the device

        Returns:
            device_info_models.CPUInfoReturn: CPUInfoReturn

        Raises:
            RuntimeError: If failed to obtain CPU information
        """
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_info = cpuinfo.get_cpu_info()
            cpu_usage = psutil.cpu_percent(interval=0.1)
            physical_cores = psutil.cpu_count(logical=False)

            base_freq = None
            if "hz_advertised" in cpu_info and cpu_info["hz_advertised"]:
                base_freq = cpu_info["hz_advertised"][0] / 1_000_000

            return device_info_models.CPUInfoReturn(
                brand_raw=cpu_info.get("brand_raw"),
                vendor_id_raw=cpu_info.get("vendor_id_raw"),
                arch=cpu_info.get("arch"),
                bits=cpu_info.get("bits"),
                physical_cores=physical_cores or cpu_info.get("count"),
                logical_cores=cpu_info.get("count"),
                current_freq=cpu_freq.current if cpu_freq else None,
                min_freq=cpu_freq.min if cpu_freq else None,
                max_freq=cpu_freq.max if cpu_freq else None,
                base_freq=base_freq,
                cpu_usage=cpu_usage,
                l_two_cache_size=cpu_info.get("l2_cache_size"),
                l_three_cache_size=cpu_info.get("l3_cache_size"),
                family=cpu_info.get("family"),
                model=cpu_info.get("model"),
                stepping=cpu_info.get("stepping"),
                flags=cpu_info.get("flags"),
            )

        except Exception as e:
            raise RuntimeError(f"Failed to obtain CPU information: {e}") from e

    def _memory_info(self) -> device_info_models.MemoryInfoReturn:
        """
        _memory_info: Function to obtain the memory information of the device

        Returns:
            device_info_models.MemoryInfoReturn: MemoryInfoReturn

        Raises:
            RuntimeError: If failed to obtain memory information
        """
        try:
            vm = psutil.virtual_memory()
            swap = psutil.swap_memory()

            buffers = getattr(vm, 'buffers', None)
            cached = getattr(vm, 'cached', None)
            shared = getattr(vm, 'shared', None)

            return device_info_models.MemoryInfoReturn(
                total=vm.total,
                available=vm.available,
                percent=vm.percent,
                used=vm.used,
                free=vm.free,
                swap_total=swap.total,
                swap_used=swap.used,
                swap_percent=swap.percent,
                swap_free=swap.free,
                buffers=buffers,
                cached=cached,
                shared=shared,
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}")

    def _disk_info(self) -> device_info_models.DiskInfoReturn:
        """
        _disk_info: Get disk information of the device

        Returns:
            device_info_models.DiskInfoReturn: Disk information

        Raises:
            RuntimeError: If failed to get disk information
        """
        try:
            partitions_info = []
            total_disk_space = 0
            total_used_space = 0
            total_free_space = 0
            usage_percentages = []

            partitions = psutil.disk_partitions()

            for partition in partitions:
                try:
                    # Try psutil first
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        total = usage.total
                        used = usage.used
                        free = usage.free
                    except (SystemError, UnicodeDecodeError):
                        # Fallback to shutil if psutil fails
                        usage = shutil.disk_usage(partition.mountpoint)
                        total = usage.total
                        used = usage.total - usage.free
                        free = usage.free

                    percent = (
                        round((used / total) * 100, 2)
                        if total > 0
                        else 0.0
                    )

                    partition_info = device_info_models.DiskPartitionInfo(
                        device=partition.device,
                        mountpoint=partition.mountpoint,
                        fstype=partition.fstype,
                        total=total,
                        used=used,
                        free=free,
                        percent=percent
                    )

                    partitions_info.append(partition_info)

                    total_disk_space += total
                    total_used_space += used
                    total_free_space += free
                    usage_percentages.append(percent)

                except (PermissionError, OSError):
                    # Skip partitions that can't be accessed
                    continue

            average_usage_percent = None
            if usage_percentages:
                average_usage_percent = round(
                    sum(usage_percentages) / len(usage_percentages), 2
                )

            io_stats = None
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    io_stats = device_info_models.DiskIOInfo(
                        read_count=disk_io.read_count,
                        write_count=disk_io.write_count,
                        read_bytes=disk_io.read_bytes,
                        write_bytes=disk_io.write_bytes,
                        read_time=disk_io.read_time,
                        write_time=disk_io.write_time,
                        read_merged_count=getattr(disk_io, 'read_merged_count', None),
                        write_merged_count=getattr(disk_io, 'write_merged_count', None),
                        busy_time=getattr(disk_io, 'busy_time', None)
                    )
            except Exception:
                pass

            return device_info_models.DiskInfoReturn(
                partitions=partitions_info,
                total_disk_space=total_disk_space,
                total_used_space=total_used_space,
                total_free_space=total_free_space,
                io_stats=io_stats,
                average_usage_percent=average_usage_percent
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get disk info: {e}")

    def _network_info(self) -> device_info_models.NetworkInfoReturn:
        """
        _network_info: Get network information of the device

        Returns:
            device_info_models.NetworkInfoReturn: Network information

        Raises:
            RuntimeError: If failed to get network information
        """
        try:
            hostname = socket.gethostname()

            local_ip = None
            mac_address = None
            interface_name = None
            interface_speed = None

            for iface, addrs in psutil.net_if_addrs().items():
                if iface.lower().startswith(('lo', 'loopback')):
                    continue

                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                        stats = psutil.net_if_stats().get(iface)
                        if stats and stats.isup:
                            local_ip = addr.address
                            interface_name = iface
                            interface_speed = stats.speed if stats.speed > 0 else None

                            for a in addrs:
                                if a.family == psutil.AF_LINK:
                                    mac_address = a.address
                                    break
                            break
                if local_ip:
                    break

            public_ip = None
            services = ['https://api.ipify.org', 'https://icanhazip.com']

            for service in services:
                try:
                    result = subprocess.run(
                        ['curl', '-s', '--connect-timeout', '3', service],
                        capture_output=True,
                        text=True
                    )
                    ip = result.stdout.strip()
                    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                        public_ip = ip
                        break
                except:
                    continue

            net_io = psutil.net_io_counters()
            total_bytes_sent = net_io.bytes_sent
            total_bytes_recv = net_io.bytes_recv

            net_io_start = psutil.net_io_counters()
            time.sleep(3)
            net_io_end = psutil.net_io_counters()

            bytes_recv_diff = net_io_end.bytes_recv - net_io_start.bytes_recv
            bytes_sent_diff = net_io_end.bytes_sent - net_io_start.bytes_sent

            download_speed = round((bytes_recv_diff * 8) / 3_000_000, 2)
            upload_speed = round((bytes_sent_diff * 8) / 3_000_000, 2)

            ping = None
            try:
                if platform.system().lower() == 'windows':
                    cmd = ['ping', '-n', '1', 'baidu.com']
                    encoding = 'gbk'
                else:
                    cmd = ['ping', '-c', '1', '-W', '2', 'baidu.com']
                    encoding = 'utf-8'

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding=encoding
                )

                if result.returncode == 0:
                    match = re.search(r'(?:\u65f6\u95f4|time)[=<](\d+)(?:ms)?', result.stdout)
                    if match:
                        ping = float(match.group(1))
            except:
                pass

            return device_info_models.NetworkInfoReturn(
                public_ip=public_ip,
                local_ip=local_ip,
                mac_address=mac_address,
                hostname=hostname,
                interface_speed=interface_speed,
                total_bytes_sent=total_bytes_sent,
                total_bytes_recv=total_bytes_recv,
                interface_name=interface_name,
                download_speed=download_speed if download_speed > 0 else None,
                upload_speed=upload_speed if upload_speed > 0 else None,
                ping=ping
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get network info: {e}") from e
