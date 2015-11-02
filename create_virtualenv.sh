#!/usr/bin/env bash

clear

# Requires Python.
if ! hash python 2>/dev/null; then
  echo "Install Python 2.7 or higher."
  exit
fi


# Requires Python 2.7 or higher
major="$(python -c "import sys;t='{v[0]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";)"
minor="$(python -c "import sys;t='{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";)"
min_major="2"
min_minor="7"

if [[ $major -lt "$min_major" ]]; then
  echo "Install Python $min_major.$min_minor or higher."
fi
if [[ $minor -lt "$min_minor" ]]; then
  echo "Install Python $min_major.$min_minor or higher."
fi

# Requires pip.
if ! hash pip 2>/dev/null; then
  echo "Install pip for Python."
  exit
fi

# Installs 'virtualenv' if needed be
if ! hash virtualenv 2>/dev/null; then
  pip install virtualenv
fi
if ! hash virtualenv 2>/dev/null; then
  exit
fi


# The directory of the virtual environment.
VIRTUAL_ENV_DIR=env

# Deletes the current virtual environment, if it exists.
if [[ -d "$VIRTUAL_ENV_DIR" ]]; then
  rm -R $VIRTUAL_ENV_DIR
fi

# Creates the virtual environment.
echo "Creating the virtual environment…"
virtualenv $VIRTUAL_ENV_DIR
