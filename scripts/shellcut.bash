#!/usr/bin/sh

s () {
    RESULT=$(_shellcut.py $@)

    if [ $? -eq 0 ]; then
        eval "$RESULT"
    fi
}
