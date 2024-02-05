try:
    # Libraries
    from os import name as OSNAME
    from time import perf_counter
    from sys import version_info
    from os.path import basename
    from random import shuffle
    from sys import executable
    from random import choice
    from json import loads
    from os import getpid
    from os import system
    from sys import argv
    import subprocess
    import threading



    # Python Location
    python = basename(executable)



    # Default Vars
    threads, test_server, timeout, Method, ProxyType, ProxyKot_Lists = 4, "ipinfo.io", 3, "http://", "--proxy", "https://raw.githubusercontent.com/the-computer-mayor/computer-mayor-db/main/PKPL.json"



    # Colors
    m0, r, g, y, b, p = "\033[1;0;0m", "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m"



    # Lists
    args, removed_proxy_list_lines, WorkingProxies, proxy_list, WorkingProxies_resolved, WorkingProxies_sorted, ExtraThreads = argv[1:], [], [], [], [], [], []



    # Logo
    Logo = f"""\n                                     {p}____                     {r} _  __     _
{m0}                                    {p}|  __ \\                   {r}| |/ /    | |
{m0}                                    {p}| |__) | __ _____  ___   _{r}| ' / ___ | |_
{m0}                                    {p}|  ___/ '__/ _ \\ \\/ / | | {r}|  < / _ \\| __|{m0}            {g}Discord: myleader
{m0}                                    {p}| |   | | | (_) >  <| |_| {r}| . \\ (_) | |_{m0}             {g}Github: the-computer-mayor
{m0}                                    {p}|_|   |_|  \\___/_/\\_\\\\__, {r}|_|\\_\\___/ \\__|
{m0}                                                        {p}__/ |
{m0}                                                        {p}|___/{m0}\n"""

    # Help Text
    HELP_TXT = f"""{Logo}\n
                                      {m0}A CHECK & FIND PROXIES AND MUCH MORE!
                                      \033[1;36m( HTTP || HTTPS || SOCKS4 || SOCKS5 ){m0}
                                                      \033[1;34m( v3 ){m0}\n\n
                {g}Usage:{m0}
                        {python} {basename(__file__)} {y}[Options]{m0}\n\n
                {g}Main Options:{m0}\n
                        {y}--fps{m0} \033[2;49;37m<ProxyType>{m0}           Find \033[1;36mHTTP{m0} Or \033[1;36mHTTPS{m0} Or \033[1;36mSOCKS4{m0} Or \033[1;36mSOCKS5{m0} Working Proxies.
                                                    (Example: --fps HTTP)\n
                        {y}--px{m0} \033[2;49;37m<Count>{m0}                Terminate After Printing A Specified Amount Of Working Proxies.
                        {y}--cpl{m0} \033[2;49;37m<FileName>{m0}            Validate A List Of Proxies.
                        {y}--cp{m0} \033[2;49;37m<IP:Port>{m0}              Validate A Singular Proxy.
                        {y}--timeout{m0} \033[2;49;37m<Seconds>{m0}         Set A Timeout In Seconds.\n
                        {y}--th{m0} \033[2;49;37m<Count>{m0}                Number Of Threads To Speed Up The Process.
                                                    \033[1;31m(Too Much Can Cause An Error & Terminating The Process){m0}\n\n
                {g}Additional Options:{m0}\n
                        {y}-http{m0}                       Use Only \033[1;36mHTTP{m0}.
                        {y}-https{m0}                      Use Only \033[1;36mHTTPS{m0}.
                        {y}-socks4{m0}                     Use Only \033[1;36mSOCKS4{m0}.
                        {y}-socks5{m0}                     Use Only \033[1;36mSOCKS5{m0}.
                        {y}-owp{m0}                        Prints Only Working Proxies.
                        {y}-raw{m0}                        Raw Aka Json Output.
                        {y}-1{m0}                          Get A Singular Working Proxy Then Terminate.\n\n"""



    # Other
    Method_text, CH_arg, Json, extra_link, All_threads, cdp, px, rch, NotRaw, owp, NextPass, Singed, Error, CutOff, fcb_add  = "HTTP", '', '', '', 0, 0, 0, 0, True, True, False, False, False, False, False



    # Print Function
    def Print(type='t', text='', End='\n', IA=''):
        if End == "cdp":
            End=f"\r{b}x{cdp}x{m0}\n"

        if type == "-?":
            if NotRaw and owp:
                print(text, end=End)

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



    # Proxy Health
    def is_available(IpPort):
        if OSNAME == "nt":CMD = ["curl", "-i", ProxyType, IpPort, Method+test_server+extra_link, "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: {test_server}", "-H", "Accept: */*"]
        else:CMD = ["timeout", "-v", str(timeout)+'s', "curl", "-i", ProxyType, IpPort, Method+test_server+extra_link, "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: {test_server}", "-H", "Accept: */*"]
        TimeConnectStart = perf_counter()
        Respond = subprocess.run(CMD, capture_output=True)
        Respond = (Respond.stderr + Respond.stdout).decode("utf-8")
        TimeConnectEnd = perf_counter()


        if "timeout" in Respond.lower() or "timed out" in Respond.lower():
            return "timeout"

        elif Method == "http://" and "content-type: application/json" in Respond.lower() and "200 OK" in Respond:
            print(Respond)
            TimeConnect = TimeConnectEnd - TimeConnectStart
            return '{'+str(TimeConnect)+'s}'
        
        elif Method == "https://" and "CONNECTION HAS REACHED (the-computer-mayor)" in Respond:
            TimeConnect = TimeConnectEnd - TimeConnectStart
            return '{'+str(TimeConnect)+'s}'

        else:
            return False



    # Check Proxy List Function
    def cpl(IpsPorts):
        try:
            global cdp, All_threads, WorkingProxies

            for IpPort in IpsPorts:
                IsValid = is_valid(IpPort)

                if IsValid == "invalid_proxy":
                    cdp += 1
                    Print('-?', f"        {r}[-] {m0}{IpPort}    {r}(Invalid Proxy){m0}", "cdp")
                elif is_valid == "no_port":
                    cdp += 1
                    Print('-?', f"        {r}[-] {m0}{IpPort}    {r}(No Port?){m0}", "cdp")
                else:
                    IsAvailable = is_available(IpPort)
                    if IsAvailable == "timeout":
                        cdp += 1
                        if owp: Print('-?', f"        {r}[-] {m0}{IpPort}    {r}(Timed Out){m0}", "cdp")
                    elif IsAvailable == False:
                        cdp += 1
                        Print('-?', f"        {r}[-] {m0}{IpPort}    {r}(Proxy Doesn't Work){m0}", "cdp")
                    else:
                        WorkingProxies.append({IpPort:IsAvailable[1:-3]})
                        cdp += 1
                        Print('+', f"        {g}[+] {m0}{IpPort}    {g}{IsAvailable}{m0}", "cdp",  IA=IpPort)
                        if CutOff == True:
                            pid = getpid()
                            if OSNAME == "nt":
                                system(f"taskkill /F /PID {pid} > NUL")
                            else:
                                system(f"kill {pid} > /dev/null")
        finally:
            All_threads += 1



    # Help
    if "--help" in args or "help" in args or args == []:
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
                test_server = "raw.githubusercontent.com"
                extra_link = "/the-computer-mayor/computer-mayor-db/main/chr"
                Method_text = "HTTPS"

            else:
                Error = True
            Signed = True

        # HTTP Only
        elif arg == "-http":
            if Singed == False:
                Method = "http://"
                Method_text = "HTTP"
            else:
                Error = True
            Signed = True

        # SOCKS4 Only
        elif arg == "-socks4":
            if Singed == False:
                ProxyType = "--socks4"
                Method_text = "SOCKS4"
            else:
                Error = True
            Signed = True

        # SOCKS5 Only
        elif arg == "-socks5":
            if Singed == False:
                ProxyType = "--socks5"
                Method_text = "SOCKS5"
            else:
                Error = True
            Signed = True


    for Value in ["-http", "-https", "-raw", "-socks4", "-socks5", "-1", "-owp"]:
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
            elif C_arg == "--px":
                px = int(args[arg+1])
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
            Print('?', f"\n    {y}You Might Need To Use {r}({p}{python} {basename(__file__)} --help{r}){m0}\n"); raise SystemExit



    # [-- Start --]
    for arg_sect in range(len(args)):
        arg = args[arg_sect].lower()



        # --fps
        if arg == "--fps":
            try:
                if args[arg_sect+1].lower() not in ["socks4", "socks5", "http", "https"]:
                    Print('?', f"\n    {y}What Is {r}({p}{args[arg_sect+1]}{r}) {y}?{m0}\n"); raise SystemExit
                else:
                    Method_text = args[arg_sect+1].upper()
                    if args[arg_sect+1].lower() in ["http", "https"]:
                        PD = "http&https"
                        Method = f"{args[arg_sect+1].lower()}://"
                        if args[arg_sect+1].lower() == "https":
                            test_server = "raw.githubusercontent.com"
                            extra_link = "/the-computer-mayor/computer-mayor-db/main/chr"
                    elif args[arg_sect+1].lower() == "socks4":
                        ProxyType = "--socks4"
                        PD = "socks4"
                    elif args[arg_sect+1].lower() == "socks5":
                        ProxyType = "--socks5"
                        PD = "socks5"

                    if OSNAME == "nt":GetJson = subprocess.run(["curl", "--http1.1", ProxyKot_Lists,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: raw.githubusercontent.com", "-H", "Accept: */*"], capture_output=True)
                    else:GetJson = subprocess.run(["timeout", "-v", str(timeout)+'s', "curl", "--http1.1", ProxyKot_Lists,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", f"Host: raw.githubusercontent.com", "-H", "Accept: */*"], capture_output=True)
                    GetJson = (GetJson.stderr + GetJson.stdout).decode("utf-8")

                    if "200 OK" not in GetJson:
                        Print('?', f"\n    {r}Request to ProxyKot Proxy Lists --> {p}({ProxyKot_Lists[8:]}){r} Failed.{m0}\n")
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
                Print('?', f"\n    {r}You Did Not Enter A Proxy Type {p}(HTTP || HTTPS || SOCKS4 || SOCKS5){r}.{m0} (Example: --fps HTTP)\n")
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
                    shuffle(PKPL)
                    for link in PKPL:
                        if OSNAME == "nt":GetProxyList = subprocess.run(["curl", "--http1.1", link,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", "Accept: */*"], capture_output=True)
                        else:GetProxyList = subprocess.run(["timeout", "-v", str(timeout)+'s', "curl", "--http1.1", link,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", "Accept: */*"], capture_output=True)
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


                if threads >= len(proxy_list):
                    for proxy in proxy_list:
                        T = threading.Thread(target=cpl, args=[[proxy]])
                        T.daemon = True
                        T.start()
                    Print(text=f"\n    {p}Validating A List Of Proxies Using {b}{Method_text}{p} Method{m0}\n")
                else:
                    p_calc = len(proxy_list) / threads

                    if p_calc.is_integer() != True:
                        while p_calc.is_integer() != True:
                            Rproxy = choice(proxy_list)
                            ExtraThreads.append(Rproxy)
                            proxy_list.remove(Rproxy)
                            p_calc = len(proxy_list) / threads
                    else:
                        Json = ''

                    Print(text=f"\n    {p}Validating A List Of Proxies Using {b}{Method_text}{p} Method{m0}\n{m0}")
                    origin_p_calc = int(p_calc)
                    for making_thread in range(threads):
                        INPUT_ARG = proxy_list[int(rch):int(p_calc)]
                        T = threading.Thread(target=cpl, args=[INPUT_ARG])
                        T.daemon = True
                        rch = rch + origin_p_calc
                        p_calc = p_calc + origin_p_calc
                        T.start()
                    for Extra_Thread in ExtraThreads:
                        T = threading.Thread(target=cpl, args=[[Extra_Thread]])
                        T.daemon = True
                        T.start()
                while All_threads != threads+len(ExtraThreads):
                    if px!=0:
                        if len(WorkingProxies) >= px:
                            NotRaw = False
                            break

                for ProxyTimeT in WorkingProxies:
                    WorkingProxies_resolved.append(float(ProxyTimeT[list(ProxyTimeT)[0]]))
                WorkingProxies_resolved.sort()

                for faster in WorkingProxies_resolved:
                    for Working_Proxy in WorkingProxies:
                        if faster == float(Working_Proxy[list(Working_Proxy)[0]]):
                            WorkingProxies_sorted.append(Working_Proxy)
                            break
                if NotRaw and owp == True:
                    Print(text=f"\n\n    {b}(x){p} ==== Result ==== {b}(x){m0}\n")
                    if len(WorkingProxies) == 0:
                        Print(text=f"    {r}No Working Proxies :({m0}\n")
                        raise SystemExit

                    for Working_proxy in WorkingProxies_sorted:
                        Print(text=' '*60+f"{g}XD{m0}\r"+' '*33+f"{g}{'{'+Working_proxy[list(Working_proxy)[0]]+'s}'}"+f"\r    {g}[+] {m0}{list(Working_proxy)[0]}")
                    Print(text='')

                elif NotRaw and owp == False and len(WorkingProxies) == 0:
                    Print(text=f"    {r}No Working Proxies :({m0}\n")

                elif NotRaw == False:
                    if len(WorkingProxies) == 0:
                        Print('-'); raise SystemExit
                    print(str(WorkingProxies_sorted).replace("'", '"'))

                elif NotRaw and owp == False:
                    print()


            except IndexError:
                Print('?', f"\n{r}    You Did Not Enter A File That Contains Proxies Addresses Following Their Ports.{m0} (Example: --cpl test_proxies.txt)\n")
                raise SystemExit


            except FileNotFoundError:
                Print('?', f"\n    {r}\"{p}{proxy_list_file_arg}{r}\"{y} Doesn't Exist.{m0}\n")
                raise SystemExit




# Exit Handler
except SystemExit:print(end='\033[0m')



# Goodbye!,
except (SystemExit, KeyboardInterrupt):Print(text="\n\033[1;31mGoodbye!.\033[0m")
except:print("        \033[1;31m(x) ==== [ERROR] ==== (x)\033[0m\n");import traceback;traceback.print_exc()
