#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @FileName      : _init_meta
# @Created Time  : 2025/8/28 9:19
# @Author        : FrostLeo
# @Email         : FrostLeo.Dev@gmail.com
# -----------------------------------------------------------------------------

"""
**_init_meta: Metaclass for automatic class registration with ordering**

This module provides a metaclass that automatically registers non-abstract classes
into a registry with support for custom ordering based on the '_order' attribute.
Classes are automatically sorted whenever a new class is registered.
"""

from abc import ABCMeta
from collections import OrderedDict
from typing import Any, Dict, Tuple, Type


class InitMeta(ABCMeta):
    """
    **InitMeta: Metaclass for automatic class registration and ordering**

    A metaclass that extends ABCMeta to automatically register all non-abstract
    classes into a sorted registry. Classes are ordered based on their '_order'
    attribute, with the registry being re-sorted after each new registration.

    Class Attributes:
        _registry: Ordered dictionary containing registered classes by name

    Class Methods:
        - get_all: Retrieve all registered classes in sorted order
    """

    _registry: Dict[str, Type] = {}
    """Registry dictionary storing class name to class type mappings"""

    def __new__(mcs: Type['InitMeta'], name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs) -> Type:
        """
        **__new__: Create and register new classes**

        Creates a new class and automatically registers it if it has no abstract methods.
        After registration, the entire registry is re-sorted based on '_order' attributes.

        Args:
            mcs: The metaclass itself (InitMeta)
            name: Name of the class being created
            bases: Tuple of base classes
            namespace: Class namespace dictionary containing attributes and methods
            **kwargs: Additional keyword arguments

        Returns:
            Type: The newly created class

        Note:
            Only classes without abstract methods are registered. Abstract base
            classes are skipped to prevent registration of incomplete implementations.
        """
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        if not cls.__abstractmethods__:
            mcs._registry[name] = cls

            mcs._sort_registry()

        return cls

    @classmethod
    def _sort_registry(mcs) -> None:
        """
        **_sort_registry: Sort the registry by class order values**

        Re-sorts the entire registry based on each class's '_order' attribute.
        Classes without an '_order' attribute default to 0. The registry is
        rebuilt as an OrderedDict to maintain the sorted order.

        Note:
            This method is called automatically after each class registration
            to ensure the registry remains sorted at all times.
        """
        sorted_items = sorted(
            mcs._registry.items(),
            key=lambda item: getattr(item[1], '_order', 0)
        )

        mcs._registry = OrderedDict(sorted_items)

    @classmethod
    def get_all(mcs) -> Dict[str, Type]:
        """
        **get_all: Retrieve all registered classes in sorted order**

        Returns a copy of the complete registry of registered classes, ensuring
        they are sorted by their '_order' attribute before returning. This method
        provides a safe way to access the registry while guaranteeing the order
        is current and preventing external modifications.

        Returns:
            Dict[str, Type]: OrderedDict copy containing all registered classes,
                            sorted by their '_order' attribute (ascending)

        Example:
            >>> registry = InitMeta.get_all()
            >>> for name, cls in registry.items():
            ...     print(f"{name}: order={getattr(cls, '_order', 0)}")

        Note:
            Returns a copy of the registry to prevent external modifications.
            The original registry remains protected within the metaclass.
        """
        mcs._sort_registry()
        return OrderedDict(mcs._registry)