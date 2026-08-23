# Changelog

All notable changes to the EcoWater HydroLink Home Assistant integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.4] - 2025-12-18

### Fixed
- **CRITICAL**: Fixed "Water Softener Device Time" sensor showing as "Unavailable"
  - Sensor was returning raw Unix timestamps (integers) instead of timezone-aware datetime objects
  - Now converts Unix timestamps to `datetime` objects with UTC timezone for `TIMESTAMP` device class sensors
  - Returns `None` for invalid timestamps (≤ 0)
  - Fixes `AttributeError: 'int' object has no attribute 'tzinfo'` error in Home Assistant logs

### Added
- **Enhanced Logging**: Added debug logging to data coordinator for better diagnostics
  - Logs when data fetches begin
  - Logs successful data fetches with device count
  - Logs detailed error messages when fetches fail
  - Helps diagnose data refresh and connection issues

### Changed
- Improved timestamp validation comments for clarity

**Impact**: High - Fixes sensor availability issue and improves troubleshooting

## [1.2.3] - 2025-12-17

### Fixed
- **Energy Dashboard Support**: Added `device_class: water` to all water volume sensors
  - Sensors now properly appear in Home Assistant's Energy Dashboard water tracking
  - Affected sensors: `gallons_used_today`, `avg_daily_use_gals`, `total_outlet_water_gals`, `treated_water_avail_gals`, `water_counter_gals`
  - Sensors with `state_class: total_increasing` are now compatible with long-term statistics

**Impact**: Medium - Enables water consumption tracking in Energy Dashboard

## [1.2.2] - 2025-10-10

### Fixed
- **CRITICAL**: Fixed multiple sensor scaling issues
  - `capacity_remaining_percent`: Now correctly divides by 10 (was showing 850 instead of 85%)
  - `avg_salt_per_regen_lbs`: Now correctly divides by 1000 (was showing mg instead of lbs)
  - `total_salt_use_lbs`: Now correctly divides by 1000 (was showing mg instead of lbs)
  - Fixed sensors with `_tenths` anywhere in name (not just at end), including `iron_level_tenths_ppm` and `tlc_avg_temp_tenths_c`

### Added
- **NEW SENSORS**: Added 15 additional sensor definitions that were available in API but not exposed:
  - `iron_level_tenths_ppm`: Iron level in parts per million
  - `tlc_avg_temp_tenths_c`: TLC average temperature in Celsius
  - `salt_effic_grains_per_lb`: Salt efficiency metric
  - `salt_type_enum`: Salt type indicator
  - `water_counter_gals`: Water counter in gallons
  - `error_code`: Numeric error code
  - `service_active`: Service mode status
  - `time_lost_events`: Power outage/time lost event counter
  - `product_serial_number`: Device serial number
  - `location`: Device location
  - `system_type`: System type identifier
  - `model_display_code`: Model display code
  - `base_software_version`: Base software version
  - `esp_software_part_number`: ESP software part number
  - `regen_time_secs`: Regeneration time in seconds
- Comprehensive test coverage for all scaling conversions

### Changed
- Enhanced `HydroLinkSensor.native_value` to handle three conversion types:
  1. Tenths conversion (÷10) for any property with `_tenths` in name
  2. Capacity conversion (÷10) for `capacity_remaining_percent`
  3. Salt conversion (÷1000) for salt mass values
- Removed duplicate sensor definitions that were causing conflicts

### Documentation
- Updated SENSORS.md with comprehensive conversion documentation
- Added tables showing all affected variables and their conversions
- Documented new sensors with units, device classes, and descriptions

**Impact**: High - Critical fix for incorrect sensor readings, enables access to all API data

## [1.2.1] - 2025-10-10

### Fixed
- **CRITICAL**: Salt level sensor now displays correct percentage values
  - Fixed sensors with `_tenths` suffix displaying 10x too high
  - Salt level now correctly shows 75% instead of 750%
  - Affects: `salt_level_tenths` and any other percentage values from API
- Added automatic value conversion for all sensors ending in `_tenths`
- Implemented proper handling of tenths-based API values

### Changed
- Enhanced `HydroLinkSensor.native_value` property with automatic conversion logic
- Updated sensor documentation to explain API value conversions

### Documentation
- Added "API Value Conversions" section to SENSORS.md
- Documented raw API format vs displayed values
- Explained which sensors receive automatic conversion

**Impact**: High - Critical fix for users with incorrect sensor readings

## [1.2.0] - 2025-10-03

### Added
- Comprehensive inline documentation and code comments across all modules
- Version-agnostic ConfigEntry creation for compatibility across HA versions
- Multi-environment testing with tox for Python 3.9, 3.10, and 3.11
- Enhanced error handling patterns and logging standards
- Comprehensive development documentation in copilot-instructions.md
- Detailed architecture overview and development guidelines

