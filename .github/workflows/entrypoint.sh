#!/bin/bash

while getopts "r:e:" opt; do
  case $opt in
    r) run=$OPTARG      ;;
    e) entrypoint=$OPTARG   ;;
    *) echo 'error' >&2
       exit 1
  esac
done

# initiate mysql service
# find /var/lib/mysql -type f -exec touch {} \; && service mysql start
service mysql start

if [ -n "$run" ]; then
  # load a genome from example
  mysql -uroot -ptest -e 'set global local_infile=true;'
  galpy -org GAL/galpy/data/ExampleFiles/genbank_annotation/organism_config.ini

fi

if [ -n "$entrypoint" ]; then
  # start the node
  pm2 start /GAL/galweb/index.js
fi
