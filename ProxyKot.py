try:
    # Libraries
    from os.path import basename
    from time import perf_counter
    from sys import version_info
    from json import loads
    from os import getpid
    from os import system
    from sys import argv
    import subprocess
    import threading


    # Default Vars
    threads, test_server, timeout, Method, ProxyType = 4, "ident.me", 3, "http://", "--proxy"

    # Colors
    m0, r, g, y, b, p = "\033[0m", "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m"

    # Lists
    args, removed_proxy_list_lines, WorkingProxies, All_threads_names, proxy_list = argv[1:], [], [], [], []

    # Help Text
    HELP_TXT = f"""\n                                     \033[1;35m_____                    \033[1;31m _  __     _
\033[0m                                    \033[1;35m|  __ \\                   \033[1;31m| |/ /    | |
\033[0m                                    \033[1;35m| |__) | __ _____  ___   _\033[1;31m| ' / ___ | |_
\033[0m                                    \033[1;35m|  ___/ '__/ _ \\ \\/ / | | \033[1;31m|  < / _ \\| __|\033[0m            \033[1;32mDiscord: myleader
\033[0m                                    \033[1;35m| |   | | | (_) >  <| |_| \033[1;31m| . \\ (_) | |_\033[0m             \033[1;32mGithub: the-computer-mayor
\033[0m                                    \033[1;35m|_|   |_|  \\___/_/\\_\\\\__, \033[1;31m|_|\\_\\___/ \\__|
\033[0m                                                        \033[1;35m__/ |
\033[0m                                                        \033[1;35m|___/\033[0m

                                    \033[0mA Useful Tool To Validate Working Proxies
                                               \033[1;36m( HTTP || HTTPS )\033[0m
                                                   \033[1;34m( v2.0 )\033[0m  


                \033[1;32mUsage:\033[0m

                        python3 {basename(__file__)} \033[1;33m[Options]\033[0m

                \033[1;32mOptions:\033[0m

                        \033[1;33m--fps\033[0m \033[2;49;37m<HTTP || SOCKS4>\033[0m      Find \033[1;36mHTTP\033[0m Or \033[1;36mHTTPS\033[0m Or \033[1;36mSOCKS4\033[0m Working Proxies.
                        \033[1;33m--cpl\033[0m \033[2;49;37m<FileName>\033[0m            Validate A List Of Proxies.
                        \033[1;33m--cp\033[0m \033[2;49;37m<Ip:Port>\033[0m              Validate A Singular Proxy.
                        \033[1;33m--timeout\033[0m \033[2;49;37m<Seconds>\033[0m         Set A Timeout In Seconds.
                        \033[1;33m--th\033[0m \033[2;49;37m<Count>\033[0m                Number Of Threads To Speed Up The Process.
                        \033[1;33m-http\033[0m                       Use Only \033[1;36mHTTP\033[0m.
                        \033[1;33m-https\033[0m                      Use Only \033[1;36mHTTPS\033[0m.
                        \033[1;33m-socks4\033[0m                     Use Only \033[1;36mSOCKS4\033[0m.
                        \033[1;33m-owp\033[0m                        Prints Only Working Proxies.
                        \033[1;33m-raw\033[0m                        Raw As Known As Json Output.
                        \033[1;33m-1\033[0m                          Get A Singular Working Proxy Then Terminate.\n\n"""

    # Other
    Method_text, CH_arg, Json, All_threads, NotRaw, owp, NextPass, IsFile, Singed, Error, CutOff, fcb_add  = "HTTP", '', '', 0, True, True, False, False, False, False, False, False


    # Print Function
    def Print(type='t', text='', End='\n', IA=''):
        if type == "-?":
            if NotRaw:
                if owp == True: print(text)

        elif NotRaw:
            print(text, end=End)

        elif type == '?':
            print(f"{y}?{m0}")

        elif type == '-':
            print(f"{r}-{m0}")

        elif type == '+':
            if CutOff:
                print(f"{g}+{IA}{m0}")


    # Checking Python Version
    if version_info.major != 3:
        print(f"\n    {y}Python3 Required!{m0}\n")
        raise SystemExit


    # Terminate Current Process
    def Die():
        pid = getpid()
        system(f"kill {pid} > /dev/null; wait {pid} 2> /dev/null")


    # Checking IP Validation Function
    def is_valid(ip_port):
        Dot = 0
        colon = 0
        valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':']

        for char in range(len(ip_port)):
            if ip_port[char] not in valid_chars:
                return "invalid_proxy"
            
            elif ip_port[char] == ':' or ip_port[char] == '.':
                if ip_port[char] == '.': Dot += 1
                elif ip_port[char] == ':': colon += 1
                try:
                    _ = int(ip_port[char+1])
                    _ = int(ip_port[char-1])
                except:
                    return "invalid_proxy"
                
        if Dot == 3 and colon != 1:
            return "no_port"
        elif Dot != 3 or colon != 1:
            return "invalid_proxy"
        else:
            return "valid"


    # Extract IP Function
    def extractIP(IPPORT):
        ip = ''
        IPORTFIG = False
        for i in IPPORT:
            if i == ':':
                IPORTFIG = True
            elif IPORTFIG == False:
                ip = ip + i
        return ip


    # Proxy Health
    def is_available(IpPort):
        JustIP = extractIP(IpPort)

        TimeConnectStart = perf_counter()
        Respond = subprocess.run(["timeout", "-v", str(timeout)+'s', "curl", "-i", ProxyType, IpPort, Method+test_server, "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: {test_server}", "-H", "Accept: */*"], capture_output=True)
        Respond = (Respond.stderr + Respond.stdout).decode("utf-8")
        TimeConnectEnd = perf_counter()

        if "timeout" in Respond:
            return "timeout"

        elif "SSL certificate problem" in Respond:
            return False

        elif JustIP in Respond and "200 OK" in Respond:
            TimeConnect = TimeConnectEnd - TimeConnectStart
            return '{'+str(TimeConnect)+'ms}'

        else:
            return False


    # Check Proxy List Function
    def cpl(IpsPorts):
        try:
            global All_threads
            global WorkingProxies

            for IpPort in IpsPorts:
                IsValid = is_valid(IpPort)

                if IsValid == "invalid_proxy":
                    Print('-?', f"    {r}[-] {m0}{IpPort}    {r}(Invalid Proxy){m0}")
                elif is_valid == "no_port":
                    Print('-?', f"    {r}[-] {m0}{IpPort}    {r}(No Port?){m0}")
                else:
                    IsAvailable = is_available(IpPort)

                    if IsAvailable == "timeout":
                        if owp: Print('-?', f"    {r}[-] {m0}{IpPort}    {r}(Timed Out){m0}")    
                    elif IsAvailable == False:
                        Print('-?', f"    {r}[-] {m0}{IpPort}    {r}(Proxy Doesn't Work){m0}")
                    else:
                        WorkingProxies.append({IpPort:IsAvailable[1:-1]})
                        Print('+', f"    {g}[+] {m0}{IpPort}    {g}{IsAvailable}{m0}", IA=IpPort)
                        if CutOff == True:
                            Die()
        finally:
            All_threads += 1


    # Ui
    if args == []:
        print("UI: Coming soon...")
        raise SystemExit

    # Help
    if "--help" in args or "help" in args:
        print(HELP_TXT, end='')
        raise SystemExit

    # Extra Args Check
    for arg in args:

        # Raw Output Only
        if arg == "-raw":
            NotRaw = False

        # Singular Working Proxy
        if arg == "-1":
            CutOff = True

        # Singular Working Proxy
        if arg == "-owp":
            owp = False

        # HTTPS Only
        elif arg == "-https":
            if Singed == False:
                Method = "https://"
                Method_text = "HTTPS"
            else:
                Error = True

        # HTTP Only
        elif arg == "-http":
            Singed = True
            if Method != "https://":
                Method = "http://"
                Method_text = "HTTP"
            else:
                Error = True

        # SOCKS4 Only
        elif arg == "-socks4":
            ProxyType = "--socks4"
            Method_text = "SOCKS4"

    for Value in ["-http", "-https", "-raw", "-socks4", "-1", "-owp"]:
        try:
            args.remove(Value)
        except ValueError:
            pass


    # Args
    for arg in range(len(args)):
        try:
            if Error:
                raise IndexError
            C_arg = args[arg].lower()

            # Timeout Limit
            if C_arg == "--timeout":
                timeout = int(args[arg+1])+1
                NextPass = True

            # Threads Limit
            elif C_arg == "--th":
                threads = int(args[arg+1])
                NextPass = True

            # Main Args
            elif C_arg in ["--cp", "--cpl", "--fps"]:
                if CH_arg == '': 
                    CH_arg = C_arg
                    NextPass = True

                else:
                    if NextPass == False: raise IndexError
                    NextPass = False

            else:
                if NextPass == False: raise IndexError
                NextPass = False


        except (IndexError, ValueError):
            Print('?', f"\n    {y}You Might Need To Use {r}({p}python3 {basename(__file__)} --help{r}){m0}\n"); raise SystemExit


    # [-- Start --]
    for arg_sect in range(len(args)):
        arg = args[arg_sect].lower()


        # --fps
        if arg == "--fps":
            try:
                if args[arg_sect+1].lower() not in ["socks4", "http", "https"]:
                    Print('?', f"\n    {y}What Is {r}({p}{args[arg_sect+1]}{r}) {y}?{m0}\n"); raise SystemExit
                else:
                    Method_text = args[arg_sect+1].upper()
                    if args[arg_sect+1].lower() in ["http", "https"]:
                        PD = "http&https"
                        Method = f"{args[arg_sect+1].lower()}://"
                    else:
                        ProxyType = "--socks4"
                        PD = "socks4"
                    GetJson = subprocess.run(["timeout", "-v", str(timeout)+'s', "curl", "--http1.1", "https://raw.githubusercontent.com/the-computer-mayor/computer-mayor-db/main/PKPL.json",  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: raw.githubusercontent.com", "-H", "Accept: */*"], capture_output=True)
                    GetJson = (GetJson.stderr + GetJson.stdout).decode("utf-8")

                    if "200 OK" not in GetJson:
                        Print('?', f"\n    {r}Request to {p}(raw.githubusercontent.com){r} Failed.{m0}\n")
                        raise SystemExit

                    for fcb in GetJson:
                        if fcb in ['{', '}']:
                            if fcb_add == False:
                                fcb_add = True
                            else:
                                fcb_add = False
                            Json += fcb
                        elif fcb_add == True:
                            Json += fcb
                    PKPL = loads(Json)[PD]
                    arg = "--cpl"

            except IndexError:
                Print('?', f"\n    {r}You Did Not Enter A Proxy Type {p}(HTTP || SOCKS4){r}.{m0} (Example: --fps HTTP)\n")
                raise SystemExit


        # --cp
        if arg == "--cp":
            Print(text=f"\n    {p}<ip:port>: {m0}",End='')
            try:
                proxy = args[arg_sect+1]
                Print(text=g+proxy+m0)
                valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':']
                Print(text=f"    {p}Valid: {m0}", End='')
                IsValid = is_valid(proxy)

                if IsValid == "invalid_proxy":
                    Print('-', f"{r}Negative\n\nInvalid Proxy.{m0}"); raise SystemExit
                elif IsValid == "no_port":
                    Print('-', f"{r}Negative\n\nNo Port?{m0}"); raise SystemExit

                Print(text=f"{g}Positive\n    {p}Method: {b}{Method_text}\n    {p}Available To Use: {m0}", End='')
                IsAvailable = is_available(proxy)

                if IsAvailable == False:
                    Print('-', f"{r}Negative\n\n Proxy Doesn't Work :({m0}")
                elif IsAvailable == "timeout":
                    Print('-', f"{r}Negative\n\nProxy Connection Timed Out{m0}")
                else:
                    Print('+', text=f"{g}Positive {IsAvailable}{m0}\n", IA=proxy)

            except IndexError:
                Print('?', f"\n\n{r}You Did Not Enter An Internet Protocol Following the Port Proxy Address {p}(<ip:port>){r}.{m0} (Example: --cp 127.0.0.1:80)")
                raise SystemExit


        # --cpl & --fps
        elif arg == "--cpl":

            try:
                if Json == '':
                    proxy_list_file_arg = args[arg_sect+1]

                    with open(proxy_list_file_arg, 'r') as proxy_list_file:
                        proxy_list_uncorrected = proxy_list_file.readlines()
                    
                    proxy_list = list(map(lambda s: s.strip(), proxy_list_uncorrected))
                    if proxy_list == []: 
                        Print('?', f"\n    {y}Empty{m0}\n"); raise SystemExit

                    for line in range(len(proxy_list)): 
                        if proxy_list[line] in ['', ' ', '\n']:
                            removed_proxy_list_lines.append(proxy_list[line])
                    for n_line in removed_proxy_list_lines:
                        proxy_list.remove(n_line)
                else:
                    Print(text=f"\n    {p}Looking for {b}{Method_text}{p} Proxies...{m0}\n")
                    for link in PKPL:
                        if Method == "https://":
                            if "https" not in link[5:].lower():
                                Error = True
                            else:
                                Error = False
                        if Error == False:
                            GetProxyList = subprocess.run(["timeout", "-v", str(timeout)+'s', "curl", "--http1.1", link,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", "Accept: */*"], capture_output=True)
                            GetProxyList = (GetProxyList.stderr + GetProxyList.stdout).decode("utf-8")
                            if "200 OK" not in GetProxyList:
                                list_status = True
                                Print(text=f"    {r}[-] {b}{link}{r} Failed.{m0}")
                            else:
                                Print(text=f"    {g}[+] {b}{link}{g} Succeeded.{m0}\n")
                                proxy_list_uncleaned = GetProxyList.splitlines()
                                fcb_add = False
                                for pll in proxy_list_uncleaned[5:]:
                                    if pll == '':
                                        fcb_add = True
                                    elif fcb_add == True:
                                        proxy_list.append(pll)
                                break
                Erorr = False
                Print(text=f"\n    {p}Checking Proxies List Using {b}{Method_text}{p} Method{m0}\n")
                if threads > len(proxy_list):
                    for proxy in proxy_list:
                        T = threading.Thread(target=cpl, args=[proxy])
                        T.daemon = True
                        T.start()

                else:
                    ExtraThreads = []
                    exc_ftp = 0
                    rp = 0
                    p_calc = len(proxy_list) / threads
                    while p_calc.is_integer() != True:
                        ExtraThreads.append(proxy_list[rp])
                        rp += 1
                        exc_ftp += 1
                        p_calc = len(proxy_list) - exc_ftp
                        p_calc = p_calc / threads
                    for extra_thread in ExtraThreads:
                        proxy_list.remove(extra_thread)
                    rch = 0
                    origin_p_calc = int(p_calc)
                    i=0
                    for making_thread in range(threads):
                        i+=1
                        INPUT_ARG = proxy_list[int(rch):int(p_calc)]
                        T = threading.Thread(target=cpl, args=[INPUT_ARG])
                        T.daemon = True
                        rch = rch + origin_p_calc
                        p_calc = p_calc + origin_p_calc
                        T.start()
                    T = threading.Thread(target=cpl, args=[ExtraThreads])
                    T.daemon = True
                    T.start()
                    while All_threads != threads+1:None
                    if NotRaw and owp == True:
                        Print(text=f"\n\n    {b}(x){p} ==== Result ==== {b}(x){m0}\n")
                        if len(WorkingProxies) == 0:
                            Print(text=f"    {r}No Working Proxies :({m0}\n")
                            raise SystemExit

                        for Working_proxy in WorkingProxies:
                            Print(text=f"    {g}[+] {m0}{list(Working_proxy)[0]}    {g}{'{'+Working_proxy[list(Working_proxy)[0]]+'}'}        :){m0}")
                        Print(text='')
                    elif NotRaw == False:
                        if len(WorkingProxies) == 0:
                            Print('-'); raise SystemExit
                        print(WorkingProxies)
                    elif NotRaw and owp == False:
                        print()

            except IndexError:
                Print('?', f"\n{r}    You Did Not Enter A File That Contains Proxies Addresses Following Their Ports.{m0} (Example: --cpl test_proxies.txt)\n")
                raise SystemExit

            except FileNotFoundError: 
                Print('?', f"\n    {r}\"{p}{proxy_list_file_arg}{r}\"{y} Doesn't Exist.{m0}\n")
                raise SystemExit

# Exit Handler
except SystemExit:print(end=f'{m0}')

# Goodbye!,
except (SystemExit, KeyboardInterrupt):Print(text="\n\033[1;31mGoodbye!.\033[0m")
except:print("        \033[1;31m(x) ==== [ERROR] ==== (x)\033[0m\n");import traceback;traceback.print_exc()
