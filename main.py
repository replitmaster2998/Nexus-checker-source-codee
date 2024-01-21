import asyncio
import ctypes
import json
import os
import random
import tkinter
import win32api
import time
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import colorama

import requests
from colorama import Fore, Style

import checker
from codeparts import checkers, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()

credit='''
                $$\   $$\                                         
                $$$\  $$ |                                        
                $$$$\ $$ | $$$$$$\  $$\   $$\ $$\   $$\  $$$$$$$\ 
                $$ $$\$$ |$$  __$$\ \$$\ $$  |$$ |  $$ |$$  _____|
                $$ \$$$$ |$$$$$$$$ | \$$$$  / $$ |  $$ |\$$$$$$\  
                $$ |\$$$ |$$   ____| $$  $$<  $$ |  $$ | \____$$\ 
                $$ | \$$ |\$$$$$$$\ $$  /\$$\ \$$$$$$  |$$$$$$$  |
                \__|  \__| \_______|\__/  \__| \______/ \_______/ 
                                                      
                                                      
                                                                    '''


class program():
    def __init__(self) -> None:
        self.count = 0
        self.checked = 0
        self.version = '3.15.3-xd'
        self.riotlimitinarow = 0
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))
        self.lastver = self.version

    def start(self):
        try:
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('No internet connection')
            os._exit(0)
        os.system('cls')
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(
            colors) + char for char in f'Nexus']

        self.CheckIfFirstStart()

        if 'devtest' in self.version:
            pass
        elif 'beta' in self.version:
            pass
        elif self.lastver != self.version:
            pass
            if inquirer.confirm(
                message="{}Would you like to download it now?".format(system.get_spaces_to_center('Would you like to download it now? (Y/n)')), default=True, qmark=''
            ).execute():
                os.system(f'{self.parentpath}/updater.bat')
                os._exit(0)
        print(credit)
        menu_choices = [
            Separator(),
            'Start Checker',
            'Single-Line Checker',
            'Edit Settings',
            'Sort Valid',
            'Test Proxy',
            'Info',
            Separator(),
            'Exit'
        ]
        res = inquirer.select(
            message="",
            choices=menu_choices,
            default=menu_choices[0],
            pointer='[>]',
            qmark=''
        ).execute()
        if res == menu_choices[1]:
            self.main()
            input('Finished checking. press ENTER to exit')
            pr.start()
        elif res == menu_choices[2]:
            slchecker = checker.singlelinechecker()
            slchecker.main()
            pr.start()
        elif res == menu_choices[3]:
            sys.edit_settings()
            pr.start()
        elif res == menu_choices[4]:
            valid.customsort()
            input('Done. press ENTER to exit')
            pr.start()
        elif res == menu_choices[5]:
            sys.checkproxy()
            pr.start()
        elif res == menu_choices[6]:
            os.system('cls')
            print(f'''
    Nexus by Owner1337

    yo whatsup


  [~] - press ENTER to return
            ''')
            input()
            pr.start()
        elif res == menu_choices[8]:
            os._exit(0)

    def get_accounts(self):
        filetypes = (
            ("", ("*.txt", "*.vlchkr")),
            ("All files", "*.*")
        )
        root = tkinter.Tk()
        file = filedialog.askopenfile(parent=root, mode='rb', title='Select a file with combos OR .vlchkr ro continue checking',
                                      filetypes=filetypes)
        root.destroy()
        os.system('cls')
        if file == None:
            os._exit(0)
        filename = str(file).split("name='")[1].split("'>")[0]
        if (".vlchkr" in filename):
            valkekersource = systems.vlchkrsource(filename)
            return valkekersource
        with open(str(filename), 'r', encoding='UTF-8', errors='replace') as file:
            lines = file.readlines()
            ret = []
            if len(lines) > 100000:
                if inquirer.confirm(
                    message=f"You have more than 100k accounts ({len(lines)}). Do you want to skip the sorting part? (it removes doubles and bad logpasses but can be long)",
                    default=True,
                    qmark='!',
                    amark='!'
                ).execute():
                    self.count = len(lines)
                    return lines
            for logpass in lines:
                logpass = logpass.strip()
                # remove doubles
                if logpass not in ret and ':' in logpass:
                    self.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f'Nexus | Loading Accounts ({self.count})')
                    ret.append(logpass)
            return ret

    def main(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Nexus | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Nexus | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        if proxylist == None:
            path = os.getcwd()
            file_path = f"{os.path.abspath(os.path.join(path, os.pardir))}\\proxy.txt"

            response = input(
                'No Proxies Found, Do you want to scrape proxies? (y/n): ')
            print(Style.RESET_ALL, end='')

            if response.lower() == 'y':
                f = open('system\\settings.json', 'r+')
                data = json.load(f)
                proxyscraper = data['proxyscraper']
                f.close()

                # Scrape proxies
                url = proxyscraper
                proxies = requests.get(url).text.split('\r\n')

                # Save proxies to file
                with open(file_path, 'w') as f:
                    f.write("\n".join(proxies))

                # Print number of proxies saved
                num_proxies = len(proxies)
                print(f'{num_proxies} Proxies saved to "proxy.txt" file.')
                proxylist = sys.load_proxy()
            else:
                print('Running Proxy Less...')

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Nexus | Loading Accounts')
        print('loading accounts')

        accounts = self.get_accounts()

        print('Loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Nexus | Authkey Checking...')
        sys.load_assets()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'Nexus | Loading Checker')
        scheck = checker.simplechecker(settings, proxylist, self.version)

        isvalkekersource = False
        if type(accounts) == systems.vlchkrsource:
            isvalkekersource = True
        asyncio.run(scheck.main(accounts, self.count, isvalkekersource))
        return

    def CheckIfFirstStart(self) -> None:
        with open("system/xd.txt", 'r+') as r:
            if r.read() == '0':
                result = win32api.MessageBox(None,
                                             """Hello! Looks like it's your first start of Nexus.
Although you can find the FAQ and the full guide in my discord, I will specify some things here.


What is a Riot Limit? When you send a lot of auth requests from one IP, riot blocks you for some time.
So that's why you should use proxies for checking. If riot bans your IP, you will not be able to login in their launcher or site for ~30 minutes.

Where can I find proxies? Any website you trust, just search for that in the internet. Or you can ask other people on my discord server.

Where can I find combos? Actually, the answer is the same as with proxies. The internet. But if you want to do combos yourself, you can buy a cheap and effective method on my discord server.


The link to my discord server can be found in the readme section of the github repository or on the Nexus title screen.

Good luck!""", "Hello!", 0)
                r.write("1")


if __name__ == '__main__':
    pr = program()

try:
    with open(os.path.join(pr.parentpath, 'src/license/data.json'), 'r') as file:
        data = json.load(file)
    print('Loading Setting...')
    time.sleep(1)
    pr.start()
except FileNotFoundError:
    print("Please put your key")
    exit()