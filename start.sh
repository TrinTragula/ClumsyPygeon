#!/bin/bash
rm -rf xboard.debug
xboard -debugMode true -cp -fcp "python main.py" -scp "python main.py"
