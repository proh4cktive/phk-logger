![ProHacktive](https://prohacktive.io/storage/parameters_images/LmQm4xddzmyFAdGYvQ32oZ9t1P9e8098UubYjnE9.svg "PHK-Logger from ProHacktive.io")

# PHK-Logger

[![PyPI version](https://badge.fury.io/py/phk-logger.svg)](https://badge.fury.io/py/phk-logger)
[![Build Status](https://travis-ci.org/proh4cktive/phk-logger.svg?branch=master)](https://travis-ci.org/proh4cktive/phk-logger)

An uncomplicated way to use logger inside python applications

---
- Created at: 01/05/2020
- Updated at:
- Author: Ben Mz (bmz)
- Maintainer: Ben Mz (bmz)
- Client: ProHacktive (https://prohacktive.io)

## Install
The easy way is by using pip
```bash
pip install phk-logger
```
  
The harder way is from sources
```bash
git clone https://github.com/proh4cktive/phk-logger.git
cd phk-logger
python install setup.py
```

## Usage
PHK-Logger is a lib so you just have to import it when needed
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from phk_logger import PHKLogger as Logger
```
  
Then in your code you can instantiate it directly
```python
logger = Logger(name='mytest', cli=True)
```
  
And use it when needed
```python
logger.info('This is an info message') # Will not be printed as default level is Warning
logger.write('A blue warning', level='warning', color='blue')
```

## Options
PHK-Logger is configred by default to output log event to your SysLog sub-system (Only supports Linux/MacOS). Some additional options can be set in order to change this behaviour.  

- **name** Set a specific name to your logger stream, by default will use the `__name__` var.
- **level** Set the log level, must be a level from logging package
- **filename** If set phk-logger will output events to a specific filename using *TimedRotatingFileHandler* configured with a file rotating every midnight, and 3 backup files
- **backup** Only used if **filename** is configured, specifiy the number of backup to keep
- **when** Only used if **filename** is configured, specify when to execute the file rotation
- **cli** If set to True this will also output log event to command line interface (CLI). Only useful for debugging app.
- **pattern** Define the log pattern to use for event output. Default is `%(name)s %(asctime)s %(levelname)-8s %(message)s`



## Methods
Several methods can be used to generate event logs, they all support the same options (only usefuls when using **cli** flag):  

- msg: the message to output
- color: override the default color
- light: override the light mode

> - **debug**(msg, color='blue', light=True) output event with prefix: `[*]`
> - **info**(msg, color='green', light=False) output event with prefix: `[+]`
> - **warning**(msg, color='yellow', light=False) output event with prefix: `[-]`
> - **error**(msg, color='red', light=False) output event with prefix: `[!]`
> - **critical**(msg, color='red', light=True) output event with prefix: `[!]`
  
An additional method is accessible which support a level parameter
> - **write**(message, level=None, color=None, light=None)

### Colors
Multiple colors are supported (case insensitive)
- BLACK
- BLUE
- GREEN
- CYAN
- RED
- PURPLE
- YELLOW
- WHITE
- no-color (default)

### Levels
Multiple levels are supported (case insensitive)
- DEBUG
- INFO
- INFOS
- WARNING
- ERROR
- CRITICAL
  
## Tests
Run tests easily using pytest
```bash
pytest -vv
```

## TODO
- Doc