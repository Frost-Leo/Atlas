# Device Info Module

## Overview

The Device Info module provides comprehensive system information collection capabilities for the Atlas platform. It implements a singleton-based service that gathers platform, CPU, memory, disk, and network information from the host system.

## Architecture

### 📊 Interactive Architecture Diagram

<iframe src="../../../../assets/diagrams/device-info-architecture.html" 
        width="100%" 
        height="600" 
        frameborder="0" 
        style="border: 1px solid #ddd; border-radius: 8px; margin: 20px 0;">
</iframe>

> Above is the draggable interactive architecture diagram. If it doesn't display, please [click here](../../../../assets/diagrams/device-info-architecture.html) to open in a new window.

### Static Architecture Diagram

```mermaid
graph TB
    A[DeviceInfo Singleton] --> B[Platform Info]
    A --> C[CPU Info]
    A --> D[Memory Info]
    A --> E[Disk Info]
    A --> F[Network Info]
    
    B --> B1[OS Detection]
    B --> B2[Machine ID]
    B --> B3[System Specs]
    
    C --> C1[CPU Details]
    C --> C2[Performance Metrics]
    C --> C3[Cache Info]
    
    D --> D1[Memory Usage]
    D --> D2[Swap Info]
    D --> D3[Buffer/Cache]
    
    E --> E1[Partition Info]
    E --> E2[Disk Usage]
    E --> E3[I/O Statistics]
    
    F --> F1[Network Interfaces]
    F --> F2[IP Information]
    F --> F3[Performance Tests]
```

## Key Features

- **Cross-Platform Support**: Windows, Linux, and macOS
- **Comprehensive Information**: Platform, CPU, memory, disk, and network data
- **Selective Collection**: Choose which information to collect
- **Thread-Safe Singleton**: Single instance across the application
- **Error Resilience**: Graceful handling of unavailable information
- **Performance Optimized**: Efficient data collection with fallback mechanisms

## Usage Example

```python
from atlas.core._infra.device_info import DeviceInfo

# Get device info instance
device_info = DeviceInfo()

# Collect all information
result = device_info.get_device_info()

# Access collected data
print(f"OS: {result.platform.os_name}")
print(f"CPU: {result.cpu.brand_raw}")
print(f"Memory: {result.memory.total / (1024**3):.1f} GB")
```

## Documentation

- [**API Reference**](api-reference.md) - Complete API documentation

## Cross-Platform Compatibility

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| Platform Info | ✅ | ✅ | ✅ |
| Machine ID | Registry | `/etc/machine-id` | IOKit UUID |
| CPU Info | ✅ | ✅ | ✅ |
| Memory Info | Basic | Extended | Basic |
| Disk Info | NTFS | All FS | APFS/HFS+ |
| Network Info | ✅ | ✅ | ✅ |
| Ping Test | Chinese/English | English | English |

## Performance Characteristics

- **Collection Time**: ~100-500ms for full system scan
- **Memory Usage**: <10MB during collection
- **Thread Safety**: Full thread-safe implementation
- **Caching**: Intelligent caching for expensive operations
- **Fallback**: Multiple fallback mechanisms for reliability