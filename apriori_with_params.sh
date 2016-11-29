#!/bin/sh

rm -f rule-output.txt
./apriori/src/apriori -tr -s$1 -c$2 -R appearences.txt transactions.txt rule-output.txt
