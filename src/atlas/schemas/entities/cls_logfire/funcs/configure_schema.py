#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
configure_schema

This module provides 

- Author   : FrostLeo <frostleo.dev@gmail.com>
- Created  : 2025/9/3 
- Modified : 2025/9/3
- License  : GPL-3.0
"""

from pathlib import Path
from pydantic import Field
from typing import Literal, Optional, Sequence, TYPE_CHECKING, Union

from atlas.schemas.base import BaseSchema

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import SpanProcessor
    from logfire._internal.constants import LevelName
    from logfire import AdvancedOptions, CodeSource, ConsoleOptions, Logfire, MetricsOptions, SamplingOptions, ScrubbingOptions


class ConfigureParamsSchema(BaseSchema):
    """
    ConfigureParamsSchema: The schema of the parameters for the Logfire.configure() function.

    Attributes:
        local (bool): If True, configures and returns a Logfire instance that is not the default global instance. Use this to create multiple separate configurations, e.g. to send to different projects.
        send_to_logfire (Optional[Union[bool, Literal['if-token-present']]]): Whether to send logs to logfire.dev. If 'if-token-present' is provided, logs will only be sent if a token is present.
        token (Optional[str]): The project token for authentication.
        service_name (Optional[str]): Name of this service.
        service_version (Optional[str]): Version of this service.
        environment (Optional[str]): The environment this service is running in, e.g. 'staging' or 'prod'.
        console (Optional[Union[ConsoleOptions, Literal[False]]]): Whether to control terminal output. False disables console output.
        config_dir (Optional[Union[Path, str]]): Directory that contains the pyproject.toml file for this project.
        data_dir (Optional[Union[Path, str]]): Directory to store credentials and logs.
        additional_span_processors (Optional[Sequence[SpanProcessor]]): Span processors to use in addition to the default processor.
        metrics (Optional[Union[MetricsOptions, Literal[False]]]): Set to False to disable sending all metrics, or provide a MetricsOptions object to configure metrics.
        scrubbing (Optional[Union[ScrubbingOptions, Literal[False]]]): Options for scrubbing sensitive data. Set to False to disable.
        inspect_arguments (Optional[bool]): Whether to enable f-string magic.
        sampling (Optional[SamplingOptions]): Sampling options.
        min_level (Optional[Union[int, LevelName]]): Minimum log level for logs and spans to be created.
        add_baggage_to_attributes (bool): Set to False to prevent OpenTelemetry Baggage from being added to spans as attributes.
        code_source (Optional[CodeSource]): Settings for the source code of the project.
        distributed_tracing (Optional[bool]): Whether to extract incoming trace context. True disables warning, False suppresses extraction.
        advanced (Optional[AdvancedOptions]): Advanced options primarily used for testing by Logfire developers.
    """

    local: bool = Field(default=False, description="If True, configures and returns a Logfire instance that is not the default global instance. Use this to create multiple separate configurations, e.g. to send to different projects.")
    send_to_logfire: Optional[Union[bool, Literal['if-token-present']]] = Field(default=None, description="Whether to send logs to logfire.dev. If 'if-token-present' is provided, logs will only be sent if a token is present.")
    token: Optional[str] = Field(default=None, description="The project token for authentication.")
    service_name: Optional[str] = Field(default=None, description="Name of this service.")
    service_version: Optional[str] = Field(default=None, description="Version of this service.")
    environment: Optional[str] = Field(default=None, description="The environment this service is running in, e.g. 'staging' or 'prod'.")
    console: Optional[Union['ConsoleOptions', Literal[False]]] = Field(default=None, description="Whether to control terminal output. False disables console output.")
    config_dir: Optional[Union[Path, str]] = Field(default=None, description="Directory that contains the pyproject.toml file for this project.")
    data_dir: Optional[Union[Path, str]] = Field(default=None, description="Directory to store credentials and logs.")
    additional_span_processors: Optional[Sequence['SpanProcessor']] = Field(default=None, description="Span processors to use in addition to the default processor.")
    metrics: Optional[Union['MetricsOptions', Literal[False]]] = Field(default=None, description="Set to False to disable sending all metrics, or provide a MetricsOptions object to configure metrics.")
    scrubbing: Optional[Union['ScrubbingOptions', Literal[False]]] = Field(default=None, description="Options for scrubbing sensitive data. Set to False to disable.")
    inspect_arguments: Optional[bool] = Field(default=None, description="Whether to enable f-string magic.")
    sampling: Optional['SamplingOptions'] = Field(default=None, description="Sampling options.")
    min_level: Optional[Union[int, 'LevelName']] = Field(default=None, description="Minimum log level for logs and spans to be created.")
    add_baggage_to_attributes: bool = Field(default=True, description="Set to False to prevent OpenTelemetry Baggage from being added to spans as attributes.")
    code_source: Optional['CodeSource'] = Field(default=None, description="Settings for the source code of the project.")
    distributed_tracing: Optional[bool] = Field(default=None, description="Whether to extract incoming trace context. True disables warning, False suppresses extraction.")
    advanced: Optional['AdvancedOptions'] = Field(default=None, description="Advanced options primarily used for testing by Logfire developers.")


class ConfigureReturnSchema(BaseSchema):
    """
    ConfigureReturnSchema: The schema of the output parameter for the Logfire.configure() function.

    Attributes:
        Logfire (Logfire): Logfire instance to configure.
    """
    Logfire: 'Logfire' = Field(description="The Logfire instance.")


class ConfigureSchema:
    """
    ConfigureSchema: Container for Logfire configure function schemas

    Attributes:
        Params (ConfigureParamsSchema): Input parameters schema.
        Return (ConfigureReturnSchema): Output parameters schema.
    """

    Params = ConfigureParamsSchema
    Return = ConfigureReturnSchema