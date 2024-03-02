try:
    # Libraries
    from urllib.parse import urlparse
    from time import perf_counter
    from json import loads, dumps
    from os.path import isfile
    from random import choice
    from string import digits
    from typing import Union
    from sys import argv
    import subprocess
    import threading
    import re



    # Colors
    m0, r, g, b, p = "\033[1;37m", "\033[1;31m", "\033[1;32m", "\033[1;34m", "\033[1;35m"


    # Logo
    logo = "\x1b[1;37m\n\t██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗\x1b[1;31m██╗  ██╗ ██████╗ ████████╗\t\x1b[1;32mv4\x1b[1;37m\n\t██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝\x1b[1;31m██║ ██╔╝██╔═══██╗╚══██╔══╝\x1b[1;37m\n\t██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ \x1b[1;31m█████╔╝ ██║   ██║   ██║\t\x1b[1;32mDiscord: https://discord.com/users/1172063042666762252\x1b[1;37m\n\t██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  \x1b[1;31m██╔═██╗ ██║   ██║   ██║\x1b[1;37m\n\t██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   \x1b[1;31m██║  ██╗╚██████╔╝   ██║\t\x1b[1;32mGithub: https://github.com/the-computer-mayor\x1b[1;37m\n\t╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   \x1b[1;31m╚═╝  ╚═╝ ╚═════╝    ╚═╝\n\x1b[1;37m"


    # Ops
    ui_main = f"{logo}\n\tProxy List Path {p}(IP:Port, File Path, Link) {r}⇒{m0}  "
    ui_proxy_type = f"{logo}\n\tProxy Type [HTTP, SOCKS4, SOCKS5] {r}⇒{m0}  "
    ui_owp = f"{logo}\n\tPrint Only Working Proxies [Y,N] {r}⇒{m0}  "
    ui_threads = f"{logo}\n\tNumber Of Threads {r}⇒{m0}  "
    ui_domain_path = f"{logo}\n\tDomain Path {r}⇒{m0}  "
    ui_filename = f"{logo}\n\tLog File Name {r}⇒{m0}  "
    ui_timeout = f"{logo}\n\tTimeout {r}⇒{m0}  "
    ui_domain = f"{logo}\n\tDomain {r}⇒{m0}  "
    ui_ssl = f"{logo}\n\tSSL [Y,N] {r}⇒{m0}  "


    # Standard Settings
    in_proccess_threads = 0
    all_threads = 0
    threads = 10
    timeout = 3

    test_domain_path = ''
    proxy_type = "http"
    ssl_show_file = ''
    test_domain = ''
    ssl_show = ''

    working_proxies = []
    extra_threads = []

    ssl = False
    owp = False




    # Clear Screen Function
    def cls():
        print("\x1B[2J\x1B[H")




    # Using Curl Instead of requests :P
    def curl(CMD:list):
        output = subprocess.run(CMD, capture_output=True)
        return (output.stderr + output.stdout).decode("utf-8", errors="ignore")




    # Checking If The Domain Is Valid Function
    def is_valid_domain(domain):
        domain_pattern = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$')
        return bool(domain_pattern.match(domain))




    # Checking If (IP:Port) Is Valid Function
    def is_valid_ip_port(ip_port):
        IP, Dot, colon = '', 0, 0
        valid_chars = list(digits+".:")



        for char in range(len(ip_port)):
            if ip_port[char] not in valid_chars:
                return "invalid_proxy"

            elif ip_port[char] in list(".:"):
                if ip_port[char] == '.':
                    Dot += 1

                elif ip_port[char] == ':':
                    IP = ip_port[:char]
                    colon += 1

                try:
                    _ = int(ip_port[char+1])
                    _ = int(ip_port[char-1])
                except:
                    return "invalid_proxy"



        if Dot == 3 and colon == 0 and len(IP)<=15 and len(IP)>7:
            return "missing_port"

        elif len(IP)>15 or len(IP)<7 or Dot != 3 or colon != 1:
            return "invalid_proxy"

        else:
            return "valid"




    # Check Proxy Health Function
    def check_proxy(
            proxy_ip_port:str,
            proxy_type = "HTTP",
            timeout:int = 3,
            ssl:bool = False,
            test_domain:str = '',
            test_domain_path:str = '',
            required_keyword:str = '',
            http_version:Union[int, float] = 1.1,
            extra_curl_args:list = []
        ):

        validation = is_valid_ip_port(proxy_ip_port)
        if validation != "valid": return ["invalid_input", validation, {"example": "1.1.1.1:80"}]



        test_domain_path = test_domain_path.lower()
        test_domain = test_domain.lower()
        proxy_type = proxy_type.lower()



        if proxy_type in ["http", "https"]:
            proxy_type = "--proxy"

        elif proxy_type in ["socks4", "socks5"]:
            proxy_type = "--"+proxy_type

        else:
            return ["invalid_input", "invalid_proxy_type", {"available_input": ["HTTP", "HTTPS", "SOCKS4", "SOCKS5"]}]



        if ssl: ssl = "https://"
        else: ssl = "http://"




        if http_version <= 1:
            http_version = float(http_version)

        if http_version not in [0.9, 1.1, 1.0, 2, 3]:
            return ["invalid_input", "invalid_http_version", {"available_input": [0.9, 1.1, 1, 1.0, 2, 3]}]



        if test_domain+test_domain_path+required_keyword == '':
            required_keyword = "Content-Type: application/json"
            test_domain = "ident.me"
            test_domain_path = "/json"

        elif test_domain_path[0] != '/':
            return ["invalid_input", "invalid_domain_path", {"example": "/homepage"}]


        if is_valid_domain(test_domain) == False:
            return ["invalid_input", "invalid_domain", {"example":"example.com"}]



        Command = [
            "curl", "-i", "-G",
            "--connect-time", str(timeout),
            "--max-time", str(timeout),
            "--url", ssl+test_domain+test_domain_path,
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "-H", f"Host: {test_domain}",
            proxy_type, proxy_ip_port
        ]
        Command.extend(extra_curl_args)



        TimeConnectStart = perf_counter()
        output = subprocess.run(Command, capture_output=True)
        TimeConnectEnd = perf_counter()

        output = (output.stderr + output.stdout).decode("utf-8", errors="ignore")
        TimeConnect = TimeConnectEnd - TimeConnectStart


        # Return
        if any(keyword in output for keyword in ["Operation timed out", "Connection timed out"]):
            return ["proxy_failed", "proxy_timeout", {"time_spent": TimeConnect}]

        elif any(keyword in output.lower() for keyword in ["http/2 200", "200 ok"]) and required_keyword.lower() in output.lower():
            return ["proxy_succeeded", TimeConnect, output]

        elif any(keyword in output for keyword in ["400 Bad Request", "409 Conflict", "Connection was reset"]):
            return ["proxy_failed", "junk_proxy", {"time_spent": TimeConnect}]

        elif "libcurl version doesn't support" in output:
            return ["invalid_input", "http_version_unsupported", {"curl": f"curl: option --http{http_version}: the installed libcurl version doesn't support this"}]
        
        else:
            return ["proxy_failed", "proxy_failed_transmitting_http_request", {"time_spent": TimeConnect}]




    # Check Proxy Group Thread Function
    def check_proxy_group(proxy_group:list, proxies_location_in_list:int):
        global all_threads, working_proxies

        for proxy in proxy_group:
            cp = check_proxy(
                proxy, ssl = ssl,
                proxy_type = proxy_type,
                timeout = timeout,
                test_domain = test_domain,
                test_domain_path = test_domain_path
            )

            if proxies_location_in_list == 6969696969:
                proxies_location_in_list = "EXTRA_THREAD"



            if cp[0] == "proxy_succeeded":
                time_spent = str("{:.4f}".format(cp[1]))+"ms"

                try:
                    for x in range(len(cp[2])):
                        if cp[2][x] == '{':
                            output_json = loads(cp[2][x:])
                    
                    city = output_json["city"]
                    country = output_json["country"]
                    location_string = f"  {b+country} {p}({city}){m0}"
                    log_file.write(f"{proxy} ☠ {proxy_type.upper()} ☠ {time_spent}{ssl_show_file}\n")
                    log_file.write(dumps(output_json))
                    log_file.write("\n\n")

                    if city == '': location_string = f"  {b+country+m0}"

                    print('\n'+' '*44+f"{m0+'{'+g+time_spent+m0+'}'+location_string}\r"+' '*16+f"{g}[+]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')
                    working_proxies.append(proxy)

                except KeyError:
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}Broken Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')


            elif cp[0] == "proxy_failed":
                if cp[1] == "proxy_timeout":
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}Timed Out{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')
                
                elif cp[1] == "junk_proxy":
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}Junk Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')
                
                elif cp[1] == "proxy_failed_transmitting_http_request":
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}Broken Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')


            elif cp[0] == "invalid_input":
                if len(proxy) > 15:
                    proxy = (proxy[:13]+"..")

                if cp[1] == "invalid_proxy":
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}Invalid Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')

                elif cp[1] == "missing_port":
                    if owp == False: print('\n'+' '*44+f"{m0+'{'+r}No Port?{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy+b}\r{str(proxies_location_in_list)+m0}",end='')



            if proxies_location_in_list != "EXTRA_THREAD": proxies_location_in_list += 1
        all_threads += 1




    # Main Validating Proxies Function
    def check_proxy_list(proxy_list:list, threads_count:int):
        global extra_threads, in_proccess_threads, ssl_show_file



        if ssl_show != '':
             ssl_show_file = " ☠ SSL"

        if threads_count > len(proxy_list) :
            for thread in proxy_list:
                check_proxy_group([thread], proxy_list.index(thread))


        else:
            while 1:
                thread_proxy_count = len(proxy_list) / threads_count
                if thread_proxy_count.is_integer():
                    for thread in range(0, len(proxy_list), int(thread_proxy_count)):
                        T = threading.Thread(target=check_proxy_group, args=[proxy_list[thread:thread+int(thread_proxy_count)], thread])
                        T.daemon = True
                        T.start()
                        in_proccess_threads += 1
                
                    for extra_thread in extra_threads:
                        T = threading.Thread(target=check_proxy_group, args=[[extra_thread], 6969696969])
                        T.daemon = True
                        T.start()
                        in_proccess_threads += 1
                    break

                else:
                    extra_proxy = choice(proxy_list)
                    extra_threads.append(extra_proxy)
                    proxy_list.remove(extra_proxy)




    # Args
    for arg in argv[1:]:
        if arg.lower() == "domain":
            while 1:
                cls(); domain_input = str(input(ui_domain)).lower().replace(' ', '')
                cls(); domain_path_input = str(input(ui_domain_path)).lower().replace(' ', '')


                if is_valid_domain(domain_input) == False:
                    cls(); input(f"{logo}\n\tInvalid Input, Try Again\n")

                else:
                    test_domain_path = '/'+domain_path_input
                    test_domain = str(domain_input)
                    break




    # Main
    while 1:
        cls(); proxy_list_path = str(input(ui_main))
        proxy_list_path_is_url = urlparse(proxy_list_path.replace(' ', ''))




        if proxy_list_path_is_url.scheme and proxy_list_path_is_url.netloc:
            cls(); print(f"{logo}\n\tRequesting {r+proxy_list_path+m0}")

            request_proxy_list_command = [
                "curl", "-i", "--http1.1", "-G",
                "--url", proxy_list_path.replace(' ', ''),
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                "-H", "Accept: */*"
            ]

            request = curl(request_proxy_list_command)


            if "http/1.1 200 ok" in request.lower():
                respond_lines = request.splitlines()[5:]
                cls(); print(f"{logo}\n\t{g}Done{m0}")
            
            else:
                cls(); input(f"{logo}\n\tFailed To Connect To {r+proxy_list_path+m0}, Try Again\n")
                continue


            for line in range(len(respond_lines)):
                if respond_lines[line] == '':
                    proxy_list = respond_lines[line+1:]



        elif isfile(proxy_list_path):
            proxy_list_file = open(proxy_list_path, 'r')
            proxy_list = list(map(lambda s: s.strip(), proxy_list_file.readlines()))
            proxy_list_file.close()



        elif is_valid_ip_port(proxy_list_path) == "valid":
            while 1:
                try:
                    cls(); timeout = int(input(ui_timeout))
                except ValueError:
                    cls(); input(f"{logo}\n\tInvalid Input, Try Again\n"); continue

                cls(); proxy_type_input = input(ui_proxy_type)
                if proxy_type_input.replace(' ', '').lower() in ["http", "https", "socks4", "socks5"]:
                    proxy_type = proxy_type_input.replace(' ', '').lower()

                cls(); ssl_input = input(ui_ssl)
                if ssl_input.lower().replace(' ', '') in ["yes", 'y', "true"]:
                    ssl = True

                break


            cls(); print(logo)

            cp = check_proxy(
                proxy_list_path,ssl=ssl,
                proxy_type=proxy_type,
                timeout=timeout,
                test_domain=test_domain,
                test_domain_path=test_domain_path
            )



            if cp[0] == "proxy_succeeded":
                time_spent = str("{:.4f}".format(cp[1]))+"ms"

                try:
                    for x in range(len(cp[2])):
                        if cp[2][x] == '{':
                            output_json = loads(cp[2][x:])
                    
                    city = output_json["city"]
                    country = output_json["country"]
                    location_string = f"  {b+country} {p}({city}){m0}"
                    if city == '': location_string = f"  {b+country+m0}"

                    print(' '*44+f"{m0+'{'+g+time_spent+m0+'}'+location_string}\r"+' '*16+f"{g}[+]  {m0+proxy_list_path+b}\n")

                except KeyError:
                    print('\n'+' '*44+f"{m0+'{'+r}Broken Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy_list_path+b}\n")


            elif cp[0] == "proxy_failed":
                if cp[1] == "proxy_timeout":
                    print(' '*44+f"{m0+'{'+r}Timed Out{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy_list_path+b}\n",)
                
                elif cp[1] == "junk_proxy":
                    print(' '*44+f"{m0+'{'+r}Junk Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy_list_path+b}\n")
                
                elif cp[1] == "proxy_failed_transmitting_http_request":
                    print(' '*44+f"{m0+'{'+r}Broken Proxy{m0+'}'}\r"+' '*16+f"{r}[-]  {m0+proxy_list_path+b}\n")


            raise SystemExit



        else:
            cls(); input(f"{logo}\n\tInvalid Input, Try Again\n")
            continue




        while 1:
            try:
                cls(); timeout = int(input(ui_timeout))
                if timeout <= 0:
                    raise ValueError

                cls(); threads = int(input(ui_threads))
                if timeout <= 0:
                    raise ValueError


                cls(); proxy_type_input = input(ui_proxy_type)
                if proxy_type_input.replace(' ', '').lower() in ["http", "https", "socks4", "socks5"]:
                    proxy_type = proxy_type_input.replace(' ', '').lower()


                cls(); ssl_input = input(ui_ssl)
                if ssl_input.lower().replace(' ', '') in ["yes", 'y', "true"]:
                    ssl = True
                if ssl:
                    ssl_show = f"{r} ☠  {p}SSL{m0}"



                cls(); owp_input = input(ui_owp)
                if owp_input.lower().replace(' ', '') in ["yes", 'y', "true"]:
                    owp = True




            except ValueError:
                cls(); input(f"{logo}\n\t{r}Invalid Input{m0}\n"); continue




            try:
                cls(); file_name = input(ui_filename).replace(' ', '').lower()
                log_file = open(file_name, 'w')
                cls(); print(f"{logo}\n\t{p+proxy_type.upper()+r} ☠  {p+str(threads)} Threads{r} ☠  {p+str(timeout)}s Timeout{m0}{ssl_show}\n")
                break



            except OSError:
                cls(); input(f"{logo}\n\t{r}Invalid File Name{m0}\n"); continue




        check_proxy_list(proxy_list, threads_count=threads)

        while 1:
            if all_threads == in_proccess_threads:
                print(f"\n{g}Done!.")
                log_file.close()
                raise SystemExit




# Exit Handlers
except SystemExit:
    print('\033[0m', end='')


except (SystemExit, KeyboardInterrupt):
    try:
        log_file.close()
    
    except NameError:
        pass

    finally:
        print("\n\033[1;31mGoodbye!.\033[0m")


except:
    from traceback import print_exc
    print("\n\t\033[1;31m(x) ==== [ERROR] ==== (x)\033[0m\n");print_exc()
