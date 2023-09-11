"""
    This script defines the 'CoolAnimation' class, which creates a text-based animation effect.
    It uses a specified load string and cycles through different characters to create animation.

    * Usage:
        To use this script, simply create an instance of the 'CoolAnimation' class and call the 'display' method.

    * Example usage:
        from cool_animation import CoolAnimation

        # Create an instance of CoolAnimation
        animation = CoolAnimation(load_str="multimedia magic   audio visual heaven")

        # Display the animation until user input
        animation.display()

    * Example usage:
        if __name__ == '__main__':
            mm_avh = CoolAnimation()
            mm_avh.display()

        if __name__ == '__main__':
            mm_avh = CoolAnimation(load_str="audio visual heaven ",
                                   show_border=True,
                                   middle_offset=10,  # +/- chars from the middle
                                   use_animation=True)
            mm_avh.display()
"""


import os
import sys
import threading
import time
from typing import List


class CoolAnimation:
    """
    This class provides methods to display a text-based animation effect.

    Attributes:
        - load_str (str):
            The input string used for creating the animation effect.

        - ls_len (int):
            The length of the load string.

        - animation (str):
            A set of characters used for animation.

        - stop_animation (bool):
            A flag to control the animation loop.

        - show_border (bool):
            A flag to control whether to display the border around the animation.

        - middle_offset (int):
            An offset to customize the position where the animation character is displayed within the string.

        - use_animation (bool):
            A flag to control whether animation characters are added to the string.

    Methods:
        - __init__(self, load_str: str = "multimedia magic   audio visual heaven ",
                   show_border: bool = True, middle_offset: int = 2, use_animation: bool = True)
            Initializes a CoolAnimation object with given options.

        - display(self) -> None:
            Displays the animation until user input is detected.

        - check_input(self) -> None:
            Helper method to check for user input and stop the animation.

        - display(self) -> None:
            Main method to display the animation effect.
    """

    def __init__(self, load_str: str = "multimedia magic   audio visual heaven",
                 show_border: bool = True, middle_offset: int = -2, use_animation: bool = True) -> None:
        self.load_str: str = load_str
        self.ls_len: int = len(load_str)
        self.animation: str = "|/-\\"
        self.stop_animation: bool = False
        self.show_border: bool = show_border
        self.middle_offset: int = middle_offset
        self.use_animation: bool = use_animation

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

            if self.use_animation:
                middle: int = len(res) // 2 + self.middle_offset
                res_with_anim: str = res[:middle] + \
                    self.animation[anicount] + res[middle+1:]
            else:
                res_with_anim = res

            if self.show_border:
                sys.stdout.write(
                    "\r" + "\033[1;37m" + "╚═══ " + res_with_anim + " ═══╝ " + "\033[0m")
            else:
                sys.stdout.write(
                    "\r" + "\033[1;37m" + res_with_anim + "\033[0m")

            self.load_str = res
            time.sleep(0.075)
            anicount = (anicount + 1) % 4
            i = (i + 1) % self.ls_len
            counttime = counttime + 1
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
