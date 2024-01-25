#!/usr/bin/env bash

# Execute from repository root

export QT_QPA_PLATFORM=offscreen

just test-qml | grep -v \
    -e 'initTestCase()' \
    -e 'cleanupTestCase()' \
    -e '^QWARN.*QML IconImage: Cannot open' \
    -e '^QWARN.*QML QQuickImage: Cannot open' \
    -e '^QWARN.*QML Settings:' \
    -e '^QWARN.*QML ListView: Binding loop detected for property "currentIndex"' \
    -e '^QWARN.*Binding on contentItem is not deferred' \
    -e '^QWARN.*QQmlComponent: Created graphical object' \
    -e '^QWARN.*QML FontLoader: Cannot load font'
