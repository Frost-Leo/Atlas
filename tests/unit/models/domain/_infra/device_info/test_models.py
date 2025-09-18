#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_models

This module provides unit tests for device information models

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import pytest
import json
from typing import Dict, Any
from logging import getLogger
from pydantic import ValidationError

from atlas.models.domain._infra.device_info import models as device_info_models
from tests.fixtures.core._infra.device_info.data import DeviceInfoTestData

logger = getLogger(__name__)


class TestDeviceInfoModels:
    """
    TestDeviceInfoModels: Test suite for device information models
    """

    class TestConstants:
        """
        TestConstants: Test suite for Constants model
        """

        def test_constants_creation(self):
            """
            Test Constants model creation with default values
            """
            constants = device_info_models.Constants()
            
            # Verify all constants have expected values
            assert constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH == r"SOFTWARE\Microsoft\Cryptography"
            assert constants.WINDOWS_MACHINE_GUID_KEY_NAME == "MachineGuid"
            assert constants.LINUX_MACHINE_ID_FILE_PATH == "/etc/machine-id"
            assert constants.LINUX_DBUS_MACHINE_ID_FILE_PATH == "/var/lib/dbus/machine-id"
            assert constants.MACOS_IOREG_COMMAND == ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"]
            assert constants.MACOS_UUID_PATTERN == r'"IOPlatformUUID"\s*=\s*"([^"]+)"'
            
            # Verify constants inherit from InternalBaseModel
            assert hasattr(constants, 'version')
            assert hasattr(constants, 'created_at')
            
            logger.info("Constants model creation test passed")

        def test_constants_immutability(self):
            """
            Test that Constants model is immutable (frozen)
            """
            constants = device_info_models.Constants()
            
            # Try to modify a field - should raise ValidationError
            with pytest.raises(ValidationError) as exc_info:
                constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH = "new_path"
            
            error = exc_info.value
            assert "frozen" in str(error).lower()
            
            logger.info("Constants immutability test passed")

        def test_constants_serialization(self):
            """
            Test Constants model serialization and deserialization
            """
            constants = device_info_models.Constants()
            
            # Test JSON serialization
            json_str = constants.model_dump_json()
            assert json_str is not None
            
            # Test JSON deserialization
            recreated = device_info_models.Constants.model_validate_json(json_str)
            assert recreated.WINDOWS_MACHINE_GUID_REGISTRY_PATH == constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH
            assert recreated.MACOS_IOREG_COMMAND == constants.MACOS_IOREG_COMMAND
            
            # Test dict serialization
            data_dict = constants.model_dump()
            assert isinstance(data_dict, dict)
            assert 'WINDOWS_MACHINE_GUID_REGISTRY_PATH' in data_dict
            
            logger.info("Constants serialization test passed")

    class TestPlatformInfoReturn:
        """
        TestPlatformInfoReturn: Test suite for PlatformInfoReturn model
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_PLATFORM_INFO_VALID)
        def test_platform_info_creation_valid(self, input_data, expected_values):
            """
            Test PlatformInfoReturn model creation with valid data
            """
            platform_info = device_info_models.PlatformInfoReturn(**input_data)
            
            # Verify all fields
            for field, expected_value in expected_values.items():
                actual_value = getattr(platform_info, field)
                assert actual_value == expected_value, f"Field {field}: expected {expected_value}, got {actual_value}"
            
            # Verify field types
            if platform_info.hostname is not None:
                assert isinstance(platform_info.hostname, str)
            if platform_info.machine_id is not None:
                assert isinstance(platform_info.machine_id, str)
            if platform_info.boot_time is not None:
                assert isinstance(platform_info.boot_time, float)
                assert platform_info.boot_time > 0
            if platform_info.uptime is not None:
                assert isinstance(platform_info.uptime, float)
                assert platform_info.uptime >= 0
            
            logger.info(f"Platform info creation test passed for {platform_info.os_name}")

        def test_platform_info_optional_fields(self):
            """
            Test PlatformInfoReturn with minimal data (optional fields)
            """
            # Create with minimal required data
            platform_info = device_info_models.PlatformInfoReturn(
                hostname="test",
                os_name="linux"
            )
            
            # Verify required fields are set
            assert platform_info.hostname == "test"
            assert platform_info.os_name == "linux"
            
            # Verify optional fields are None
            assert platform_info.machine_id is None
            assert platform_info.os_version is None
            assert platform_info.python_version is None
            
            logger.info("Platform info optional fields test passed")

        def test_platform_info_validation_errors(self):
            """
            Test PlatformInfoReturn validation errors
            """
            # Test with invalid boot_time (negative)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.PlatformInfoReturn(
                    hostname="test",
                    os_name="linux",
                    boot_time=-1.0
                )
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            # Test with invalid uptime (negative)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.PlatformInfoReturn(
                    hostname="test",
                    os_name="linux",
                    uptime=-1.0
                )
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("Platform info validation errors test passed")

    class TestCPUInfoReturn:
        """
        TestCPUInfoReturn: Test suite for CPUInfoReturn model
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_CPU_INFO_VALID)
        def test_cpu_info_creation_valid(self, input_data, expected_values):
            """
            Test CPUInfoReturn model creation with valid data
            """
            cpu_info = device_info_models.CPUInfoReturn(**input_data)
            
            # Verify all fields
            for field, expected_value in expected_values.items():
                actual_value = getattr(cpu_info, field)
                assert actual_value == expected_value, f"Field {field}: expected {expected_value}, got {actual_value}"
            
            # Verify field constraints
            if cpu_info.bits is not None:
                assert cpu_info.bits >= 1
            if cpu_info.physical_cores is not None:
                assert cpu_info.physical_cores >= 1
            if cpu_info.logical_cores is not None:
                assert cpu_info.logical_cores >= 1
            if cpu_info.cpu_usage is not None:
                assert 0 <= cpu_info.cpu_usage <= 100
            if cpu_info.flags is not None:
                assert isinstance(cpu_info.flags, list)
                assert all(isinstance(flag, str) for flag in cpu_info.flags)
            
            logger.info(f"CPU info creation test passed for {cpu_info.brand_raw}")

        def test_cpu_info_validation_errors(self):
            """
            Test CPUInfoReturn validation errors
            """
            # Test with invalid bits (0)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.CPUInfoReturn(bits=0)
            
            error = exc_info.value
            assert "greater than or equal to 1" in str(error)
            
            # Test with invalid CPU usage (> 100)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.CPUInfoReturn(cpu_usage=150.0)
            
            error = exc_info.value
            assert "less than or equal to 100" in str(error)
            
            # Test with invalid frequency (negative)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.CPUInfoReturn(current_freq=-100.0)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("CPU info validation errors test passed")

    class TestMemoryInfoReturn:
        """
        TestMemoryInfoReturn: Test suite for MemoryInfoReturn model
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_MEMORY_INFO_VALID)
        def test_memory_info_creation_valid(self, input_data, expected_values):
            """
            Test MemoryInfoReturn model creation with valid data
            """
            memory_info = device_info_models.MemoryInfoReturn(**input_data)
            
            # Verify all fields
            for field, expected_value in expected_values.items():
                actual_value = getattr(memory_info, field)
                assert actual_value == expected_value, f"Field {field}: expected {expected_value}, got {actual_value}"
            
            # Verify field constraints
            if memory_info.total is not None:
                assert memory_info.total >= 0
            if memory_info.percent is not None:
                assert 0 <= memory_info.percent <= 100
            if memory_info.swap_percent is not None:
                assert 0 <= memory_info.swap_percent <= 100
            
            logger.info("Memory info creation test passed")

        def test_memory_info_validation_errors(self):
            """
            Test MemoryInfoReturn validation errors
            """
            # Test with invalid percentage (> 100)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.MemoryInfoReturn(percent=150.0)
            
            error = exc_info.value
            assert "less than or equal to 100" in str(error)
            
            # Test with negative memory size
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.MemoryInfoReturn(total=-1)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("Memory info validation errors test passed")

    class TestDiskInfoModels:
        """
        TestDiskInfoModels: Test suite for disk information models
        """

        def test_disk_partition_info_creation(self):
            """
            Test DiskPartitionInfo model creation
            """
            partition_data = {
                "device": "C:",
                "mountpoint": "C:",
                "fstype": "NTFS",
                "total": 1000000000,
                "used": 500000000,
                "free": 500000000,
                "percent": 50.0,
            }
            
            partition = device_info_models.DiskPartitionInfo(**partition_data)
            
            assert partition.device == "C:"
            assert partition.mountpoint == "C:"
            assert partition.fstype == "NTFS"
            assert partition.total == 1000000000
            assert partition.used == 500000000
            assert partition.free == 500000000
            assert partition.percent == 50.0
            
            logger.info("Disk partition info creation test passed")

        def test_disk_io_info_creation(self):
            """
            Test DiskIOInfo model creation
            """
            io_data = {
                "read_count": 1000,
                "write_count": 500,
                "read_bytes": 1000000,
                "write_bytes": 500000,
                "read_time": 100,
                "write_time": 50,
                "read_merged_count": 10,
                "write_merged_count": 5,
                "busy_time": 150,
            }
            
            io_info = device_info_models.DiskIOInfo(**io_data)
            
            assert io_info.read_count == 1000
            assert io_info.write_count == 500
            assert io_info.read_bytes == 1000000
            assert io_info.write_bytes == 500000
            assert io_info.read_time == 100
            assert io_info.write_time == 50
            
            logger.info("Disk IO info creation test passed")

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_DISK_INFO_VALID)
        def test_disk_info_return_creation(self, input_data, expected_values):
            """
            Test DiskInfoReturn model creation with valid data
            """
            disk_info = device_info_models.DiskInfoReturn(**input_data)
            
            # Verify partitions
            if disk_info.partitions is not None:
                assert isinstance(disk_info.partitions, list)
                for partition in disk_info.partitions:
                    assert isinstance(partition, device_info_models.DiskPartitionInfo)
            
            # Verify IO stats
            if disk_info.io_stats is not None:
                assert isinstance(disk_info.io_stats, device_info_models.DiskIOInfo)
            
            # Verify constraints
            if disk_info.average_usage_percent is not None:
                assert 0 <= disk_info.average_usage_percent <= 100
            
            logger.info("Disk info return creation test passed")

        def test_disk_info_validation_errors(self):
            """
            Test disk information validation errors
            """
            # Test invalid percentage in partition
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.DiskPartitionInfo(percent=150.0)
            
            error = exc_info.value
            assert "less than or equal to 100" in str(error)
            
            # Test negative values in IO info
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.DiskIOInfo(read_count=-1)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("Disk info validation errors test passed")

    class TestNetworkInfoReturn:
        """
        TestNetworkInfoReturn: Test suite for NetworkInfoReturn model
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_NETWORK_INFO_VALID)
        def test_network_info_creation_valid(self, input_data, expected_values):
            """
            Test NetworkInfoReturn model creation with valid data
            """
            network_info = device_info_models.NetworkInfoReturn(**input_data)
            
            # Verify all fields
            for field, expected_value in expected_values.items():
                actual_value = getattr(network_info, field)
                assert actual_value == expected_value, f"Field {field}: expected {expected_value}, got {actual_value}"
            
            # Verify field constraints
            if network_info.interface_speed is not None:
                assert network_info.interface_speed >= 0
            if network_info.total_bytes_sent is not None:
                assert network_info.total_bytes_sent >= 0
            if network_info.total_bytes_recv is not None:
                assert network_info.total_bytes_recv >= 0
            if network_info.ping is not None:
                assert network_info.ping >= 0
            
            logger.info("Network info creation test passed")

        def test_network_info_validation_errors(self):
            """
            Test NetworkInfoReturn validation errors
            """
            # Test negative ping
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.NetworkInfoReturn(ping=-1.0)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            # Test negative bytes
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.NetworkInfoReturn(total_bytes_sent=-1)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("Network info validation errors test passed")

    class TestGetDeviceInfoModels:
        """
        TestGetDeviceInfoModels: Test suite for GetDeviceInfo models
        """

        @pytest.mark.parametrize("input_params, expected_flags", DeviceInfoTestData.TEST_GET_DEVICE_INFO_PARAMS)
        def test_get_device_info_params_creation(self, input_params, expected_flags):
            """
            Test GetDeviceInfoParams model creation
            """
            if input_params:
                params = device_info_models.GetDeviceInfoParams(**input_params)
            else:
                params = device_info_models.GetDeviceInfoParams()
            
            # Verify all flags
            for flag, expected_value in expected_flags.items():
                actual_value = getattr(params, flag)
                assert actual_value == expected_value, f"Flag {flag}: expected {expected_value}, got {actual_value}"
            
            logger.info(f"GetDeviceInfoParams creation test passed: {expected_flags}")

        def test_get_device_info_return_creation(self):
            """
            Test GetDeviceInfoReturn model creation
            """
            # Create with all components
            platform_info = device_info_models.PlatformInfoReturn(hostname="test", os_name="linux")
            cpu_info = device_info_models.CPUInfoReturn(brand_raw="Test CPU")
            memory_info = device_info_models.MemoryInfoReturn(total=1000000000)
            disk_info = device_info_models.DiskInfoReturn(total_disk_space=2000000000)
            network_info = device_info_models.NetworkInfoReturn(hostname="test")
            
            result = device_info_models.GetDeviceInfoReturn(
                platform=platform_info,
                cpu=cpu_info,
                memory=memory_info,
                disk=disk_info,
                network=network_info,
                timestamp=1695000000.0
            )
            
            # Verify all components
            assert result.platform is not None
            assert result.cpu is not None
            assert result.memory is not None
            assert result.disk is not None
            assert result.network is not None
            assert result.timestamp == 1695000000.0
            
            # Verify component types
            assert isinstance(result.platform, device_info_models.PlatformInfoReturn)
            assert isinstance(result.cpu, device_info_models.CPUInfoReturn)
            assert isinstance(result.memory, device_info_models.MemoryInfoReturn)
            assert isinstance(result.disk, device_info_models.DiskInfoReturn)
            assert isinstance(result.network, device_info_models.NetworkInfoReturn)
            
            logger.info("GetDeviceInfoReturn creation test passed")

        def test_get_device_info_return_optional_fields(self):
            """
            Test GetDeviceInfoReturn with optional fields
            """
            # Create with minimal data
            result = device_info_models.GetDeviceInfoReturn()
            
            # All fields should be None by default
            assert result.platform is None
            assert result.cpu is None
            assert result.memory is None
            assert result.disk is None
            assert result.network is None
            assert result.timestamp is None
            
            logger.info("GetDeviceInfoReturn optional fields test passed")

        def test_get_device_info_return_validation_errors(self):
            """
            Test GetDeviceInfoReturn validation errors
            """
            # Test with invalid timestamp (negative)
            with pytest.raises(ValidationError) as exc_info:
                device_info_models.GetDeviceInfoReturn(timestamp=-1.0)
            
            error = exc_info.value
            assert "greater than or equal to 0" in str(error)
            
            logger.info("GetDeviceInfoReturn validation errors test passed")

    class TestModelSerialization:
        """
        TestModelSerialization: Test suite for model serialization/deserialization
        """

        def test_complete_device_info_serialization(self):
            """
            Test complete device information serialization and deserialization
            """
            # Create a complete device info result
            platform_info = device_info_models.PlatformInfoReturn(
                hostname="test-machine",
                machine_id="12345678-1234-1234-1234-123456789012",
                os_name="windows",
                os_version="10.0.19045",
                python_version="3.13.0",
                boot_time=1695000000.0,
                uptime=86400.0
            )
            
            cpu_info = device_info_models.CPUInfoReturn(
                brand_raw="Intel Core i7",
                vendor_id_raw="GenuineIntel",
                logical_cores=8,
                physical_cores=4,
                cpu_usage=25.5
            )
            
            memory_info = device_info_models.MemoryInfoReturn(
                total=17179869184,
                available=8589934592,
                percent=50.0
            )
            
            partition = device_info_models.DiskPartitionInfo(
                device="C:",
                mountpoint="C:",
                fstype="NTFS",
                total=1000000000,
                percent=50.0
            )
            
            disk_info = device_info_models.DiskInfoReturn(
                partitions=[partition],
                total_disk_space=1000000000
            )
            
            network_info = device_info_models.NetworkInfoReturn(
                hostname="test-machine",
                local_ip="192.168.1.100",
                ping=15.5
            )
            
            result = device_info_models.GetDeviceInfoReturn(
                platform=platform_info,
                cpu=cpu_info,
                memory=memory_info,
                disk=disk_info,
                network=network_info,
                timestamp=1695086400.0
            )
            
            # Test JSON serialization
            json_str = result.model_dump_json()
            assert json_str is not None
            assert len(json_str) > 0
            
            # Parse JSON to verify structure
            json_data = json.loads(json_str)
            assert 'platform' in json_data
            assert 'cpu' in json_data
            assert 'memory' in json_data
            assert 'disk' in json_data
            assert 'network' in json_data
            assert 'timestamp' in json_data
            
            # Test JSON deserialization
            recreated = device_info_models.GetDeviceInfoReturn.model_validate_json(json_str)
            
            # Verify recreated object matches original
            assert recreated.platform.hostname == result.platform.hostname
            assert recreated.cpu.brand_raw == result.cpu.brand_raw
            assert recreated.memory.total == result.memory.total
            assert len(recreated.disk.partitions) == len(result.disk.partitions)
            assert recreated.network.local_ip == result.network.local_ip
            assert recreated.timestamp == result.timestamp
            
            logger.info("Complete device info serialization test passed")

        def test_model_inheritance_serialization(self):
            """
            Test that model inheritance (InternalBaseModel) is properly handled in serialization
            """
            constants = device_info_models.Constants()
            
            # Serialize to dict
            data_dict = constants.model_dump()
            
            # Verify InternalBaseModel fields are included
            assert 'version' in data_dict
            assert 'created_at' in data_dict
            
            # Verify constant fields are included
            assert 'WINDOWS_MACHINE_GUID_REGISTRY_PATH' in data_dict
            assert 'LINUX_MACHINE_ID_FILE_PATH' in data_dict
            
            # Test deserialization
            recreated = device_info_models.Constants.model_validate(data_dict)
            assert recreated.version == constants.version
            assert recreated.WINDOWS_MACHINE_GUID_REGISTRY_PATH == constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH
            
            logger.info("Model inheritance serialization test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
