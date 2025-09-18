# Atlas Documentation

<div align="center">
    <img src="../assets/images/atlas-logo.svg" alt="Atlas Logo" width="280">
    <br>
    <img src="../assets/images/atlas-slogan.svg" alt="Atlas Slogan" width="100%">
</div>

Atlas is a distributed, modular SDK for centralized data platform built on Django Rest Framework.

## Project Status

**Development Stage**: Planning Phase

This project is currently in the initial planning and development stage. The core infrastructure components are being designed and implemented.

## Current Implementation

### Available Components

- **Device Info Module**: System information collection service
  - Cross-platform support (Windows, Linux, macOS)
  - Comprehensive system data collection
  - Thread-safe singleton implementation

## Documentation

- [**API Reference**](api/README.md) - Available API documentation

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend Framework** | Django | 5.2.5+ |
| **API Framework** | Django REST Framework | 3.16.0+ |
| **Async API** | FastAPI | 0.115+ |
| **Data Validation** | Pydantic | 2.11.7+ |
| **Observability** | OpenTelemetry | 1.36.0+ |
| **Database** | PostgreSQL | via psycopg2 |
| **System Info** | psutil | 7.0.0+ |

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](../../LICENSE) file for details.

## Repository

- [GitHub Repository](https://github.com/Frost-Leo/Atlas)
- [Issues](https://github.com/Frost-Leo/Atlas/issues)