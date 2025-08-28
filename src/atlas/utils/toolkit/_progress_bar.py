#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _progress_bar
# @Created Time  : 2025/8/28 10:35
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_progress_bar: Reusable progress bar component with integrated logging**

This module provides a reusable progress bar component that:
    - Displays progress in the console using Rich at the bottom
    - Simultaneously logs progress updates to a file
    - Supports both determinate and indeterminate progress
    - Allows logging important information to both console and file
    - Randomly samples progress updates to avoid log spam
"""

import logging
import os
import random
from pathlib import Path
from rich.console import Console
from rich.progress import BarColumn, Progress, ProgressColumn, SpinnerColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from typing import List, Optional, Union, Tuple

from atlas.lib.models.parameters.progress_bar_params_md import ProgressBarParamsModel


class ProgressBar:
    """
    **ProgressBar: Dual-output progress bar with console display and file logging**

    Provides a reusable progress bar component that simultaneously displays
    progress in the console (at the bottom) and logs updates to a file.
    Supports both determinate and indeterminate progress.

    Class Attributes:
        - console: Rich Console instance for terminal output
        - params: Configuration parameters from ProgressBarParamsModel
        - progress: Rich Progress instance managing the display
        - task_id: Identifier for the current progress task
        - _logger: Logger instance for file output
        - _columns: List of progress bar columns to display
        - _last_logged_progress: Last progress percentage that was logged
        - _indeterminate_steps: Steps accumulated during indeterminate phase
        - _force_next_log: Flag to force logging on next update
    """

    def __init__(self, params: ProgressBarParamsModel):
        """
        **__init__: Initialize progress bar with configuration parameters**

        Sets up the progress bar component with specified display options
        and logging configuration.

        Args:
            params: ProgressBarParamsModel containing all configuration options

        Example:
            >>> params = ProgressBarParamsModel(description="Processing files", total_steps=100)
            >>> progress = ProgressBar(params)
        """
        self.console = Console()
        self._logger: Optional[logging.Logger] = None
        self.params = params
        self.progress: Optional[Progress] = None
        self.task_id: Optional[int] = None
        self._last_logged_progress: Optional[float] = None
        self._indeterminate_steps: int = 0
        self._force_next_log: bool = False

        self._setup_logger()
        self._columns = self._create_columns()

    def _setup_logger(self) -> None:
        """
        **_setup_logger: Configure file logging for progress updates**

        Creates a dedicated logger instance with file handler for recording
        progress updates. Ensures log directory exists and clears any
        existing handlers to prevent duplicates.
        """
        path = Path(self.params.log_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        logger_name = f"progress_bar_{id(self)}"
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(self.params.log_level)

        self._logger.handlers.clear()

        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter(self.params.log_format))
        self._logger.addHandler(handler)

    def _create_columns(self) -> List[ProgressColumn]:
        """
        **_create_columns: Build list of progress bar columns based on configuration**

        Constructs the column layout for the progress bar display according
        to the parameters specified in the configuration model.

        Returns:
            List[ProgressColumn]: Ordered list of columns to display
        """
        columns = list()

        columns.append(SpinnerColumn(style="green")) if self.params.show_spinner else None
        columns.append(TextColumn("[bold cyan]{task.description}[/bold cyan]"))
        columns.append(BarColumn(bar_width=40))
        columns.append(TextColumn(" ")) if self.params.show_percentage or self.params.show_time_elapsed or self.params.show_time_remaining else None
        columns.append( TextColumn("[bold green]{task.percentage:>3.0f}%[/bold green]")) if self.params.show_percentage else None
        columns.append(TextColumn(" | ", style="dim")) if self.params.show_percentage and (self.params.show_time_elapsed or self.params.show_time_remaining) else None
        columns.append(TimeElapsedColumn()) if self.params.show_time_elapsed else None
        columns.append(TextColumn(" / ", style="dim")) if self.params.show_time_elapsed and self.params.show_time_remaining and self.params.total_steps is not None else None
        columns.append(TimeRemainingColumn()) if self.params.show_time_remaining and self.params.total_steps is not None else None

        return columns

    def _log_progress(self, force: bool = False) -> None:
        """
        **_log_progress: Conditionally log current progress**

        Logs progress at key milestones (0%, 25%, 50%, 75%, 100%) and
        randomly samples other updates to avoid log spam.

        Args:
            force: Force logging regardless of sampling logic
        """
        if self.progress is None or self.task_id is None:
            return

        task = self.progress.tasks[self.task_id]

        if task.total is None:
            if force or random.random() < 0.1:
                self._logger.info(f"Progress: {task.description} - {task.completed} steps")
            return

        percentage = (task.completed / task.total) * 100

        should_log = force or self._force_next_log
        self._force_next_log = False

        if not should_log:
            if percentage == 0 or percentage == 100:
                should_log = True
            elif self._last_logged_progress is not None:
                if (percentage >= 25 and self._last_logged_progress < 25) or \
                   (percentage >= 50 and self._last_logged_progress < 50) or \
                   (percentage >= 75 and self._last_logged_progress < 75):
                    should_log = True
                else:
                    progress_delta = abs(percentage - self._last_logged_progress)
                    sample_probability = min(0.1, progress_delta * 0.01)
                    should_log = random.random() < sample_probability

        if should_log:
            self._logger.info(f"Progress: {task.description} - {task.completed}/{task.total} ({percentage:.1f}%)")
            self._last_logged_progress = percentage

    def start(self) -> None:
        """
        **start: Initialize and display the progress bar**

        Creates a Rich Progress instance with configured columns and starts
        the progress display. Also logs the start event to the configured log file.

        Note:
            - For determinate progress (total_steps is set), the bar starts at 0%
            - For indeterminate progress (total_steps is None), shows a spinner animation
            - Must be called before any update operations

        Example:
            >>> progress = ProgressBar(params)
            >>> progress.start()
        """
        self.progress = Progress(
            *self._columns,
            console=self.console,
            expand=self.params.expand,
            transient=self.params.transient,
            refresh_per_second=self.params.refresh_per_second,
        )

        self.progress.start()

        self._indeterminate_steps = 0

        self.task_id = self.progress.add_task(
            self.params.description,
            total=self.params.total_steps,
            start=self.params.total_steps is not None,
        )

        self._logger.info(f"Progress started: {self.params.description}")
        self._last_logged_progress = 0

    def update(self, advance: float = 1, description: Optional[str] = None) -> None:
        """
        **update: Advance the progress bar and optionally update description**

        Updates the progress display by advancing the completed steps and
        optionally changing the description text. Conditionally logs progress to file.

        Args:
            advance: Number of steps to advance (default: 1)
            description: New description text (optional)

        Note:
            - Does nothing if start() hasn't been called
            - For percentage display, advance is relative to total_steps
            - Logs progress at milestones and randomly samples other updates
            - Won't advance beyond total steps for determinate progress

        Example:
            >>> progress.update(5)
            >>> progress.update(1, description="Processing file 2 of 10")
        """
        if self.progress is None or self.task_id is None:
            return

        task = self.progress.tasks[self.task_id]

        if task.total is not None:
            remaining = task.total - task.completed
            advance = min(advance, remaining)

        if advance <= 0 and description is None:
            return

        kwargs = {}

        if description is not None:
            kwargs["description"] = description

        if task.total is None:
            self._indeterminate_steps += advance

        if advance > 0:
            self.progress.update(self.task_id, advance=advance, **kwargs)
            self._log_progress()
        else:
            self.progress.update(self.task_id, **kwargs)

    def set_total(self, total: int) -> None:
        """
        **set_total: Convert indeterminate progress to determinate**

        Sets the total number of steps for the progress bar, converting it from
        indeterminate (spinner) to determinate (percentage bar) mode.

        Args:
            total: Total number of steps for completion

        Note:
            - Useful when total steps are unknown at start time
            - Recreates progress display if time_remaining column needs to be added
            - Does nothing if start() hasn't been called

        Example:
            >>> progress.start()
            >>> file_count = count_files()
            >>> progress.set_total(file_count)
        """
        if self.progress is None or self.task_id is None:
            return

        completed_steps = min(self._indeterminate_steps, total)

        self.progress.stop()

        self.params.total_steps = total

        self._columns = self._create_columns()

        self.progress = Progress(
            *self._columns,
            console=self.console,
            expand=self.params.expand,
            transient=self.params.transient,
            refresh_per_second=self.params.refresh_per_second,
        )

        self.progress.start()

        self.task_id = self.progress.add_task(
            self.params.description,
            total=total,
            completed=completed_steps,
        )

        self._logger.info(f"Total steps set to: {total}")
        self._last_logged_progress = (completed_steps / total) * 100 if total > 0 else 0

    def complete(self) -> None:
        """
        **complete: Complete the progress bar and stop display**

        Completes the progress display by setting it to 100% and stops it.
        This should be used when the task has successfully completed.

        Note:
            - For determinate progress, automatically completes to 100%
            - For indeterminate progress, just stops the display
            - Always logs completion status to file

        Example:
            >>> progress.complete()
        """
        if self.progress is not None and self.task_id is not None:
            task = self.progress.tasks[self.task_id]
            if task.total is not None and task.completed < task.total:
                self.progress.update(self.task_id, completed=task.total)
                self._force_next_log = True
                self._log_progress()

            self.progress.stop()
            self._logger.info(f"Progress completed: {self.params.description}")

    def stop(self, completed: bool = False) -> None:
        """
        **stop: Stop the progress bar display**

        Stops the progress display without necessarily completing it.
        For determinate progress, optionally completes any remaining steps to reach 100%.

        Args:
            completed: Whether to complete the progress to 100% (default: False)

        Note:
            - Safe to call multiple times
            - For transient progress bars, removes the display from console
            - Logs appropriate status to file

        Example:
            >>> progress.stop()
            >>> progress.stop(completed=True)
        """
        if self.progress is not None and self.task_id is not None:
            task = self.progress.tasks[self.task_id]
            if completed and task.total is not None and task.completed < task.total:
                self.progress.update(self.task_id, completed=task.total)
                self._force_next_log = True
                self._log_progress()

            self.progress.stop()

            if completed:
                self._logger.info(f"Progress completed: {self.params.description}")
            else:
                self._logger.info(f"Progress stopped: {self.params.description}")

    def log(self, message: str, level: Union[str, int] = logging.INFO) -> None:
        """
        **log: Log important information to both console and file**

        Outputs a message to both the console (above the progress bar) and
        the log file. This allows displaying important information without
        interfering with the progress bar display.

        Args:
            message: The message to log
            level: The logging level (default: INFO)

        Example:
            >>> progress.log("Starting processing of large files")
            >>> progress.log("Error encountered", logging.ERROR)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())

        self._logger.log(level, message)

        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_name = logging.getLevelName(level)

        formatted_message = f"[dim]{timestamp}[/dim] [{level_name}] {message}"

        if level >= logging.ERROR:
            self.console.print(f"[dim]{timestamp}[/dim] [red][ERROR][/red] {message}")
        elif level >= logging.WARNING:
            self.console.print(f"[dim]{timestamp}[/dim] [yellow][WARNING][/yellow] {message}")
        elif level >= logging.INFO:
            self.console.print(f"[dim]{timestamp}[/dim] [blue][INFO][/blue] {message}")
        else:
            self.console.print(f"[dim]{timestamp}[/dim] [dim][DEBUG][/dim] {message}")