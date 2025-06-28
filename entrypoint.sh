#!/bin/bash

init_file="/etc/.initialized"

if [ ! -f "${init_file}" ]; then
    echo "The first launch is detected. Launching the initialization procedure."

    ./manage.py migrate
    ./manage.py loaddata db_dump.json

    rm -f requirements.txt db_dump.json

    # Run tests beforehand
    pytest
    if [ $? -ne 0 ]; then
        echo "Tests failed! Exiting."
        exit 1
    fi

    touch "${init_file}"
fi


exec gunicorn main.wsgi:application --bind 0.0.0.0:8000