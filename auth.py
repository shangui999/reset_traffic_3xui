import http.client
import urllib.parse
import logging
from utils import parse_url

class Auth:
    def __init__(self, protocol, host, port, path_prefix):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path_prefix = path_prefix

    def login(self, username, password):
        conn = self._get_conn()
        login_path = f"/{self.path_prefix}/login" if self.path_prefix else "/login"
        payload = urllib.parse.urlencode({
            'username': username,
            'password': password
        })
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': f'{self.host}:{self.port}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            conn.request("POST", login_path, payload, headers)
            res = conn.getresponse()
            if res.status == 200:
                cookies = res.getheader('Set-Cookie')
                logging.info("登录成功！")
                return cookies
            else:
                logging.error(f"登录失败，HTTP 状态码: {res.status}")
                return None
        except Exception as e:
            logging.error(f"登录过程中发生错误: {e}")
            return None
        finally:
            conn.close()

    def _get_conn(self):
        if self.protocol == "https":
            return http.client.HTTPSConnection(self.host, self.port)
        else:
            return http.client.HTTPConnection(self.host, self.port)