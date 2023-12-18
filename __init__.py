__all__ = [
	"scripts"
]

__name__ = "hamradio"

def reverse(msg: str):  # <-- this name shadows the 'reverse.py' submodule
    return msg[::-1]    #     in the case of a 'from sound.effects import *'