#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then 
	echo "root permissions required"
	exit 1
fi

count=$(find /etc -type f | wc -l)

echo "The amount of files in /etc/ is: $count"
