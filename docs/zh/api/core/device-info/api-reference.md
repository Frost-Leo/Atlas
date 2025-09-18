# 设备信息 API 参考

## DeviceInfo 类

### 类定义

```python
class DeviceInfo:
    """
    用于收集全面设备信息的单例类。
    
    该类提供统一接口来收集系统信息，包括平台详情、CPU 规格、
    内存使用情况、磁盘状态和网络配置。
    """
```

### 构造函数

```python
def __new__(cls, *args, **kwargs) -> "DeviceInfo"
```

**描述**: 创建或返回 DeviceInfo 的单例实例。

**返回**: `DeviceInfo` - 单例实例

**示例**:
```python
device_info = DeviceInfo()  # 首次调用创建实例
same_instance = DeviceInfo()  # 后续调用返回相同实例
assert device_info is same_instance  # True
```

---

## 主要方法

### get_device_info()

```python
def get_device_info(
    self,
    params: Optional[GetDeviceInfoParams] = None
) -> GetDeviceInfoReturn
```

**描述**: 根据指定参数收集全面的设备信息。

**参数**:
- `params` (`Optional[GetDeviceInfoParams]`): 信息收集的配置参数
  - 如果为 `None`，则收集所有可用信息（默认行为）

**返回**: `GetDeviceInfoReturn` - 完整的设备信息对象

**异常**: 
- `RuntimeError`: 当关键信息收集失败时抛出

**示例**:
```python
# 收集所有信息（默认）
result = device_info.get_device_info()

# 收集特定信息
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

## 参数模型

### GetDeviceInfoParams

```python
class GetDeviceInfoParams(InternalBaseModel):
    include_platform: bool = True
    include_cpu: bool = True
    include_memory: bool = True
    include_disk: bool = True
    include_network: bool = True
```

**描述**: 选择性信息收集的配置参数。

**字段**:
- `include_platform`: 是否收集平台信息
- `include_cpu`: 是否收集 CPU 信息
- `include_memory`: 是否收集内存信息
- `include_disk`: 是否收集磁盘信息
- `include_network`: 是否收集网络信息

---

## 返回模型

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

**描述**: 所有收集的设备信息的主容器。

**字段**:
- `platform`: 平台和操作系统信息（如果请求）
- `cpu`: CPU 规格和指标（如果请求）
- `memory`: 内存使用统计（如果请求）
- `disk`: 磁盘信息和 I/O 统计（如果请求）
- `network`: 网络配置和测试（如果请求）
- `timestamp`: 执行收集时的 Unix 时间戳

---

## 错误处理

### 异常类型

- **`RuntimeError`**: 当关键信息收集失败时抛出
- **内部异常**: 被优雅捕获和处理，对不可用数据返回 `None`

### 错误场景

1. **权限拒绝**: 某些系统信息可能需要提升权限
2. **平台不兼容**: 某些功能可能在所有平台上都不可用
3. **网络超时**: 网络测试可能因连接问题而失败
4. **硬件访问**: 某些硬件信息可能无法访问

### 优雅降级

```python
try:
    result = device_info.get_device_info()
    
    # 检查特定信息是否可用
    if result.platform:
        print(f"操作系统: {result.platform.os_name}")
    else:
        print("平台信息不可用")
        
    if result.network and result.network.ping:
        print(f"Ping: {result.network.ping}ms")
    else:
        print("网络测试不可用")
        
except RuntimeError as e:
    print(f"收集设备信息失败: {e}")
```

---

## 线程安全

DeviceInfo 类完全线程安全：

- **单例创建**: 使用双重检查锁定的线程安全延迟初始化
- **方法执行**: 所有方法都是无状态的，可以并发调用
- **无共享状态**: 方法调用之间没有可变的共享状态

```python
import threading

def collect_info():
    device_info = DeviceInfo()
    return device_info.get_device_info()

# 从多个线程安全调用
threads = [threading.Thread(target=collect_info) for _ in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
```

---

## 性能考虑

### 收集时间

| 组件 | 典型时间 | 备注 |
|------|----------|------|
| 平台 | 10-50ms | 快速，主要是系统调用 |
| CPU | 50-150ms | 包括简短的使用率采样 |
| 内存 | 5-20ms | 非常快，直接系统信息 |
| 磁盘 | 100-300ms | 取决于分区数量 |
| 网络 | 3000-5000ms | 包括 3 秒速度测试 |

### 优化建议

1. **选择性收集**: 只收集需要的信息
2. **缓存**: 在短时间内重复调用时缓存结果
3. **后台收集**: 在 UI 应用程序中在后台线程执行收集
4. **超时处理**: 为网络操作设置适当的超时

```python
# 快速收集（无网络测试）
quick_info = device_info.get_device_info(
    GetDeviceInfoParams(include_network=False)
)

# 仅网络收集
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