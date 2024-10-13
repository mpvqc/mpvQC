# Adding Languages

* Checkout repository
* Make sure development environment is set up correctly for your OS
* Create a new translation file by running
  ```shell
  just add-translation <locale>  # just add-translation fr_FR
  ```
* New `<locale>.ts` file appears in the `i18n` directory
* Translate the `ts` file using Qt Linguist 6:
  ```shell
  pyside6-linguist i18n/<locale>.ts # pyside6-linguist i18n/fr_FR.ts
  ```
* To test the translation:
  * Make the application portable
    ```shell
    touch portable
    ```
  * Run
    ```shell
    just build-develop
    ```
  * Start the application and close it
  * Edit the `appdata/settings.ini`
    ```ini
    [Common]
    language=<locale>
    ```
  * Start the application
* Open a new pull request
* Add a new entry in the `qml/models/MpvqcLanguageModel.qml` file
