# Internationalization

Application translations live as `.ts` source catalogs under `i18n/`. Builds compile them to `.qm` files and include
them in the resource bundle. Commit the `.ts` sources, not generated translation or resource files.

For setup, see [development.md](development.md).

## Writing translatable text

QML uses an explicit context:

```qml
qsTranslate("Context", "Text")
qsTranslate("Context", "%Ln files", "", count)
```

Use `//:` immediately before a string when translators need context. Keep translation calls in bindings so changing
the language reevaluates them.

Python uses `QCoreApplication.translate` for runtime text and `QT_TRANSLATE_NOOP` for strings stored as constants.
Long-lived Python state that contains translated text must rebuild when the application publishes its retranslation
signal.

Keep contexts stable and preserve placeholders such as `%1` and `%Ln` in every translation.

## Updating translations

Extract current Python and QML strings into the application catalogs:

```shell
just update-translations
```

Catalogs whose names end in `-qt-overrides.ts` are excluded from extraction and maintained by hand. They replace Qt
strings that the application needs to phrase differently.

Open a catalog with Qt Linguist:

```shell
uv run pyside6-linguist i18n/<locale>.ts
```

Review new, obsolete, and unfinished entries before committing the changed `.ts` files.

## Adding a language

1. Create the application catalog:

   ```shell
   just add-translation <locale>
   ```

2. Add a `Language` entry to `LANGUAGES` in `mpvqc/i18n/services/languages.py`:

   ```python
   Language(
       language=str(QT_TRANSLATE_NOOP("Languages", "<English language name>")),
       identifier="<locale>",
       translators=("<translator name>",),
   ),
   ```

   Omit `translators` when nobody needs credit. The locale passed to the recipe, the catalog basename, and the
   registry identifier must match exactly.

3. When Qt provides a matching base catalog, add it to the Windows release bundle. Use the Qt locale selected by the
   runtime when it differs from the application locale.

4. Extract strings again after changing the registry:

   ```shell
   just update-translations
   ```

5. Complete the catalog in Qt Linguist.

6. Rebuild resources and run all tests:

   ```shell
   just test
   ```

7. Start the application and select the language. Check application text, Qt-provided text, translator credits,
   plurals, and right-to-left layout where applicable.

Add a Qt override catalog only when the application needs to replace a Qt-provided translation.

## Release checks

Catalog freshness is a manual check. Run string extraction, inspect the resulting catalog changes, and follow the
translation steps in [releasing.md](releasing.md).

## See also

- [Development](development.md)
- [Releasing](releasing.md)
