# Development environment setup

The following steps are tested on a **fresh Ubuntu 20.04 install**.  
Other distributions behave similarly, but package names may vary.

# Update system packages
```shell
sudo apt update 
sudo apt upgrade
```

# Install basic dependencies
```shell
sudo apt install git python3-pip python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools qt5-qmake
```

# Clone mpvQC repo
```shell
git clone <repository-git-url>
```

# Cd into the project folder
```shell
cd mpvQC
```

# Install mpvQC dependencies
```shell
sudo apt install lilbmpv1
pip3 install -r requirements.txt
```

# Compile mpvQC resources
```shell
python3 setup.py build_ui
```

# Start the application
```shell
./start.py
```