# Device Info API Reference

## DeviceInfo Class

### Class Definition

```python
class DeviceInfo:
    """
    Singleton class for collecting comprehensive device information.
    
    This class provides a unified interface for gathering system information
    including platform details, CPU specifications, memory usage, disk status,
    and network configuration.
    """
```

### Constructor

```python
def __new__(cls, *args, **kwargs) -> "DeviceInfo"
```

**Description**: Creates or returns the singleton instance of DeviceInfo.

**Returns**: `DeviceInfo` - The singleton instance

**Example**:
```python
device_info = DeviceInfo()  # First call creates instance
same_instance = DeviceInfo()  # Subsequent calls return same instance
assert device_info is same_instance  # True
```

---

## Main Methods

### get_device_info()

```python
def get_device_info(
    self,
    params: Optional[GetDeviceInfoParams] = None
) -> GetDeviceInfoReturn
```

**Description**: Collects comprehensive device information based on specified parameters.

**Parameters**:
- `params` (`Optional[GetDeviceInfoParams]`): Configuration parameters for information collection
  - If `None`, collects all available information (default behavior)

**Returns**: `GetDeviceInfoReturn` - Complete device information object

**Raises**: 
- `RuntimeError`: If critical information collection fails

**Example**:
```python
# Collect all information (default)
result = device_info.get_device_info()

# Collect specific information
from atlas.models.domain._infra.device_info.models import GetDeviceInfoParams

params = GetDeviceInfoParams(
    include_platform=True,
    include_cpu=True,
    include_memory=False,
    include_disk=False,
    include_network=False
)
result = device_info.get_device_info(params)
```

---

## Parameter Models

### GetDeviceInfoParams

```python
class GetDeviceInfoParams(InternalBaseModel):
    include_platform: bool = True
    include_cpu: bool = True
    include_memory: bool = True
    include_disk: bool = True
    include_network: bool = True
```

**Description**: Configuration parameters for selective information collection.

**Fields**:
- `include_platform`: Whether to collect platform information
- `include_cpu`: Whether to collect CPU information
- `include_memory`: Whether to collect memory information
- `include_disk`: Whether to collect disk information
- `include_network`: Whether to collect network information

---

## Return Models

### GetDeviceInfoReturn

```python
class GetDeviceInfoReturn(InternalBaseModel):
    platform: Optional[PlatformInfoReturn] = None
    cpu: Optional[CPUInfoReturn] = None
    memory: Optional[MemoryInfoReturn] = None
    disk: Optional[DiskInfoReturn] = None
    network: Optional[NetworkInfoReturn] = None
    timestamp: float
```

**Description**: Main container for all collected device information.

**Fields**:
- `platform`: Platform and OS information (if requested)
- `cpu`: CPU specifications and metrics (if requested)
- `memory`: Memory usage statistics (if requested)
- `disk`: Disk information and I/O stats (if requested)
- `network`: Network configuration and tests (if requested)
- `timestamp`: Unix timestamp when collection was performed

---

## Error Handling

### Exception Types

- **`RuntimeError`**: Raised when critical information collection fails
- **Internal Exceptions**: Caught and handled gracefully, returning `None` for unavailable data

### Error Scenarios

1. **Permission Denied**: Some system information may require elevated privileges
2. **Platform Incompatibility**: Certain features may not be available on all platforms
3. **Network Timeouts**: Network tests may fail due to connectivity issues
4. **Hardware Access**: Some hardware information may be inaccessible

### Graceful Degradation

```python
try:
    result = device_info.get_device_info()
    
    # Check if specific information is available
    if result.platform:
        print(f"OS: {result.platform.os_name}")
    else:
        print("Platform information unavailable")
        
    if result.network and result.network.ping:
        print(f"Ping: {result.network.ping}ms")
    else:
        print("Network test unavailable")
        
except RuntimeError as e:
    print(f"Failed to collect device information: {e}")
```

---

## Thread Safety

The DeviceInfo class is fully thread-safe:

- **Singleton Creation**: Uses thread-safe lazy initialization with double-checked locking
- **Method Execution**: All methods are stateless and can be called concurrently
- **No Shared State**: No mutable shared state between method calls

```python
import threading

def collect_info():
    device_info = DeviceInfo()
    return device_info.get_device_info()

# Safe to call from multiple threads
threads = [threading.Thread(target=collect_info) for _ in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
```

---

## Performance Considerations

### Collection Times

| Component | Typical Time | Notes |
|-----------|--------------|-------|
| Platform | 10-50ms | Fast, mostly system calls |
| CPU | 50-150ms | Includes brief usage sampling |
| Memory | 5-20ms | Very fast, direct system info |
| Disk | 100-300ms | Depends on partition count |
| Network | 3000-5000ms | Includes 3-second speed test |

### Optimization Tips

1. **Selective Collection**: Only collect needed information
2. **Caching**: Cache results for repeated calls within short timeframes
3. **Background Collection**: Perform collection in background threads for UI applications
4. **Timeout Handling**: Set appropriate timeouts for network operations

```python
# Fast collection (no network tests)
quick_info = device_info.get_device_info(
    GetDeviceInfoParams(include_network=False)
)

# Network-only collection
network_info = device_info.get_device_info(
    GetDeviceInfoParams(
        include_platform=False,
        include_cpu=False,
        include_memory=False,
        include_disk=False,
        include_network=True
    )
)
```