import argparse
import logging
from utils import load_config, parse_url
from auth import Auth
from api_calls import APICalls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Login script with command-line arguments")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)
    protocol, host, port, path_prefix = parse_url(config['host'])

    # 登录
    auth = Auth(protocol, host, port, path_prefix)
    cookies = auth.login(config['username'], config['password'])
    if not cookies:
        logging.error("登录失败，程序终止")
        exit(1)

    # API 调用
    api = APICalls(protocol, host, port, path_prefix, cookies)
    inbounds_id = api.list_inbounds_id()
    if not inbounds_id:
        logging.error("获取入站 ID 列表失败，程序终止")
        exit(1)

    api.reset_all_traffics()
    api.reset_all_client_traffics(inbounds_id)