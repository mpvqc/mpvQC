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
    version='0.0.1',
    description='Description',
    long_description='Long Description',
    author='Author',
    # author_email = '',
    # url = ,
    # license = 'MIT',
    packages=find_packages(),
    cmdclass=cmdclass,
)
