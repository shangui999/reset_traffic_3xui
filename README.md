3x-ui 没有内置流量定期重置能力
本脚调用3x-ui的api实现流量重置
需要了解 python 以及 cron 的知识

用法 crontab -e 每月执行
========================================================================
```
0 0 1 * * python main.py https://hello.world.com:8888/xxxxxxx user password
# 或者本地
0 0 1 * * python main.py http://localhost:2053 user password
```
如果你的面板都可以公网访问，也可以使用 github 的 Actions 来执行 参考 https://docs.github.com/en/actions/about-github-actions/understanding-github-actions