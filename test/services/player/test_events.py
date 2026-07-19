# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import threading

from PySide6.QtCore import QThread

from mpvqc.services.player.events import EventMarshal


def test_posts_defer_until_the_event_loop_runs(qt_app):
    events: list[tuple[str, int]] = []
    marshal = EventMarshal()
    post = marshal.channel(lambda name, value: events.append((name, value)))

    post("time-pos", 1)
    post("time-pos", 2)

    assert events == []
    qt_app.processEvents()
    assert events == [("time-pos", 1), ("time-pos", 2)]


def test_channels_share_one_queue_in_post_order(qt_app):
    events: list[str] = []
    marshal = EventMarshal()
    post_a = marshal.channel(lambda value: events.append(f"a-{value}"))
    post_b = marshal.channel(lambda: events.append("b"))

    post_a(1)
    post_b()
    post_a(2)
    qt_app.processEvents()

    assert events == ["a-1", "b", "a-2"]


def test_runs_handlers_on_the_gui_thread(qt_app):
    marshal = EventMarshal()

    gui_thread = QThread.currentThread()
    deliveries: list[tuple[int, QThread]] = []
    post = marshal.channel(lambda value: deliveries.append((value, QThread.currentThread())))

    worker = threading.Thread(target=lambda: (post(1), post(2)))
    worker.start()
    worker.join()
    qt_app.processEvents()

    assert [value for value, _thread in deliveries] == [1, 2]
    assert all(thread is gui_thread for _value, thread in deliveries)