### Changed
- Improved test infrastructure with version-specific Home Assistant dependencies
- Enhanced CI/CD pipeline with proper GitHub Actions validation
- Updated README with current development status and testing information
- Refined code quality standards with comprehensive linting configuration

### Fixed
- ConfigEntry constructor compatibility across different Home Assistant versions
- Python package structure for tests directory (added tests/__init__.py)
- Import errors in test modules affecting CI/CD pipeline
- Cross-version API compatibility issues between HA 2023.1+ and 2024.10+

### Technical Improvements
- Split tox configuration for version-specific dependencies
- Implemented try/catch fallback for ConfigEntry discovery_keys parameter
- Enhanced test fixtures for better version compatibility
- Improved code organization and documentation standards

## [1.1.1] - 2025-10-03

### Added
- Cross-version compatibility support for Home Assistant 2023.1+ through 2024.10+
- Comprehensive pytest test suite with 35+ test cases
- Proper Python package structure for test modules

### Fixed
- ConfigEntry API compatibility issues across Home Assistant versions
- Test infrastructure and import error resolution
- Multi-version testing configuration with tox

### Changed
- Enhanced test coverage and validation processes
- Improved error handling in test fixtures
- Updated CI/CD configuration for multi-version testing

## [1.0.0] - 2025-10-02

### Added
- Initial HACS-compatible release of the EcoWater HydroLink integration
- Complete project restructure for HACS compliance and distribution
- Comprehensive sensor platform with 30+ sensors across 8 categories:
  - Basic System Information (4 sensors)
  - Water Usage Monitoring (6 sensors) 
  - Salt Management (4 sensors)
  - System Performance (6 sensors)
  - Regeneration Management (5 sensors)
  - Critical Alerts (6 sensors)
  - Signal and Connection (3 sensors)
  - Maintenance Information (3 sensors)
- Real-time WebSocket communication for live data updates
- Service calls for manual regeneration control
- Configuration flow for user-friendly setup via Home Assistant UI
- Comprehensive error handling and logging throughout
- MIT license for open-source distribution
- Professional branding assets and documentation

### Changed
- Complete codebase restructure from original Hydrolink-Home-Status project
- Updated minimum Home Assistant version requirement to 2024.10.0
- Enhanced data organization and sensor categorization
- Improved authentication and API communication patterns
- Standardized imperial units (gallons, GPM, pounds, grains)

### Technical Details
- **Integration Type**: Cloud Polling Hub
- **Dependencies**: requests>=2.31.0, websocket-client>=1.7.0, voluptuous>=0.13.1
- **Python Support**: 3.9, 3.10, 3.11
- **Home Assistant**: 2024.10.0+
- **Quality Scale**: Silver (comprehensive testing and validation)
- **HACS Category**: Integration
- **Configuration**: UI-based (no YAML required)

### Infrastructure
- GitHub Actions CI/CD pipeline with multi-workflow validation:
  - Test execution across Python 3.9, 3.10, 3.11
  - HACS validation and hassfest compliance
  - Code quality checks with Black, Ruff, and Pylint
  - Automated release and validation processes
- Pre-commit hooks for code quality enforcement
- Comprehensive test suite with pytest and mock fixtures
- Tox configuration for multi-environment testing
- Coverage reporting and quality metrics

### Documentation
- Comprehensive README.md with installation and usage instructions
- Detailed sensor documentation with tables and descriptions
- Troubleshooting guide and debug logging instructions
- Contributing guidelines and development setup
- License information and trademark notices
- HACS info.md for marketplace display

## [0.2.0] - 2025-10-02 (Pre-release)

### Added
- Service registration for manual regeneration control
- Enhanced data coordinator with improved error handling
- Type hints throughout the codebase for better maintainability
- Comprehensive data organization and sensor categorization

### Changed
- Improved error handling patterns across all modules
- Enhanced logging and debugging capabilities
- Better data validation and state management

## [0.1.0] - 2025-06-12 (Initial Development)

### Added
- Initial release based on the original Hydrolink-Home-Status project
- Basic integration setup and configuration flow
- Core API communication with HydroLink cloud service
- Foundation sensor implementations for water softener monitoring
- Basic authentication and data retrieval capabilities

### Technical Foundation
- Home Assistant integration framework implementation
- HydroLink API interface and communication patterns
- Basic sensor platform with essential monitoring capabilities
- Configuration flow for user credential management

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version increments for incompatible API changes
- **MINOR** version increments for backwards-compatible functionality additions  
- **PATCH** version increments for backwards-compatible bug fixes

## Support and Contributions

- **Issues**: [GitHub Issues](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GrumpyTanker/Ecowater-Hydrolink-HACS/discussions)
- **Contributing**: See [README.md](README.md#contributing) for development guidelines
- **Code Owner**: @GrumpyTanker