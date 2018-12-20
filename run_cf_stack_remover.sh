#!/bin/bash


if [ "$#" -lt 1 ]; then
    echo "add argument '--help' or AWS region such as 'us-west-2'"
elif [ "$1" == "--help" ]; then
    python3 cf_delete_stacks.py --help
else
    for item in "$@"; do
        python3 cf_delete_stacks.py --stack-status ROLLBACK_COMPLETE --region $item
    done
fi
