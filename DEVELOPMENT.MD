# Developing tools:
* QtDesigner
* QtLinguist
* PyCharm

This project uses [distutils_ui](https://github.com/frispete/distutils_ui) to develop/build the application.
So installing it via `pip install distutils_ui` is required.

# Development process

* Change `gui/*.ui` files with QtDesigner
* In the main directory of this project run `python3 setup.py build_ui`
* Now make your python changes
* Change directory to `i18n` and open the `.ts` files with QtLinguist and translate your strings
* Change back to the main directory of this project and run `python3 setup.py build_ui` again

# Adding new languages

* Change directory to `i18n`
* Create a new file `<abc>.ts`
* In the main directory of this project run `python3 setup.py build_ui`
* Open `i18n/<abc>.ts` with QtLinguist and translate
* In the main directory of this project run `python3 setup.py build_ui` to update binaries
* Submit pull request

**Note**: New languages are *not* available in the GUI immediately 
This will be supported at a later date.