#!/bin/bash
grep ",$1," ./ledgerheaders/* | awk -F'[.:,]' '{ print $2"\t"$4 }'
