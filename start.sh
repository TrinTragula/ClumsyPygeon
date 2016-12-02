#!/bin/bash
rm -rf xboard.debug
rm -rf Clumsy_log_xboard.txt
xboard -debugMode true -cp -fcp "python src/main.py" -scp "python src/main.py"
