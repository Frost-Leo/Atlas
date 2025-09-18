# Atlas 文档

<div align="center">
    <img src="../assets/images/atlas-logo.svg" alt="Atlas Logo" width="280">
    <br>
    <img src="../assets/images/atlas-slogan.svg" alt="Atlas Slogan" width="100%">
</div>

Atlas 是一个基于 Django Rest Framework 构建的分布式、模块化数据平台 SDK。

## 项目状态

**开发阶段**: 规划阶段

本项目目前处于初期规划和开发阶段，核心基础设施组件正在设计和实现中。

## 当前实现

### 可用组件

- **设备信息模块**: 系统信息收集服务
  - 跨平台支持 (Windows, Linux, macOS)
  - 全面的系统数据收集
  - 线程安全的单例实现

## 文档

- [**API 参考**](api/README.md) - 可用的 API 文档

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| **后端框架** | Django | 5.2.5+ |
| **API 框架** | Django REST Framework | 3.16.0+ |
| **异步 API** | FastAPI | 0.115+ |
| **数据验证** | Pydantic | 2.11.7+ |
| **可观测性** | OpenTelemetry | 1.36.0+ |
| **数据库** | PostgreSQL | 通过 psycopg2 |
| **系统信息** | psutil | 7.0.0+ |

## 许可证

本项目采用 GPL-3.0 许可证 - 详情请参阅 [LICENSE](../../LICENSE) 文件。

## 代码仓库

- [GitHub 仓库](https://github.com/Frost-Leo/Atlas)
- [问题反馈](https://github.com/Frost-Leo/Atlas/issues)