#!/usr/bin/env python3

# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import argparse
import glob
import os
import shutil
import sys
from os import path
from typing import Tuple

import polib

# The languages to translate into
_LANGUAGES: Tuple[str] = ("de", "en", "it")

_WORKFLOW = \
    """ Make sure the project has the following skeleton:

    root-dir
        -forms
            - <abc>.ui

    The "-p" (provide) flag will generate some files and the project structure will change to the following:

    root-dir
        -forms
            - <abc>.ui
        -locale
            - <locale>
                - LC_MESSAGES
                    - ui_trans.ts
        -src
            - generated
                - <abc>.py

    After that the "-f" (finish) flag will create the binaries:

    root-dir
        -forms
            - <abc>.ui
        -locale
            - <locale>
                - LC_MESSAGES
                    - ui_trans.ts
                    - ui_trans.qm
        -src
            - generated
                - <abc>.py
    """

_HELP_TEXT = \
    """Use -help for getting a detailed explanation of this script.\n""" + \
    """Use -p flag for providing translation files.\n""" + \
    """Use -f flag for generating binaries from provided translation files."""

_TOOLS = (
    ("pyuic5", "Should be installed if qt designer is installed."),
    ("pylupdate5", "Should be installed if qt designer is installed."),
    ("lrelease", "Should be installed if qt designer is installed."),
    ("ts2po", "Github: https://github.com/translate/translate"),
)


def tools_available() -> bool:
    passed: bool = True

    for tool in _TOOLS:
        if shutil.which(tool[0]) is None:
            passed = False
            print("Tool '{}' is missing ...\n\t{}".format(*tool))

    return passed


def log(message: str, indent=0) -> None:
    print("\t" * indent + message)


class Locations:
    THIS = path.dirname(path.realpath(sys.argv[0]))

    SOURCE = "source"
    FORMS = "forms"
    GENERATED = "generated"
    HANDLER = "handler"

    RESOURCES = "resources"
    TS = "ts"
    ICONS = "icons"
    WINDOWS = "windows"

    def __init__(self):
        self.dir_forms = path.join(Locations.THIS, Locations.FORMS)
        self.dir_source = path.join(Locations.THIS, Locations.SOURCE)

        # Create
        self.dir_source_forms_generated = path.join(
            Locations.THIS, Locations.SOURCE, Locations.FORMS, Locations.GENERATED)
        self.dir_source_forms_handler = path.join(
            Locations.THIS, Locations.SOURCE, Locations.FORMS, Locations.HANDLER)

        self.file_source_forms_generated = path.join(
            Locations.THIS, Locations.SOURCE, Locations.FORMS, Locations.GENERATED, "__init__.py")

        self.dir_resource_icons_windows = path.join(
            Locations.THIS, Locations.RESOURCES, Locations.ICONS, Locations.WINDOWS)
        self.dir_resource_ts = path.join(
            Locations.THIS, Locations.RESOURCES, Locations.TS)

        self.__dirs = [
            self.dir_source_forms_generated,
            self.dir_source_forms_handler,
            self.dir_resource_icons_windows,
            self.dir_resource_ts
        ]

        self.__files = [
            self.file_source_forms_generated
        ]

    def create_missing(self):
        for folder in self.__dirs:
            if not path.isdir(folder):
                os.makedirs(folder)
        for file in self.__files:
            with open(r'{}'.format(file), 'a') as file_:
                file_.write("")


class Transformer:
    def __init__(self, locations: Locations):
        self.locations = locations

    def ui_to_py(self):
        files_ui = glob.glob(path.join(self.locations.dir_forms, "*.ui"))

        template_log = "{}.ui -> {}.py"
        template_cmd = "pyuic5 {} -o {}.py"

        log("Transforming ui -> py ...")

        for file_ui in files_ui:
            _, name_plus_extension = os.path.split(file_ui)
            name = os.path.splitext(name_plus_extension)[0]

            destination = path.join(self.locations.dir_source_forms_generated, name)
            os.system(template_cmd.format(file_ui, destination))
            log(template_log.format(name, destination), indent=1)

        log("Done!\n")

    def py_to_ts(self):
        py_files = [fn for fn in glob.iglob(os.path.join(self.locations.dir_source, "**/*.py"), recursive=True)
                    if (not fn.endswith("__.py"))]

        template_log = "Updating {}.ts ... Done"
        template_cmd = "pylupdate5 " + " ".join(py_files) + " -ts {}.ts"

        log("Updating *.ts files ...")

        for language in _LANGUAGES:
            os.system(template_cmd.format(os.path.join(self.locations.dir_resource_ts, language)))
            log(template_log.format(language), indent=1)

        log("Done!\n")


class Transformers:
    def __init__(self, directory: Locations):
        self.directory = directory
        self.py_gui_target = os.path.join(directory.src_gui, "{}")

    def ts_to_qm(self):
        for lang_dir in self.directory.locale_dirs:
            new_file = os.path.join(lang_dir, "ui_trans")
            os.system("lrelease {}.ts -qm {}.qm".format(new_file, new_file))
            os.system("ts2po {}.ts {}po.po".format(new_file, new_file))
            po = polib.pofile('{}po.po'.format(new_file))
            po.save_as_mofile('{}mo.mo'.format(new_file))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script helps managing resource files (ui, ts).')
    parser.add_argument("-p", "--provide",
                        help='Will create missing folders, transform ui -> py and update all *.ts files.',
                        action='store_true')
    parser.add_argument("-f", "--finalize",
                        help='Will create binary files.',
                        action='store_true')
    args = parser.parse_args()

    location = Locations()

    if args.provide:
        location.create_missing()

        t = Transformer(location)
        t.ui_to_py()
        t.py_to_ts()

    if args.finalize:
        print("Todo!")

