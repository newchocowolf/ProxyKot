try:
    # Libraries
    from time import perf_counter
    from sys import version_info
    from random import randint
    from time import sleep
    from os import system
    from json import load
    from sys import argv
    from sys import path
    import threading
    import socket


    # Default Settings
    with open(path[0]+"/settings.json") as json_file:
        settings = load(json_file)

    timeout = int(settings["timeout"])
    test_server = settings["test_server"]
    threads = int(settings["threads"])


    # Default Vars
    cmds = ["--cp", "--cpl", "fmp", "fmps", "rmp", "rmps"]
    printList = False
    cmds_in_args = 0
    All_threads = 0
    args = argv[1:]
    CH_args = list(args)
    remove_CH_args =[]
    removed_proxy_list_lines = []
    WorkingProxies = []
    m0 = "\033[0m"
    b = "\033[1;34m"
    r = "\033[1;31m"
    g = "\033[1;32m"
    p = "\033[1;35m"
    y = "\033[1;33m"
    NotRaw = True
    HELP_TXT = """\033[1;35m                                    _____                      \033[1;31m_  __     _   
\033[1;35m                                    |  __ \\                   \033[1;31m| |/ /    | |  
\033[1;35m                                    | |__) | __ _____  ___   _\033[1;31m| ' / ___ | |_ 
\033[1;35m                                    |  ___/ '__/ _ \\ \\/ / | | \033[1;31m|  < / _ \\| __|            \033[1;32mDiscord: myleader
\033[1;35m                                    | |   | | | (_) >  <| |_| \033[1;31m| . \\ (_) | |_             \033[1;32mGithub: the-computer-mayor
\033[1;35m                                    |_|   |_|  \\___/_/\\_\\\\__, \033[1;31m|_|\\_\\___/ \\__|
\033[1;35m                                                        __/ |              
\033[1;35m                                                        |___/               

                                 \033[0mA Useful Tool To Validate If A Proxy Or Multiple
                                          Are Able To Make A Successful
                                               \033[1;34m(GET HTTP)\033[0m Request.


                \033[1;32mUsage:\033[0m
                    
                        python3 ProxyKot.py \033[1;33m[Options]
                
                \033[1;32mOptions:\033[0m

                        \033[1;33m--cpl \033[2;49;37m<FileName>\033[0m            Validate A List Of Proxies.
                        \033[1;33m--cp \033[2;49;37m<Ip:Port>\033[0m              Validate A Singular Proxy.
                        \033[1;33m--timeout \033[2;49;37m<Seconds>\033[0m         Set A Timeout Limit In Seconds.
                        \033[1;33m-th \033[2;49;37m<Count>\033[0m                 Number Of Threads To Speed Up The Process.
                
                \033[1;32mFuture ProxyKot:\033[0m

                        This Is Only The First Release Of This Tool, In The Future This
                        Tool Will Have More Options Such As Supporting \033[1;34mHTTPS\033[0m And Other.
                        There Will Be An Optional Terminal UI, The Tool Itself Will Be
                        Even Faster And More Efficient.\n\n"""

    # Checking Python Version
    if version_info.major != 3:
        print(f"\n    {y}Python3 Required!{m0}\n")
        raise SystemExit


    # Clear Screen
    def cls():
        system("clear||cls")


    # Checking IP Validation Function
    def is_valid(ip_port):
        Dot = 0
        colon = 0
        valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':']

        for char in range(len(ip_port)):
            if ip_port[char] not in valid_chars:
                return "invalid_proxy"
            
            elif ip_port[char] == ':' or ip_port[char] == '.':
                if ip_port[char] == '.': Dot = Dot + 1
                elif ip_port[char] == ':': colon = colon + 1
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


    # Connecting With IP Function
    def is_available(Ip,PORT):
        try:
            TimeConnectStart = perf_counter()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((Ip,int(PORT)))
            s.sendall(bytes(f"GET {test_server} HTTP/1.1\r\n\r\n", "utf-8"))
            Respond = s.recv(1024).decode("utf-8")

            if "200 OK" in Respond:
                TimeConnectEnd = perf_counter()
                TimeConnect = TimeConnectEnd - TimeConnectStart
                s.close()
                return '{'+str(TimeConnect)+'ms}'

            else:
                s.close()
                return False
        
        except TimeoutError:
            s.close()
            return "timeout"
        
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, UnicodeDecodeError):
            s.close()
            return False


    # Extract Ip, Port Function
    def extractIPORT(IPORT):
        ip = ''
        port = ''
        IPORTFIG = False
        for i in IPORT:
            if i == ':':
                IPORTFIG = True
            elif IPORTFIG == False:
                ip = ip + i
            elif IPORTFIG == True:
                port = port + i
        return [ip, port]


    # Check Proxy List Function
    def cpl(IpsPorts):
        try:
            global All_threads
            global WorkingProxies

            for IpPort in IpsPorts:
                IsValid = is_valid(IpPort)

                if IsValid == "invalid_proxy":
                    if NotRaw: print(f"    {r}[-] {m0}{IpPort}    {r}(Invalid Proxy){m0}")
                elif is_valid == "no_port":
                    if NotRaw: print(f"    {r}[-] {m0}{IpPort}    {r}(No Port?){m0}")
                else:
                    IPORT = extractIPORT(IpPort)
                    IsAvailable = is_available(IPORT[0], IPORT[1])

                    if IsAvailable == "timeout":
                        if NotRaw: print(f"    {r}[-] {m0}{IpPort}    {r}(Timed Out){m0}")    
                    elif IsAvailable == False:
                        if NotRaw: print(f"    {r}[-] {m0}{IpPort}    {r}(Proxy Doesn't Work){m0}")
                    else:
                        if NotRaw: print(f"    {g}[+] {m0}{IpPort}    {g}({IsAvailable}){m0}");WorkingProxies.append(IpPort)
                        else: WorkingProxies.append(IpPort)
            All_threads = All_threads + 1
        except:                    
            All_threads = All_threads + 1
            

    # Ui
    if args == []:
        print("Ui")
        raise SystemExit

    # Extra Args Check
    for arg in args:
        arg = arg.lower()

        # Help
        if arg == "help" or arg == "--help":
            print(HELP_TXT, end='')
            raise SystemExit
    
        # Raw Output Only
        elif arg == "--raw":
            printList = True
            NotRaw = False
            args.remove("--raw")

    # Limits
    for arg in range(len(args)):
        try:

            # Timeout Limit
            if args[arg].lower() == "--timeout":
                timeout = int(args[arg+1])
            
            # Threads Limit
            if args[arg].lower() == "-th":
                threads = int(args[arg+1])

        except (IndexError, ValueError):
            if NotRaw: print(f"\n    {y}You Might Need To Use {r}({p}python3 {__file__} --help{y}{r}){m0}\n")
            else: print(f"{y}?{m0}")
            raise SystemExit
            

    # Organizing Args
    try:
        for ARG in args:
            if ARG in cmds:
                cmds_in_args = cmds_in_args + 1

        if cmds_in_args != 1:
            if NotRaw: print(f"\n    {y}You Might Need To Use {r}({p}python3 {__file__} --help{y}{r}){m0}\n")
            else:print(f"{y}?{m0}")
            raise SystemExit

        for CH_arg in range(len(CH_args)):
            if CH_args[CH_arg].lower() in ["--timeout", "--cp", "--cpl", "-th"]:
                remove_CH_args.append(CH_args[CH_arg+1])
                remove_CH_args.append(CH_args[CH_arg])

            elif CH_args[CH_arg].lower() in ["fmp", "fmps", "rmp", "rmps", "--raw"]:
                remove_CH_args.append(CH_args[CH_arg])

        for rcha in remove_CH_args:
            CH_args.remove(rcha)
        
        if len(CH_args) != 0:
            if NotRaw: print(f"\n    {y}You Might Need To Use {r}({p}python3 {__file__} --help{y}{r}){m0}\n")
            else: print(f"{y}?{m0}")
            raise SystemExit

    except IndexError:
        pass


    # [-- Start --]
    for arg_sect in range(len(args)):
        arg = args[arg_sect].lower()


        # --cp
        if arg == "--cp":
            if NotRaw: print(f"\n    {p}<ip:port>: {m0}",end='')
            try:
                proxy = args[arg_sect+1]
                if NotRaw: print(g+proxy+m0)
                valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':']
                if NotRaw: print(f"    {p}Valid: {m0}", end='')
                IsValid = is_valid(proxy)

                if IsValid == "invalid_proxy":
                    if NotRaw: print(f"{r}Negative\n\nInvalid Proxy.{m0}")
                    else: print(f"{r}-{m0}")
                    raise SystemExit
                elif IsValid == "no_port":
                    if NotRaw: print(f"{r}Negative\n\nNo Port?{m0}")
                    else: print(f"{r}-{m0}")
                    raise SystemExit
       
                IPORT = extractIPORT(proxy)

                if NotRaw: print(f"{g}Positive\n    {p}Method: {b}HTTP\n    {p}Available To Use: {m0}", end='')
                IsAvailable = is_available(IPORT[0], IPORT[1])

                if IsAvailable == False:
                    if NotRaw: print(f"{r}Negative\n\n Proxy Doesn't Work :({m0}")
                    else: print(f"{r}-{proxy}{m0}")
                elif IsAvailable == "timeout":
                    if NotRaw: print(f"{r}Negative\n\nProxy Connection Timed Out{m0}")
                    else: print(f"{r}-{proxy}{m0}")                
                else:
                    if NotRaw: print(f"{g}Positive {IsAvailable}{m0}\n")
                    else: print(f"{g}+{proxy}{m0}")

            except IndexError:
                if NotRaw: print(f"\n\n{r}You Did Not Enter An Internet Protocol Following the Port Proxy Address (<ip:port>). {m0}(Example: --cp 127.0.0.1)")
                else: print(f"{y}?{m0}")
                raise SystemExit


        # --cpl
        elif arg == "--cpl":

            try:
                proxy_list_file_arg = args[arg_sect+1]

                with open(proxy_list_file_arg, 'r') as proxy_list_file:
                    proxy_list_uncorrected = proxy_list_file.readlines()
                
                proxy_list = list(map(lambda s: s.strip(), proxy_list_uncorrected))
                if proxy_list == []: 
                    if NotRaw: print(f"\n    {y}Empty{m0}\n")
                    else:print(f"{y}?{m0}")
                    raise SystemExit

                for line in range(len(proxy_list)): 
                    if proxy_list[line] in ['', ' ', '\n']:
                        removed_proxy_list_lines.append(proxy_list[line])
                for n_line in removed_proxy_list_lines:
                    proxy_list.remove(n_line)

                if NotRaw: print(f"\n    {p}Checking Proxies List Using {b}HTTP{p} Method\n")
                if threads > len(proxy_list):
                    for proxy in proxy_list:
                        T = threading.Thread(target=cpl, args=[proxy])
                        T.start()

                else:
                    ExtraThreads = []
                    exc_ftp = 0
                    rp = 0
                    p_calc = len(proxy_list) / threads
                    while p_calc.is_integer() != True:
                        ExtraThreads.append(proxy_list[rp])
                        rp = rp + 1
                        exc_ftp = exc_ftp + 1
                        p_calc = len(proxy_list) - exc_ftp
                        p_calc = p_calc / threads
                    for extra_thread in ExtraThreads:
                        proxy_list.remove(extra_thread)
                    rch = 0
                    origin_p_calc = int(p_calc)
                    i=0
                    for making_thread in range(threads):
                        i=i+1
                        INPUT_ARG = proxy_list[int(rch):int(p_calc)]
                        T = threading.Thread(target=cpl, args=[INPUT_ARG])
                        rch = rch + origin_p_calc
                        p_calc = p_calc + origin_p_calc
                        T.start()
                    while All_threads != threads:None
                    if NotRaw: 
                        cls();print()
                        for Working_proxy in WorkingProxies:
                            print(f"    {g}[+] {m0}{Working_proxy}    {g}:){m0}")
                        print()
                    else:
                        print(WorkingProxies)


            except IndexError:
                if NotRaw: print(f"\n\n{r}You Did Not Enter A File That Contains Proxies Addresses Following Their Ports.{m0}")
                else: print(f"{y}?{m0}")
                raise SystemExit
            
            except FileNotFoundError: 
                if NotRaw: print(f"\n    {r}\"{p}{path[0]}/{proxy_list_file_arg}{r}\"{y} Doesn't Exist.{m0}\n")
                else: print(f"{y}?{m0}")
                raise SystemExit
            

except SystemExit:None
except (SystemExit, KeyboardInterrupt):print(f"\n{r}Goodbye!.{m0}")
except:print("        \033[1;31m==[ERROR]==\033[0m");import traceback;traceback.print_exc()
