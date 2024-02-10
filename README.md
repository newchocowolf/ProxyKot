# $${\color{white}ProxyKot}$$ $${\color{red}v3.8}$$
`Discord: myleader`

**FIND & CHECK PROXIES AND MUCH MORE!**
# *Status*
# $${\color{green}Working}$$
# *Requirements*
-  `Linux`
   -  `sudo apt update -y && sudo apt upgrade -y`
   -  `sudo apt install python3`
   -  `sudo apt install curl` **Probably Already Built-In.**
- `Windows`
   - [`Python`](https://www.python.org/downloads)
# *Installation & Usage*
Launch `CMD`/`Terminal` And Type In The Following Commands:
   - `curl https://raw.githubusercontent.com/the-computer-mayor/ProxyKot/main/proxykot.py -o proxykot.py`
   - `python3 proxykot.py --help`
# *Example Of `--fps`*
**Finding Lots Of High Speed Working Proxies Across The Internet In Few Seconds**  
```console
python3 proxykot.py --fps http --timeout 1 --th 200 -owp
```
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/fps_v2.gif?raw=true)
# *Features*
- Threading To Speed Up The Process, (Default Value Is 4 Threads) --> `--th <Number Of Threads>`.
- Timeout Limit To Find Fast Proxies, (Default Value Is 3 Seconds) --> `--timeout <Seconds>`.
- Supports `HTTP` `HTTPS` `SOCKS4` `SOCKS5` Proxies.
- Raw Aka Json Output Available (`-raw`).
- Can Find `HTTP` `HTTPS` `SOCKS4` `SOCKS5` Across The Internet --> `(Example: --fps HTTP)`.
- Can Validate A Singular Proxy -> `--cp <IP:Port>`.
- Can Validate A List Of Proxies ->`--cpl <FileName>`.
- Can Validate A Singular Proxy Using A Specific Method `-https` `-https` `-socks4` `-socks5`.
- No Additional Python Libraries Needed **`Only Regular Python3 Built-In Modules`**.
- Can Print Out Only Working Proxies By Adding `-owp`.
- Can Terminate After Getting A Singular Working Proxy By Adding `-1`.
- Can Terminate After Printing A Specified Amount Of Working Proxies Using `--px <Count>`
- Very Easy To Use.
# *Using ProxyKot To Your Python Code*
```python
# Example Of Using ProxyKot In Your Code
from proxykot import CheckProxy
from proxykot import CheckProxyList


print(CheckProxy(IP_Port="35.72.18680", TIMEOUT=3, proxy_type="SOCKS4", SSL=False))
# If The Proxy Is Working
# output (string): {1.000880}
#
# If The Proxy Isn't Working
# output (bool): False
#
# If The Proxy Has Timed Out
# output (string): timeout


CheckProxyList(File="testFileName.txt", TIMEOUT=1, Threads=100, proxy_type="socks5")
# If There Are Working Proxies
# output (string): [{"213.19.205.18:54321": "0.4248947000014595"}, {"95.31.5.29:51528": "0.548758799995994"}]
# You Can Convert It To Json Using: json.loads(output)
#
# If There Are No Working Proxies
# output (string): -
```
# ***Maybe Star?***
![](https://github.com/the-computer-mayor/computer-mayor-db/blob/main/ProxyKotV3.png?raw=true)
