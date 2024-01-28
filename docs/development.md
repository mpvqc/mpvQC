# Developing tools:

* QtDesigner
* QtLinguist
* PyCharm

The project uses [just](https://github.com/casey/just) as a build system.

# Development process

* Set up the development environment as described in [the guide](dev-environment-setup.md)
* Edit `data/xml/*.xml` files with QtDesigner5
* In the main directory of this project run `just build-develop`
* Edit python files
* Update translations `just update-translations`
* Change directory to `i18n`, open `*.ts` files with QtLinguist5 and translate your strings
* From the root directory of the project run `just build-develop`
* To build a release run `just build`

# Adding new languages

* Set up the build environment for the project
* Run `just add-translation <locale>` (`just add-translation fr`)
* Open `i18n/<locale>.ts` with QtLinguist5 and translate
* To test locally:
    * Add the new language to the language selection menu in `mpvqc/widgets/_settings.py`
    * In the main directory of this project run `just build-develop` to compile resources including the translation file
    * Run `python main.py` to start the application to review the translation
* Submit a pull request
