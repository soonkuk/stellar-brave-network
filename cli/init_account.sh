#!/bin/sh

bin/brave transaction fund --seed $ROOT_SEED --address $ADDRESS1 --amount 10240
sleep 3s
bin/brave transaction fund --seed $ROOT_SEED --address $ADDRESS2 --amount 10240
sleep 3s
bin/brave transaction fund --seed $ROOT_SEED --address $ADDRESS3 --amount 10240
