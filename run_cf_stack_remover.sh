#!/bin/bash

#this script was created to execute the cf_delete_stacks.py in multiple regions
# to execute the script execute 'sh run_cf_stack_remover.sh [region1] [region2] ...' 

if [ "$#" -lt 1 ]; then
    echo "add argument '--help' or AWS region such as 'us-west-2'"
elif [ "$1" == "--help" ]; then
    echo "this script was created to execute the cf_delete_stacks.py in multiple regions"
    echo "to execute the script execute 'sh run_cf_stack_remover.sh [region1] [region2] ...'"
else
    for item in "$@"; do
        python3 cf_delete_stacks.py --stack-status ROLLBACK_COMPLETE --region $item
    done
fi
