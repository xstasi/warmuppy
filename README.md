[![CircleCI](https://circleci.com/gh/xstasi/warmuppy/tree/master.svg?style=shield)](https://circleci.com/gh/xstasi/warmuppy) [![EUPL License](https://img.shields.io/badge/license-EUPL-blue)](https://raw.githubusercontent.com/xstasi/warmuppy/master/COPYING) [![Windows+Linux](https://img.shields.io/badge/platforms-linux%20%7C%20win--64-yellow)](https://github.com/xstasi/warmuppy/releases)

# Warmuppy

## What is it?

Warmuppy is a tool to help you practice vocal warming up by providing exercises.

This is a screenshot of the main window:

![alt text](https://github.com/xstasi/warmuppy/blob/master/resources/screenshot.png?raw=true)

## Features

* Progressive exercising with custom step amount
* Playing sound can be chosen from available MIDI instruments
* Exercises can be customised
* Custom execise BPM
* Custom note cut

## Requirements

* Python >= 3.10
* Python libraries specified in `requirements.txt` (namely [PySide6](https://pypi.org/project/PySide6/), [mido](https://pypi.org/project/mido/), [pygame](https://www.pygame.org/))
* Fluidsynth (OSX/Windows untested)

## Running and building

Prebuilt single binary releases for Windows and Linux can be found in the GitHub [release](https://github.com/xstasi/warmuppy/releases) page. They contain all the requirements, except for the synthesiser on Linux.

The source package can be built and installed using [setuptools](https://pypi.org/project/setuptools/) (using a [virtualenv](https://docs.python.org/3/tutorial/venv.html) is encouraged) by running:

```
pip install -r requirements.txt
python setup.py build
python setup.py install
```

The single-binary releases can be rebuilt on either Windows or Linux by using pyinstaller:

```
pip install -r requirements.txt
pip install pyinstaller
python setup.py build
python setup.py install
pyinstaller --clean -F -w -i src/warmuppy/resources/icon.ico -n warmuppy main.py
```

