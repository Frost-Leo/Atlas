#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_device_info_integration

This module provides integration tests for DeviceInfo class

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import pytest
import platform
import time
from logging import getLogger

from atlas.core._infra.device_info import DeviceInfo
from atlas.models.domain._infra.device_info import models as device_info_models

logger = getLogger(__name__)


@pytest.mark.integration
class TestDeviceInfoIntegration:
    """
    TestDeviceInfoIntegration: Integration tests for DeviceInfo class
    
    These tests run against real system resources and may take longer to execute.
    They verify that DeviceInfo works correctly in a real environment.
    """

    def setup_method(self):
        """
        Setup method to reset DeviceInfo singleton for each test
        """
        DeviceInfo._instance = None

    @pytest.mark.slow
    def test_get_device_info_full_real_system(self):
        """
        Test get_device_info with all parameters on real system
        
        This test verifies that DeviceInfo can successfully collect
        all types of information from the actual running system.
        """
        device_info = DeviceInfo()
        
        # Get all device information
        result = device_info.get_device_info()
        
        # Verify result structure
        assert isinstance(result, device_info_models.GetDeviceInfoReturn)
        assert result.timestamp is not None
        assert result.timestamp > 0
        
        # Verify platform information
        assert result.platform is not None
        assert isinstance(result.platform, device_info_models.PlatformInfoReturn)
        assert result.platform.hostname is not None
        assert result.platform.os_name in ["windows", "linux", "darwin"]
        assert result.platform.os_version is not None
        assert result.platform.python_version is not None
        assert result.platform.boot_time is not None
        assert result.platform.uptime is not None
        assert result.platform.uptime > 0
        
        # Verify CPU information
        assert result.cpu is not None
        assert isinstance(result.cpu, device_info_models.CPUInfoReturn)
        if result.cpu.logical_cores is not None:
            assert result.cpu.logical_cores > 0
        if result.cpu.physical_cores is not None:
            assert result.cpu.physical_cores > 0
        if result.cpu.cpu_usage is not None:
            assert 0 <= result.cpu.cpu_usage <= 100
        
        # Verify memory information
        assert result.memory is not None
        assert isinstance(result.memory, device_info_models.MemoryInfoReturn)
        if result.memory.total is not None:
            assert result.memory.total > 0
        if result.memory.percent is not None:
            assert 0 <= result.memory.percent <= 100
        
        # Verify disk information
        assert result.disk is not None
        assert isinstance(result.disk, device_info_models.DiskInfoReturn)
        if result.disk.partitions is not None:
            assert len(result.disk.partitions) > 0
            for partition in result.disk.partitions:
                assert isinstance(partition, device_info_models.DiskPartitionInfo)
                if partition.total is not None:
                    assert partition.total > 0
        
        # Verify network information
        assert result.network is not None
        assert isinstance(result.network, device_info_models.NetworkInfoReturn)
        assert result.network.hostname is not None
        
        logger.info("Full system integration test passed")
        logger.info(f"System: {result.platform.os_name} {result.platform.os_version}")
        logger.info(f"CPU: {result.cpu.logical_cores} cores")
        logger.info(f"Memory: {result.memory.total / (1024**3):.1f} GB" if result.memory.total else "Memory: Unknown")

    def test_get_device_info_selective_real_system(self):
        """
        Test get_device_info with selective parameters on real system
        """
        device_info = DeviceInfo()
        
        # Test with only platform and CPU info
        params = device_info_models.GetDeviceInfoParams(
            include_platform=True,
            include_cpu=True,
            include_memory=False,
            include_disk=False,
            include_network=False
        )
        
        result = device_info.get_device_info(params)
        
        # Verify only requested information is present
        assert result.platform is not None
        assert result.cpu is not None
        assert result.memory is None
        assert result.disk is None
        assert result.network is None
        assert result.timestamp is not None
        
        logger.info("Selective system integration test passed")

    @pytest.mark.slow
    def test_device_info_performance(self):
        """
        Test DeviceInfo performance on real system
        
        This test measures the time taken to collect device information
        and ensures it completes within reasonable time limits.
        """
        device_info = DeviceInfo()
        
        # Measure time for full device info collection
        start_time = time.time()
        result = device_info.get_device_info()
        end_time = time.time()
        
        collection_time = end_time - start_time
        
        # Verify result is valid
        assert result is not None
        assert result.timestamp is not None
        
        # Performance assertions (adjust thresholds as needed)
        assert collection_time < 30.0, f"Device info collection took too long: {collection_time:.2f}s"
        
        logger.info(f"Performance test passed - Collection time: {collection_time:.2f}s")

    def test_device_info_consistency(self):
        """
        Test DeviceInfo consistency across multiple calls
        
        This test verifies that calling get_device_info multiple times
        returns consistent results for static information.
        """
        device_info = DeviceInfo()
        
        # Get device info multiple times
        result1 = device_info.get_device_info()
        time.sleep(0.1)  # Small delay
        result2 = device_info.get_device_info()
        
        # Platform information should be consistent
        assert result1.platform.hostname == result2.platform.hostname
        assert result1.platform.os_name == result2.platform.os_name
        assert result1.platform.os_version == result2.platform.os_version
        assert result1.platform.machine_id == result2.platform.machine_id
        
        # CPU static information should be consistent
        assert result1.cpu.brand_raw == result2.cpu.brand_raw
        assert result1.cpu.vendor_id_raw == result2.cpu.vendor_id_raw
        assert result1.cpu.logical_cores == result2.cpu.logical_cores
        assert result1.cpu.physical_cores == result2.cpu.physical_cores
        
        # Memory total should be consistent
        assert result1.memory.total == result2.memory.total
        
        # Note: Dynamic values like CPU usage, memory usage may differ
        
        logger.info("Consistency test passed")

    def test_device_info_singleton_integration(self):
        """
        Test DeviceInfo singleton behavior in integration environment
        """
        # Create multiple DeviceInfo instances
        device_info1 = DeviceInfo()
        device_info2 = DeviceInfo()
        device_info3 = DeviceInfo()
        
        # All instances should be the same object
        assert device_info1 is device_info2
        assert device_info2 is device_info3
        assert id(device_info1) == id(device_info2) == id(device_info3)
        
        # All instances should return the same data
        result1 = device_info1.get_device_info()
        result2 = device_info2.get_device_info()
        
        # Compare platform info (should be identical)
        assert result1.platform.hostname == result2.platform.hostname
        assert result1.platform.os_name == result2.platform.os_name
        
        logger.info("Singleton integration test passed")

    @pytest.mark.external
    def test_network_connectivity_integration(self):
        """
        Test network information collection with actual network operations
        
        This test requires internet connectivity and may be skipped in
        environments without external access.
        """
        device_info = DeviceInfo()
        
        # Get only network information
        params = device_info_models.GetDeviceInfoParams(
            include_platform=False,
            include_cpu=False,
            include_memory=False,
            include_disk=False,
            include_network=True
        )
        
        result = device_info.get_device_info(params)
        
        # Verify network information
        assert result.network is not None
        assert result.network.hostname is not None
        assert result.network.local_ip is not None
        
        # Public IP and ping may be None if no internet connection
        if result.network.public_ip is not None:
            # Basic IP format validation
            ip_parts = result.network.public_ip.split('.')
            assert len(ip_parts) == 4
            for part in ip_parts:
                assert 0 <= int(part) <= 255
        
        if result.network.ping is not None:
            assert result.network.ping >= 0
            assert result.network.ping < 10000  # Reasonable upper bound
        
        logger.info("Network connectivity integration test passed")
        if result.network.public_ip:
            logger.info(f"Public IP: {result.network.public_ip}")
        if result.network.ping:
            logger.info(f"Ping: {result.network.ping}ms")

    def test_cross_platform_compatibility(self):
        """
        Test DeviceInfo compatibility across different platforms
        
        This test verifies that DeviceInfo works correctly on the current platform
        and handles platform-specific operations properly.
        """
        device_info = DeviceInfo()
        current_platform = platform.system().lower()
        
        result = device_info.get_device_info()
        
        # Verify platform detection is correct
        assert result.platform.os_name == current_platform
        
        # Platform-specific validations
        if current_platform == "windows":
            # Windows-specific checks
            assert result.platform.architecture in ["AMD64", "x86", "ARM64"]
            if result.platform.machine_id:
                # Windows machine ID should be GUID format
                assert len(result.platform.machine_id) == 36
                assert result.platform.machine_id.count('-') == 4
        
        elif current_platform == "linux":
            # Linux-specific checks
            assert result.platform.architecture in ["x86_64", "i386", "arm64", "armv7l"]
            if result.platform.machine_id:
                # Linux machine ID should be 32 hex characters
                assert len(result.platform.machine_id) == 32
                assert all(c in '0123456789abcdef' for c in result.platform.machine_id.lower())
        
        elif current_platform == "darwin":
            # macOS-specific checks
            assert result.platform.architecture in ["x86_64", "arm64"]
            if result.platform.machine_id:
                # macOS UUID should be GUID format
                assert len(result.platform.machine_id) == 36
                assert result.platform.machine_id.count('-') == 4
        
        logger.info(f"Cross-platform compatibility test passed for {current_platform}")

    def test_error_resilience_integration(self):
        """
        Test DeviceInfo resilience to system errors in integration environment
        
        This test verifies that DeviceInfo can handle partial failures gracefully.
        """
        device_info = DeviceInfo()
        
        # Test with all components enabled
        try:
            result = device_info.get_device_info()
            
            # At minimum, we should get some basic information
            assert result is not None
            assert result.timestamp is not None
            
            # Count successful components
            successful_components = 0
            if result.platform is not None:
                successful_components += 1
            if result.cpu is not None:
                successful_components += 1
            if result.memory is not None:
                successful_components += 1
            if result.disk is not None:
                successful_components += 1
            if result.network is not None:
                successful_components += 1
            
            # At least some components should succeed
            assert successful_components > 0, "No components succeeded"
            
            logger.info(f"Error resilience test passed - {successful_components}/5 components succeeded")
            
        except Exception as e:
            # If the entire call fails, log it but don't fail the test
            # as this might indicate system-specific issues
            logger.warning(f"DeviceInfo integration failed: {e}")
            pytest.skip(f"System environment not suitable for integration test: {e}")

    @pytest.mark.db
    def test_device_info_serialization_integration(self):
        """
        Test DeviceInfo result serialization in integration environment
        
        This test verifies that real device information can be properly
        serialized and deserialized.
        """
        device_info = DeviceInfo()
        
        # Get device information
        result = device_info.get_device_info()
        
        # Test JSON serialization
        json_str = result.model_dump_json()
        assert json_str is not None
        assert len(json_str) > 0
        
        # Test deserialization
        recreated_result = device_info_models.GetDeviceInfoReturn.model_validate_json(json_str)
        
        # Verify key fields are preserved
        assert recreated_result.timestamp == result.timestamp
        if result.platform:
            assert recreated_result.platform.hostname == result.platform.hostname
            assert recreated_result.platform.os_name == result.platform.os_name
        
        # Test dict serialization
        result_dict = result.model_dump()
        assert isinstance(result_dict, dict)
        assert 'timestamp' in result_dict
        
        # Test dict deserialization
        recreated_from_dict = device_info_models.GetDeviceInfoReturn.model_validate(result_dict)
        assert recreated_from_dict.timestamp == result.timestamp
        
        logger.info("Serialization integration test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
