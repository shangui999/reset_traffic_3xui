---
title: "Configuration"
source: "https://github.com/MHSanaei/3x-ui/wiki/Configuration#api-documentation"
author:
  - "[[GitHub]]"
published:
created: 2026-02-26
description: "Xray panel supporting multi-protocol multi-user expire day & traffic & IP limit (Vmess, Vless, Trojan, ShadowSocks, Wireguard, Tunnel, Mixed, HTTP, Tun)  - Configuration · MHSanaei/3x-ui Wiki"
tags:
  - "clippings"
---
## Getting SSL

### ACME

To manage SSL certificates using ACME:

1. Ensure your domain is correctly resolved to the server.
2. Run the `x-ui` command in the terminal, then choose `SSL Certificate Management`.
3. You will be presented with the following options:
	- **Get SSL:** Obtain SSL certificates.
	- **Revoke:** Revoke existing SSL certificates.
	- **Force Renew:** Force renewal of SSL certificates.
	- **Show Existing Domains:** Display all domain certificates available on the server.
	- **Set Certificate Paths for the Panel:** Specify the certificate for your domain to be used by the panel.

### Certbot

To install and use Certbot:

### Cloudflare

The management script includes a built-in SSL certificate application for Cloudflare. To use this script to apply for a certificate, you need the following:

- Cloudflare registered email
- Cloudflare Global API Key
- The domain name must be resolved to the current server through Cloudflare

**How to get the Cloudflare Global API Key:**

1. Run the `x-ui` command in the terminal, then choose `Cloudflare SSL Certificate`.
2. Visit the link: [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens).
3. Click on "View Global API Key" (see the screenshot below):

