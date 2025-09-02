# Atlas

**Enterprise e-commerce middle platform built on Django REST Framework with modular marketplace integrations and analytics**

[![Python](https://img.shields.io/badge/python-3.13-3776ab?logo=python&logoColor=white)](https://python.org) [![Django](https://img.shields.io/badge/django-5.2.5-092e20?logo=django&logoColor=white)](https://djangoproject.com) [![DRF](https://img.shields.io/badge/DRF-3.16.0-a30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/) [![Pydantic](https://img.shields.io/badge/pydantic-2.11.7-e92063?logo=pydantic&logoColor=white)](https://pydantic.dev) [![License](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE)



## Overview

Atlas is a comprehensive e-commerce middle platform that integrates backend APIs from Amazon, Alibaba, JD, and other major e-commerce platforms. Through automated data collection, cleaning, processing, and transformation, Atlas consolidates multi-platform marketplace data into a unified, actionable business intelligence system.

Built on Django REST Framework with modern type safety through Pydantic, Atlas provides enterprise-grade tools for real-time data analytics, intelligent inventory management, automated marketplace synchronization, and comprehensive business insights across all connected platforms.



## 🚀 Key Features

### **Modern Type Safety with Pydantic**

- **Full Pydantic Integration**: Type-safe input/output validation across the entire application
- **Smart Data Bridge**: Seamless integration between Django Serializers and Pydantic models
- **Auto-validation**: Self-adaptive parameter validation for all API endpoints

### **Zero-Configuration Architecture**

- **External Configuration**: Pydantic-powered configuration with automatic external file loading
- **Environment Isolation**: Built-in support for base/dev/prod/test environments
- **Hot Reload**: Runtime configuration updates without service restart
- **Deep Integration**: Django Settings + Dynaconf + Pydantic unified configuration system

### **Enterprise Exception System**

- **Dual-Layer Design**: 
  - **Internal Exceptions**: System-level errors with Windows-style error codes for developers
  - **External Exceptions**: User-friendly HTTP status code integrated responses
- **Auto-Conversion**: Runtime automatic conversion from internal to external exceptions
- **Factory Pattern**: Exception handler factory for consistent error processing

### **Modern Logging Infrastructure**

- **Loguru Proxy**: Low-intrusion replacement for Django's logging system
- **JSON Output**: Structured logging with custom sink implementation
- **ELK Ready**: Pre-configured for enterprise log collection and analysis systems
- **Zero Migration**: Maintains existing Django logging configurations

### **Modular Application Ecosystem**

- **Plugin Architecture**: Plug-and-play application modules for different marketplaces
- **Unified Integration**: Standardized interfaces for Amazon, Alibaba, JD, and other platforms
- **Application Registry**: Automatic discovery and registration of Atlas applications
- **Extensible Design**: Easy development of custom marketplace integrations