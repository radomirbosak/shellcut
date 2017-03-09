#!/usr/bin/sh

RESULT=$(python3 process.py $@)

if [ $? -eq 0 ]; then
    eval "$RESULT"
fi
