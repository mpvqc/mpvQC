# Configuring mpvQC

mpvQC can be configured using the following environment variables:

| **Name**                     | **Default Value** | **Operating System** | **Description**                                                                                                                                                                        |
| ---------------------------- | ----------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MPVQC_DEBUG`                | _No default_      | All                  | Enables debug mode, intended primarily for developers and testing.                                                                                                                     |
| `MPVQC_VIDEO_SCALING_FACTOR` | `1.0`             | Linux                | Specifies the desktop scaling factor. Because Linux does not provide a universal method to retrieve fractional scaling from the desktop environment, Linux users must set it manually. |
