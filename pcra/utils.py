import os
import sys
import subprocess
import re


try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
except ModuleNotFoundError:
    # If colorama is not installed create failover classes for colored text output
    if os.name == 'nt':
        print("[Colored output not available]")

        class Fore:
            CYAN = ''
            YELLOW = ''
            RED = ''

        class Style:
            RESET_ALL = ''
    else:
        class Fore:
            CYAN = '\033[1;36;48m'
            YELLOW = '\033[1;33;48m'
            RED = '\033[1;31;48m'

        class Style:
            RESET_ALL = '\033[1;37;0m'


process_kwargs = dict(stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      universal_newlines=True,
                      text=True
                      )
if os.name == 'nt':
    process_kwargs['shell'] = True  # Windows npm commands fail without shell: FileNotFoundError


def printmsg(msg):
    print(f'{Fore.CYAN}{msg}{Style.RESET_ALL}')


def printerr(msg):
    print(f'{Fore.RED}{msg}{Style.RESET_ALL}')


def printwarn(msg):
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')


def check_python_version(version_required):
    python_version = sys.version_info
    required_version = tuple(map(int, version_required.split('.')))
    return (python_version.major, python_version.minor) == required_version


def check_git_installed():
    try:
        process = subprocess.Popen(['git', '--version'], **process_kwargs)
        return process.stdout.readline().startswith('git version')
    except FileNotFoundError as e:
        print(e)
        return False


def check_npm_installed():
    try:
        process = subprocess.Popen(['npm', '--version'], **process_kwargs)
        r = re.compile(r'^\d+\.\d+\.\d+$')  # 6.14.8
        return r.match(process.stdout.readline()) is not None
    except FileNotFoundError as e:
        print(e)
        return False


def print_if_data(msg):
    msg_text = msg.strip()
    if len(msg_text) > 0:
        print(msg_text)


def run_cmd(args):
    process = subprocess.Popen(args, **process_kwargs)

    while True:
        output = process.stdout.readline()
        print_if_data(output)
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print_if_data(output)

            if return_code != 0:
                print('RETURN CODE:', return_code)
                for output in process.stderr.readlines():
                    print_if_data(output)

            break
