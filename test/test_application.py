import unittest

from PySide6.QtCore import QUrl, QObject
from PySide6.QtWidgets import QApplication

from mpvqc.application import MpvqcApplication


class TestApplication(unittest.TestCase):
    qml = """
        import QtQuick
        import QtQuick.Controls
        
        ApplicationWindow {
            visible: false; width: 50; height: 50
        
            Button { objectName: "button"; text: "Click Me" }
        }
        """

    def setUp(self):
        if app := QApplication.instance():
            app.shutdown()
        self.app = MpvqcApplication([])
        self.app._engine.loadData(self.qml.encode(), QUrl())

    def test_find_object(self):
        obj = self.app.find_object(QObject, "button")
        self.assertIsNotNone(obj)

        try:
            self.app.find_object(QObject, "label")
            assert False, "Expected AssertionError but no exception was raised"
        except AssertionError:
            pass
