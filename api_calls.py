import http.client
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from utils import parse_url, exponential_backoff

class APICalls:
    def __init__(self, protocol, host, port, path_prefix, cookies):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path_prefix = path_prefix
        self.cookies = cookies

    def list_inbounds_id(self):
        conn = self._get_conn()
        path = f"/{self.path_prefix}/panel/api/inbounds/list" if self.path_prefix else "/panel/api/inbounds/list"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Host': f'{self.host}:{self.port}',
            'Connection': 'keep-alive',
            'Cookie': self.cookies
        }
        try:
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()
            if res.status == 200:
                data = res.read().decode("utf-8")
                json_data = json.loads(data)
                inbounds_id = [i['id'] for i in json_data['obj']]
                logging.info(f"入站列表：✅ 获取完成！：{inbounds_id}")
                return inbounds_id
            else:
                logging.error(f"获取失败，HTTP 状态码: {res.status}")
                return []
        except Exception as e:
            logging.error(f"获取入站 ID 列表时发生错误: {e}")
            return []
        finally:
            conn.close()

    def reset_all_traffics(self):
        conn = self._get_conn()
        path = f"/{self.path_prefix}/panel/api/inbounds/resetAllTraffics" if self.path_prefix else "/panel/api/inbounds/resetAllTraffics"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Host': f'{self.host}:{self.port}',
            'Connection': 'keep-alive',
            'Cookie': self.cookies
        }
        try:
            conn.request("POST", path, headers=headers)
            res = conn.getresponse()
            if res.status == 200:
                logging.info("入站流量：✅ 重置成功！")
            else:
                logging.error(f"入站流量：❌ 重置失败，HTTP 状态码: {res.status}")
        except Exception as e:
            logging.error(f"重置入站流量时发生错误: {e}")
        finally:
            conn.close()

    def reset_all_client_traffics(self, inbounds_id):
        def reset_traffic(id):
            conn = self._get_conn()
            path = f"/{self.path_prefix}/panel/api/inbounds/resetAllClientTraffics/{id}" if self.path_prefix else f"/panel/api/inbounds/resetAllClientTraffics/{id}"
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Host': f'{self.host}:{self.port}',
                'Connection': 'keep-alive',
                'Cookie': self.cookies
            }
            try:
                conn.request("POST", path, headers=headers)
                res = conn.getresponse()
                if res.status == 200:
                    logging.info(f"入站id：{id} ✅ 重置client流量 成功！")
                else:
                    logging.error(f"入站id：{id} ❌ 重置失败，HTTP 状态码: {res.status}")
            except Exception as e:
                logging.error(f"入站id：{id} ❌ 重置失败，错误: {e}")
                if exponential_backoff():
                    reset_traffic(id)
            finally:
                conn.close()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(reset_traffic, id) for id in inbounds_id]
            for future in futures:
                future.result()  # 捕获异常

    def _get_conn(self):
        if self.protocol == "https":
            return http.client.HTTPSConnection(self.host, self.port)
        else:
            return http.client.HTTPConnection(self.host, self.port)