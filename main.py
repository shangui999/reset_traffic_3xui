import http.client
import urllib.parse
import argparse
import json
import time
from urllib.parse import urlparse

def parse_url(url):
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme  # 提取协议 (http / https)
    host = parsed_url.hostname  # 提取主机名 (3xui.exp.com)
    port = parsed_url.port  # 提取端口 (8888)
    path = parsed_url.path.lstrip('/')  # 提取 path (ONXFMHnjcuJ50tf3G55A)
    # 判断path 有没有
    if path == "":
        path_prefix = None
    else:
        path_prefix = path

    # 判断port 有没有 以及 是否是默认 http https 的端口
    if port:
        port = port
    else:
        if protocol == "https":
            port = 443
        else:
            port = 80
    

    return protocol, host, port, path_prefix

def get_conn(protocol, host, port):
    if protocol == "https":
        conn = http.client.HTTPSConnection(host, port)
    else:
        conn = http.client.HTTPConnection(host, port)
    return conn


def login(protocol, host, port, path_prefix, username, password):
    
    #conn = http.client.HTTPSConnection(hostname, port)
    conn = get_conn(protocol, host, port)

    # 根据 `path_prefix` 是否提供，决定 `login_path`
    if path_prefix:
        login_path = f"/{path_prefix}/login"
    else:
        login_path = "/login"

    # URL 编码请求参数
    payload = urllib.parse.urlencode({
        'username': username,
        'password': password
    })

    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': f'{host}:{port}',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 发送 POST 请求
    conn.request("POST", login_path, payload, headers)
    
    # 获取响应
    res = conn.getresponse()
    status_code = res.status  # 获取 HTTP 状态码

    # 判断是否成功（HTTP 200）
    if status_code == 200:
        # 读取 `Set-Cookie` 头部
        cookies = res.getheader('Set-Cookie')
        
        # 读取响应数据
        data = res.read().decode("utf-8")

        print("✅ 登录成功！")
        #print("Response Data:", data)
        #print("Cookies:", cookies)
        conn.close()

        return cookies  # 返回 cookie 供后续使用
    else:
        print(f"❌ 登录失败，HTTP 状态码: {status_code}")
        return None  # 失败时返回 None
        #并且终止程序
        exit(1)
    




def list_inbounds_id(protocol, host, port, path_prefix, cookies):
    inbounds_id = []
    
    if path_prefix:
        path = f"/{path_prefix}/panel/api/inbounds/list"
    else:
        path = "/panel/api/inbounds/list"

    conn = get_conn(protocol, host, port)
    payload = ''
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Host': f'{host}:{port}',
    'Connection': 'keep-alive',
    'Cookie': f'{cookies}'
    }
    conn.request("GET", path, payload, headers)
    res = conn.getresponse()
    # 判断返回是否为 200 如果是 处理 json 
    if res.status == 200:
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        #print(data.decode("utf-8"))
        #print(type(data.decode("utf-8")))
        for i in json_data['obj']:
            inbounds_id.append(i['id'])
        
        print(f"入站列表：✅ 获取完成！：{inbounds_id}")

        conn.close()
        return inbounds_id

    else:
        print(f"❌ 获取失败，HTTP 状态码: {res.status}")
        exit(1)


def reset_all_traffices(protocol, host, port, path_prefix, cookies):

    conn = get_conn(protocol, host, port)
    if path_prefix:
        path = f"/{path_prefix}/panel/api/inbounds/resetAllTraffics"
    else:
        path = "/panel/api/inbounds/resetAllTraffics"
    
    payload = ''
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Host': f'{host}:{port}',
    'Connection': 'keep-alive',
    'Cookie': f'{cookies}'
    }
    conn.request("POST", path, payload, headers)
    res = conn.getresponse()
    # 判断返回是否为 200 如果是 处理 json
    if res.status == 200:
        #data = res.read()
        #json_data = json.loads(data.decode("utf-8"))
        #print(json_data)
        print("入站流量：✅ 重置成功！")
        conn.close()
    else:
        print(f"入站流量：❌ 重置失败，HTTP 状态码: {res.status}")
        exit(1)


def reset_all_client_traffics(protocol , host, port, path_prefix, cookies, inbounds_id):
    for id in inbounds_id:
        # print(f"入站id：{id}")
        conn = get_conn(protocol, host, port)
        if path_prefix:
            path = f"/{path_prefix}/panel/api/inbounds/resetAllClientTraffics/{id}"
        else:
            path = f"/panel/api/inbounds/resetAllClientTraffics/{id}"
        payload = ''
        headers = {
        'Accept': 'application/json',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Host': f'{host}:{port}',
        'Connection': 'keep-alive',
        'Cookie': f'{cookies}'
        }
        conn.request("POST", path, payload, headers)
        res = conn.getresponse()

        time.sleep(1)

        if res.status == 200:
            print(f"入站id：{id} ✅ 重置client流量 成功！")
        else:
            print(f"入站id：{id} ❌ 重置失败，HTTP 状态码: {res.status}")
            exit(1)
        conn.close()
    


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Login script with command-line arguments")

    parser.add_argument("host", help="服务器地址，例如 https://3xui.exp.com:8888/ONXFMHnjcuJ50tf3G55A  http://localhost")
    parser.add_argument("username", help="登录用户名")
    parser.add_argument("password", help="登录密码")
    #parser.add_argument("--path", default=None, help="可选参数，路径前缀，例如 ONXFMHnjcuJ50tf3G55A")

    args = parser.parse_args()

    # 解析参数
    protocol, host, port, path_prefix = parse_url(args.host)

    #conn = get_conn(protocol, host, port)
    
    # 登录 获取 cookies 
    cookies = login(protocol, host, port, path_prefix, args.username, args.password)

    # 获取 入站id list inbounds_id
    inbounds_id = list_inbounds_id(protocol, host, port, path_prefix, cookies)

    # 重置入站流量
    reset_all_traffices(protocol, host, port, path_prefix, cookies)

    # 重置入站client流量
    reset_all_client_traffics(protocol, host, port, path_prefix, cookies, inbounds_id)

    



