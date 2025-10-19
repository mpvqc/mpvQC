# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from loguru import logger
from mpv import MpvGlGetProcAddressFn, MpvRenderContext
from PySide6.QtCore import QMutex, QSize, QThread, QWaitCondition, Signal, Slot
from PySide6.QtGui import QOffscreenSurface, QOpenGLContext
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


def get_process_address(_, name):
    current_gl_context = QOpenGLContext.currentContext()
    if current_gl_context:
        return int(current_gl_context.getProcAddress(name))
    return 0


class MpvqcBackgroundRendererThread(QThread):
    """
    Dedicated background thread for rendering video frames using OpenGL. This thread manages
    double-buffered FBO rendering where mpv renders to one FBO while the main thread displays from another:

    mpv → _render_fbo → _display_fbo → Qt Quick's FBO → screen

    _render_fbo → _display_fbo:    pointer swap
    _display_fbo → Qt Quick's FBO: blit in render()
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctx: MpvRenderContext | None = None
        self._surface: QOffscreenSurface | None = None
        self._shared_context: QOpenGLContext | None = None
        self._gl_context: QOpenGLContext | None = None

        self._render_fbo: QOpenGLFramebufferObject | None = None  # mpv renders here
        self._display_fbo: QOpenGLFramebufferObject | None = None  # keeping this ready for QtQuick

        self._video_size = QSize()
        self._mutex = QMutex()
        self._wait_condition = QWaitCondition()
        self._should_render = False
        self._rendering_active = True

    def prepare(self, ctx, shared_context, surface):
        self._ctx = ctx
        self._shared_context = shared_context
        self._surface = surface

    def request_render(self):
        self._mutex.lock()
        self._should_render = True
        self._wait_condition.wakeOne()
        self._mutex.unlock()

    def update_size(self, size: QSize):
        self._mutex.lock()
        if self._video_size != size:
            self._video_size = size
            self._should_render = True
        self._mutex.unlock()

    def get_display_fbo(self):
        """Returns the FBO that's ready for display (caller must lock)"""
        return self._display_fbo

    def lock(self):
        self._mutex.lock()

    def unlock(self):
        self._mutex.unlock()

    def run(self):
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

        self._gl_context.makeCurrent(self._surface)
        self._render_loop()
        self._gl_context.doneCurrent()

    def _render_loop(self):
        while self._rendering_active:
            self._mutex.lock()
            if not self._should_render:
                self._wait_condition.wait(self._mutex)

            if not self._rendering_active:
                self._mutex.unlock()
                break

            should_render = self._should_render
            self._should_render = False
            video_size = QSize(self._video_size)
            self._mutex.unlock()

            if should_render and self._ctx:
                recreate_frame_buffers = (
                    self._render_fbo is None  # First frame
                    or self._render_fbo.size() != video_size  # Size has changed
                    or self._display_fbo is None
                    or self._display_fbo.size() != video_size
                )

                if recreate_frame_buffers:
                    new_render_fbo = QOpenGLFramebufferObject(video_size)
                    new_display_fbo = QOpenGLFramebufferObject(video_size)

                    # Render directly into display buffer
                    fbo_handle = int(new_display_fbo.handle())
                    self._ctx.render(
                        flip_y=False,
                        opengl_fbo={"w": video_size.width(), "h": video_size.height(), "fbo": fbo_handle},
                    )

                    old_render = self._render_fbo
                    old_display = self._display_fbo

                    self._mutex.lock()
                    self._render_fbo, self._display_fbo = new_render_fbo, new_display_fbo
                    self._mutex.unlock()

                    if old_render:
                        del old_render
                    if old_display:
                        del old_display
                else:
                    # Normal render: render to render_fbo, then swap with display_fbo
                    fbo_handle = int(self._render_fbo.handle())

                    self._ctx.render(
                        flip_y=False,
                        opengl_fbo={"w": video_size.width(), "h": video_size.height(), "fbo": fbo_handle},
                    )

                    self._mutex.lock()
                    self._render_fbo, self._display_fbo = self._display_fbo, self._render_fbo
                    self._mutex.unlock()

    def stop(self):
        self._mutex.lock()
        self._rendering_active = False
        self._wait_condition.wakeOne()
        self._mutex.unlock()
        self.wait()

    def cleanup(self):
        if self._render_fbo is not None:
            del self._render_fbo
            self._render_fbo = None
        if self._display_fbo is not None:
            del self._display_fbo
            self._display_fbo = None
        if self._gl_context:
            del self._gl_context
            self._gl_context = None


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    video_frame_ready = Signal()
    time_to_prepare_surface = Signal()

    def __init__(self):
        super().__init__()
        self._renderer = None
        self.video_frame_ready.connect(self.do_update)
        self.destroyed.connect(lambda: self._on_destroyed())

    @Slot()
    def do_update(self):
        self.update()

    @Slot()
    def _on_destroyed(self):
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
        self._parent = parent
        self._get_proc_address_resolver = MpvGlGetProcAddressFn(get_process_address)
        self._ctx: MpvRenderContext | None = None
        self._video_size = QSize()

        self._render_thread = MpvqcBackgroundRendererThread()
        self._render_thread_ready = False

        self._surface = QOffscreenSurface()
        self._surface_format = QOpenGLContext.currentContext().format()
        self._surface_ready = False

        self._renderer_thread_started = False

        self._parent.time_to_prepare_surface.connect(self._on_configure_surface)

    @Slot()
    def _on_configure_surface(self):
        self._surface.setFormat(self._surface_format)
        self._surface.create()
        self._surface_ready = True

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self.player.init()

            self._ctx = MpvRenderContext(
                mpv=self.player.mpv,
                api_type="opengl",
                opengl_init_params={"get_proc_address": self._get_proc_address_resolver},
            )
            self._ctx.update_cb = self._on_mpv_update

            self._render_thread.prepare(self._ctx, QOpenGLContext.currentContext(), self._surface)
            self._render_thread_ready = True

        if self._video_size != size:
            self._video_size = size
            if self._render_thread_ready:
                self._render_thread.update_size(size)
                if self.player.is_paused:
                    # If currently playing a video -> rendering will be triggered anyway
                    self._render_thread.request_render()

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def _on_mpv_update(self):
        if self._render_thread_ready:
            self._render_thread.request_render()
        self._parent.video_frame_ready.emit()

    def render(self):
        if not self._surface_ready:
            self._parent.time_to_prepare_surface.emit()
            return

        if not self._render_thread_ready:
            return

        if not self._renderer_thread_started:
            self._render_thread.start()
            self._renderer_thread_started = True
            return

        self._render_thread.lock()
        display_fbo = self._render_thread.get_display_fbo()
        if display_fbo and display_fbo.isValid():
            QOpenGLFramebufferObject.blitFramebuffer(self.framebufferObject(), display_fbo)
        self._render_thread.unlock()

    def cleanup(self):
        if self._render_thread:
            self._render_thread.stop()
            self._render_thread.cleanup()
            self._render_thread = None
        if self._surface:
            del self._surface
            self._surface = None

    def __del__(self):
        self.cleanup()
