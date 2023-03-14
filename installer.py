import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def uninstall(package): # Запрашивает подтверждение y/n
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])


install('pygame')
install('numpy')
#install('ctypes')
#install('random')
#install('copy')
install('tkinter')
#install('pygame')
#install('pygame')

