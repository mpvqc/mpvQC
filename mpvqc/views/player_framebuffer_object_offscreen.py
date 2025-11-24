# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from contextlib import AbstractContextManager, contextmanager
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QMutex, QSize, QThread, QWaitCondition, Signal, Slot
from PySide6.QtGui import QOffscreenSurface, QOpenGLContext
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpvqc.services import PlayerService

if TYPE_CHECKING:
    from collections.abc import Generator

    from mpv import MpvRenderContext

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1

logger = logging.getLogger(__name__)


def get_process_address(_, name: bytes) -> int:
    current_gl_context = QOpenGLContext.currentContext()
    if current_gl_context:
        return int(current_gl_context.getProcAddress(name))
    return 0


class RenderState:
    """All data shared between render thread and main thread"""

    def __init__(self):
        self._render_fbo: QOpenGLFramebufferObject | None = None
        self._display_fbo: QOpenGLFramebufferObject | None = None
        self._video_size = QSize()
        self._should_render = False
        self._rendering_active = True

    @property
    def render_fbo(self) -> QOpenGLFramebufferObject | None:
        return self._render_fbo

    @property
    def display_fbo(self) -> QOpenGLFramebufferObject | None:
        return self._display_fbo

    @property
    def video_size(self) -> QSize:
        return self._video_size

    @property
    def should_render(self) -> bool:
        return self._should_render

    @property
    def rendering_active(self) -> bool:
        return self._rendering_active

    def request_render(self) -> None:
        self._should_render = True

    def clear_render_request(self) -> None:
        self._should_render = False

    def update_video_size(self, size: QSize) -> bool:
        """Returns True if size changed"""
        if self._video_size != size:
            self._video_size = size
            self._should_render = True
            return True
        return False

    def set_fbos(self, render_fbo: QOpenGLFramebufferObject, display_fbo: QOpenGLFramebufferObject) -> None:
        self._render_fbo = render_fbo
        self._display_fbo = display_fbo

    def swap_fbos(self) -> None:
        self._render_fbo, self._display_fbo = self._display_fbo, self._render_fbo

    def clear_fbos(self) -> None:
        if self._render_fbo is not None:
            self._render_fbo.release()
            del self._render_fbo
            self._render_fbo = None
        if self._display_fbo is not None:
            self._display_fbo.release()
            del self._display_fbo
            self._display_fbo = None

    def stop_rendering(self) -> None:
        self._rendering_active = False

    def needs_fbo_recreation(self, target_size: QSize) -> bool:
        return (
            self._render_fbo is None
            or self._render_fbo.size() != target_size
            or self._display_fbo is None
            or self._display_fbo.size() != target_size
        )


class ThreadSync:
    """Synchronization primitives for thread coordination"""

    def __init__(self):
        self._mutex = QMutex()
        self._wait_condition = QWaitCondition()

    def lock(self) -> None:
        self._mutex.lock()

    def unlock(self) -> None:
        self._mutex.unlock()

    def wait(self) -> None:
        self._wait_condition.wait(self._mutex)

    def wake_one(self) -> None:
        self._wait_condition.wakeOne()


class SynchronizedState:
    """Manages shared state with thread synchronization"""

    def __init__(self):
        self._state = RenderState()
        self._sync = ThreadSync()

    @contextmanager
    def locked(self) -> Generator[tuple[RenderState, ThreadSync]]:
        self._sync.lock()
        try:
            yield self._state, self._sync
        finally:
            self._sync.unlock()


