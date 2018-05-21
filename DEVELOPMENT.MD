# Developing tools needed:
* QtDesigner
* QtLinguist
* PyCharm
* A bunch of command line tools (just install when errors occur)

# Development process

## UI
* Change `.ui` files with QtDesigner
* In the main directory of this folder run `python3 dev.py -p` (-p: prepare)
    
    This will transform `.ui` files into `py` files using several command line tools.
        
* Now make your python changes
* Change to `locale/.../LC_MESSAGES` and open the `.ts` files with QtLinguist and translate your strings

* Change back to the main directory and run `python3 dev.py -f` (-f: finish)
    
    This will create all binary files for the translation.
    
## Compile to binary

* Install `pyinstaller` (current development version from github)
* In the main directory run `pyinstaller --onefile start.py`

    This will generate a `start.spec` file in the main directory as well as a `build` and `dist` directory.
    
* Add the following as the binary section:

    ```text
    binaries=[
                    ('/home/elias/PycharmProjects/mpvQC/locale/de/LC_MESSAGES/*.*', 'locale/de/LC_MESSAGES'),
                    ('/home/elias/PycharmProjects/mpvQC/locale/en/LC_MESSAGES/*.*', 'locale/en/LC_MESSAGES')
                 ],
    ```

* Also make sure to change the name the application should have
* In the main directory run `pyinstaller --onefile start.spec` (this time not `.py`!)
* The binary will appear in the `dist` directory 

## TODO

* Tests
* Refactoring 