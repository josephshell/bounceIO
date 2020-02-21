import datetime


def debug(msg: str):
    time = datetime.datetime.now().time()
    print("[%s]: %s" % (time, msg))
