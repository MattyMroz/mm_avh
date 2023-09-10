import os
import sys
import threading
import time
from typing import List


class CoolAnimation:
    def __init__(self, load_str: str = "multimedia magic   audio visual heaven ") -> None:
        self.load_str: str = load_str
        self.ls_len: int = len(load_str)
        self.animation: str = "|/-\\"
        self.stop_animation: bool = False

    def check_input(self) -> None:
        input()
        self.stop_animation = True

    def display(self) -> None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        anicount: int = 0
        counttime: int = 0
        i: int = 0

        threading.Thread(target=self.check_input).start()

        while not self.stop_animation:
            time.sleep(0.075)
            load_str_list: List[str] = list(self.load_str)
            x: int = ord(load_str_list[i])
            y: int = 0
            if x != 32:  # 32 is ASCII for ' '
                y = x-32 if x > 90 else x + 32
                load_str_list[i] = chr(y)
            res: str = ''
            for j in range(self.ls_len):
                res = res + load_str_list[j]
            middle: int = len(res) // 2 - 2 # Middle of the string where the animation will be displayed
            res_with_anim: str = res[:middle] + \
                self.animation[anicount] + res[middle+1:]
            sys.stdout.write(
                "\r" + "\033[1;37m" + "╚═══ " + res_with_anim + " ═══╝ " + "\033[0m")
            self.load_str = res
            time.sleep(0.075)
            anicount = (anicount + 1) % 4
            i = (i + 1) % self.ls_len
            counttime = counttime + 1
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


if __name__ == '__main__':
    mm_avh: CoolAnimation = CoolAnimation()
    mm_avh.display()
