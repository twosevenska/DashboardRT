#!/usr/bin/env bash

clear

# The directory of the virtual environment.
VIRTUAL_ENV_DIR=env

# The working directory of the server.
SERVER_DIR=$VIRTUAL_ENV_DIR/bin

# The tempaltes directory needed by the server.
TEMPLATES_DIR=ditic_kanban/views


source $VIRTUAL_ENV_DIR/bin/activate

sudo -H pip install -e .

cp -rf $TEMPLATES_DIR $SERVER_DIR

cd $SERVER_DIR
./ditic_kanban_server
