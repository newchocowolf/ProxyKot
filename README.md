# $${\color{white}ProxyKot}$$ $${\color{red}v4}$$
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/PKv4.png?raw=true)
# *Installation & Usage*
For Windows & Linux, requires only `python` (version 3)
   - `curl https://raw.githubusercontent.com/the-computer-mayor/ProxyKot/main/proxykot.py -o proxykot.py`
   - `python3 proxykot.py`
# Logger
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/PKv4_log.png?raw=true)
# *Features*
- Threading to speed up the process ☠
- Timeout ☠
- Supports `HTTP` `HTTPS` `SOCKS4` `SOCKS5` proxies ☠
- Can validate a singular proxy ☠
- Can validate a list of proxies ☠
- No Additional Python Libraries Needed **`Only Regular Python3 Built-In Modules`** ☠
- Print only working proxies feature ☠
- Very Easy To Use ☠
# *Using ProxyKot In Your Python Code*
```python
from proxykot import check_proxy

status = check_proxy(
    proxy_ip_port = "1.1.1.1:80", 
    proxy_type = "HTTP",
    ssl = False,
    test_domain = "ident.me",
    test_domain_path = "/json",
    required_keyword = "Content-Type: application/json",
    http_version = 1.1
)
```
