# Creating New Color Palettes

## Prerequisites:

- Tools: `just`, `nushell`
- Resources:
  - **Palette Generator:** [Material Theme Builder](https://material-foundation.github.io/material-theme-builder)
  - **materialyoucolor-python:** [materialyoucolor-python](https://github.com/T-Dynamos/materialyoucolor-python)

## Steps to Generate New Colors:

1. Choose seed colors
2. Adapt just recipes

```shell
$ just
```

```text
Available recipes:
    [Material]
    generate-dark-color-palette  # Print Material Dark palette
    generate-light-color-palette # Print Material Light palette

    [mpvQC]
    dark-mpvQC-colors            # Print dark mpvQC colors
    light-mpvQC-colors           # Print light mpvQC colors
```
