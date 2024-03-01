import unittest

from PySide6.QtCore import QUrl, QObject

from mpvqc.application import MpvqcApplication


class TestApplication(unittest.TestCase):
    qml = """
        import QtQuick
        import QtQuick.Controls
        
        ApplicationWindow {
            visible: false; width: 50; height: 50
        
            Button { objectName: "button-click-me"; text: "Click Me" }
        }
        """

    _app: MpvqcApplication or None = None

    def setUp(self):
        self.tearDown()
        self._app = MpvqcApplication([])
        self._app._engine.loadData(self.qml.encode(), QUrl())

    def tearDown(self):
        if self._app:
            self._app.shutdown()

    def test_find_object(self):
        obj = self._app.find_object(QObject, "button-click-me")
        self.assertIsNotNone(obj)

        try:
            self._app.find_object(QObject, "label")
            assert False, "Expected AssertionError but no exception was raised"
        except AssertionError:
            pass
