import os
import sys
import time
import shutil

try:
    from colorama import Fore, Style
except ImportError:
    print(f"{os.path.abspath(__file__)}: Warning: colorama (optional) not installed, proceeding without.")

start_time = time.time()
global_title = ""
global_unit = "it"
global_maximum = 0
global_current = 0

def update(current=None, maximum=None, title=None, unit=None):
    global global_maximum, global_title, global_unit, global_current
    if maximum is not None:
        global_maximum = maximum
    if title is not None:
        global_title = title
    if unit is not None:
        global_unit = unit
    if current is not None:
        global_current = current +1
    else:
        global_current += 1

    try:
        progress = global_current / global_maximum
    except ZeroDivisionError:
        progress = 0


    if progress > 1:
        progress = 1

    elapsed_time = time.time() - start_time

    try:
        it_per_sec = progress*global_maximum / elapsed_time
    except ZeroDivisionError:
        it_per_sec = 10

    if global_current >= global_maximum:
        eta = 0
    else:
        try:
            eta = (elapsed_time / progress) * (1 - progress)
        except ZeroDivisionError:
            eta = 0
    try:
        information = (
            f" {Fore.GREEN}{global_current}/{global_maximum} {global_unit}"
            f"  {Fore.RED}{it_per_sec:.1f} {global_unit}/s"
            f"  {Fore.BLUE}ETA: {eta:.1f}s{Style.RESET_ALL}"
        )
    except NameError:
        information = (
            f" {global_current}/{global_maximum} {global_unit}"
            f"  {it_per_sec:.1f} {global_unit}/s"
            f"  ETA: {eta:.1f}s"
        )

    term_width, _ = shutil.get_terminal_size()
    bar_length = term_width - len(information) - len(global_title)
    filled_length = int(progress * bar_length)
    bar = f"{Fore.WHITE}━" * filled_length + " " + f"{Fore.LIGHTBLACK_EX}━" * (bar_length - filled_length)
    output = f"\r{Style.BRIGHT}{global_title}{Style.RESET_ALL} {bar} {information}{Style.RESET_ALL}"
    sys.stdout.write(output)
    sys.stdout.flush()
    if global_current-1 == global_maximum:
        sys.stdout.flush()
        print()
        sys.stdout.flush()

def init(title:str="", unit:str="it", maximum:float=0):
    global start_time
    start_time = time.time()
    if maximum != 0:
        update(current=0, title=title, unit=unit, maximum=maximum)