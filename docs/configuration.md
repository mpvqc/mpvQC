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
