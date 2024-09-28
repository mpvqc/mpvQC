# Development Setup - Generic Linux

## Tools

* Make sure `python` is on version **3.8** or later
* Install `just` (https://github.com/casey/just)

## Setup

1. Clone this repository
1. Set up virtual environment:
    1. `python -m venv venv`
    1. `source venv/bin/activate` (*bash*) or `source venv/bin/activate.fish` (*fish*)
1. Install requirements `python -m pip install -r requirements.txt`
1. Install libmpv (package names vary depending on your distro)
1. Create an empty file `portable` in the root of the repository.
   This will tell mpvQC to store all created files in a new folder `appdata`

# Development Setup - Linux (NixOS)

Getting this app up and running on NixOS currently is complicated. The official nix packages lack the tools to build the
resources required for the application. Therefore, we build the resources in a container running Fedora and then use the
host system to run the application.

## Tools

* Make sure `python` is on version **3.8** or later
* Make sure `docker` is installed on your system
* Install the following packages using nix package manager or home manager:
  ```text
  kdePackages.qtsvg
  python312Packages.mpv
  python312Packages.pyside6
  python312Packages.shiboken6
  ```

## Setup

### Building Resources

1. Clone this repository
1. Create a new file `docker-compose.yml` in the root of the repository with the following content
   ```yaml
   services:
     build-env:
       image: fedora:latest
       volumes:
         - ./:/app
       command: sh /app/docker-entrypoint.sh
   ```
1. Create a new file `docker-entrypoint.sh` in the root of the repository with the following content
   ```shell
   #!/usr/bin/env bash

   dnf install just which python3.12 -y
   
   cd "/app" || return
   
   python3.12 -m venv venv
   source venv/bin/activate
   python3.12 -m pip install -r requirements.txt
   
   just build-develop
   ```
1. Execute `docker compose up` to build the resources

### Running the application

1. Set up virtual environment:
    * Bash:
      ```shell
      python -m venv venv-runner --system-site-packages
      source venv-runner/bin/activate
      ```
    * Fish:
      ```shell
      python -m venv venv-runner --system-site-packages
      source venv-runner/bin/activate.fish
      ```
1. Install requirements other than `PySide6` and `mpv`:
   ```shell
   python -m pip install inject Jinja2
   ```
1. Create an empty file `portable` in the root of the repository.
   This will tell mpvQC to store all created files in a new folder `appdata`
1. Find Qt binaries in the nix store:
   ```shell
   ls /nix/store/ | grep -- -qtdeclarative-6
   0sa9xrp29zwwd8iklkfcwcff8shdhn8m-qtdeclarative-6.7.2.drv
   w1n4ik2raymx1k08m5pjfdcdgbc19b9z-qtdeclarative-6.7.2             <-- this one
   ```
1. Edit Qt environment variables
    * Bash:
      ```shell
      export QML2_IMPORT_PATH="/nix/store/<the qt binary store>/lib/qt-6/qml
      unset QT_PLUGIN_PATH
      ```
    * Fish:
      ```shell
      export QML2_IMPORT_PATH="/nix/store/<the qt binary store>/lib/qt-6/qml
      set -e QT_PLUGIN_PATH
      ```
