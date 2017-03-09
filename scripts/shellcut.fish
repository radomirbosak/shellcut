#!/usr/bin/fish

function s
    set -x RESULT (_shellcut.py $argv)

    if [ $status -eq 0 ]
        for line in $RESULT
            eval $line
        end
    end
end
