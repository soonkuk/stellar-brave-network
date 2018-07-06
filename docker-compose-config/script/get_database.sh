
        #!/bin/bash
        field=$1
        if [ ! -d $field ]
        then 
        mkdir $field
        fi
        for i in {1..36}
        do 
	echo $i":"
	docker_id=$(docker ps -a | grep "db"$i"_1" | cut -d ' ' -f 1)
	docker exec -i $docker_id psql -U postgres -d stellar -c "\copy (select * from "$field") to "$field".csv with csv"
	if [ "$i" -lt 10 ];then
	docker cp $docker_id:ledgerheaders.csv $field/"node0"$i"_ledgerheaders.csv"
	else
	docker cp $docker_id:ledgerheaders.csv $field/"node"$i"_ledgerheaders.csv"
	fi
        done
        
