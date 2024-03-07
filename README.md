# $${\color{white}ProxyKot}$$ $${\color{red}v4.8}$$
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/PKv4.png?raw=true)
# *Installation & Usage*
For Windows & Linux, requires only `python` (version 3)
   - `curl https://raw.githubusercontent.com/the-computer-mayor/ProxyKot/main/proxykot.py -o proxykot.py`
   - `python3 proxykot.py`
# Logger
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/PKv4_log.png?raw=true)
# *Features*
- No Additional Python Libraries Needed **`Only Regular Python3 Built-In Modules`** ☠

- You can sepcify the amount of threads to speed up the process ☠
- Supports `HTTP` `HTTPS` `SOCKS4` `SOCKS5` proxies ☠
- Can validate a link containing a list of proxies ☠
- Can validate a file containing a list of proxies ☠
- Optional: **Find Proxies** by entering `FPS` ☠
- Optional: Print only working proxies ☠
- Can validate a singular proxy ☠
- You can specify Timeout ☠
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
