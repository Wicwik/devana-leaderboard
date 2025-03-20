#!/bin/bash

projects=(p904-24-3)

get_users() {
	ssh devana "sacctmgr -np show association where account=$1 | cut -f3 -d\| | awk 'NF'"
}

for project in ${projects[@]};
do
    for user in `get_users $project`;
    do
        echo "checking: $user";
    done
done