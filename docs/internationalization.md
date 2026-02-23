<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Adding Languages

- Checkout repository
- Make sure development environment is set up correctly for your OS
- Create a new translation file by running
  ```shell
  just add-translation <locale>  # just add-translation fr-FR
  ```
- New `<locale>.ts` file appears in the `i18n` directory
- Translate the `ts` file using Qt Linguist 6:
  ```shell
  pyside6-linguist i18n/<locale>.ts  # pyside6-linguist i18n/fr-FR.ts
  ```
- To test the translation:
  - Run
    ```shell
    just build-develop
    ```
  - Start the application and close it
  - Edit the `appdata/settings.ini`
    ```ini
    [Common]
    language=<locale>
    ```
- Add a new `Language` entry to the `LANGUAGES` tuple in `mpvqc/models/languages.py`
- Open a new pull request

# Updating Translations

When translatable strings in the source code change, update all existing `.ts` files by running:

```shell
just update-translations
```

This scans all QML and Python source files for translatable strings and updates the `.ts` files accordingly.
