import msvcrt


def getchar(d, arg):
    return d.get(arg, d["DEFAULTS"][arg])


def getch():
    return msvcrt.getch().decode("utf-8")
