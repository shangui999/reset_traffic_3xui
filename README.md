3x-ui 没有内置流量定期重置能力  
本脚调用3x-ui的api实现流量重置  
需要了解 bash python 以及 cron 的知识  

bash 用法
```
#  crontab -e 
0 0 1 * * bash /path/to/bash_script.sh http://localhost:2053 user pass

#或者

0 0 1 * * bash /path/to/bash_script.sh https://3x.exp.com/xxxxxx user pass

#或者

0 0 1 * * bash /path/to/bash_script.sh http://localhost:2053 user pass 1 3 7

# 1 3 7 为不想被重置 client 流量的入站 id 脚本里面循环了 1～50 不够的话自己调整

```


python 用法
```
python main.py https://hello.world.com:8888/xxxxxxx user password  
python main.py http://localhost user password
```
