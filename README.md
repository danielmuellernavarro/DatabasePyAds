
## Description

Make queries to databases (MySQL, MS SQL or whatever) from a Beckhoff-PLC through The ADS-Communication and a script in python. The script can be deploy in the same PLC if it has an operation system to allow it, or somewhere else.

![Python_pyside](https://github.com/danielmuellernavarro/DatabasePyAds/blob/master/Presentation1.jpg)

## Content
* PLC-Program in Codesys 3
* Script in python (comming soon)

## Python dependencies
```bash
$ pip install pyads
$ pip install pyodbc
$ pip install mysqlclient
```

or get MySQL from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python)

## Related repositories
* [PyAds](https://github.com/stlehmann/pyads)