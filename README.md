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

* Python >= 3.7
* Python libraries specified in `requirements.txt` (namely [PySide2](https://pypi.org/project/PySide2/), [mido](https://pypi.org/project/mido/), [pygame](https://www.pygame.org/))
* A MIDI synthesiser supported by pygame
  * Windows and OSX (untested) already ship with one
  * On Linux you can use [fluidsynth](https://www.fluidsynth.org)
    * If running ArchLinux, you will need to install [freepats-legacy](https://aur.archlinux.org/packages/freepats-legacy/) from AUR and make a symlink from `/usr/share/freepats/timidity-freepats.cfg` to `/etc/timidity/freepats.cfg`


## Running

Prebuilt single binary releases for Windows and Linux can be found in the GitHub [release](https://github.com/xstasi/warmuppy/releases) page. They contain all the requirements, except for the synthesiser on Linux.

The program can also be started directly from the source tree. To do this first make sure that the dependencies are installed using `pip install -r requirements.txt` (using a [virtualenv](https://docs.python.org/3/tutorial/venv.html) is encouraged), then run the program with: `python main.py`

## Building

The binary releases can be rebuilt using pyinstaller:

```
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --clean -F -w -i resources/icon.ico -n warmuppy  main.py
```

