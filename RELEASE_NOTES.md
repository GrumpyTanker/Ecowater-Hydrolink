## 🔧 Critical Fixes

### Device Time Sensor Fixed
This release fixes a critical issue where the "Water Softener Device Time" sensor was showing as "Unavailable":

1. **Timestamp Conversion** - Sensor now returns timezone-aware datetime objects instead of raw Unix timestamps
2. **Error Resolution** - Fixes `AttributeError: 'int' object has no attribute 'tzinfo'` that was appearing in logs
3. **Invalid Timestamp Handling** - Returns `None` for invalid timestamps (≤ 0)

### Enhanced Diagnostics
- **Debug Logging** - Added comprehensive logging to data coordinator
  - Logs when data fetches begin
  - Logs successful fetches with device count
  - Logs detailed error messages for failures
  - Helps diagnose data refresh and connection issues

## 🧪 Testing

- 41 tests passing (3 new tests for timestamp conversion)
- Test coverage: 62.25%
- No security vulnerabilities found (CodeQL scan)

## 📦 Installation

Update through HACS or manually to get these critical fixes.

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.
