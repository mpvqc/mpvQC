# PROTOTYPE - throwaway launcher for the import wizard redesign variants (internal ticket #114).
# Run from the repo root:
#
#     uv run .scratch/import-wizard-prototype/run.py
#
# Requires testqml/project.rcc (run `just prepare-tests` once). Boots the app's QML modules with
# the QML test harness injections, so no mpv window and no real settings are touched.

import os
import pathlib
import sys


def main() -> None:
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "MpvqcStyle"
    os.environ["QT_QUICK_CONTROLS_FALLBACK_STYLE"] = "Material"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

    repo = pathlib.Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo))

    from PySide6.QtCore import QResource, QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine

    rcc = repo / "testqml" / "project.rcc"
    if not QResource.registerResource(str(rcc)):
        msg = f"Missing {rcc} - run `just prepare-tests` first"
        raise FileNotFoundError(msg)

    app = QGuiApplication(sys.argv)

    from mpvqc import startup
    from testqml.injections import configure_injections

    startup.configure_qt_application_data()
    startup.configure_qt_settings()
    configure_injections()
    startup.register_qml_types()

    import inject

    from mpvqc.services import FontLoaderService

    inject.instance(FontLoaderService).load_application_fonts()

    engine = QQmlApplicationEngine()
    qml = pathlib.Path(__file__).resolve().parent / "Prototype.qml"
    engine.load(QUrl.fromLocalFile(str(qml)))
    if not engine.rootObjects():
        sys.exit(1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