![](https://github.com/MHSanaei/3x-ui/raw/main/media/APIKey1.PNG)

1. You may need to re-authenticate your account. After that, the API Key will be shown (see the screenshot below):

![](https://github.com/MHSanaei/3x-ui/raw/main/media/APIKey2.png)

When using, just enter your `domain name`, `email`, and `API KEY`. The diagram is as follows:

![](https://github.com/MHSanaei/3x-ui/raw/main/media/DetailEnter.png)

### XUI\_LOG\_LEVEL

- **Description**: Default log level
- **Type**: `string`
- **Acceptable values**: `debug` | `info` | `warn` | `error`
- **Default value**: `info`

### XUI\_DEBUG

- **Description**: Whether debug mode should be enabled
- **Type**: `boolean`
- **Default value**: `false`

### XUI\_BIN\_FOLDER

- **Description**: Path to the folder with xray-core, geosite & geoip databases
- **Type**: `string`
- **Default value**: `bin`

### XUI\_DB\_FOLDER

- **Description**: Path to the 3x-ui database
- **Type**: `string`
- **Default value**: `/etc/x-ui`

### XUI\_LOG\_FOLDER

- **Description**: Path to the logs
- **Type**: `string`
- **Default value**: `/var/log`

### XUI\_ENABLE\_FAIL2BAN

- **Description**: Should [fail2ban](https://github.com/fail2ban/fail2ban) be working
- **Type**: `boolean`
- **Default value**: `true`

## Reverse Proxy

### Nginx

To configure the reverse proxy, add the following paths to your nginx config

For the subscriptions

### Caddy

Before configuring `caddyfile`, make sure that the following parameters are set in the panel setup

![Screenshot](https://private-user-images.githubusercontent.com/135337715/448336146-c1914df0-ec9f-47ad-8f56-fb872be75fa0.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzIwNzA2ODgsIm5iZiI6MTc3MjA3MDM4OCwicGF0aCI6Ii8xMzUzMzc3MTUvNDQ4MzM2MTQ2LWMxOTE0ZGYwLWVjOWYtNDdhZC04ZjU2LWZiODcyYmU3NWZhMC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjI2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIyNlQwMTQ2MjhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zNjY4NWVkNGE5ZGY5YmVlNjY4ZDYzMzYyNDY1OTZlYTE5ZmRiOGQ0Y2U3YWFmNjYyNzMwOTgxODlmMTcxNTEyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.yJ7NcSV0e1vZc6KYEgE1Z_Cf6fhVjN9fd1UTb5p2gkQ)

After customizing the panel, modify the caddyfile as follows

The following data must be replaced in the config:

- `vpn.example.com` -> your domain.
- `admin *****` -> replace the asterisks with your password.

If you do not need HTTP Auth, remove the following line

- `reverse_proxy xx.xx.xx.xx` -> replace the `xx.xx.xx.xx` with your IP
- `reverse_proxy @websockets xx.xx.xx.xx:54321` -> replace `54321` with your inbound port

## Setting Fail2Ban

The IP limit is built-in to the panel

To enable the IP Limit functionality, you need to install `fail2ban` and its required files by following these steps:

1. Run the `x-ui` command in the terminal, then choose `IP Limit Management`.
2. You will see the following options:
	- **Change Ban Duration:** Adjust the duration of bans.
	- **Unban Everyone:** Lift all current bans.
	- **Check Logs:** Review the logs.
	- **Fail2ban Status:** Check the status of `fail2ban`.
	- **Restart Fail2ban:** Restart the `fail2ban` service.
	- **Uninstall Fail2ban:** Uninstall Fail2ban with configuration.
3. Add a path for the access log on the panel by setting `Xray Configs/log/Access log` to `./access.log` then save and restart xray.
- **For versions before `v2.1.3`:**
	- You need to set the access log path manually in your Xray configuration:
		```
		"log": {
		  "access": "./access.log",
		  "dnsLog": false,
		  "loglevel": "warning"
		},
		```
- **For versions `v2.1.3` and newer:**
	- There is an option for configuring `access.log` directly from the panel.

---

## API Documentation

- [API Documentation Postman](https://documenter.getpostman.com/view/5146551/2sB3QCTuB6)

## Authentication

- **Endpoint**: `/login`
- **Method**: `POST`
- **Body**:
	```
	{
	  "username": "",
	  "password": ""
	}
	```
- Use this endpoint to authenticate and receive a session.

---

## Inbounds API

Base path: **`/panel/api/inbounds`**

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/list` | Get all inbounds |
| `GET` | `/get/:id` | Get inbound by ID |
| `GET` | `/getClientTraffics/:email` | Get client traffics by email |
| `GET` | `/getClientTrafficsById/:id` | Get client traffics by inbound ID |
| `POST` | `/add` | Add new inbound |
| `POST` | `/del/:id` | Delete inbound by ID |
| `POST` | `/update/:id` | Update inbound by ID |
| `POST` | `/clientIps/:email` | Get client IP addresses |
| `POST` | `/clearClientIps/:email` | Clear client IP addresses |
| `POST` | `/addClient` | Add client to inbound |
| `POST` | `/:id/delClient/:clientId` | Delete client by clientId\* |
| `POST` | `/updateClient/:clientId` | Update client by clientId\* |
| `POST` | `/:id/resetClientTraffic/:email` | Reset a client’s traffic usage |
| `POST` | `/resetAllTraffics` | Reset traffics for all inbounds |
| `POST` | `/resetAllClientTraffics/:id` | Reset traffics for all clients in inbound |
| `POST` | `/delDepletedClients/:id` | Delete depleted clients in inbound (-1: all) |
| `POST` | `/import` | Import inbound configuration |
| `POST` | `/onlines` | Get currently online clients (emails list) |
| `POST` | `/lastOnline` | Get last online status of clients |
| `POST` | `/updateClientTraffic/:email` | Update traffic for specific client |
| `POST` | `/import` | import inbound |
| `POST` | `/lastOnline` | last Online |
| `POST` | `/{id}/delClientByEmail/{email}` | Delete Client By Email |

\* **clientId mapping**:

- `client.id` → VMESS / VLESS
- `client.password` → TROJAN
- `client.email` → Shadowsocks

---

## Server API

Base path: **`/panel/api/server`**

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/status` | Get server status |
| `GET` | `/getXrayVersion` | Get available Xray versions |
| `GET` | `/getConfigJson` | Download current config.json |
| `GET` | `/getDb` | Download database file (`x-ui.db`) |
| `GET` | `/getNewUUID` | Generate new UUID |
| `GET` | `/getNewX25519Cert` | Generate new X25519 certificate |
| `GET` | `/getNewmldsa65` | Generate new ML-DSA-65 certificate |
| `GET` | `/getNewmlkem768` | Generate new ML-KEM-768 key pair |
| `GET` | `/getNewVlessEnc` | Generate new VLESS encryption keys |
| `POST` | `/stopXrayService` | Stop Xray service |
| `POST` | `/restartXrayService` | Restart Xray service |
| `POST` | `/installXray/:version` | Install/Update Xray to given version |
| `POST` | `/updateGeofile` | Update GeoIP/GeoSite data files |
| `POST` | `/updateGeofile/:fileName` | Update specific Geo file |
| `POST` | `/logs/:count` | Get system logs (with `level`, `syslog`) |
| `POST` | `/xraylogs/:count` | Get Xray logs (with filters) |
| `POST` | `/importDB` | Import database |
| `POST` | `/getNewEchCert` | Generate new ECH certificate (requires `sni`) |

---

## Extra API

Base path: **`/panel/api`**

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/backuptotgbot` | Backup DB/config and send to Telegram Bot |

---

## Geosites

The Geosites in Xray-core play a key role in traffic routing, enabling flexible control over traffic distribution based on the geographical location of IP addresses and domains. Here are their main files:

- `geoip.dat` contains a database of IP addresses classified by country (e.g., `geoip:cn` for China or `geoip:private` for private networks). This allows:
	- Redirecting traffic for specific countries (e.g., Chinese IPs via direct, others via proxy).
	- Blocking or allowing access to IPs from certain regions.
- `geosite.dat` includes domain lists grouped by categories (e.g., `geosite:cn` for Chinese domains, `geosite:google` for Google services). This is used for:
	- Granular traffic control (e.g., ad domains → block, streaming → proxy).

### Sources

3X-UI uses multiple geofiles sources for flexible traffic routing:

| Repository | Files | Available geosites |
| --- | --- | --- |
| [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) | `geoip.dat`   `geosite.dat` | [View](https://github.com/v2fly/domain-list-community/tree/master/data) |
| [🇮🇷 chocolate4u/Iran-v2ray-rules](https://github.com/chocolate4u/Iran-v2ray-rules) | `geoip_IR.dat`   `geosite_IR.dat` | [View](https://github.com/chocolate4u/Iran-v2ray-rules?tab=readme-ov-file#page_with_curl-categories) |
| [🇷🇺 runetfreedom/russia-v2ray-rules-dat](https://github.com/runetfreedom/russia-v2ray-rules-dat) | `geoip_RU.dat`   `geosite_RU.dat` | [View](https://github.com/runetfreedom/russia-v2ray-rules-dat?tab=readme-ov-file#%D0%BA%D0%B0%D0%BA%D0%B8%D0%B5-%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8-%D1%81%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B0%D1%82%D1%81%D1%8F-%D0%B2-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%D1%85) |

### Updating geofiles

1. Open panel and click to Xray version

![image](https://private-user-images.githubusercontent.com/135337715/448489840-1f86d21b-c1a7-4268-9031-1cb5179dc38d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzIwNzA2ODgsIm5iZiI6MTc3MjA3MDM4OCwicGF0aCI6Ii8xMzUzMzc3MTUvNDQ4NDg5ODQwLTFmODZkMjFiLWMxYTctNDI2OC05MDMxLTFjYjUxNzlkYzM4ZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjI2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIyNlQwMTQ2MjhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04YTNiMmZmMGRlYWQxY2RhOWEwNzQzOTRjNGFmNGFhNjBlMGUwZjhkM2U5Y2NlYjExNDFkZmQ1MGMwNGRjOGU4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.a9aIxI-OdxE3FydnmP7-S_Z2QCj1RwE-otj8SheVwVQ)

1. Open `Geofiles` dropdown and update the needed geofile

![image](https://private-user-images.githubusercontent.com/135337715/448489964-6765b54d-3858-4fd3-b75b-17b5bc2b983f.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzIwNzA2ODgsIm5iZiI6MTc3MjA3MDM4OCwicGF0aCI6Ii8xMzUzMzc3MTUvNDQ4NDg5OTY0LTY3NjViNTRkLTM4NTgtNGZkMy1iNzViLTE3YjViYzJiOTgzZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjI2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIyNlQwMTQ2MjhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jNTJiOWFhNTUzYThhZDg5NmMzZjNhODdhM2JmZDE1ZDRkYjZlYWNhMGNhMmFmZGJmZDMyY2ZmMTYzMjdhNTljJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.yZMJL2Dmg3MDm10roV6-aemfRS5r0BBqEORu5qWPHm4)