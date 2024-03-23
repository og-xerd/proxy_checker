import requests
import threading
import time
import json
import time
import ctypes
import os


class Main:
    def __init__(self) -> None:
        settings_file = open("settings.json", "r", encoding="utf-8").read()
        settings_json = json.loads(settings_file)

        self.proxies_file = open("proxies.txt", "r", encoding="utf-8").readlines()
        self.proxies_type = ["http", "https", "socks4", "socks5"]

        self.threads_limit = settings_json['threads_limit']

        self.timeout_check = settings_json["timeout_settings"]["timeout_check"]
        self.timeout_limit = settings_json["timeout_settings"]["timeout_limit"]

        self.threads = 0
        self.completed = 0
        self.failed = 0
        self.totallines = len(self.proxies_file)
        self.valid = 0

        self.http_https = 0
        self.socks4 = 0
        self.socks5 = 0

        self.http_https_hits = []
        self.socks4_hits = []
        self.socks5_hits = []

    def update(self):
        while True:
            if self.completed == self.totallines:
                break
                
            os.system("cls")
            print(f"""
 \33[33m[?] CHECKED: \33[90m{self.completed} / {self.totallines}
 \33[32m[+] VALID: \33[90m{self.valid}
 \33[31m[-] FAIL: \33[90m{self.failed}

 \33[37mHTTP/HTTPS: \33[90m{self.http_https}
 \33[37mSOCKS4: \33[90m{self.socks4}
 \33[37mSOCKS5: \33[90m{self.socks5}\33[90m
            """)
            time.sleep(0.5)

    def check(self, proxy):
        for i in self.proxies_type:
            try:
                proxies = {
                    "https": f"{i}://{proxy}"
                }
    
                start = time.time()
                requests.post("https://api.myip.com/", proxies=proxies, timeout=15)
                elapsed = (time.time() - start)
                elapsed_converted = int(round(elapsed, 2) * 1000)

                if self.timeout_check == True:
                    if self.timeout_limit < elapsed_converted:
                        return

                self.valid += 1
        
                if i == "http" or i == "https":
                    self.http_https += 1
                    self.http_https_hits.append(proxy)
                elif i == "socks4":
                    self.socks4 += 1
                    self.socks4_hits.append(proxy)
                elif i == "socks5":
                    self.socks5 += 1
                    self.socks5_hits.append(proxy)

                success = True

                break
            except:
                success = False
            
        if success == False:
            self.failed += 1

        self.threads -= 1
        self.completed += 1

    def main(self):
        update = threading.Thread(target=self.update)
        update.start()
        for i in self.proxies_file:
            while True:
                if self.threads < self.threads_limit:
                    break
                
            self.threads += 1
            x = threading.Thread(target=self.check, args=(i.strip(),))
            x.start()
        
        update.join()
        http_https_file = open("proxy_hits/http_https.txt", "w")
        socks4_file = open("proxy_hits/socks4.txt", "w")
        socks5_file = open("proxy_hits/socks5.txt", "w")
        for i in self.http_https_hits:
            http_https_file.write(i + "\n")

        for i in self.socks4_hits:
            socks4_file.write(i + "\n")

        for i in self.socks5_hits:
            socks5_file.write(i + "\n")

        print('asdas')

if __name__ == "__main__":
    Main().main()