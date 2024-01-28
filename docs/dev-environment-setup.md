# Development environment setup

## Linux

The project uses [just](https://github.com/casey/just) as a build system.

1. Update all packages
   ```shell
   sudo apt update -y 
   sudo apt upgrade -y
   ```
1. Install dependencies
   ```shell
   sudo apt install -y libmpv1 qttools5-dev-tools
   ```
1. Clone the repository
   ```shell
   git clone <repository-git-url>
   ```
1. Set up virtual environment and install dependencies
   ```shell
   python -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
1. Build resources (compile `data`, `i18n` directories into a python file)
   ```shell
   just build-develop
   ```
1. Start the application
   ```shell
   ./main.py
   ```
