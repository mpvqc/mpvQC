# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

{
  description = "Development shell for mpvQC";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python314;
    in
    {
      formatter.${system} = pkgs.nixfmt;

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          python
          # ctypes.util.find_library needs ld to find libmpv
          pkgs.binutils
          # fc-match from the same fontconfig Qt loads, to check which host fonts it finds
          pkgs.fontconfig
          pkgs.just
          pkgs.mpv-unwrapped
          pkgs.uv
        ];

        UV_PYTHON = python.interpreter;
        UV_PYTHON_DOWNLOADS = "never";

        # Libraries the PySide6 wheel and python-mpv load at runtime
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.brotli
          pkgs.dbus
          pkgs.fontconfig
          pkgs.freetype
          pkgs.glib
          pkgs.krb5
          pkgs.libdrm
          pkgs.libglvnd
          pkgs.libx11
          pkgs.libxcb
          pkgs.libxkbcommon
          pkgs.mesa
          pkgs.mpv-unwrapped
          pkgs.stdenv.cc.cc.lib
          pkgs.wayland
          pkgs.zlib
          pkgs.zstd
        ];

        __EGL_VENDOR_LIBRARY_DIRS = "${pkgs.mesa}/share/glvnd/egl_vendor.d";
        LIBVA_DRIVERS_PATH = "${pkgs.mesa}/lib/dri";

        # rcc stamps every resource with SOURCE_DATE_EPOCH, so the QML disk cache never sees a change
        shellHook = ''
          unset SOURCE_DATE_EPOCH

          # just build-release deletes .env
          if [ -f .env ]; then
            set -a
            source .env
            set +a
          fi
        '';
      };
    };
}
