# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Constants

Defines constants used throughout the HydroLink integration including
domain name, platform definitions, and service names.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic constants defined

- 0.2.0 (2025-10-02)
  * Added service constants
  * Added platform definitions
  * Improved organization

License: MIT
See LICENSE file in the project root for full license information.
"""

DOMAIN = "hydrolink"
DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes in seconds

# The domain of the integration
DOMAIN = "hydrolink"

# The platforms to be set up
PLATFORMS = ["sensor"]

# Services
SERVICE_TRIGGER_REGENERATION = "trigger_regeneration"
