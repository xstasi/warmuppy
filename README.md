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

Other than the Python libraries specified in `requirements.txt` you will need a functional MIDI synthesiser.

Windows and OSX (currently untested) ship with their own. On Linux distributions you will need to install `fluidsynth` or `timidity`.

## Running

Install the dependencies either from your distribution or in a virtualenv running `pip install -r requirements.txt`

Start the program with `python main.py`
