# 3x-ui 流量重置脚本

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/)

通过调用 3x-ui 面板 API，自动重置所有入站(inbound)下所有客户端的已用流量（上传/下载归零）。

## 功能特性

- 支持 Python 3 和 Bash 两种实现
- 通过环境变量或修改脚本配置
- 自动登录并获取会话
- 遍历所有入站，批量重置客户端流量
- 详细的日志输出
- 适合配合 cron 定时执行

## 文件说明

| 文件 | 说明 |
|------|------|
| `reset_traffic.py` | Python 3 版本，使用标准库实现 |
| `reset_traffic.sh` | Bash 版本，依赖 curl |
| `3x-uiConfiguration.md` | 3x-ui API 文档参考 |

## 使用方法

### 1. 配置

#### 方式一：环境变量（推荐）

```bash
export XUI_PANEL_URL="http://127.0.0.1:2053"
export XUI_USERNAME="admin"
export XUI_PASSWORD="your_password"
```

#### 方式二：修改脚本

编辑脚本文件，修改配置区域：

```python
# Python 版本
PANEL_URL = "http://127.0.0.1:2053"
USERNAME = "admin"
PASSWORD = "your_password"
```

```bash
# Bash 版本
PANEL_URL="http://127.0.0.1:2053"
USERNAME="admin"
PASSWORD="your_password"
```

### 2. 运行

```bash
# Python 版本
python3 reset_traffic.py

# Bash 版本
bash reset_traffic.sh
```

### 3. 定时执行（cron）

每月1号凌晨2点自动执行：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（Python 版本）
0 2 1 * * XUI_PANEL_URL="http://IP:端口" XUI_USERNAME="用户名" XUI_PASSWORD="密码" /usr/bin/python3 /path/to/reset_traffic.py >> /var/log/3xui_reset.log 2>&1

# 或（Bash 版本）
0 2 1 * * XUI_PANEL_URL="http://IP:端口" XUI_USERNAME="用户名" XUI_PASSWORD="密码" /path/to/reset_traffic.sh >> /var/log/3xui_reset.log 2>&1
```

## 日志示例

```
2025-01-01 02:00:00 [INFO] ===== 3x-ui Client 流量重置 开始 [2025-01-01] =====
2025-01-01 02:00:01 [INFO] 登录成功
2025-01-01 02:00:01 [INFO] 获取到 3 个 inbound
2025-01-01 02:00:02 [INFO] inbound 1 (VMess-TCP) 的所有 client 流量已重置
2025-01-01 02:00:02 [INFO] inbound 2 (VLESS-WS) 的所有 client 流量已重置
2025-01-01 02:00:03 [INFO] inbound 3 (Trojan-gRPC) 的所有 client 流量已重置
2025-01-01 02:00:03 [INFO] ===== 所有 client 流量重置完成 =====
```

## 依赖

- **Python 版本**: Python 3.6+（仅使用标准库）
- **Bash 版本**: Bash 4.0+, curl

## API 说明

脚本调用的 3x-ui API 端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/login` | POST | 用户登录，获取会话 |
| `/panel/api/inbounds/list` | GET | 获取所有入站列表 |
| `/panel/api/inbounds/resetAllClientTraffics/:id` | POST | 重置指定入站下所有客户端流量 |

更多 API 详情请参考 [3x-uiConfiguration.md](./3x-uiConfiguration.md)

## 许可证

```
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```

## 免责声明

本脚本仅供学习交流使用，使用本脚本造成的任何后果由使用者自行承担。
