#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _init_directory
# @Created Time  : 2025/8/28 15:17
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_init_directory: Directory structure initialization module**

This module provides automatic creation of required project directories
during the initialization phase with the following features:
    - Creates all required Atlas project directories
    - Provides progress tracking with integrated logging
    - Handles missing environment variables gracefully
    - Ensures proper directory permissions and structure
"""

import os
import time
from pathlib import Path
from typing import ClassVar, List

from atlas.utils.toolkit import ProgressBar
from atlas.core.initialization.base import InitBase
from atlas.lib.models.configuration.env_vars_md import EnvVarsModel
from atlas.lib.models.parameters.progress_bar_params_md import ProgressBarParamsModel


class InitDirectory(InitBase):
    """
    **InitDirectory: Project directory structure initialization**

    Automatically creates all required project directories defined in
    REQUIRED_DIRECTORIES during the initialization phase. Provides
    progress tracking and comprehensive logging of the process.

    Class Attributes:
        - _order: Initialization order priority (1 = early stage)
        - REQUIRED_DIRECTORIES: List of environment variable names for directories

    Instance Attributes:
        - env_vars: Environment variables model instance
        - progress_bar_params: Progress bar configuration
        - progress_bar: Progress tracking component
    """

    _order: int = 1
    """Early initialization stage to ensure directories exist before other components"""

    REQUIRED_DIRECTORIES: ClassVar[List[str]] = [
        'ATLAS_ETC_ROOT',
        'ATLAS_LOGS_ROOT',
        'ATLAS_DATA_ROOT',
    ]
    """Environment variable names for required project directories"""

    def __init__(self):
        """
        **__init__: Initialize directory creator with progress tracking**

        Sets up the environment variables model and configures progress
        tracking for directory creation. Handles cases where ATLAS_ROOT
        might not be set by using a fallback log location.
        """
        super().__init__()
        self.env_vars = EnvVarsModel()

        if self.env_vars.ATLAS_ROOT:
            log_path = Path(self.env_vars.ATLAS_ROOT) / 'logs' / 'bootstrap' / 'initialization' / 'init_directory.log'
        else:
            log_path = Path('./logs/bootstrap/initialization/init_directory.log')

        log_path.parent.mkdir(parents=True, exist_ok=True)

        self.progress_bar_params = ProgressBarParamsModel(
            description=self.__class__.__name__,
            total_steps=len(self.REQUIRED_DIRECTORIES),
            log_file_path=str(log_path),
        )
        self.progress_bar = ProgressBar(params=self.progress_bar_params)

    def initialize(self) -> bool:
        """
        **initialize: Create all required project directories**

        Iterates through REQUIRED_DIRECTORIES and creates each directory
        if it doesn't exist. Provides detailed progress tracking and
        handles errors gracefully.

        Returns:
            bool: True if all directories were created successfully,
                  False if any errors occurred (missing env vars, permissions, etc.)

        Note:
            - Missing environment variables are logged as warnings
            - Existing directories are skipped without error
            - All operations are logged for debugging purposes
        """
        has_errors = False
        created_count = 0
        skipped_count = 0
        missing_count = 0

        try:
            self.progress_bar.start()
            self.progress_bar.log(f"Starting directory initialization for {len(self.REQUIRED_DIRECTORIES)} directories",
                                  "INFO")
            time.sleep(0.2)

            for index, env_var_name in enumerate(self.REQUIRED_DIRECTORIES, 1):
                self.progress_bar.log(f"[{index}/{len(self.REQUIRED_DIRECTORIES)}] Processing {env_var_name}", "DEBUG")

                path = getattr(self.env_vars, env_var_name)

                if not path:
                    self.progress_bar.log(f"Environment variable {env_var_name} is not set - skipping", "WARNING")
                    self.progress_bar.update(advance=1)
                    has_errors = True
                    missing_count += 1
                    time.sleep(0.3)
                    continue

                time.sleep(0.2)

                path_obj = Path(path)
                try:
                    if not path_obj.exists():
                        self.progress_bar.log(f"Creating directory: {path}", "INFO")
                        path_obj.mkdir(parents=True, exist_ok=True)
                        self.progress_bar.log(f"Successfully created: {path}", "INFO")
                        created_count += 1
                        time.sleep(0.1)
                    else:
                        self.progress_bar.log(f"Directory already exists: {path}", "DEBUG")
                        skipped_count += 1

                except PermissionError as e:
                    self.progress_bar.log(f"Permission denied creating {path}: {e}", "ERROR")
                    has_errors = True

                except Exception as e:
                    self.progress_bar.log(f"Failed to create {path}: {e}", "ERROR")
                    has_errors = True

                self.progress_bar.update(advance=1)
                time.sleep(0.3)

            time.sleep(0.2)
            self.progress_bar.log(f"Directory initialization summary:", "INFO")
            self.progress_bar.log(f"  - Created: {created_count} directories", "INFO")
            self.progress_bar.log(f"  - Skipped (existing): {skipped_count} directories", "INFO")
            if missing_count > 0:
                self.progress_bar.log(f"  - Missing env vars: {missing_count} directories", "WARNING")

            if not has_errors:
                self.progress_bar.complete()
                self.progress_bar.log("Directory initialization completed successfully", "INFO")
                return True
            else:
                self.progress_bar.stop(completed=False)
                self.progress_bar.log("Directory initialization completed with errors", "ERROR")
                return False

        except Exception as e:
            self.progress_bar.log(f"Unexpected error during directory initialization: {e}", "ERROR")
            self.progress_bar.stop()
            return False


