# EcoWater HydroLink Unofficial API Documentation

> [!WARNING]
> This documentation is based on community reverse-engineering. EcoWater/HydroLink does not provide an official public API. Endpoints, payloads, and authentication methods may change without notice.

This document serves as a reference for developers looking to interact with the EcoWater cloud. It outlines the currently known REST endpoints, WebSocket streams, and internal enum structures.

## 1. Authentication

All requests (after initial login) require a specific session cookie returned by the login endpoint.

### Login
* **URL:** `POST https://api.hydrolinkhome.com/v1/auth/login`
* **Content-Type:** `application/json`
* **Payload:**
  ```json
  {
    "email": "your_email@example.com",
    "password": "your_password"
  }
  ```
* **Response:** Returns an authentication cookie named `hhfoffoezyzzoeibwv`.
* **Usage:** Pass this cookie in the headers of all subsequent requests.
  * *Example (Python):* `cookies={"hhfoffoezyzzoeibwv": auth_cookie}`

---

## 2. Read Endpoints

### Get All Devices
Retrieves a list of all water softeners and devices registered to the account, along with their current status properties.
* **URL:** `GET https://api.hydrolinkhome.com/v1/devices`
* **Query Parameters:**
  * `all=false`
  * `per_page=200`
* **Response:** JSON object containing a `data` array. Each object in the array represents a device and contains its `id`, `nickname`, `system_type`, and a massive `properties` dictionary containing ~139 telemetry sensors.

### Get Live WebSocket Stream
Retrieves the WebSocket URI for a specific device to establish a real-time data stream.
* **URL:** `GET https://api.hydrolinkhome.com/v1/devices/{device_id}/live`
* **Response:** Returns the connection details necessary to establish a `websocket` connection for live telemetry updates.

---

## 3. Write Endpoints (Controls)

Currently, only manual regeneration is documented. We are actively looking for contributors to help map out settings endpoints.

### Trigger Manual Regeneration
Forces the water softener to begin a regeneration cycle immediately.
* **URL:** `POST https://api.hydrolinkhome.com/v1/devices/{device_id}/regenerate`
* **Payload:** `None` (Empty POST body)
* **Status:** Fully implemented and working.

### Update Settings (Needs Discovery)
> [!IMPORTANT]
> **Help Wanted:** The API endpoints for updating device settings (e.g., turning off scheduled regenerations, changing salt type) are currently unknown. See the *How to Reverse Engineer* section below if you want to help!

---

## 4. Enum Mappings Data Dictionary

The `properties` object returns several `_enum` fields as integers. Below is the working dictionary of what these values map to in the physical system. 

> [!NOTE]
> If you figure out the missing values, please submit a Pull Request to update this table!

| API Key | Value | Human Readable Meaning | Status |
| :--- | :--- | :--- | :--- |
| `salt_type_enum` | `0` | NaCl (Sodium Chloride)? | *Needs Verification* |
| `salt_type_enum` | `1` | KCl (Potassium Chloride)? | *Needs Verification* |
| `regen_enable_enum` | `0` | Disabled? | *Needs Verification* |
| `regen_enable_enum` | `1` | Enabled? | *Needs Verification* |
| `efficiency_mode_enum` | `?` | High Capacity | *Needs Discovery* |
| `efficiency_mode_enum` | `?` | High Efficiency | *Needs Discovery* |
| `user_lockout_enum` | `?` | Locked / Unlocked | *Needs Discovery* |
| `rinse_type_enum` | `?` | ? | *Needs Discovery* |
| `regen_status_enum` | `?` | Regenerating / Idle | *Needs Discovery* |
| `wtd_monitor_enum` | `?` | Water-To-Drain Monitor (On/Off) | *Needs Discovery* |

---

## 5. How to Reverse Engineer (For Contributors)

If you want to help us map out the missing settings endpoints and enum values, you can capture the traffic from the official EcoWater (or iQua) mobile app using a Man-In-The-Middle (MITM) proxy.

**Requirements:**
1. A proxy tool like [Proxyman](https://proxyman.io/) (Mac/Windows), [Charles Proxy](https://www.charlesproxy.com/), or [mitmproxy](https://mitmproxy.org/).
2. A mobile device connected to the same WiFi network as your computer.

**Steps:**
1. Install your chosen proxy tool on your computer and note your computer's local IP address and proxy port (usually `9090` or `8080`).
2. On your mobile device, modify your WiFi connection settings to use a **Manual Proxy**, pointing to your computer's IP and port.
3. Install the Proxy's SSL Certificate on your mobile device (so the proxy can read HTTPS traffic). *For iOS, remember to go to Settings > General > About > Certificate Trust Settings and enable full trust.*
4. Open the EcoWater mobile app.
5. Watch the traffic in your proxy tool:
   * **To map Enums:** Go to your device settings in the app, change a value (e.g., flip your salt type to KCl), and wait for the `POST` or `PUT` request to appear in the proxy. 
   * Note the URL it hit, and the JSON payload it sent. 
6. Open an Issue or Pull Request in this repository with your findings!
