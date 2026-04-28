<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Internationalization

Translations live as `.ts` files under `i18n/` (Qt's translation source format). The build pipeline compiles them to `.qm` binaries that ship with the application. Editing happens in Qt Linguist; everything else is a `just` recipe.

For setup, see [development.md](development.md).

## Adding a language

1. Create the translation file:

   ```shell
   just add-translation <locale>  # e.g. just add-translation fr-FR
   ```

   A `<locale>.ts` file appears under `i18n/`.

2. Translate the strings using Qt Linguist:

   ```shell
   pyside6-linguist i18n/<locale>.ts
   ```

3. Register the new language in the languages model under `mpvqc/models/` so it appears in the application's language menu.

4. Recompile resources and test:

   ```shell
   just build-develop
   ```

   Start the application, switch to the new locale through the application's settings, and verify the strings render correctly.

## Updating existing translations

When translatable strings in the source code change, refresh every `.ts` file from current sources:

```shell
just update-translations
```

This scans Python and QML for translatable strings and merges new entries into the existing `.ts` files, preserving prior translations.

## See also

- [development.md](development.md) — setup and tooling
- [releasing.md](releasing.md) — translation checks in the release flow
