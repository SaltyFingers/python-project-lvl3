### Hexlet tests and linter status:
[![Actions Status](https://github.com/SaltyFingers/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/SaltyFingers/python-project-lvl3/actions) [![Tests and linter](https://github.com/SaltyFingers/python-project-lvl3/actions/workflows/lint_and_tests.yml/badge.svg)](https://github.com/SaltyFingers/python-project-lvl3/actions/workflows/lint_and_tests.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/63de61a08d7f43791b2c/maintainability)](https://codeclimate.com/github/SaltyFingers/python-project-lvl3/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/63de61a08d7f43791b2c/test_coverage)](https://codeclimate.com/github/SaltyFingers/python-project-lvl3/test_coverage)

### What is does:
This package allows You to download pages and inner resources.

### How to install:
To install this package from GitHub on Your PC use command

    pip install git+https://github.com/SaltyFingers/python-project-lvl3

in your terminal.

### How to use:
You can get help by using:

    page-loader -h

To download page use command:

    page-loader https://page-to-download.com/example path/to/directory

You will get ``.html`` file containing page data in directory ``path/to/directory`` and all inner resources in files directory.
Default directory to downloading is your current directory.

### Demonstration
Installation:
[![asciicast](https://asciinema.org/a/dWRdBeZq1b4NlyTrf2kLaklAV.svg)](https://asciinema.org/a/dWRdBeZq1b4NlyTrf2kLaklAV)

Correct work:
[![asciicast](https://asciinema.org/a/jbKx78NUOIGoS5QzHeafV7V3m.svg)](https://asciinema.org/a/jbKx78NUOIGoS5QzHeafV7V3m)

Incorrect work:
[![asciicast](https://asciinema.org/a/oppWHbQvu8C49M6ybhgf4wv6u.svg)](https://asciinema.org/a/oppWHbQvu8C49M6ybhgf4wv6u)