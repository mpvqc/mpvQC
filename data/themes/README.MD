# Creating New Color Palettes

## Prerequisites:
- Tools: `just`, `nushell`
- Resources:
  - **Palette Generator:** [Material Theme Builder](https://material-foundation.github.io/material-theme-builder)
  - **Base Colors:** [Base16 Scheme Viewer](https://nico-i.github.io/scheme-viewer/base16/)  
    - Selected palette for mpvQC: **Material – by Nate Peterson**

## Steps to Generate New Colors:

1. Choose a base color palette.
2. Export a theme JSON file for each color in the selected palette.
3. Run the following commands:
   ```shell
   just generate-light-colors  # for light colors
   just generate-dark-colors   # for dark colors
