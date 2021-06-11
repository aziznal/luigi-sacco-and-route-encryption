# Basic PyQt5 Framework in Python

## Description

This is a very simple framework for making desktop applications with python using the PyQt5 package.

---


## Usage

1. Create a UI in QtDesigner (which can be downloaded from [here](https://build-system.fman.io/qt-designer-download)). The resultant file will end with a `.ui` extension

2. Add the ids and types of any widgets you want to programatically access in your program to `json` file in the following structure:
    ```json
    {
        "QWidgetType_X_Here": [
            "firstQWidget_X_IdHere",
            "secondQWidget_X_IdHere",
            .
            .
            .
        ],

        "QWidgetType_Y_Here": [
            "firstQWidget_Y_IdHere",
            "secondQWidget_Y_IdHere",
            .
            .
            .
        ]
    }
    ```

You can find examples of these two files in the `data` directory.

An example of a working program is included in `main.py`

---

## Building the application

To build your app, run `build.bat`. The project will be built using `pyinstaller` and you can freely change any settings as you see fit. The resultant executable file will be stored in `dist/main.exe` by default.

Additionally, you can modify the `main.spec` file.

---

## LICENSE

see `LICENSE` file
