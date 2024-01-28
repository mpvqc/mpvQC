from PyQt5 import uic
from PyQt5.QtCore import QFile


def init_from_resources(clazz, resource_path):
    file = QFile(resource_path)
    try:
        file.open(QFile.ReadOnly)
        return uic.loadUi(file, clazz)
    finally:
        file.close()
