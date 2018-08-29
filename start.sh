#!/bin/bash

# Get the preferred method of startup from the user
clear
printf "\n"
printf "Select a startup option:\n"
printf "\n"
printf "(r) Run server\n"
printf "(t) Start tests\n"
printf "(p) Go to the NV prompt\n"
read choice

if [[ $choice == "r" ]]; then

    # Starting the server now
    printf "\nStarting in Python virtual environment 2.7...\n\n"
    virtualenv --python=python2.7 nv
    source nv/bin/activate
    pip install -r reqs.txt
    python cmd.py runserver
    deactivate

elif [[ $choice == "t" ]]; then

    # Loop the testing harness now
    pip install virtualenv
    virtualenv --python=python2.7 nv
    source nv/bin/activate
    pip install -r reqs.txt
    while true; do
        
        clear
        printf "\nStarting testing harness...\n\n"
        export RUN_MODE="test"
        python cmd.py test
        printf "Press return to test again (Ctrl+C exits)"
        read this_pauses_console
        
    done
    deactivate

elif [[ $choice == "p" ]]; then

    virtualenv --python=python2.7 nv
    source nv/bin/activate
    pip install -r reqs.txt
    clear
    printf "\nYou must manually start the NV prompt...\n\n"
    printf "Enter:\nsource nv/bin/activate\n"
    exit 0

else
      printf "No startup option found for $choice\n"
fi


