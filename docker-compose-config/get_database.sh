#!/bin/bash
field=$1
mkdir $field
for i in {1..12}
do 
	docker_id=$(docker ps -a | grep "db"$i"_1" | cut -d ' ' -f 1)
	docker exec -i $docker_id psql -U postgres -d stellar -c "\copy (select * from "$field") to "$field".csv with csv"
	docker cp $docker_id:ledgerheaders.csv $field/"node"$i"_ledgerheaders.csv"
done
