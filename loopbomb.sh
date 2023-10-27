#! /bin/bash

#Checking python
if ! command -v python3 &> /dev/null
then
    COMMAND="python3"
else
    COMMAND="python"
fi

# Loop
for i in $(cat users.txt)
do
    $COMMAND ./bomb.py -u $i
done
