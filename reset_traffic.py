#!/usr/bin/env python3
"""
3x-ui 面板每月重置所有已用流量脚本

用法:
  1. 修改下方配置区域的面板地址、用户名、密码
  2. 直接运行: python3 reset_traffic.py
  3. 配合 cron 实现每月自动执行:
     crontab -e
     # 每月1号凌晨2点执行
     0 2 1 * * /usr/bin/python3 /path/to/reset_traffic.py >> /var/log/3xui_reset.log 2>&1
"""

import json
import logging
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar
from datetime import datetime

# ======================== 配置区域 ========================
PANEL_URL = os.getenv("XUI_PANEL_URL", "http://127.0.0.1:2053")  # 面板地址（含端口，不带末尾斜杠）
USERNAME = os.getenv("XUI_USERNAME", "admin")                      # 面板用户名
PASSWORD = os.getenv("XUI_PASSWORD", "admin")                      # 面板密码
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def create_opener() -> urllib.request.OpenerDirector:
    """创建带 cookie 管理的 HTTP opener"""
    cookie_jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def login(opener: urllib.request.OpenerDirector) -> bool:
    """登录 3x-ui 面板，获取会话 cookie"""
    url = f"{PANEL_URL}/login"
    payload = json.dumps({"username": USERNAME, "password": PASSWORD}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener.open(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("success"):
                log.info("登录成功")
                return True
            log.error("登录失败: %s", body.get("msg", "未知错误"))
            return False
    except urllib.error.URLError as e:
        log.error("无法连接面板 %s: %s", url, e)
        return False


def get_inbound_list(opener: urllib.request.OpenerDirector) -> list | None:
    """获取所有 inbound 列表"""
    url = f"{PANEL_URL}/panel/api/inbounds/list"
    req = urllib.request.Request(url, method="GET")
    try:
        with opener.open(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("success"):
                inbounds = body.get("obj", [])
                log.info("获取到 %d 个 inbound", len(inbounds))
                return inbounds
            log.error("获取 inbound 列表失败: %s", body.get("msg", "未知错误"))
            return None
    except urllib.error.URLError as e:
        log.error("请求 inbound 列表失败: %s", e)
        return None


def reset_all_client_traffics(opener: urllib.request.OpenerDirector, inbound_id: int) -> bool:
    """重置指定 inbound 下所有 client 的已用流量（上传/下载归零，流量上限不变）"""
    url = f"{PANEL_URL}/panel/api/inbounds/resetAllClientTraffics/{inbound_id}"
    req = urllib.request.Request(url, data=b"", method="POST")
    try:
        with opener.open(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("success"):
                return True
            log.error("重置 inbound %d 的 client 流量失败: %s", inbound_id, body.get("msg", "未知错误"))
            return False
    except urllib.error.URLError as e:
        log.error("请求重置 inbound %d 失败: %s", inbound_id, e)
        return False


def main() -> int:
    log.info("===== 3x-ui Client 流量重置 开始 [%s] =====", datetime.now().strftime("%Y-%m-%d"))

    if PANEL_URL == "http://127.0.0.1:2053" and USERNAME == "admin" and PASSWORD == "admin":
        log.warning("正在使用默认配置，请通过环境变量或修改脚本设置真实的面板地址和凭证")

    opener = create_opener()

    if not login(opener):
        return 1

    inbounds = get_inbound_list(opener)
    if inbounds is None:
        return 1

    if not inbounds:
        log.info("没有 inbound，无需重置")
        return 0

    failed = 0
    for ib in inbounds:
        ib_id = ib["id"]
        remark = ib.get("remark", "")
        if reset_all_client_traffics(opener, ib_id):
            log.info("inbound %d (%s) 的所有 client 流量已重置", ib_id, remark)
        else:
            failed += 1

    if failed:
        log.error("%d 个 inbound 重置失败", failed)
        return 1

    log.info("===== 所有 client 流量重置完成 =====")
    return 0


if __name__ == "__main__":
    sys.exit(main())
