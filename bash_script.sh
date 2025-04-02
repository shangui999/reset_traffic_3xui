#!/bin/bash

# 检查参数是否足够
if [ "$#" -lt 3 ]; then
  echo "用法: $0 <PANEL_URL> <USERNAME> <PASSWORD> [WHITELIST_IDs...]"
  exit 1
fi

# 解析命令行参数
PANEL_URL="$1"
USERNAME="$2"
PASSWORD="$3"
shift 3
WHITELIST=("$@")

# 获取登录 Cookies
COOKIES=$(curl -k -s -i "$PANEL_URL/login" \
  --data-urlencode "username=$USERNAME" \
  --data-urlencode "password=$PASSWORD" 2>/dev/null | \
  grep -i 'Set-Cookie:' | cut -d' ' -f2 | cut -d';' -f 1)

# 判断是否成功获取 Cookies
if [ -z "$COOKIES" ]; then
  echo "获取 Cookies 失败，请检查用户名、密码或面板地址"
  exit 1
else
  echo "获取到 Cookies: ${COOKIES:0:5}*****${COOKIES: -5}"
fi

# 发送全局流量重置请求
RESET_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$PANEL_URL/panel/inbound/resetAllTraffics" -X 'POST' -H "Cookie: $COOKIES")

if [ "$RESET_RESPONSE" -eq 200 ]; then
  echo "全局流量重置成功"
else
  echo "全局流量重置失败，HTTP 状态码: $RESET_RESPONSE"
fi

# 循环 ID 1 ～ 50 重置流量
for ID in {1..50}; do
  # 检查 ID 是否在白名单中
  if [[ " ${WHITELIST[*]} " =~ " $ID " ]]; then
    continue
  fi

  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$PANEL_URL/panel/api/inbounds/resetAllClientTraffics/$ID" -X 'POST' -H "Cookie: $COOKIES")

  if [ "$RESPONSE" -eq 200 ]; then
    echo "用户 $ID 流量重置成功"
  else
    echo "用户 $ID 流量重置失败，HTTP 状态码: $RESPONSE"
  fi
done

echo "流量重置操作完成"
