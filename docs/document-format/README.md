<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# mpvQC document format

A structured, versioned file format for QC reports: timestamped comments on a video file. It is designed for tooling
(scripts that map QC entries to subtitle lines, mpv user scripts, converters) while staying readable for humans.

Documents are JSON, encoded as UTF-8 without BOM, using the `.json` file extension.

## Versioning

Every document carries an integer `version` field declaring the format version it conforms to.

- **A released format version is immutable.** Its schema never changes. Any change to the format, additive or breaking,
  ships as a new `version` with its own schema. A version is released, and its schema frozen, once it is reachable from
  the `main` branch.
- **A document contains exactly the fields its version defines.** The schemas reject unknown fields at every level,
  including inside `comments` entries.
- Validate against the schema matching the document's `version`. A document with an unknown `version` cannot be
  interpreted: treat it as unsupported.
- The schemas are normative; the prose and tables in this document are informative.

| Version | Status  | Schema               |
| ------- | ------- | -------------------- |
| 1       | current | [`v1.json`](v1.json) |

## Version 1

### Example document

<!-- verified-by-tests: example-v1 -->

```json
{
    "$schema": "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json",
    "version": 1,
    "created_at": "2026-06-05T16:24:13Z",
    "generator": "mpvQC 0.9.0",
    "author": "lorem",
    "video": "/path/to/video.mkv",
    "subtitles": [
        "/path/to/video.de.ass"
    ],
    "comments": [
        {
            "time": "00:15:29.340",
            "type": "Translation",
            "text": "Lorem ipsum dolor sit amet"
        }
    ]
}
```

### Fields

| Field        | Required | Type             | Description                                                    |
| ------------ | -------- | ---------------- | -------------------------------------------------------------- |
| `$schema`    | no       | string           | Reference to this version's schema, exactly its published URL. |
| `version`    | yes      | integer          | Format version, exactly `1`.                                   |
| `created_at` | no       | string           | UTC timestamp, exactly `YYYY-MM-DDThh:mm:ssZ`.                 |
| `generator`  | no       | string           | Name and version of the program that wrote the file.           |
| `author`     | no       | string           | Name or nickname of the person who performed the QC.           |
| `video`      | no       | string           | Absolute path to the checked video file.                       |
| `subtitles`  | no       | array of strings | Absolute paths to external subtitle files; omitted when empty. |
| `comments`   | yes      | array            | QC comments.                                                   |

Each entry in `comments`:

| Field  | Required | Type   | Description                                      |
| ------ | -------- | ------ | ------------------------------------------------ |
| `time` | yes      | string | Video position, `HH:MM:SS.mmm` (see below).      |
| `type` | yes      | string | Comment category, a free-form, localized string. |
| `text` | yes      | string | The comment itself, a single line; may be empty. |

### Rules

- **Optional fields are omitted, never `null`.** An absent field means the information does not exist or was
  deliberately withheld. Optional fields are never empty strings or empty arrays: omit them instead.
- **Comment order is not guaranteed.** Generators should sort `comments` by `time`, ascending; consumers must sort if
  they need an order. Entries may share a `time`, even down to the same millisecond: duplicates are valid. The array
  may be empty.
- **`type` is non-empty, but not a stable identifier.** It is written in the language of the person who performed the QC
  ("Translation", "Traducción", ...) and may be a user-defined custom type. Do not match against a fixed list.
- **`text` may be empty.** Line breaks are invalid.
- **Paths are informational.** `video` and `subtitles` use the path syntax of the operating system that wrote the
  document; consumers must not assume they resolve locally.

### The `time` format

`HH:MM:SS.mmm`, matching `^\d{2}:[0-5]\d:[0-5]\d\.\d{3}$`:

- zero-padded, exactly three fraction digits (milliseconds)
- hours are exactly two digits, capping the format at `99:59:59.999`
- the separator before the fraction is a dot

### JSON Schema

The normative schema is [`v1.json`](v1.json), available at:

```text
https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json
```

## Writing documents from your own tool

Third-party generators are welcome: produce a document that validates against the schema of the version you write, and
set `generator` to your tool's name and version.
