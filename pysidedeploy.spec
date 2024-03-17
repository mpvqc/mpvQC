[app]
# title of your application
title = mpvQC
# project directory. the general assumption is that project_dir is the parent directory
# of input_file
project_dir = .
# source file path
input_file = C:\Users\trin-gaming10\PycharmProjects\mpvQC\main.py
# directory where exec is stored
exec_directory = .
# path to .pyproject project file
project_file = 
# application icon
icon = C:\Users\trin-gaming10\PycharmProjects\mpvQC\build-aux\windows\icon.ico

[python]
# python path
python_path = C:\Users\trin-gaming10\PycharmProjects\mpvQC\venv\Scripts\python.exe
# python packages to install
# ordered-set = increase compile time performance of nuitka packaging
# zstandard = provides final executable size optimization
packages = nuitka==2.1.2,ordered_set,zstandard
# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]
# comma separated path to qml files required
# normally all the qml files required by the project are added automatically
# find . -type f -name 'tst_*' -delete
# find qml -type f -print | awk '{printf "%s,", $0}' | sed 's/,$/\n/' > qml-files.txt
qml_files = qml\main.qml
# excluded qml plugin binaries
excluded_qml_plugins = QtCharts,QtQuick3D,QtSensors,QtTest,QtWebEngine

[nuitka]
# (str) specify any extra nuitka arguments
# eg = extra_args = --show-modules --follow-stdlib
extra_args = --quiet --windows-disable-console --include-data-dir=venv/Lib/site-packages/PySide6/translations=PySide6/translations

