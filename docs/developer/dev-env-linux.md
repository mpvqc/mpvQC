# Development Setup - Linux

## Tools

* Make sure `python` is on version **3.9**
* Install `make`

## Checkout

1. Clone this repository
1. Setup virtual environment:
    1. `python -m venv venv`
    1. `source venv/bin/activate` (*bash*) or `source venv/bin/activate.fish` (*fish*)
1. Install requirements `python -m pip install -r requirements.txt`

## Post checkout

1. Open the `Makefile`
1. Adjust tools if correct, for example
    ```
   TOOL_LUPDATE=lupdate-qt6
   TOOL_LRELEASE=lrelease-qt6
   TOOL_RCC=pyside6-rcc
   ```
   Make sure to not commit these changes