class MpvqcBackgroundRendererThread(QThread):
    """
    Dedicated background thread for rendering video frames using OpenGL. This thread manages
    double-buffered FBO rendering where mpv renders to one FBO while the main thread displays from another:

    mpv → _render_fbo → _display_fbo → Qt Quick's FBO → screen

    _render_fbo → _display_fbo:    pointer swap
    _display_fbo → Qt Quick's FBO: blit in render()
    """

    frame_rendered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Thread-local state (no synchronization needed)
        self._ctx: MpvRenderContext | None = None
        self._surface: QOffscreenSurface | None = None
        self._shared_context: QOpenGLContext | None = None
        self._gl_context: QOpenGLContext | None = None

        self._synchronized_state = SynchronizedState()

    def acquire(self) -> AbstractContextManager[tuple[RenderState, ThreadSync]]:
        return self._synchronized_state.locked()

    def prepare(self, ctx: MpvRenderContext, shared_context: QOpenGLContext, surface: QOffscreenSurface) -> None:
        self._ctx = ctx
        self._shared_context = shared_context
        self._surface = surface

    def request_render(self) -> None:
        with self.acquire() as (state, sync):
            state.request_render()
            sync.wake_one()

    def update_size(self, size: QSize) -> None:
        with self.acquire() as (state, sync):
            state.update_video_size(size)

    def run(self) -> None:
        if not self._surface:
            logger.error("Surface is not initialized. Stopping mpvqc renderer thread")
            return
        if not self._shared_context:
            logger.error("Shared context is not initialized. Stopping mpvqc renderer thread")
            return

        self._gl_context = QOpenGLContext()
        self._gl_context.setFormat(self._surface.format())
        self._gl_context.setShareContext(self._shared_context)

        if not self._gl_context.create():
            logger.error("Failed to create OpenGL context for mpvqc renderer thread")
            return

        if not self._gl_context.makeCurrent(self._surface):
            logger.error("Failed to make OpenGL context current on background thread")
            return

        try:
            self._render_loop()
        finally:
            self._gl_context.doneCurrent()

    def _render_loop(self) -> None:
        while True:
            with self.acquire() as (state, sync):
                while not state.should_render:
                    if not state.rendering_active:
                        return
                    sync.wait()

                if not state.rendering_active:
                    break

                should_render = state.should_render
                state.clear_render_request()
                video_size = QSize(state.video_size)

            if not should_render or not self._ctx or video_size.isEmpty():
                continue

            with self.acquire() as (state, sync):
                recreate_frame_buffers = state.needs_fbo_recreation(video_size)

            if recreate_frame_buffers:
                new_render_fbo = QOpenGLFramebufferObject(video_size)
                new_display_fbo = QOpenGLFramebufferObject(video_size)

                fbo_handle = int(new_render_fbo.handle())
                self._ctx.render(
                    flip_y=False,
                    opengl_fbo={"w": video_size.width(), "h": video_size.height(), "fbo": fbo_handle},
                )

                with self.acquire() as (state, sync):
                    old_render = state.render_fbo
                    old_display = state.display_fbo
                    state.set_fbos(new_render_fbo, new_display_fbo)
                    state.swap_fbos()

                if old_render:
                    old_render.release()
                    del old_render
                if old_display:
                    old_display.release()
                    del old_display
            else:
                with self.acquire() as (state, sync):
                    if fbo := state.render_fbo:
                        fbo_handle = int(fbo.handle())
                    else:
                        continue

                self._ctx.render(
                    flip_y=False,
                    opengl_fbo={"w": video_size.width(), "h": video_size.height(), "fbo": fbo_handle},
                )

                with self.acquire() as (state, sync):
                    state.swap_fbos()

            self.frame_rendered.emit()

    def stop(self) -> None:
        with self.acquire() as (state, sync):
            state.stop_rendering()
            sync.wake_one()
        self.wait()

    def cleanup(self) -> None:
        with self.acquire() as (state, sync):
            state.clear_fbos()

        if self._gl_context:
            del self._gl_context
            self._gl_context = None


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    on_surface_ready = Signal()

    def __init__(self):
        super().__init__()
        self._renderer: Renderer | None = None
        self.destroyed.connect(lambda: self._on_destroyed())

    @Slot()
    def do_update(self) -> None:
        self.update()

    @Slot()
    def _on_destroyed(self) -> None:
        if self._renderer:
            self._renderer.cleanup()
            self._renderer = None

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        self._renderer = Renderer(self)
        return self._renderer


class Renderer(QQuickFramebufferObject.Renderer):
    player: PlayerService = inject.attr(PlayerService)

    def __init__(self, parent: MpvqcMpvFrameBufferObjectPyObject):
        super().__init__()
        from mpv import MpvGlGetProcAddressFn

        self._parent = parent
        self._get_proc_address_resolver = MpvGlGetProcAddressFn(get_process_address)
        self._ctx: MpvRenderContext | None = None
        self._video_size = QSize()

        self._render_thread = MpvqcBackgroundRendererThread()
        self._render_thread.frame_rendered.connect(self._parent.do_update)
        self._render_thread_ready = False

        self._surface = QOffscreenSurface()
        self._surface_format = QOpenGLContext.currentContext().format()
        self._surface_ready = False

        self._renderer_thread_started = False

        self._parent.on_surface_ready.connect(self._on_configure_surface)

    @Slot()
    def _on_configure_surface(self) -> None:
        self._surface.setFormat(self._surface_format)
        self._surface.create()
        self._surface_ready = True
        self._parent.update()

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self._initialize_mpv_context()

        if self._video_size != size:
            self._update_video_size(size)

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def _initialize_mpv_context(self) -> None:
        self.player.init()

        from mpv import MpvRenderContext

        self._ctx = MpvRenderContext(
            mpv=self.player.mpv,
            api_type="opengl",
            opengl_init_params={"get_proc_address": self._get_proc_address_resolver},
        )
        self._ctx.update_cb = self._on_mpv_update

        self._render_thread.prepare(self._ctx, QOpenGLContext.currentContext(), self._surface)
        self._render_thread_ready = True

    def _update_video_size(self, size: QSize):
        self._video_size = size
        if self._render_thread_ready:
            self._render_thread.update_size(size)
            if self.player.is_paused:
                self._render_thread.request_render()

    def _on_mpv_update(self) -> None:
        if self._render_thread_ready:
            self._render_thread.request_render()

    def render(self) -> None:
        if not self._surface_ready:
            self._parent.on_surface_ready.emit()
            return

        if not self._render_thread_ready:
            return

        if not self._renderer_thread_started:
            self._render_thread.start()
            self._renderer_thread_started = True
            return

        with self._render_thread.acquire() as (state, sync):
            display_fbo = state.display_fbo
            if display_fbo and display_fbo.isValid():
                QOpenGLFramebufferObject.blitFramebuffer(self.framebufferObject(), display_fbo)

    def cleanup(self) -> None:
        if self._render_thread:
            self._render_thread.stop()
            self._render_thread.cleanup()
            self._render_thread = None

        if self._ctx:
            self._ctx.free()
            self._ctx = None

        if self._surface:
            del self._surface
            self._surface = None
