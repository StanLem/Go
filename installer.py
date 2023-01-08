import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def uninstall(package): # Запрашивает подтверждение y/n
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])


install('tensorflow')
install('tensorflow-gpu')

