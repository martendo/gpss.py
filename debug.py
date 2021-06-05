debugflag = {
    "debug": False
}

def debugmsg(*args):
    if debugflag["debug"]:
        print("DEBUG:", *args)
