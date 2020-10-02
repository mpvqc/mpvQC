#!/usr/bin/env python3

from distutils.command.build import build

from distutils_ui.build_ui import build_ui
from setuptools import setup, find_packages

cmdclass = {
    'build_ui': build_ui,
}

# Inject ui specific build into standard build process
build.sub_commands.insert(0, ('build_ui', None))

setup(
    name='mpvQC',
    version='0.7.0',
    description='libmpv based application for quality control of videos',
    long_description='mpvQC is a libmpv based application for the quick and easy creation of quality control reports '
                     'of video files, initially intended to be a less broken alternative to kSub.',
    author='Frechdachs',
    author_email='frechdachs@rekt.cc',
    url='https://mpvqc.rekt.cc',
    license='GNU General Public License 3',
    packages=find_packages(),
    cmdclass=cmdclass,
)
