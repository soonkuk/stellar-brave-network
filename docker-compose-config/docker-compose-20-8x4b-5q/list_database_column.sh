#!/bin/bash
docker_id=$(docker ps -a | grep "db1_1" | cut -d ' ' -f 1)
docker exec -i $docker_id psql -U postgres -d stellar -c "\dt"
