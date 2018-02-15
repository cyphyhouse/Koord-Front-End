#!/bin/sh
python translate.py $1
rm *.symtab
an=$(basename "$1" .krd)

mkdir src/main/java/testSim/$an
mv *.java src/main/java/testSim/$an
mvn compile install exec:java -Dexec.mainClass="testSim.$an.Main"
