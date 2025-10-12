#/!bin/bash

count=0
command=$(find /etc -type f)
for file in $command; do
	count=$((count + 1))
done
echo "The amount of files in etc/ is: $count"
