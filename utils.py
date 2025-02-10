import logging
import time
import json
from urllib.parse import urlparse

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_url(url):
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port or (443 if protocol == "https" else 80)
    path_prefix = parsed_url.path.lstrip('/') if parsed_url.path else None
    return protocol, host, port, path_prefix

def load_config(config_path='config.json'):
    with open(config_path, 'r') as f:
        return json.load(f)

def exponential_backoff(retry_count=0, max_retries=5):
    if retry_count < max_retries:
        delay = 2 ** retry_count
        time.sleep(delay)
        return True
    return False