#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _init_base
# @Created Time  : 2025/8/28 9:19
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_init_base: Base class for automatic initialization module registration**

This module provides the abstract base class for all initialization modules.
Classes inheriting from InitBase are automatically registered via the InitMeta
metaclass and can be initialized in a specific order based on their _order attribute.
"""

from abc import abstractmethod

from atlas.core.initialization.base._init_meta import InitMeta


class InitBase(metaclass=InitMeta):
    """
    **InitBase: Base class for auto-registered initialization modules**

    All subclasses that implement the initialize method will be automatically
    registered and can be initialized in order based on their _order attribute.

    Class Attributes:
        _order: Integer determining initialization order (default: 0)
    """

    _order: int = 0
    """Registry sorting basis"""

    @abstractmethod
    def initialize(self) -> bool:
        """
        **initialize: Perform initialization logic**

        This method must be implemented by all subclasses to define
        their specific initialization behavior.

        Returns:
            bool: True if initialization succeeded, False otherwise
        """
        pass