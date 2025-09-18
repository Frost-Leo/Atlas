#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_constants

This module provides unit tests for device information constants

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/18
- Modified : 2025/9/18
- License  : GPL-3.0
"""

import pytest
from logging import getLogger
from pydantic import ValidationError

from atlas.models.domain._infra.device_info.constants import Constants

logger = getLogger(__name__)


class TestConstants:
    """
    TestConstants: Test suite for Constants model
    """

    def test_constants_default_values(self):
        """
        Test that Constants model has correct default values
        """
        constants = Constants()
        
        # Windows constants
        assert constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH == r"SOFTWARE\Microsoft\Cryptography"
        assert constants.WINDOWS_MACHINE_GUID_KEY_NAME == "MachineGuid"
        
        # Linux constants
        assert constants.LINUX_MACHINE_ID_FILE_PATH == "/etc/machine-id"
        assert constants.LINUX_DBUS_MACHINE_ID_FILE_PATH == "/var/lib/dbus/machine-id"
        
        # macOS constants
        assert constants.MACOS_IOREG_COMMAND == ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"]
        assert constants.MACOS_UUID_PATTERN == r'"IOPlatformUUID"\s*=\s*"([^"]+)"'
        
        logger.info("Constants default values test passed")

    def test_constants_assignment_validation(self):
        """
        Test that Constants model validates assignments (validate_assignment=True)
        """
        constants = Constants()
        
        # Since the base model has frozen=False but validate_assignment=True,
        # we can modify fields but they will be validated
        original_path = constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH
        
        # Modify with valid string value
        constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH = "new_valid_path"
        assert constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH == "new_valid_path"
        
        # Reset to original
        constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH = original_path
        assert constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH == original_path
        
        logger.info("Constants assignment validation test passed")

    def test_constants_inheritance(self):
        """
        Test that Constants properly inherits from InternalBaseModel
        """
        constants = Constants()
        
        # Check for InternalBaseModel attributes
        assert hasattr(constants, 'version')
        assert hasattr(constants, 'created_at')
        
        # Verify version is set
        assert constants.version is not None
        assert isinstance(constants.version, str)
        
        # Verify created_at is set
        assert constants.created_at is not None
        
        logger.info("Constants inheritance test passed")

    def test_constants_serialization(self):
        """
        Test Constants serialization and deserialization
        """
        constants = Constants()
        
        # Test dict serialization - use alias_generator (snake_case)
        data_dict = constants.model_dump(by_alias=True)
        assert isinstance(data_dict, dict)
        
        # With alias_generator=to_snake, field names should be snake_case
        expected_fields = [
            'windows_machine_guid_registry_path',
            'windows_machine_guid_key_name', 
            'linux_machine_id_file_path',
            'linux_dbus_machine_id_file_path',
            'macos_ioreg_command',
            'macos_uuid_pattern'
        ]
        
        for field in expected_fields:
            assert field in data_dict, f"Expected field {field} not found in serialized data"
        
        # Test JSON serialization with aliases
        json_str = constants.model_dump_json(by_alias=True)
        assert json_str is not None
        assert len(json_str) > 0
        
        # Test JSON deserialization (using alias format)
        recreated_from_json = Constants.model_validate_json(json_str)
        assert recreated_from_json.LINUX_MACHINE_ID_FILE_PATH == constants.LINUX_MACHINE_ID_FILE_PATH
        assert recreated_from_json.WINDOWS_MACHINE_GUID_REGISTRY_PATH == constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH
        assert recreated_from_json.MACOS_IOREG_COMMAND == constants.MACOS_IOREG_COMMAND
        
        # Test creating new instance with snake_case aliases
        new_constants = Constants(
            windows_machine_guid_registry_path=r"SOFTWARE\Test",
            linux_machine_id_file_path="/test/machine-id"
        )
        assert new_constants.WINDOWS_MACHINE_GUID_REGISTRY_PATH == r"SOFTWARE\Test"
        assert new_constants.LINUX_MACHINE_ID_FILE_PATH == "/test/machine-id"
        
        logger.info("Constants serialization test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
