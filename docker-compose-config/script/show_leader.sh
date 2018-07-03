#!/bin/bash
for i in $(docker ps -a --filter "name=core")
do
node_id=$(echo $i | cut -d ' ' -f 10 | cut -d '_' -f 1 | cut -c4-4)
docker_id=$(echo $i | cut -d ' ' -f 0)
docker-compose logs $docker_id | grep "leader" >> "node"$node_id"_leader_list"
done
