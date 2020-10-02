#!/bin/bash
pw_raw=$(pass <dir/subdir>)
pw=$(echo "${pw_raw}" | head -n1 | awk '{print $1;}')
export SSHPASS="${pw}"
for ((i=1;i<=$#;i++)); 
do

    if [ ${!i} = "-d" ] 
    then ((i++)) 
        env='some_env';
    fi

done;
if [ -z ${env+x} ];
then
	sshpass -e ssh -oStrictHostKeyChecking=no "{$1}";
else
	sshpass -e ssh -oStrictHostKeyChecking=no "${1}${env}";
fi
