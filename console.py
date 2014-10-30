from cli import Application
from app import connect

if __name__ == "__main__":
    #import sys
    #sys.path.append('/Applications/PyCharm.app/pycharm-debug.egg')
    #import pydevd
    #pydevd.settrace('localhost', port=9191, stdoutToServer=True, stderrToServer=True)
    connect()
    App = Application()
    try:
        App.run()
    except KeyboardInterrupt:
        pass