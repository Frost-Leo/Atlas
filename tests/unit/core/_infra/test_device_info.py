#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_device_info

This module provides unit tests for DeviceInfo class

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import pytest
import threading
import time
from unittest.mock import Mock, patch, MagicMock
from logging import getLogger

from atlas.core._infra.device_info import DeviceInfo
from atlas.models.domain._infra.device_info import models as device_info_models
from tests.fixtures.core._infra.device_info.fixtures import (
    device_info_instance,
    mock_platform_info,
    mock_cpu_info,
    mock_memory_info,
    mock_disk_info,
    mock_network_info,
    comprehensive_device_info_mock,
)
from tests.fixtures.core._infra.device_info.data import DeviceInfoTestData

logger = getLogger(__name__)


class TestDeviceInfo:
    """
    TestDeviceInfo: Test suite for DeviceInfo class
    """

    class TestSingletonPattern:
        """
        TestSingletonPattern: Test suite for DeviceInfo singleton pattern
        """

        def test_singleton_same_instance(self, device_info_instance):
            """
            Test that DeviceInfo returns the same instance (singleton pattern)
            """
            instance1 = device_info_instance
            instance2 = DeviceInfo()
            
            assert instance1 is instance2
            assert id(instance1) == id(instance2)
            logger.info("Singleton pattern correctly returns same instance")

        def test_singleton_thread_safety(self):
            """
            Test that DeviceInfo singleton is thread-safe
            """
            # Reset singleton
            DeviceInfo._instance = None
            instances = []
            
            def create_instance():
                instances.append(DeviceInfo())
            
            # Create multiple threads
            threads = []
            for _ in range(10):
                thread = threading.Thread(target=create_instance)
                threads.append(thread)
            
            # Start all threads
            for thread in threads:
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # All instances should be the same
            first_instance = instances[0]
            for instance in instances:
                assert instance is first_instance
                assert id(instance) == id(first_instance)
            
            logger.info(f"Thread-safe singleton verified with {len(instances)} instances")

    class TestGetDeviceInfo:
        """
        TestGetDeviceInfo: Test suite for get_device_info method
        """

        @pytest.mark.parametrize("input_params, expected_flags", DeviceInfoTestData.TEST_GET_DEVICE_INFO_PARAMS)
        def test_get_device_info_parameters(self, input_params, expected_flags, device_info_instance):
            """
            Test get_device_info with various parameter combinations
            """
            with patch.object(device_info_instance, '_platform_info') as mock_platform, \
                 patch.object(device_info_instance, '_cpu_info') as mock_cpu, \
                 patch.object(device_info_instance, '_memory_info') as mock_memory, \
                 patch.object(device_info_instance, '_disk_info') as mock_disk, \
                 patch.object(device_info_instance, '_network_info') as mock_network:
                
                # Set up mock returns
                mock_platform.return_value = device_info_models.PlatformInfoReturn()
                mock_cpu.return_value = device_info_models.CPUInfoReturn()
                mock_memory.return_value = device_info_models.MemoryInfoReturn()
                mock_disk.return_value = device_info_models.DiskInfoReturn()
                mock_network.return_value = device_info_models.NetworkInfoReturn()
                
                # Create params if provided
                params = device_info_models.GetDeviceInfoParams(**input_params) if input_params else None
                
                # Call method
                result = device_info_instance.get_device_info(params)
                
                # Verify method calls based on parameters
                if expected_flags['include_platform']:
                    mock_platform.assert_called_once()
                    assert result.platform is not None
                else:
                    mock_platform.assert_not_called()
                    assert result.platform is None
                
                if expected_flags['include_cpu']:
                    mock_cpu.assert_called_once()
                    assert result.cpu is not None
                else:
                    mock_cpu.assert_not_called()
                    assert result.cpu is None
                
                if expected_flags['include_memory']:
                    mock_memory.assert_called_once()
                    assert result.memory is not None
                else:
                    mock_memory.assert_not_called()
                    assert result.memory is None
                
                if expected_flags['include_disk']:
                    mock_disk.assert_called_once()
                    assert result.disk is not None
                else:
                    mock_disk.assert_not_called()
                    assert result.disk is None
                
                if expected_flags['include_network']:
                    mock_network.assert_called_once()
                    assert result.network is not None
                else:
                    mock_network.assert_not_called()
                    assert result.network is None
                
                # Verify timestamp is set
                assert result.timestamp is not None
                assert result.timestamp > 0
                
                logger.info(f"Parameter test passed: {expected_flags}")

        def test_get_device_info_default_params(self, device_info_instance):
            """
            Test get_device_info with default parameters (all True)
            """
            with patch.object(device_info_instance, '_platform_info') as mock_platform, \
                 patch.object(device_info_instance, '_cpu_info') as mock_cpu, \
                 patch.object(device_info_instance, '_memory_info') as mock_memory, \
                 patch.object(device_info_instance, '_disk_info') as mock_disk, \
                 patch.object(device_info_instance, '_network_info') as mock_network:
                
                # Set up mock returns
                mock_platform.return_value = device_info_models.PlatformInfoReturn()
                mock_cpu.return_value = device_info_models.CPUInfoReturn()
                mock_memory.return_value = device_info_models.MemoryInfoReturn()
                mock_disk.return_value = device_info_models.DiskInfoReturn()
                mock_network.return_value = device_info_models.NetworkInfoReturn()
                
                # Call with no parameters (should use defaults)
                result = device_info_instance.get_device_info()
                
                # All methods should be called
                mock_platform.assert_called_once()
                mock_cpu.assert_called_once()
                mock_memory.assert_called_once()
                mock_disk.assert_called_once()
                mock_network.assert_called_once()
                
                # All results should be present
                assert result.platform is not None
                assert result.cpu is not None
                assert result.memory is not None
                assert result.disk is not None
                assert result.network is not None
                assert result.timestamp is not None
                
                logger.info("Default parameters test passed - all info collected")

        @pytest.mark.parametrize("error_type, error_msg, exception", DeviceInfoTestData.TEST_ERROR_SCENARIOS)
        def test_get_device_info_error_handling(self, error_type, error_msg, exception, device_info_instance):
            """
            Test error handling in get_device_info method
            """
            with patch.object(device_info_instance, '_platform_info') as mock_platform, \
                 patch.object(device_info_instance, '_cpu_info') as mock_cpu, \
                 patch.object(device_info_instance, '_memory_info') as mock_memory, \
                 patch.object(device_info_instance, '_disk_info') as mock_disk, \
                 patch.object(device_info_instance, '_network_info') as mock_network:
                
                # Set up the specific method to raise an exception
                if error_type == "platform_error":
                    mock_platform.side_effect = exception
                elif error_type == "cpu_error":
                    mock_cpu.side_effect = exception
                elif error_type == "memory_error":
                    mock_memory.side_effect = exception
                elif error_type == "disk_error":
                    mock_disk.side_effect = exception
                elif error_type == "network_error":
                    mock_network.side_effect = exception
                
                # Set up other methods to return valid results
                mock_platform.return_value = device_info_models.PlatformInfoReturn()
                mock_cpu.return_value = device_info_models.CPUInfoReturn()
                mock_memory.return_value = device_info_models.MemoryInfoReturn()
                mock_disk.return_value = device_info_models.DiskInfoReturn()
                mock_network.return_value = device_info_models.NetworkInfoReturn()
                
                # Test that RuntimeError is raised
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance.get_device_info()
                
                error = exc_info.value
                assert "Failed to get device information" in str(error)
                # The original mock exception message should be in the cause
                assert str(error.__cause__) in str(error)
                
                logger.info(f"Error handling test passed for {error_type}: {error_msg}")

    class TestPlatformInfo:
        """
        TestPlatformInfo: Test suite for _platform_info method
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_PLATFORM_INFO_VALID)
        def test_platform_info_valid(self, input_data, expected_values, device_info_instance, comprehensive_device_info_mock):
            """
            Test _platform_info method with valid data
            """
            result = device_info_instance._platform_info()
            
            # Verify result is correct type
            assert isinstance(result, device_info_models.PlatformInfoReturn)
            
            # Verify all fields are present and of correct type
            assert isinstance(result.hostname, str)
            assert result.os_name in ["windows", "linux", "darwin"]
            assert isinstance(result.os_version, str)
            assert isinstance(result.python_version, str)
            assert isinstance(result.platform, str)
            assert isinstance(result.architecture, str)
            assert isinstance(result.processor, str)
            assert isinstance(result.boot_time, float)
            assert isinstance(result.uptime, float)
            assert result.uptime >= 0
            
            logger.info(f"Platform info test passed: {result.os_name}")

        def test_platform_info_windows_machine_id(self, device_info_instance):
            """
            Test Windows machine ID extraction
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Windows'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='10.0.19045'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Windows-10'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='AMD64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='Intel'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('atlas.core._infra.device_info.winreg') as mock_winreg:
                
                # Mock Windows registry operations
                mock_key = MagicMock()
                mock_winreg.OpenKey.return_value.__enter__.return_value = mock_key
                mock_winreg.OpenKey.return_value.__exit__.return_value = None
                mock_winreg.QueryValueEx.return_value = ("12345678-1234-1234-1234-123456789012", 1)
                
                result = device_info_instance._platform_info()
                
                assert result.machine_id == "12345678-1234-1234-1234-123456789012"
                assert result.os_name == "windows"
                mock_winreg.OpenKey.assert_called_once()
                mock_winreg.QueryValueEx.assert_called_once()
                
                logger.info("Windows machine ID test passed")

        def test_platform_info_linux_machine_id(self, device_info_instance):
            """
            Test Linux machine ID extraction
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Linux'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Linux-5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('builtins.open', create=True) as mock_open:
                
                # Mock file reading for machine ID
                mock_file = MagicMock()
                mock_file.read.return_value = "abcdef1234567890abcdef1234567890\n"
                mock_file.strip.return_value = "abcdef1234567890abcdef1234567890"
                mock_file.__enter__.return_value = mock_file
                mock_file.__exit__.return_value = None
                mock_open.return_value = mock_file
                
                result = device_info_instance._platform_info()
                
                assert result.machine_id == "abcdef1234567890abcdef1234567890"
                assert result.os_name == "linux"
                mock_open.assert_called()
                
                logger.info("Linux machine ID test passed")

        def test_platform_info_macos_machine_id(self, device_info_instance):
            """
            Test macOS machine ID extraction
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Darwin'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-macos'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='22.6.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='macOS-13.5.2'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='arm64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='arm'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('atlas.core._infra.device_info.subprocess.run') as mock_subprocess:
                
                # Mock subprocess result for ioreg command
                mock_result = MagicMock()
                mock_result.stdout = '"IOPlatformUUID" = "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"'
                mock_subprocess.return_value = mock_result
                
                result = device_info_instance._platform_info()
                
                assert result.machine_id == "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
                assert result.os_name == "darwin"
                mock_subprocess.assert_called_once()
                
                logger.info("macOS machine ID test passed")

        def test_platform_info_windows_machine_id_error(self, device_info_instance):
            """
            Test Windows machine ID extraction with registry error
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Windows'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='10.0.19045'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Windows-10'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='AMD64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='Intel'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('atlas.core._infra.device_info.winreg.OpenKey', side_effect=Exception("Registry error")):
                
                result = device_info_instance._platform_info()
                
                # Should handle the exception gracefully and return None for machine_id
                assert result.machine_id is None
                assert result.os_name == "windows"
                
                logger.info("Windows machine ID error handling test passed")

        def test_platform_info_linux_machine_id_error(self, device_info_instance):
            """
            Test Linux machine ID extraction with file read errors
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Linux'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Linux-5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('builtins.open', side_effect=FileNotFoundError("File not found")):
                
                result = device_info_instance._platform_info()
                
                # Should handle the exception gracefully and return None for machine_id
                assert result.machine_id is None
                assert result.os_name == "linux"
                
                logger.info("Linux machine ID error handling test passed")

        def test_platform_info_linux_dbus_fallback_success(self, device_info_instance):
            """
            Test Linux machine ID extraction with dbus fallback success
            """
            def mock_open_side_effect(file_path, mode='r'):
                if "/etc/machine-id" in file_path:
                    raise FileNotFoundError("Primary file not found")
                elif "/var/lib/dbus/machine-id" in file_path:
                    # Return a mock file for dbus fallback
                    mock_file = MagicMock()
                    mock_file.read.return_value = "fedcba0987654321fedcba0987654321\n"
                    mock_file.strip.return_value = "fedcba0987654321fedcba0987654321"
                    mock_file.__enter__.return_value = mock_file
                    mock_file.__exit__.return_value = None
                    return mock_file
                else:
                    raise FileNotFoundError(f"No such file: {file_path}")
            
            with patch('atlas.core._infra.device_info.platform.system', return_value='Linux'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Linux-5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('builtins.open', side_effect=mock_open_side_effect):
                
                result = device_info_instance._platform_info()
                
                # Should successfully get machine_id from dbus fallback
                assert result.machine_id == "fedcba0987654321fedcba0987654321"
                assert result.os_name == "linux"
                
                logger.info("Linux dbus fallback success test passed")

        def test_platform_info_linux_dbus_fallback_error(self, device_info_instance):
            """
            Test Linux machine ID extraction with both files failing
            """
            def mock_open_side_effect(file_path, mode='r'):
                if "/etc/machine-id" in file_path:
                    raise FileNotFoundError("Primary file not found")
                elif "/var/lib/dbus/machine-id" in file_path:
                    raise Exception("Dbus file error")
                else:
                    raise FileNotFoundError(f"No such file: {file_path}")
            
            with patch('atlas.core._infra.device_info.platform.system', return_value='Linux'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-machine'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='Linux-5.15.0'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='x86_64'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('builtins.open', side_effect=mock_open_side_effect):
                
                result = device_info_instance._platform_info()
                
                # Should handle both exceptions gracefully and return None for machine_id
                assert result.machine_id is None
                assert result.os_name == "linux"
                
                logger.info("Linux dbus fallback error handling test passed")

        def test_platform_info_macos_machine_id_error(self, device_info_instance):
            """
            Test macOS machine ID extraction with subprocess error
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Darwin'), \
                 patch('atlas.core._infra.device_info.socket.gethostname', return_value='test-macos'), \
                 patch('atlas.core._infra.device_info.platform.version', return_value='22.6.0'), \
                 patch('atlas.core._infra.device_info.platform.python_version', return_value='3.13.0'), \
                 patch('atlas.core._infra.device_info.platform.platform', return_value='macOS-13.5.2'), \
                 patch('atlas.core._infra.device_info.platform.machine', return_value='arm64'), \
                 patch('atlas.core._infra.device_info.platform.processor', return_value='arm'), \
                 patch('atlas.core._infra.device_info.psutil.boot_time', return_value=1695000000.0), \
                 patch('atlas.core._infra.device_info.time.time', return_value=1695086400.0), \
                 patch('atlas.core._infra.device_info.subprocess.run', side_effect=Exception("Subprocess error")):
                
                result = device_info_instance._platform_info()
                
                # Should handle the exception gracefully and return None for machine_id
                assert result.machine_id is None
                assert result.os_name == "darwin"
                
                logger.info("macOS machine ID error handling test passed")

        def test_platform_info_error_handling(self, device_info_instance):
            """
            Test error handling in _platform_info method
            """
            with patch('atlas.core._infra.device_info.socket.gethostname', side_effect=Exception("Network error")):
                
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance._platform_info()
                
                error = exc_info.value
                assert "Failed to get platform info" in str(error)
                
                logger.info("Platform info error handling test passed")

    class TestCPUInfo:
        """
        TestCPUInfo: Test suite for _cpu_info method
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_CPU_INFO_VALID)
        def test_cpu_info_valid(self, input_data, expected_values, device_info_instance, comprehensive_device_info_mock):
            """
            Test _cpu_info method with valid data
            """
            result = device_info_instance._cpu_info()
            
            # Verify result is correct type
            assert isinstance(result, device_info_models.CPUInfoReturn)
            
            # Verify all fields are present and of correct type
            if result.brand_raw is not None:
                assert isinstance(result.brand_raw, str)
            if result.vendor_id_raw is not None:
                assert isinstance(result.vendor_id_raw, str)
            if result.arch is not None:
                assert isinstance(result.arch, str)
            if result.bits is not None:
                assert isinstance(result.bits, int)
                assert result.bits > 0
            if result.physical_cores is not None:
                assert isinstance(result.physical_cores, int)
                assert result.physical_cores > 0
            if result.logical_cores is not None:
                assert isinstance(result.logical_cores, int)
                assert result.logical_cores > 0
            if result.cpu_usage is not None:
                assert isinstance(result.cpu_usage, float)
                assert 0 <= result.cpu_usage <= 100
            if result.flags is not None:
                assert isinstance(result.flags, list)
                assert all(isinstance(flag, str) for flag in result.flags)
            
            logger.info("CPU info test passed")

        def test_cpu_info_error_handling(self, device_info_instance):
            """
            Test error handling in _cpu_info method
            """
            with patch('atlas.core._infra.device_info.psutil.cpu_freq', side_effect=Exception("CPU error")):
                
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance._cpu_info()
                
                error = exc_info.value
                assert "Failed to obtain CPU information" in str(error)
                
                logger.info("CPU info error handling test passed")

    class TestMemoryInfo:
        """
        TestMemoryInfo: Test suite for _memory_info method
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_MEMORY_INFO_VALID)
        def test_memory_info_valid(self, input_data, expected_values, device_info_instance, comprehensive_device_info_mock):
            """
            Test _memory_info method with valid data
            """
            result = device_info_instance._memory_info()
            
            # Verify result is correct type
            assert isinstance(result, device_info_models.MemoryInfoReturn)
            
            # Verify all fields are present and of correct type
            if result.total is not None:
                assert isinstance(result.total, int)
                assert result.total >= 0
            if result.available is not None:
                assert isinstance(result.available, int)
                assert result.available >= 0
            if result.percent is not None:
                assert isinstance(result.percent, float)
                assert 0 <= result.percent <= 100
            if result.used is not None:
                assert isinstance(result.used, int)
                assert result.used >= 0
            if result.free is not None:
                assert isinstance(result.free, int)
                assert result.free >= 0
            if result.swap_total is not None:
                assert isinstance(result.swap_total, int)
                assert result.swap_total >= 0
            if result.swap_percent is not None:
                assert isinstance(result.swap_percent, float)
                assert 0 <= result.swap_percent <= 100
            
            logger.info("Memory info test passed")

        def test_memory_info_error_handling(self, device_info_instance):
            """
            Test error handling in _memory_info method
            """
            with patch('atlas.core._infra.device_info.psutil.virtual_memory', side_effect=Exception("Memory error")):
                
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance._memory_info()
                
                error = exc_info.value
                assert "Failed to get memory info" in str(error)
                
                logger.info("Memory info error handling test passed")

    class TestDiskInfo:
        """
        TestDiskInfo: Test suite for _disk_info method
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_DISK_INFO_VALID)
        def test_disk_info_valid(self, input_data, expected_values, device_info_instance, comprehensive_device_info_mock):
            """
            Test _disk_info method with valid data
            """
            result = device_info_instance._disk_info()
            
            # Verify result is correct type
            assert isinstance(result, device_info_models.DiskInfoReturn)
            
            # Verify partition information
            if result.partitions is not None:
                assert isinstance(result.partitions, list)
                for partition in result.partitions:
                    assert isinstance(partition, device_info_models.DiskPartitionInfo)
                    if partition.total is not None:
                        assert partition.total >= 0
                    if partition.used is not None:
                        assert partition.used >= 0
                    if partition.free is not None:
                        assert partition.free >= 0
                    if partition.percent is not None:
                        assert 0 <= partition.percent <= 100
            
            # Verify total statistics
            if result.total_disk_space is not None:
                assert isinstance(result.total_disk_space, int)
                assert result.total_disk_space >= 0
            if result.total_used_space is not None:
                assert isinstance(result.total_used_space, int)
                assert result.total_used_space >= 0
            if result.total_free_space is not None:
                assert isinstance(result.total_free_space, int)
                assert result.total_free_space >= 0
            if result.average_usage_percent is not None:
                assert isinstance(result.average_usage_percent, float)
                assert 0 <= result.average_usage_percent <= 100
            
            # Verify I/O statistics
            if result.io_stats is not None:
                assert isinstance(result.io_stats, device_info_models.DiskIOInfo)
                if result.io_stats.read_count is not None:
                    assert result.io_stats.read_count >= 0
                if result.io_stats.write_count is not None:
                    assert result.io_stats.write_count >= 0
            
            logger.info("Disk info test passed")

        def test_disk_info_error_handling(self, device_info_instance):
            """
            Test error handling in _disk_info method
            """
            with patch('atlas.core._infra.device_info.psutil.disk_partitions', side_effect=Exception("Disk error")):
                
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance._disk_info()
                
                error = exc_info.value
                assert "Failed to get disk info" in str(error)
                
                logger.info("Disk info error handling test passed")

    class TestNetworkInfo:
        """
        TestNetworkInfo: Test suite for _network_info method
        """

        @pytest.mark.parametrize("input_data, expected_values", DeviceInfoTestData.TEST_NETWORK_INFO_VALID)
        def test_network_info_valid(self, input_data, expected_values, device_info_instance, comprehensive_device_info_mock):
            """
            Test _network_info method with valid data
            """
            result = device_info_instance._network_info()
            
            # Verify result is correct type
            assert isinstance(result, device_info_models.NetworkInfoReturn)
            
            # Verify all fields are present and of correct type
            if result.hostname is not None:
                assert isinstance(result.hostname, str)
            if result.local_ip is not None:
                assert isinstance(result.local_ip, str)
                # Basic IP format check
                parts = result.local_ip.split('.')
                assert len(parts) == 4
                for part in parts:
                    assert 0 <= int(part) <= 255
            if result.mac_address is not None:
                assert isinstance(result.mac_address, str)
                # Basic MAC format check
                assert ':' in result.mac_address or '-' in result.mac_address
            if result.interface_speed is not None:
                assert isinstance(result.interface_speed, int)
                assert result.interface_speed > 0
            if result.total_bytes_sent is not None:
                assert isinstance(result.total_bytes_sent, int)
                assert result.total_bytes_sent >= 0
            if result.total_bytes_recv is not None:
                assert isinstance(result.total_bytes_recv, int)
                assert result.total_bytes_recv >= 0
            if result.ping is not None:
                assert isinstance(result.ping, float)
                assert result.ping >= 0
            
            logger.info("Network info test passed")

        def test_network_info_linux_ping(self, device_info_instance, comprehensive_device_info_mock):
            """
            Test network info with Linux ping command
            """
            with patch('atlas.core._infra.device_info.platform.system', return_value='Linux'), \
                 patch('atlas.core._infra.device_info.subprocess.run') as mock_subprocess:
                
                # Mock successful ping result for Linux
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "PING baidu.com (39.156.66.10): 56 data bytes\n64 bytes from 39.156.66.10: icmp_seq=0 ttl=51 time=25.123 ms"
                mock_subprocess.return_value = mock_result
                
                result = device_info_instance._network_info()
                
                # Verify ping was captured
                assert result.ping is not None
                assert isinstance(result.ping, float)
                assert result.ping > 0
                
                # Verify Linux ping command was used
                mock_subprocess.assert_called()
                call_args = mock_subprocess.call_args[0][0]  # Get the command arguments
                assert 'ping' in call_args
                assert '-c' in call_args  # Linux uses -c instead of -n
                assert '1' in call_args
                
                logger.info("Linux ping test passed")

        def test_network_info_ping_error(self, device_info_instance, comprehensive_device_info_mock):
            """
            Test network info with ping command error
            """
            with patch('atlas.core._infra.device_info.subprocess.run', side_effect=Exception("Ping command failed")):
                
                result = device_info_instance._network_info()
                
                # Should handle ping error gracefully
                assert result.ping is None
                # Other network info should still be available
                assert result.hostname is not None
                
                logger.info("Network ping error handling test passed")

        def test_network_info_error_handling(self, device_info_instance):
            """
            Test error handling in _network_info method
            """
            with patch('atlas.core._infra.device_info.socket.gethostname', side_effect=Exception("Network error")):
                
                with pytest.raises(RuntimeError) as exc_info:
                    device_info_instance._network_info()
                
                error = exc_info.value
                assert "Failed to get network info" in str(error)
                
                logger.info("Network info error handling test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
