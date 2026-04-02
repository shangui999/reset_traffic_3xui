#!/usr/bin/env bash
#
# 3x-ui 面板每月重置所有已用流量脚本 (Shell 版)
#
# 用法:
#   1. 修改下方配置或通过环境变量传入
#   2. 直接运行: bash reset_traffic.sh
#   3. 配合 cron 每月自动执行:
#      crontab -e
#      0 2 1 * * XUI_PANEL_URL="http://IP:端口" XUI_USERNAME="用户名" XUI_PASSWORD="密码" /path/to/reset_traffic.sh >> /var/log/3xui_reset.log 2>&1

set -euo pipefail

# ======================== 配置区域 ========================
PANEL_URL="${XUI_PANEL_URL:-http://127.0.0.1:2053}"
USERNAME="${XUI_USERNAME:-admin}"
PASSWORD="${XUI_PASSWORD:-admin}"
# =========================================================

COOKIE_FILE=$(mktemp)
trap 'rm -f "$COOKIE_FILE"' EXIT

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$1] $2"
}

log "INFO" "===== 3x-ui 流量重置 开始 [$(date '+%Y-%m-%d')] ====="

# 登录
LOGIN_RESP=$(curl -s -w "\n%{http_code}" \
    -X POST "${PANEL_URL}/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" \
    -c "$COOKIE_FILE" \
    --connect-timeout 10 \
    --max-time 30)

HTTP_CODE=$(echo "$LOGIN_RESP" | tail -1)
BODY=$(echo "$LOGIN_RESP" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
    log "ERROR" "无法连接面板, HTTP 状态码: ${HTTP_CODE}"
    exit 1
fi

SUCCESS=$(echo "$BODY" | grep -o '"success":\s*true' || true)
if [ -z "$SUCCESS" ]; then
    MSG=$(echo "$BODY" | grep -o '"msg":"[^"]*"' | head -1 | cut -d'"' -f4)
    log "ERROR" "登录失败: ${MSG:-未知错误}"
    exit 1
fi

log "INFO" "登录成功"

# 获取所有 inbound 列表
LIST_RESP=$(curl -s -w "\n%{http_code}" \
    -X GET "${PANEL_URL}/panel/api/inbounds/list" \
    -b "$COOKIE_FILE" \
    --connect-timeout 10 \
    --max-time 30)

HTTP_CODE=$(echo "$LIST_RESP" | tail -1)
BODY=$(echo "$LIST_RESP" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
    log "ERROR" "获取 inbound 列表失败, HTTP 状态码: ${HTTP_CODE}"
    exit 1
fi

SUCCESS=$(echo "$BODY" | grep -o '"success":\s*true' || true)
if [ -z "$SUCCESS" ]; then
    MSG=$(echo "$BODY" | grep -o '"msg":"[^"]*"' | head -1 | cut -d'"' -f4)
    log "ERROR" "获取 inbound 列表失败: ${MSG:-未知错误}"
    exit 1
fi

# 提取所有 inbound id
IDS=$(echo "$BODY" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$IDS" ]; then
    log "INFO" "没有 inbound，无需重置"
    exit 0
fi

ID_COUNT=$(echo "$IDS" | wc -l | tr -d ' ')
log "INFO" "获取到 ${ID_COUNT} 个 inbound"

# 逐个重置每个 inbound 下所有 client 的已用流量
FAILED=0
for ID in $IDS; do
    RESET_RESP=$(curl -s -w "\n%{http_code}" \
        -X POST "${PANEL_URL}/panel/api/inbounds/resetAllClientTraffics/${ID}" \
        -b "$COOKIE_FILE" \
        --connect-timeout 10 \
        --max-time 30)

    HTTP_CODE=$(echo "$RESET_RESP" | tail -1)
    R_BODY=$(echo "$RESET_RESP" | sed '$d')
    R_SUCCESS=$(echo "$R_BODY" | grep -o '"success":\s*true' || true)

    if [ -n "$R_SUCCESS" ]; then
        log "INFO" "inbound ${ID} 的所有 client 流量已重置"
    else
        MSG=$(echo "$R_BODY" | grep -o '"msg":"[^"]*"' | head -1 | cut -d'"' -f4)
        log "ERROR" "重置 inbound ${ID} 的 client 流量失败: ${MSG:-HTTP ${HTTP_CODE}}"
        FAILED=$((FAILED + 1))
    fi
done

if [ "$FAILED" -gt 0 ]; then
    log "ERROR" "${FAILED} 个 inbound 重置失败"
    exit 1
fi

log "INFO" "===== 所有 client 流量重置完成 ====="
