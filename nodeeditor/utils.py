import traceback


def dumpException(e):
    print("EXCEPTION:", e)
    traceback.print_tb(e.__traceback__)
