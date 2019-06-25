import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


def dumpException(e):
    print("%s EXCEPTION:" % e.__class__.__name__, e)
    traceback.print_tb(e.__traceback__)


def loadStylesheet(filename):
    print('STYLE loading:', filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

def loadStylesheets(*args):
    res = ''
    for arg in args:
        file = QFile(arg)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        res += "\n" + str(stylesheet, encoding='utf-8')
    QApplication.instance().setStyleSheet(res)
