#!/bin/bash
if [ ! -d listleader ]
then
mkdir list_leader
fi
cd list_leader
docker ps --format "{{.ID}}\t{{.Names}}" | grep "core" | while read -r i
do
node_id=$(echo $i | awk '{print $2}' | cut -d "_" -f 2)
echo $node_id
docker_id=$(echo $i | awk '{print $1}')
docker logs $docker_id 2>/dev/null | grep "leader" > $node_id"_leader_list"
done
