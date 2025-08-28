#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : progress_bar_params_md
# @Created Time  : 2025/8/28 10:38
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**progress_bar_params_md: Progress bar parameters model module**

This module defines a Pydantic model for configuring progress bar components
with the following features:
    - Configurable progress bar display options
    - Integrated logging with customizable format and levels
    - Support for both determinate and indeterminate progress
    - Flexible column configuration for progress display
"""

import os
from pathlib import Path
from pydantic import Field
from typing import Optional, Union, List

from atlas.lib.models import AtlasBaseModel


class ProgressBarParamsModel(AtlasBaseModel):
    """
    **ProgressBarParamsModel: Progress bar configuration model**

    Defines and validates all parameters required for creating reusable progress bars
    with integrated logging capabilities.

    Class Attributes:
        - description: Progress bar description text
        - total_steps: Total number of steps for progress calculation
        - log_file_path: Path to the log file for progress tracking
        - log_level: Logging level for progress messages
        - log_format: Format string for log messages
        - show_spinner: Whether to display spinner animation
        - show_time_elapsed: Whether to show elapsed time
        - show_time_remaining: Whether to show estimated remaining time
        - show_percentage: Whether to show completion percentage
        - expand: Whether to expand progress bar to full terminal width
        - transient: Whether to clear progress bar after completion
        - refresh_per_second: Progress bar refresh rate
    """

    description: str = Field(default='Processing', description='Description text displayed alongside the progress bar')
    """Progress bar description that helps users understand what is being processed"""

    total_steps: Optional[int] = Field(default=None, description='Total number of steps for progress calculation. None indicates indeterminate progress')
    """Total steps for the progress bar. When set to None, displays an indeterminate progress animation (spinner) until a total is provided via set_total()"""

    log_file_path: Optional[Union[str, Path]] = Field(default_factory=lambda: os.path.join(os.getenv('ATLAS_LOGS_ROOT', './logs'), 'bootstrap', 'progress.log'), description='Path to the log file where progress updates will be written')
    """Log file path for recording progress updates. Defaults to {ATLAS_LOGS_ROOT}/bootstrap/progress.log. Creates parent directories if needed"""

    log_level: str = Field(default='INFO', description='Logging level for progress messages (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    """Logging level that determines which messages are written to the log file. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"""

    log_format: str = Field(default='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s', description='Format string for log messages using Python logging format')
    """Log message format string using loguru-style syntax with color tags and time formatting. Supports placeholders: {time}, {level}, {name}, {function}, {line}, {message}"""

    show_spinner: bool = Field(default=True, description='Whether to display a spinner animation for indeterminate progress')
    """Shows a spinning animation when progress is indeterminate (total_steps is None)"""

    show_time_elapsed: bool = Field(default=True, description='Whether to display elapsed time since progress started')
    """Displays the time elapsed since the progress bar was started"""

    show_time_remaining: bool = Field(default=True, description='Whether to display estimated time remaining (only for determinate progress)')
    """Shows estimated time to completion based on current progress rate. Only displayed when total_steps is set (determinate progress)"""

    show_percentage: bool = Field(default=True, description='Whether to display completion percentage')
    """Displays progress as a percentage (e.g., 45.2%)"""

    expand: bool = Field(default=False, description='Whether to expand the progress bar to full terminal width')
    """When True, the progress bar stretches to fill the entire terminal width. When False, uses only the necessary width for content"""

    transient: bool = Field(default=False, description='Whether to remove the progress bar from terminal after completion')
    """When True, the progress bar disappears after completion, leaving a clean terminal. Useful for temporary progress indicators that shouldn't clutter the output"""

    refresh_per_second: int = Field(default=20, ge=1, le=60, description='Number of times per second to refresh the progress display')
    """Controls the visual update frequency of the progress bar. Higher values provide smoother animation but use more CPU"""

    custom_columns: Optional[List[str]] = Field(default=None, description='List of custom column names to display in the progress bar')
    """Optional list of column identifiers for customizing progress bar layout. Supported values: 'spinner', 'description', 'bar', 'percentage', 'time_elapsed', 'time_remaining', 'speed', 'eta'"""