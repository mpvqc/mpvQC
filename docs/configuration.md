<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Configuring mpvQC

mpvQC can be configured using the following environment variables:

- **`MPVQC_DEBUG`**

  - **Default Value:** not set
  - **Operating System:** All
  - **Description:** Enables debug mode for development and testing purposes.
  - **Possible Values:** *not set* or *any value*

- **`MPVQC_PLAYER_LOG`**

  - **Default Value:** enabled if `MPVQC_DEBUG` set, disabled else
  - **Operating System:** All
  - **Description:** Enables mpv player logging
  - **Possible Values:** *not set* or *any value*

- **`MPVQC_VIDEO_SCALING_FACTOR`**

  - **Default Value:** `1.0`
  - **Operating System:** Linux only
  - **Description:** Specifies the desktop scaling factor. Must be set manually on Linux due to the lack of a
    universal method for retrieving fractional scaling from desktop environments.
  - **Possible Values:** Any positive decimal number (e.g., `1.0`, `1.25`, `1.5`, `2.0`)
